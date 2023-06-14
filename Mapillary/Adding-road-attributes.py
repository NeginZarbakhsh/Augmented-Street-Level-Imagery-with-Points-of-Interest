import pandas as pd
from shapely.geometry import Point
import utm
import math
import os
import osmnx as ox
from pathlib import Path
import glob

def filter_mapillary(csv_file_path):
  #Read the metadata of images sourneded 4 location in US
  df = pd.read_csv(csv_file_path,low_memory=False)
  csv_file_name = os.path.basename(csv_file_path)      

  # Remove thoes roads that computed compass angle is more than 30 degree differ from the compass angle based on the below paper recommendation
  # REF: https://openaccess.thecvf.com/content_CVPR_2020/papers/Warburg_Mapillary_Street-Level_Sequences_A_Dataset_for_Lifelong_Place_Recognition_CVPR_2020_paper.pdf
  df = df[abs(df['computed_compass_angle'] - df['compass_angle'])<=30]
  # Create Coordinates of lat & Lng
  df ['Coordinates'] = list(zip(df['latitude'], df['longitude']))


  # ## Filter images:
  # Here, we filter images based on 2 rules:

  # 1.   Iamges close to the building (less than 30 meteres)
  # 2.   Images that are located between 31-50 meter while have right angle (we assumed right angle is the angle that the difference between actual angle and camera angle is less than 30)

  # This way, we are assuming, we are filtering the better images that have a bigger portion of buildings in their FOVs.

  # UTM conversion for further calculation
  df['camera_utm'] = df.apply(lambda row: utm.from_latlon(row['Computed coordinatess Lat'], row['Computed coordinatess Lng']), axis=1)
  df['POI_midpoint_utm'] = df.apply(lambda row: utm.from_latlon(row['latitude'], row['longitude']), axis=1)

  # assign the new coordinate columns back to the original dataframe
  df['x_meters_midpoint_POI'] = df['camera_utm'].apply(lambda x: x[0])
  df['y_meters_midpoint_POI'] = df['camera_utm'].apply(lambda x: x[1])

  df['x_meters_camera_coordinates'] = df['POI_midpoint_utm'].apply(lambda x: x[0])
  df['y_meters_camera_corrdinates'] = df['POI_midpoint_utm'].apply(lambda x: x[1])

  # define the north direction as a vector
  north_vector = [0, 1] # assuming that north is in the y-axis direction

  def calculate_angle(row):
      # calculate the vector between the camera coordinates and the midpoint of the POI
      vector = [row['x_meters_camera_coordinates']-row['x_meters_midpoint_POI'],row['y_meters_camera_corrdinates']-row['y_meters_midpoint_POI']]
      # calculate the dot product of the north vector and the vector between the points
      dot_product = north_vector[0]*vector[0] + north_vector[1]*vector[1]
      # calculate the magnitude of the north vector and the vector between the points
      north_magnitude = math.sqrt(north_vector[0]**2 + north_vector[1]**2)
      vector_magnitude = math.sqrt(vector[0]**2 + vector[1]**2)
      # calculate the cosine of the angle between the north vector and the vector between the points
      cos_angle = dot_product / (north_magnitude * vector_magnitude)
      # calculate the angle in degrees
      angle = math.degrees(math.acos(cos_angle))
      return angle

  # apply the calculation to each row and store the result in a new column
  df['angle'] = df.apply(calculate_angle, axis=1)
  df['angle_diff'] = abs (df['angle']- df['computed_compass_angle'])
  # df = df[['HD-Distance_m','angle_diff','id','thumb_2048_url']]
  #This will filter the rows where the HD-Distance is less than or equal to 30,
  #or where the HD-Distance is between 31 and 50 and the angle_diff is less than or equal to 35.
  df2 = df.loc[(df['HD-Distance_m'] <= 30) | ((df['HD-Distance_m'] > 31) & (df['HD-Distance_m'] <= 50) & (df['angle_diff'] <= 35))].reset_index(drop=True)

  def select_rows_from_group(group_df):
      selected_rows = []
      if len(group_df) <= 5:
          #print('The grouped_data belongs to {} coordinates has less than 5 images'.format(set(group_df['Coordinates'])))
          selected_rows = group_df.index.tolist()
      else:
          #print('The grouped_data belongs to {} coordinates has more than 5 images'.format(set(group_df['Coordinates'])))
          # Select 4 rows based on the smallest values of HD-Distance_m that also have the smallest angle_diff
          hd_angle_rows = group_df.nsmallest(2, ['HD-Distance_m', 'angle_diff'])
          selected_rows.extend(hd_angle_rows.index.tolist())

          # Select 2 rows based on the next smallest values of HD-Distance_m
          remaining_hd_rows = group_df.loc[~group_df.index.isin(selected_rows)]
          next_hd_rows = remaining_hd_rows.nsmallest(2, 'HD-Distance_m')
          selected_rows.extend(next_hd_rows.index.tolist())

          # Select 2 rows based on the smallest values of angle_diff
          remaining_rows = group_df.loc[~group_df.index.isin(selected_rows)]
          next_angle_rows = remaining_rows.nsmallest(1, 'angle_diff')
          selected_rows.extend(next_angle_rows.index.tolist())
      
      return group_df.loc[selected_rows, 'image_ids'].tolist()

  # Group the DataFrame by 'Coordinates' column and apply the function to each group
  selected_image_ids = df2.groupby('Coordinates').apply(select_rows_from_group).explode().reset_index(drop=True)

  # Filter the original DataFrame based on the selected image IDs
  selected_rows_df = df2[df2['image_ids'].isin(selected_image_ids)].reset_index(drop=True)

  # Add Road Attributes From OSM

  # Create empty lists to store the closest road information
  closest_highway = []  
  closest_length = []
  closest_geometry = []
  closest_name = []

  # Iterate over each row in selected_rows_df
  for index, row in selected_rows_df.iterrows():
      # Get the latitude and longitude of the point where the photo shooted
      point_lat = row['Computed coordinatess Lat']
      point_lon = row['Computed coordinatess Lng']

      # Download road network as a graph object centered at the coordinate and within a specified distance
      G = ox.graph_from_point((point_lat, point_lon), dist=300, network_type='all')
      G2 = ox.get_undirected(G)

      # Convert the graph to a graph data frame
      df_G = ox.graph_to_gdfs(G2)
      df_lines = df_G[1].copy()

      # Project the street network to a specific coordinate reference system (CRS)-UTM to consider ditsance calculation in meter
      df_lines_proj = ox.project_gdf(df_lines).reset_index().reset_index().to_crs(epsg=32638)

      # Calculate the distance between the point and each road geometry
      point = Point(row['x_meters_camera_coordinates'], row['y_meters_camera_corrdinates'])
      df_lines_proj['distance'] = df_lines_proj['geometry'].distance(point)

      # Find the road with the shortest distance to the point
      closest_road = df_lines_proj.loc[df_lines_proj['distance'].idxmin()]

      # Add the road information to the corresponding lists
      closest_highway.append(closest_road['highway'])
      closest_length.append(closest_road['length'])
      closest_geometry.append(closest_road['geometry'])
      closest_name.append(closest_road['name'] if 'name' in closest_road else '')

  # Add the closest road information to selected_rows_df
  selected_rows_df['road_attributes(highway)'] = closest_highway
  selected_rows_df['road_attributes(road_lenght)'] = closest_length
  selected_rows_df['road_attributes(road_geometry)'] = closest_geometry
  selected_rows_df['road_attributes(road_name)'] = closest_name

  gdf_final  = selected_rows_df.copy()
        
# Get a list of all the CSV files in the directory
csv_files = glob.glob('/*.csv') # change to desire directory
# # Loop over the list of CSV files and apply the function to each file
for csv_file in csv_files:
    print ('Gathering the Data for the file name: \n')
    print ('#############################################')
    print (csv_file)
    print ('#############################################\n')
    filter_mapillary(csv_file)


