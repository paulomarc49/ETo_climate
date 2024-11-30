# ETo Climate Clustering  

## 1. GENERAL REQUIREMENTS

* Linux operating system.
* WRF system.
* HPC (optional).
* Python.
* Google Colab TPU.
* Google Colab High RAM CPU.

## 2. WRF 

The **WRF** system must be downloaded and installed on a Linux distribution in a local machine or an HPC. For this project, **Linux Mint MATE** was chosen as the operating system in te local machine and **Ubuntu Server** for the HPC. This repository provides detailed instructions for configuring and processing data using the Weather Research and Forecasting (**WRF**) model. The workflow is designed for a specific geographical domain, enabling the processing of meteorological variables and the generation of outputs for advanced analysis. Executing this study for other domains requires prior modification and configuration of the code provided in this repository.

Disclaimer: The configuration and code in this repository are intended for research purposes only. Users are responsible for adapting the workflow to their specific needs and ensuring compliance with applicable regulations and licensing agreements for the software and data used.

### 2.1. WRF system prerequisites  
Ensure the following libraries and packages are installed on your operating system:  

- `csh`  
- `gcc`  
- `gfortran`  
- `libpng-dev`  
- `ncview`  
- `python3-gdal`  
- `python3-netcdf4`  
- `zlib1g-dev`  
- `hdf5`  
- `mpich`  
- `netcdf-c`  
- `netcdf-f`  
- `pnetcdf`  

### 2.2. WRF Domain 
The **WRF** system must be installed and configured using the "namelist" file located in the WPS directory to define a specific area of interest. For this study, which focuses on the Ecuadorian Andes and Amazon region, the following specifications apply:

- **Projection**: Mercator  
- **Initial Latitude**: 0.600000  
- **Initial Longitude**: -79.000000  
- **Initial Coordinates**: 0°36’00.0"N, 79°00’00.0"W  
- **Pixel Dimensions**: 3.3 km x 3.3 km  
- **Final Latitude**: -4.466667  
- **Final Longitude**: -73.916667  
- **Final Coordinates**: 4°28’00.0"S, 73°55’00.0"W  

### 2.3. WRF Variables of Interest  
The **WRF** system also have to be configured to processes the following meteorological variables in the specified order:  

1. **Rn**: Net Radiation  
2. **G**: Ground Heat Flux  
3. **T**: Air Temperature  
4. **∆**: Vapor Pressure Curve  
5. **γ**: Psychrometric Constant  
6. **es**: Saturation Vapor Pressure  
7. **ea**: Actual Vapor Pressure  
8. **u2**: Wind Speed  

## 3. WORKFLOW  

Once the **WRF** system is instaled and configured for the domain of interest, the block diagram in figure 1 ![Description of the image](./images/example-image.png) shows the flow chart process must folow to achive a ETo climate clustering. 



#### 1.3.1 Step 1: Download and Process GFS Data  
Run the Python script `getdata_gfs.py` to download and prepare GFS (Global Forecast System) data required for running WRF.  

#### 1.3.2 Step 2: Run WRF Preprocessing System (WPS)  
Execute the WPS modules:  
- **GEOGRID**: Processes static data.  
- **UNGRIB**: Processes dynamic data.  
- **METGRID**: Combines outputs from GEOGRID and UNGRIB for WRF input.  

Once preprocessing is complete, the outputs can be used in the WRF model.  

#### 1.3.3 Step 3: Run WRF  
For real-data cases (like this study), execute the **REAL** module before running WRF. Then, execute WRF using daily dynamic data to simulate weather conditions for the study period. The output will be in **NetCDF** format.  

---

## 2. NetCDF to NumPy Conversion  
Use the Python script `collect_data.py` to transform WRF output from **NetCDF** to **NumPy** format for further processing. First, create a folder with a text file containing the paths to the **NetCDF** daily files you want to convert.  

---

## 3. ETo Weather Clustering  

### 3.1 ETo Weather Training  
Run the Jupyter notebook `ETo_weather_training_reproducibility.ipynb` to:  
- Select hyperparameters (e.g., use one month for training and one month for validation, as in this project).  
- Normalize data and save the normalization model using the `joblib` library.  
- Train the main model (e.g., two years of training data were used in this project).  
- Save the trained custom Scikit-learn SOM model using the `joblib` library.  

### 3.2 ETo Weather Prediction  
Run the Jupyter notebook `ETo_weather_prediction_reproducibility.ipynb` to:  
- Load the trained custom Scikit-learn SOM model and predict clusters for the testing dataset (e.g., two years of testing data were used in this project).  
- Save the predicted labels for future use in **ETo Climate Clustering**.  

---

## 4. ETo Climate Clustering  
Run the Jupyter notebook `ETo_climate_training_prediction_reproducibility.ipynb` to:  
- Load the cluster labels from the **ETo Weather Clustering** step.  
- Perform hyperparameter selection.  

---

## 5. Example Usage of WRF system  

### 5.1 Acquire Dynamic Data  
Run the following command in bash:
```bash
python getdata_gfs.py 20241126
```

### 5.2. Run WRF
Run the following command in bash:
```bash
run_wrf ANDES_03 20241126 &
```
