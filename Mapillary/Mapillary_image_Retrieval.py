import pandas as pd # for dataframes, converting str to a df
import io # preparing a string stream
import mapillary.interface as mly
import time
import glob
import os
from requests import HTTPError
import random
import requests
from tqdm import tqdm  # Import tqdm for the progress bar
from requests.exceptions import RequestException
#from multiprocessing import Pool
# import the geojson model from mapillary
from mapillary.models.geojson import GeoJSON
import json
from mapillary.models.client import Client
from mapillary.config.api.entities import Entities


def download_mapillary(csv_file_path):
  #put the token gained from' https://www.mapillary.com/app/?lat=20&lng=0&z=1.5'
  access_token = 'MLY|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #replace it with your token
  mly.set_access_token(access_token)

  #read the POI data
  safegraph_df = pd.read_csv(csv_file_path,low_memory=False)
  csv_file_name = os.path.basename(csv_file_path) #define the folder name

  image_id_list: list = []

  # Iterating over the rows of the df
  for index, row in enumerate(safegraph_df.iterrows()):

    # An empty dictionary that will hold our data as we go along
    coordinates_to_image_id_dict: dict = {}
    
    # Converting each row into a dictionary, then extracting the POI features
    placekey,	parent_placekey,	location_name,	brands,	store_id,	top_category,	sub_category,	naics_code,	latitude,	longitude,street_address,	city,	region,	postal_code,tracking_closed_since,	polygon_wkt,includes_parking_lot,	wkt_area_sq_meters = dict(row[1])['placekey'], dict(row[1])['parent_placekey'], dict(row[1])['location_name'], dict(row[1])['brands'],dict(row[1])['store_id'], dict(row[1])['top_category'], dict(row[1])['sub_category'], dict(row[1])['naics_code'],dict(row[1])['latitude'], dict(row[1])['longitude'], dict(row[1])['street_address'], dict(row[1])['city'],dict(row[1])['region'], dict(row[1])['postal_code'], dict(row[1])['tracking_closed_since'], dict(row[1])['polygon_wkt'],dict(row[1])['includes_parking_lot'],dict(row[1])['wkt_area_sq_meters']

    # Save the longitude and the latitude in the dict defined above
    coordinates_to_image_id_dict['placekey'] = placekey
    coordinates_to_image_id_dict['parent_placekey'] = parent_placekey
    coordinates_to_image_id_dict['location_name']= location_name
    coordinates_to_image_id_dict['brands']= brands
    coordinates_to_image_id_dict['store_id']= store_id
    coordinates_to_image_id_dict['top_category']= top_category
    coordinates_to_image_id_dict['sub_category']= sub_category
    coordinates_to_image_id_dict['naics_code']= naics_code
    coordinates_to_image_id_dict['latitude']= latitude
    coordinates_to_image_id_dict['longitude']= longitude
    coordinates_to_image_id_dict['street_address']= street_address
    coordinates_to_image_id_dict['city']= city
    coordinates_to_image_id_dict['region']= region
    coordinates_to_image_id_dict['postal_code']= postal_code
    coordinates_to_image_id_dict['tracking_closed_since']= tracking_closed_since
    coordinates_to_image_id_dict['polygon_wkt']= polygon_wkt
    coordinates_to_image_id_dict['includes_parking_lot']= includes_parking_lot
    coordinates_to_image_id_dict['wkt_area_sq_meters']= wkt_area_sq_meters



    # Get a `FeatureCollection` given the coordinates defined above, and
    # converting to a dictionary
    try:
     data: dict = mly.get_image_close_to(latitude=latitude,
                                        longitude=longitude,
                                        radius=40, # set the radius to collect all close_to images
                                        min_captured_at="2018-01-01", # set the minimum date for image collection
                                        image_type="pano").to_dict() # collection of panaroma images
     
    #For some lat and long, we will encounter the errors listed below, and we will proceed to the next POI while dealing with them.
    except HTTPError as error:
      print(error)
      continue                                    
    except AttributeError:
     print ('attribute error non-type close_to')
     continue

    # Define an empty list which will store our image_ids
    coordinates_to_image_id_dict['image_ids'] = []

    # Iterate over the features retrieved
    for index, feature in enumerate(data['features']):
      # Append to the list the image_id from the feature
      coordinates_to_image_id_dict['image_ids'].append(feature['properties']['id'])

    # Finally, append this dictionary to the final result
    # That is, the image_id_list variable
    image_id_list.append(coordinates_to_image_id_dict)

  # Useful list of fields we can use
  # For a complete list of possible values, please visit the below link
  # https://mapillary.github.io/mapillary-python-sdk/docs/mapillary.config.api/mapillary.config.api.entities#static-get_imageimage_id-str-fields-list
  fields_to_pass_for_the_image: list = ['merge_cc',
                                        'mesh',
                                        'altitude',
                                        'sfm_cluster',
                                        'atomic_scale',
                                        'camera_parameters',
                                        'camera_type',
                                        'captured_at',
                                        'compass_angle',
                                        'computed_altitude',
                                        'computed_compass_angle',
                                        'computed_geometry',
                                        'computed_rotation',
                                        'exif_orientation',
                                        'quality_score',
                                        'height',
                                        'width',
                                        'sequence',
                                        'thumb_2048_url',
                                        'thumb_1024_url',
                                        'thumb_256_url']

  # Retry settings
  max_retries = 5
  retry_delay = 60  # seconds

  # Count the total number of images
  total_images = sum(len(image_ids['image_ids']) for image_ids in image_id_list)
  print (f"Total_images:{total_images}.")
  
  # Create a progress bar
  progress_bar = tqdm(total=total_images, desc='Downloading Images')
  iteration_counter = 0  # Counter to track the number of iterations

  for index, image_ids in enumerate(image_id_list):
    image_id_list[index]['property_data'] = []
    for image_id in image_ids['image_ids']:
        retries = 0
        while retries < max_retries:
            try:
                response = Client().get(Entities.get_image(image_id=image_id, fields=fields_to_pass_for_the_image))
                data = json.loads(response.content.decode('utf-8'))
                image_id_list[index]['property_data'].append(data)
                progress_bar.update(1)  # Increment the progress bar
                break  # Success, exit the retry loop
            except RequestException as e: #If an exception of type RequestException occurs, it is caught in the except block
                print(f"Request failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay) #waits for retry_delay seconds before retrying the request
                retries += 1
        if retries == max_retries: #after reaching the maximum number of retries
            print("Maximum retries reached. Unable to retrieve data.")
            print("Sleeping for one day before continuing...")
            time.sleep(24 * 60 * 60)  # Sleep for 24 hours (one day)
            continue

        iteration_counter += 1
        if iteration_counter % 500 == 0:  # Update the progress bar every 500 iterations instead of every single iteration
            progress_bar.update(500)


  progress_bar.close()  # Close the progress bar when done

 
  json_file_name = os.path.splitext(csv_file_name)[0] + '.json'
  with open(json_file_name, 'w') as file_pointer:
      json.dump(image_id_list, file_pointer, indent=4)
  print('Finishing.......................')


# Get a list of all the CSV files in the directory
csv_files = glob.glob('/.../*.csv') #replace it with the folder that contains your POI data


# Loop over the list of CSV files and apply the function to each file
for csv_file in csv_files:
    print ('Gathering the Data for the file name: \n')
    print ('#############################################')
    print (csv_file)
    print ('#############################################\n')
    download_mapillary(csv_file)



