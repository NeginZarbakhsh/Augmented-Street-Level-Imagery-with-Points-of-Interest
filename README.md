# paper4--paper

## :newspaper: News

- *2020-12-30* - Added information about evaluation server
- *2020-07-14* - Released patch v1.1 fixing some corrupt images

## Description

Mapillary Street-level Sequences (MSLS) is a large-scale long-term place recognition dataset that contains 1.6M street-level images.

- ⬇️ Download: 
- 📄 Paper: 


## 🔥 Data Curation - Mapillary Street-view Images

To reproduce the data, we've included all of the steps described in the paper, as follows:

- Gathering all images in the neighborhood of specific POI coordinate: [Mapillary/Mapillary_image_Retrieval.py](Mapillary/Mapillary_image_Retrieval.py).




## 📦 Package structure

- `images_vol_X.zip`: images, split into 6 parts for easier download.
- `metadata.zip`: a single zip archive containing the metadata.
- `patch_vX.Y.zip`: unzip any patches on top of the dataset to upgrade.

All the archives can be extracted in the same directory resulting in the following tree:

- train_val
    - `city`
        - query / database
            - images/`key`.jpg
            - seq_info.csv
            - subtask_index.csv
            - raw.csv
            - postprocessed.csv
- test
    - `city`
        - query / database
            - images/`key`.jpg
            - seq_info.csv
            - subtask_index.csv

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

- **subtask_index.csv**: Precomputed image indices for each subtask in order to evaluate models on (all, summer2winter, winter2summer, day2night, night2day, old2new, new2old)

## ⚖ Legal

Copyright © Meta Platforms, Inc

This repository is MIT licensed.

[Terms of Use](https://opensource.facebook.com/legal/terms)

[Privacy Policy](https://opensource.facebook.com/legal/privacy)
