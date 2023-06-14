import requests
import base64
import mapbox_vector_tile
import pandas as pd
import time 
import glob
import os
import json
# Mapillary access token -- user should provide their own
access_token = 'MLY|xxxxxxxxxxxx'

def download_mapillary(csv_file_path):
  df = pd.read_csv(csv_file_path,low_memory=False)
  df2 = df[['height', 'width', 'image_ids']].reset_index()
  df2 = df2.drop_duplicates() # drop the duplicates images
  print ('#############################################')
  print (df2.shape) # print the shape of the dataframe
  print ('#############################################')
  csv_file_name = os.path.basename(csv_file_path) #define the folder name
  csv_path = '/home/negin/March 2023/USCANADA/Finalsafegraph-clean/Final JSON file Gathered/CSV Folders for true and totals/True_CSVs-after_15_select/With_Mapillary_objects/'

  # Create an empty list to store dictionaries
  result_rows = []
  objects_images= []

  for index, row in df2.iterrows():
      image_id_list = int(row['image_ids'][:-4])

      detections_url = f'https://graph.mapillary.com/{image_id_list}/detections?access_token={access_token}&fields=geometry,value,geometry'
      
      while True:
        # request the detection
        response = requests.get(detections_url)
        if response.status_code == 200:
           json_data= response.json()  # Convert the response to JSON 
           objects_images.append(json_data)
           break  # Break the loop if the response status code is 200
      
        # If the response status code is not 200, sleep for one day
        print(f"Received response with status code {response.status_code}. Sleeping for one day...")
        time.sleep(24 * 60 * 60)  # Sleep for one day (in seconds)  

      # Iterate over the detections
      for detection in json_data['data']: # get the data from the response
          value = detection['value'] # get the value of the detection
          base64_string = detection['geometry'] # get the base64 encoded geometry

          # decode from base64
          vector_data = base64.decodebytes(base64_string.encode('utf-8')) # decode the base64 string

          # decode the vector tile into detection geometry
          decoded_geometry = mapbox_vector_tile.decode(vector_data) # decode the vector tile

          # select just the coordinate xy pairs from this detection
          detection_coordinates = decoded_geometry['mpy-or']['features'][0]['geometry']['coordinates'] # get the coordinates of the detection
          
          segmentation_id = decoded_geometry['mpy-or']['features'][0]['id'] # get the segmentation id
          segmentation_type = decoded_geometry['mpy-or']['features'][0]['type'] # get the segmentation type
          
          # normalize by the 4096 extent, then multiply by image height and width to get true coordinate location
          pixel_coords = [[[x/4096 * row['width'], y/4096 * row['height']] for x, y in tuple(coord_pair)] for coord_pair in detection_coordinates]

          # Append the values as a dictionary to the list
          result_rows.append({'id': image_id_list,
                              'detections.pixel_coords_normalized': pixel_coords,
                              'detections.geometry': base64_string,
                              'detection_coordinates' :detection_coordinates,
                              'detections.value': value, 
                              'segmentation_id':segmentation_id,
                              'segmentation_type': segmentation_type})

  # Create a DataFrame by concatenating the dictionaries in the list
  result_df = pd.concat([pd.DataFrame(row) for row in result_rows], ignore_index=True)
  combined_jsons = {"data": objects_images}  # Create a dictionary to hold the combined data

  with open(csv_path + csv_file_name[:-4] +'.json', "w") as file:
     json.dump(combined_jsons , file, indent=4 )  # Convert the JSON data to a string using json.dumps()
  gdf_final = result_df.copy() 
  gdf_final.to_csv(csv_path + csv_file_name)
# Get a list of all the CSV files in the directory
#csv_files = glob.glob('/home/negin/March 2023/USCANADA/Finalsafegraph-clean/Final JSON file Gathered/CSV Folders for true and totals/True_CSVs-after_15_select/*.csv') #replace it with the folder that contains your POI data
csv_files = glob.glob('/*.csv') #replace it with the folder that contains your POI data

# Loop over the list of CSV files and apply the function to each file
for csv_file in csv_files:
    print ('Gathering the Data for the file name: \n')
    print ('#############################################')
    print (csv_file)
    print ('#############################################\n')
    download_mapillary(csv_file)