# paper4--paper

## Description

? is a large-scale ?dataset that contains 1.6M street-level images.

- ⬇️ Download: 
- 📄 Paper: 


## 🔥 Data Curation - Mapillary Street-view Images

To reproduce the data, we've included all of the steps described in the paper, as follows:

- Gathering all images in the neighborhood of specific POI coordinate: [Mapillary/Mapillary_image_Retrieval.py](Mapillary/Mapillary_image_Retrieval.py).
- Filtering images based on POIs building footprints: [Mapillary/Filtering_POI_Polygon_based_Approach.py](Mapillary/Filtering_POI_Polygon_based_Approach.py)

The meta files include the following information:

- **raw.csv**: raw data recorded during capture
	- key
	- lon
	- lat
	- ca
	- captured_at
	- pano

- **seq_info.csv**: Sequence information
	- key
	- sequence_id
	- frame_number

- **postprocessed.csv**: Data derived from the raw images and metadata
	- key
	- utm (easting and northing)
	- night
	- control_panel
	- view_direction (Forward, Backward, Sideways)
	- unique_cluster


## ⚖ Legal

This repository is MIT licensed.


