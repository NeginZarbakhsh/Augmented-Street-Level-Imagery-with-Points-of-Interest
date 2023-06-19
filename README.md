# Augmented Street-Level  Imagery with Points of Interest (Data and Resources Track)

## Description

? is a  ?dataset that containsstreet-level images.

- ⬇️ Download: 
- 📄 Paper: 


## 🔥 Data Curation - Mapillary Street-view Images

To reproduce the data, we've included all of the steps described in the paper, as follows:

- Gathering all images in the neighborhood of specific POI coordinate: [Mapillary/Mapillary_image_Retrieval.py](Mapillary/Mapillary_image_Retrieval.py).
- Filtering images based on POIs building footprints: [Mapillary/Filtering_POI_Polygon_based_Approach.py](Mapillary/Filtering_POI_Polygon_based_Approach.py).
- Selecting selective images for balance data:[Mapillary/filtering_selective_images.py](filtering_selective_images.py).
- Adding road network from Open Street Map (OSM): [Mapillary/Adding-road-attributes.py] (Adding-road-attributes.py)
- Detecd Objects through Mapillary API: [Mapillary/Mapillary_detectedobjects.py] (Mapillary_detectedobjects.py)

The meta files include the following information:

- **raw.csv**: raw data recorded during capture
	- 
	- lon
	- lat
	- ca
	- captured_at
	


## ⚖ Legal

This repository is MIT licensed.


