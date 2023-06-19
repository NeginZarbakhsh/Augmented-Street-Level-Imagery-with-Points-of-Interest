# Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)

## Description

This repository contains the code and resources related to the research paper titled "Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)" The paper explores a method to generate new street-level imagery data using street-view images and annotating them with Points of Interest (POIS). This README provides an overview of the project, installation instructions, usage guidelines, and contact information for further inquiries.

- ⬇️ Download: You can download the dataset from url https://zenodo.org/deposit/8020056
- 📄 Paper: 


## 🔥 Data Curation Code - Augment Mapillary Street-level Imagery with POIs

To reproduce the data, we've included all of the steps described in the paper, as follows:

- Gathering all images in the neighborhood of specific POI coordinate: [Mapillary/Mapillary_image_Retrieval.py](Mapillary/Mapillary_image_Retrieval.py).
- Filtering images based on POIs building footprints: [Mapillary/Filtering_POI_Polygon_based_Approach.py]Mapillary/(Mapillary/Filtering_POI_Polygon_based_Approach.py).
- Selecting selective images for balance data:[Mapillary/filtering_selective_images.py](Mapillary/filtering_selective_images.py).
- Adding road network from Open Street Map (OSM): [Mapillary/Adding-road-attributes.py] (Mapillary/Adding-road-attributes.py)
- Detect Objects through Mapillary API: [Mapillary/Mapillary_detectedobjects.py] (Mapillary/Mapillary_detectedobjects.py)

The meta files include the following information:

- **raw.csv**: raw data recorded during capture
	- 
	- lon
	- lat
	- ca
	- captured_at
	


## ⚖ Legal

This repository is MIT licensed.


