# paper4--paper

## Description

? is a large-scale ?dataset that contains 1.6M street-level images.

- ⬇️ Download: 
- 📄 Paper: 


## 🔥 Data Curation - Mapillary Street-view Images

To reproduce the data, we've included all of the steps described in the paper, as follows:

- Gathering all images in the neighborhood of specific POI coordinate: [Mapillary/Mapillary_image_Retrieval.py](Mapillary/Mapillary_image_Retrieval.py).
- Filtering images based on POIs building footprints: [Mapillary/Filtering_POI_Polygon_based_Approach.py](Mapillary/Filtering_POI_Polygon_based_Approach.py).
- Selecting selective images for balance data:[filtering_selective_images.py](filtering_selective_images.py).
- Adding road network from Open Street Map (OSM): [Adding-road-attributes.py] (Adding-road-attributes.py)
- Detecd Objects through Mapillary API: [Mapillary_detectedobjects.py] (Mapillary_detectedobjects.py)

The meta files include the following information:

- **raw.csv**: raw data recorded during capture
	- 
	- lon
	- lat
	- ca
	- captured_at
	


## ⚖ Legal

This repository is MIT licensed.


