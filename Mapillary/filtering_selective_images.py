import pandas as pd
import utm
import math
import os
import shutil
from pathlib import Path
import shutil
import glob
import requests
import mapillary as mly

def filter_mapillary(csv_file_path):
  # Mapillary access token -- user should provide their own
  access_token = 'MLY|xxxxxxxxxxxxxxx' # user should provide their own
  mly.interface.set_access_token(access_token)  

  #Read the metadata of images 
  df = pd.read_csv(csv_file_path,low_memory=False)
  csv_file_name = os.path.basename(csv_file_path)   
     

  # Remove thoes roads that computed compass angle is more than 30 degree differ from the compass angle based on the below paper recommendation
  # REF: https://openaccess.thecvf.com/content_CVPR_2020/papers/Warburg_Mapillary_Street-Level_Sequences_A_Dataset_for_Lifelong_Place_Recognition_CVPR_2020_paper.pdf
  df = df[abs(df['computed_compass_angle'] - df['compass_angle'])<=30] # 30 degree difference
  # Create Coordinates of lat & Lng
  df ['Coordinates'] = list(zip(df['latitude'], df['longitude'])) # create a new column of coordinates


  # ## Filter images:
  # Here, we filter images based on 2 rules:

  # 1.   Iamges close to the building (less than 30 meteres)
  # 2.   Images that are located between 31-50 meter while have right angle (we assumed right angle is the angle that the difference between actual angle and camera angle is less than 30)

  # This way, we are assuming, we are filtering the better images that have a bigger portion of buildings in their FOVs.

  # UTM conversion for further calculation
  df['camera_utm'] = df.apply(lambda row: utm.from_latlon(row['Computed coordinatess Lat'], row['Computed coordinatess Lng']), axis=1) # convert the camera coordinates to utm
  df['POI_midpoint_utm'] = df.apply(lambda row: utm.from_latlon(row['latitude'], row['longitude']), axis=1) # convert the POI midpoint coordinates to utm

  # assign the new coordinate columns back to the original dataframe
  df['x_meters_midpoint_POI'] = df['camera_utm'].apply(lambda x: x[0]) # assign the x coordinate to a new column
  df['y_meters_midpoint_POI'] = df['camera_utm'].apply(lambda x: x[1]) # assign the y coordinate to a new column

  df['x_meters_camera_coordinates'] = df['POI_midpoint_utm'].apply(lambda x: x[0]) # assign the x coordinate to a new column
  df['y_meters_camera_corrdinates'] = df['POI_midpoint_utm'].apply(lambda x: x[1]) # assign the y coordinate to a new column

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
  #This will filter the rows where the HD-Distance is less than or equal to 30,
  #or where the HD-Distance is between 31 and 50 and the angle_diff is less than or equal to 35.
  df2 = df.loc[(df['HD-Distance_m'] <= 30) | ((df['HD-Distance_m'] > 31) & (df['HD-Distance_m'] <= 50) & (df['angle_diff'] <= 35))].reset_index(drop=True)


    # ## Selective images:
  filtered_dfs = []
  def select_rows_from_group(group_df):
      selected_rows = []
      if len(group_df) <= 15:
          #print('The grouped_data belongs to {} coordinates has less than 15 images'.format(set(group_df['Coordinates'])))
          selected_rows = group_df.index.tolist() # select all rows
      else:
          #print('The grouped_data belongs to {} coordinates has more than 5 images'.format(set(group_df['Coordinates'])))
          # Select 6 rows based on the smallest values of HD-Distance_m that also have the smallest angle_diff
          hd_angle_rows = group_df.nsmallest(6, ['HD-Distance_m', 'angle_diff']) # select 6 rows
          selected_rows.extend(hd_angle_rows.index.tolist()) # add the selected rows to the list of selected rows
         # Select 3 rows based on the smallest values of angle_diff
          remaining_rows = group_df.loc[~group_df.index.isin(selected_rows)] # select the rows that are not in the selected rows
          next_angle_rows = remaining_rows.nsmallest(3, 'angle_diff') # select 3 rows
          selected_rows.extend(next_angle_rows.index.tolist()) # add the selected rows to the list of selected rows

          # Select rmaining rows based on the next smallest values of HD-Distance_m
          remaining_hd_rows = group_df.loc[~group_df.index.isin(selected_rows)] # select the rows that are not in the selected rows
          #Remaining count to reach 15
          remaining_count = 15 - len(selected_rows)
          next_hd_rows = remaining_hd_rows.nsmallest(remaining_count, 'HD-Distance_m')
          selected_rows.extend(next_hd_rows.index.tolist())
          assert len(set(selected_rows)) == 15, f"{selected_rows}"
          filtered_group_df = group_df.loc[selected_rows]
          filtered_dfs.append(filtered_group_df)
  print('Copying images between folders...')
  print('#'*50)
  filtered_df = df2.groupby('Coordinates').apply(select_rows_from_group) # apply the function to each group
  filtered_df = pd.concat(filtered_dfs).reset_index(drop=True) # concatenate the filtered dataframes
  print('Finishing copying images between folders...')
  print('#'*50)      
  
  gdf_final = filtered_df.copy() 
  csv_path = '/#####/' # Change the path to your directory

  gdf_final.to_csv(csv_path + csv_file_name)

  def copy_images_between_folders(gdf_final):

        gdf_final['sub_category'].fillna('nan', inplace=True) #filling na values for subcategory
        gdf_final['source_path'] = Path("/#####/")/gdf_final['top_category']/gdf_final['sub_category']/gdf_final['Coordinates'].astype('str')# Change the path to your directory
        gdf_final['destination_path'] = Path("/####/")/gdf_final['top_category']/gdf_final['sub_category']/gdf_final['Coordinates'].astype('str') # Change the path to your directory
        gdf_final['destination_path2'] = Path("#####/")/gdf_final['top_category']/gdf_final['sub_category']  # Change the path to your directory
    
        for i in range(len(gdf_final)):
            destination_path = gdf_final['destination_path'][i]
            destination_path.mkdir(parents=True, exist_ok=True)
            destination_path2 = gdf_final['destination_path2'][i]
            destination_path2.mkdir(parents=True, exist_ok=True)

            image_path = gdf_final['source_path'][i] / gdf_final['image_ids'][i]

            if os.path.exists(image_path):
                shutil.copy(image_path, destination_path)
                shutil.copy(image_path, destination_path2)
            else:
                image_id = gdf_final['id'][i]
                filename = str(image_id) + '.jpg'
                url = mly.interface.image_thumbnail(image_id=image_id, resolution=2048)  # The desired filename for the image

                response = requests.get(url)
                response.raise_for_status()  # Raise an exception if the request was unsuccessful

                source_path = gdf_final['source_path'][i]
                os.makedirs(source_path, exist_ok=True)  # Create the source directory if it doesn't exist

                file_path = os.path.join(source_path, filename)
                with open(file_path, 'wb') as file:
                    file.write(response.content)

                shutil.copy(image_path, destination_path)
                shutil.copy(image_path, destination_path2)
                
    # Call the function
  print('Copying images between folders...')
  print('#'*50)
  copy_images_between_folders(gdf_final)
  print('#'*50)
  print('Finishing copying images between folders...')
# Get a list of all the CSV files in the directory
csv_files = glob.glob('/##/*.csv') # Change the path to your directory
# # Loop over the list of CSV files and apply the function to each file
for csv_file in csv_files:
    print ('Gathering the Data for the file name: \n')
    print ('#############################################')
    print (csv_file)
    print ('#############################################\n')
    filter_mapillary(csv_file)




  
