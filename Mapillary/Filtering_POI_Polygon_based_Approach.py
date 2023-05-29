from pathlib import Path
import pandas as pd
import numpy as np
import shapely
import shapely.geometry
import geopandas as gpd
import shutil
import pathlib
import requests
import time
from datetime import datetime, date
import matplotlib.pyplot as plt
import os,json
import time
import urllib.error
import urllib.request
from haversine import haversine, Unit
import glob

def look_at_360_images (json_file_path):
    # Now the json_data list contains the data for each file
    # You can iterate over the list and perform operations on each file's data
    # Create an empty list to hold the data for each file
    json_data = []
    with open(json_file_path) as json_file2:
    # Load the contents of the file and store it in the list
        data = json.load(json_file2)
        json_data.append(data)

    for data in json_data:
        # Flatten data & include lat & lng
        df_netsed_list = pd.json_normalize(data, record_path=['property_data'], # flatten the nested list
                                            meta=['placekey','parent_placekey','location_name','brands','store_id','top_category','sub_category','naics_code','latitude','longitude','street_address','city','region','postal_code','tracking_closed_since','polygon_wkt','includes_parking_lot','wkt_area_sq_meters'])
        file_name = json_file_path[-7:]
        # Add file name to dataframe
        df_netsed_list['file_name'] = file_name


    # Drop columns with NA values for camera parameters which later would be used for filtering POI images
    df_netsed_list = df_netsed_list.dropna(subset = ['computed_geometry.coordinates', 'camera_parameters', 'computed_compass_angle']).reset_index(drop = True)

    # Split columns into multiple columns
    split_camera_parameters = pd.DataFrame(df_netsed_list['camera_parameters'].tolist(), columns = ['camera_parameters (Focal Lenght)', 'camera_parameters (K1)', 'camera_parameters (K2)'])#split column of lists into three new columns
    # #join split columns back to original DataFrame
    df_netsed_list = pd.concat([df_netsed_list, split_camera_parameters ], axis=1)

    # Split columns into multiple columns
    split_coordinates = pd.DataFrame(df_netsed_list ['computed_geometry.coordinates'].tolist(), columns = ['Computed coordinatess Lng', 'Computed coordinatess Lat'])#split column of lists into three new columns
    # #join split columns back to original DataFrame
    df_netsed_list = pd.concat([df_netsed_list, split_coordinates], axis=1)
    df_netsed_list = df_netsed_list.dropna(subset = ['Computed coordinatess Lng', 'Computed coordinatess Lat','camera_parameters (Focal Lenght)' ]).reset_index(drop = True)

    df_netsed_list['captured_at_date'] = pd.to_datetime(df_netsed_list['captured_at'],unit='ms').dt.floor('S') # remove secoend
    df_netsed_list['captured_at_year'] = df_netsed_list['captured_at_date'].dt.year
    df_netsed_list['captured_at_month'] = df_netsed_list['captured_at_date'].dt.month
    df_netsed_list['captured_at_day'] = df_netsed_list['captured_at_date'].dt.day
    df_netsed_list['captured_at_hour'] = df_netsed_list['captured_at_date'].dt.time
    mapillary_df = df_netsed_list.drop(columns = ['computed_geometry.type', 'camera_parameters', 'computed_geometry.coordinates', 'captured_at', 'geometry.type'])

    locations_gpd = gpd.GeoDataFrame(mapillary_df,geometry=gpd.points_from_xy(mapillary_df['Computed coordinatess Lng'], mapillary_df['Computed coordinatess Lat']),crs='EPSG:4326')
    locations_gpd = locations_gpd.to_crs(32638) #Reproject
    locations_gpd['geometry'] = locations_gpd['geometry'].buffer(60) #Buffer
    locations_gpd['area_camera_fov']= locations_gpd['geometry'].area
    gdf_4326 = locations_gpd.to_crs(epsg=4326)
    gdf_4326['building_poly'] = gpd.GeoSeries.from_wkt(gdf_4326['polygon_wkt'])
    gdf_final = gpd.GeoDataFrame(gdf_4326, crs='epsg:4326')
    
    #check if the Polygons are valids
    # gdf_final[~gdf_final['geometry'].is_valid].shape
    # gdf_final[~gdf_final['building_poly'].is_valid].shape

    def intersect(x):
        return x[0].intersects(x[1])
    # Consider the two columns have polygone to check their intersection
    gdf3 = gdf_final.filter(items=['geometry', 'building_poly'])


    # Function to calculate Haversine distance between two points
    def haversine_distance(row):
        p1 = (row['Computed coordinatess Lat'], row['Computed coordinatess Lng'])
        p2 = (row['latitude'], row['longitude'])
        return haversine(p1, p2, unit=Unit.METERS)

    # Add a new column with the Haversine distance between the points
    gdf_final['HD-Distance_m'] = gdf_final.apply(haversine_distance, axis=1)
    gdf_final ['filter'] = gdf3.apply(intersect, axis =1)
    # Create Coordinates of lat & Lng
    gdf_final ['Coordinates'] = list(zip(gdf_final ['latitude'], gdf_final ['longitude']))
    # add 'jpg' to all image ids
    gdf_final ['image_ids'] = gdf_final ['id'].astype ('str') +'.jpg'

    gdf_final.to_csv('total+'+ file_name[:-5] + '.csv')
    gdf_true = gdf_final[gdf_final['filter']== True]
    gdf_false = gdf_final[gdf_final['filter']== False]
    gdf_true.to_csv('True+'+ file_name[:-5] + '.csv')

    # helper functions to download images
    def download_file(url, dst_path):
        try:
            with urllib.request.urlopen(url) as web_file:
                data = web_file.read()
                with open(dst_path, mode='wb') as local_file:
                    local_file.write(data)
        except urllib.error.URLError as e:
            print(e)
            
    def download_file_to_dir(url, dst_dir):
        download_file(url, os.path.join(dst_dir, os.path.basename(url)))

    # Specify download folder
    main_folder = '/...../' #Replace it with your path
    sub_folder = '..../' #Replace it with your path

    # iterate over all the rows
    for index, row in gdf_true.iterrows():

        # create the folder path
        folder_path = os.path.join(main_folder, sub_folder, str(row['top_category']), str(row['sub_category']), str(row['Coordinates']))

        # create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # create the file path
        file_path = os.path.join(folder_path, row['image_ids'])

        # download the image
        response = requests.get(row['thumb_2048_url'])
        with open(file_path, 'wb') as f:
            f.write(response.content)

# Get a list of all the CSV files in the directory
json_files = glob.glob('...../*.json') # Replace it with your folder path
# # Loop over the list of CSV files and apply the function to each file
for json_file in json_files:
    print ('Gathering the Data for the file name: \n')
    print ('#############################################')
    print (json_file)
    print ('#############################################\n')
    look_at_360_images(json_file)
