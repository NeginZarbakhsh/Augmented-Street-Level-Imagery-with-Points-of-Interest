# Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)
![Dataset](https://github.com/NeginZarbakhsh/Augmented-Street-Level-Imagery-with-Points-of-Interest/blob/main/Images/The%20count%20of%20POIs%20in%2010%20US%20regions.png)
## Description

This repository contains the code and resources related to the research paper titled "Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)" The paper explores a method to generate new street-level imagery data using street-view images and annotating them with Points of Interest (POIS). This README provides an overview of the project, installation instructions, usage guidelines, and contact information for further inquiries.

- ⬇️ Download: You can download the dataset from [Download Dataset](https://zenodo.org/deposit/8020056)
- 📄 Paper: You can download the paper from [Download Paper](?)


## 🔥 Data Curation Code - Augment Mapillary Street-level Imagery with POIs

### Setup and Environment

To set up the environment for running the code, follow these steps:

1. Clone the repository: git clone https://github.com/NeginZarbakhsh/Augmented-Street-Level-Imagery-with-Points-of-Interest.git
2. Navigate to the cloned repository directory: cd Augmented-Street-Level-Imagery-with-Points-of-Interest
3. pip install -r requirements.txt
4. Once the dependencies are installed, you're ready to run the below codes to reproduce data explained in the paper:

	- Gathering all images in the neighborhood of specific POI coordinate: [Mapillary/Mapillary_image_Retrieval.py](Mapillary/Mapillary_image_Retrieval.py).
	- Filtering images based on POIs building footprints: [Mapillary/Filtering_POI_Polygon_based_Approach.py](Mapillary/Filtering_POI_Polygon_based_Approach.py).
	- Selecting selective images for balance data:[Mapillary/filtering_selective_images.py](Mapillary/filtering_selective_images.py).
	- Adding road network from Open Street Map (OSM): [Mapillary/Adding-road-attributes.py](Mapillary/Adding-road-attributes.py)
	- Detect Objects through Mapillary API: [Mapillary/Mapillary_detectedobjects.py](Mapillary/Mapillary_detectedobjects.py)
 - 
### Metadata
The meta files include the following information:

#### Camera-related Parameters: 

###### Mapillary API: 
- Altitude: Camera altitude calculated from sea level
- Camera-parameters: Array of focal length, k1, k2
- Camera-type: Type of camera projection (perspective, fisheye, equirectangular)
- Compass-angle: Angle of the camera relative to the ground 
- Rotation: Orientation of the camera
- Quality-score: Image quality 
- Height & Width: Height and width of the images
- Sequence-id: The id of a set of images captured in series
- ID: Image unique identification
- Geometry Coordinates: Latitude and longitude of camera
- Captured-at: Capture time (hour, day, month, year)
- Others: merge_cc, atomic_scale, mesh.id, mesh.url, sfm_cluster.id, sfm_cluster.url
- 
###### Calculated parameters: 
- x_meters_camera_coordinates, y_meters_camera_corrdinates: Camera coordinates in UTM system
- Angle: The right angle that should capture POIs in the Fields of view
- Angle_diff: The difference between the angle and the current one 

#### POI-related Parameters:

- Top-category: NAICS_code broad category 
- Sub-category: NAICS_code detailed category
- NAICS_code: Standard for classifying POIs functionality

#### Road-related Parameters:
In OpenStreetMap (OSM), road attributes provide information about various aspects of a road segment. Here's an explanation of the commonly used road attributes in OSM:


- road_attributes(highway): The highway tag describes the type or classification of a road. It indicates the functional class of the road and determines its importance, size, and usage. Some common values for the highway tag include:
	- motorway: A high-speed, controlled-access road typically designed for long-distance travel, often with multiple lanes and grade-separated interchanges.
	- primary: Major roads connecting cities, towns, or important destinations.
	- secondary: Roads connecting smaller towns or providing access to local destinations.
	- residential: Roads primarily used for residential areas.
	- service: Roads serving specific purposes, such as access roads, driveways, or private roads.
- road_attributes(road_lenght): It refers to the length of a road segment. It provides the measured or estimated length of the road in a specific unit (e.g., meters or kilometers). This attribute helps in understanding the spatial extent or coverage of a road segment
- road_attributes(road_geometry) : This attribute describes the geometric shape or layout of a road segment. It includes information about the road's curvature, alignment, and any notable features, such as bends, intersections, or roundabouts. This attribute helps in visualizing the physical characteristics of the road segment.
- road_attributes(road_name) : This attribute represents the name assigned to a road segment. It typically includes the official or commonly recognized name of the road, such as "Main Street" or "Highway 201." The road name attribute helps in identifying and referencing specific roads within the map data.

#### Detected Objects Parameters:


## ⚖ Legal

This repository is MIT licensed.

## Contact
For any questions, feedback, or inquiries related to this project, please contact [negin.zarbakhsh@ucdconnect.ie].
