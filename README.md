# Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)
![Dataset](https://github.com/NeginZarbakhsh/Augmented-Street-Level-Imagery-with-Points-of-Interest/blob/main/Images/The%20count%20of%20POIs%20in%2010%20US%20regions.png)
## Description

This repository contains the code and resources related to the research paper titled "Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)" The paper explores a method to generate new street-level imagery data using street-view images and annotating them with Points of Interest (POIS). This README provides an overview of the project, installation instructions, usage guidelines, and contact information for further inquiries.

- ⬇️ Download: You can download the dataset from url https://zenodo.org/deposit/8020056
- 📄 Paper: 


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
#### POI-related Parameters:

	- Top-category: NAICS_code broad category 
 	- Sub-category: NAICS_code detailed category
  	- NAICS_code: Standard for classifying POIs functionality



## ⚖ Legal

This repository is MIT licensed.

## Contact
For any questions, feedback, or inquiries related to this project, please contact [negin.zarbakhsh@ucdconnect.ie].
