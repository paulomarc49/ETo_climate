ETo climate Clustering 

---

# 1. WRF Model Configuration and Data Processing Workflow

The **WRF** system must be downloaded and installed on a Linux distribution. For this project, Linux Mint MATE was chosen as the operating system. This repository offers detailed instructions for configuring and processing data using the Weather Research and Forecasting (WRF) model. The workflow is tailored to a specific geographical domain, enabling the processing of meteorological variables and the generation of outputs for advanced analysis.

## 1.1. Requirements

### 1.1.1. Prerequisites
Ensure the following libraries and packages are installed on yur operating system:
- csh
- gcc
- gfortran
- libpng-dev
- ncview
- python3-gdal
- python3-netcdf4
- zlib1g-dev
- hdf5
- mpich
- netcdf-c
- netcdf-f
- pnetcdf 

### 1.1.2. Install and Configure WRF
The **WRF** software must be installed and configured to work with the following domain specifications:

- **Projection**: Mercator  
- **Initial Latitude**: 0.600000  
- **Initial Longitude**: -79.000000  
- **Initial Coordinates**: 0°36’00.0"N, 79°00’00.0"W  
- **Pixel Dimensions**: 3.3 km x 3.3 km  
- **Final Latitude**: -4.466667  
- **Final Longitude**: -73.916667  
- **Final Coordinates**: 4°28’00.0"S, 73°55’00.0"W  

## 1.2. Variables of Interest
The workflow processes the following meteorological variables in the specified order:

1. **Rn**: Net Radiation  
2. **G**: Ground Heat Flux  
3. **T**: Air Temperature  
4. **∆**: Vapor Pressure Curve  
5. **γ**: Psychometric Constant  
6. **es**: Saturation Vapor Pressure  
7. **ea**: Actual Vapor Pressure  
8. **u2**: Wind Speed  

## 1.3. Workflow

### 1.3.1. Step 1: Download and Process GFS Data
Run the Python script `getdata_gfs.py` to download and prepare GFS (Global Forecast System) data required for running WRF.  

### 1.3.2. Step 2: Run WRF Preprocessing System (WPS)
Execute the WPS where the module called GEOGRID preprocesses the static data, the module called UNGRIB preprocesses the dynamic data. Both outputs are then used as inputs for the module called METGRID.
Once the preprocessing is done and the output of the WPS is ready, it is used in the WRF model.

### 1.3.3. Step 3: Run WRF
If the WRF model is using real data and not simulations like in this case of study, a final step must be performed in a module called REAL and then finally the WRF starts processing the data. Execute the WRF model with daily dynamic data to simulate weather conditions over the study time of interest. The output must be in **NetCDF** format.  

---

# 2. NetCDF to NumPy convertion
Use the Python script `collect_data.py` to transform the WRF output from **NetCDF** to **NumPy** format for further processing. You must need to firstly create a folder with a text file with the paths pointing to the **NetCDF** daily files you want to convert. 

---

# 3. ETo weather clustering

## 3.1. ETo weather training
Execute the jupiter notebook named: `ETo_weather_training_reproducibility.ipynb`.

- Perform hyperparameters selection (One month for training and one month for validation were used in the present project).
- Normalize the data and save the normalization model using the joblib library.
- Train the main model (Two years training data were used in the present project)
- Save the trained custom Scikit-learn SOM model with the joblib library

# 3.2. ETo weather prediction
Execute the jupiter notebook named: `ETo_weather_prediction_reproducibility.ipynb`.

- Load the trained custom Scikit-learn SOM model and predict the clusters for the testing dataset split (Two years testing data were used in the present project).
- Save the lables predicted for future use in the ETo climate clustering

---

# 4. ETo climate  clustering
Execute the jupiter notebook named: `ETo_climate_training_prediction_reproducibility.ipynb`.

- Load the clusters lables from the ETo weather clustering.
- Perform hyperparameters selection.

---

# 5. Example Usage
 
## 5.1. Run `getdata_gfs.py`
In bash: python getdata_gfsdd/mm/yyyy
