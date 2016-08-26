Smart Public Transport System: London's Bicycle Sharing Scheme
by Juan Navarrete, supervised by Nigel Goddard and Pedro Baiz
==============================================================

├── data
│   ├── parsed (supplied as a tar file which should be uncompressed here)
│   └── raw (supplied as a tar file which should be uncompressed here)
│       ├── cycles --> json files with bicycle availability readings
│       ├── priorities --> csv file containing the station priorities classification
│       ├── redistribution --> csv files containing bicycle redistribution data
│       └── weather --> json files containing weather data
├── reports
│   ├── images --> images used in the dissertation
│   └── maps --> maps created with folium
│── src
│   ├── data --> scripts used to parse, transform and visualize the data
│   ├── ingestion --> shell scripts used to ingest the data
│   └── temp
│
│
│── analysis_exploratory.ipynb --> ipython notebook containing the exploratory data analysis
│── analysis_performance_indicators.ipynb --> ipython notebook containing the analysis of the performance indicators
│── build_full_dataset.ipynb --> ipython notebook that builds the dataset without resampling
│── build_resampled_dataset.ipynb --> ipython notebook that builds the resampled dataset
│── modeling_features.ipynb --> ipython notebook containing experiments to determine the best features
│── modeling_predictions.ipynb --> ipython notebook containing the training and evaluation of the final models
│── modeling_regularize.ipynb --> ipython notebook containing the experiments to regularize the data
│── preprocessing_bike_availability.ipynb --> ipython notebook containing the preprocessing of bicycle availability data
│── preprocessing_bike_redistribution.ipynb --> ipython notebook containing the preprocessing of bicycle redistribution data
│── preprocessing_weather_readings.ipynb --> ipython notebook containing the preprocessing of weather conditions data
│── resampled_train_models.ipynb --> ipython notebook containing preprocessing of bicycle availability data
│── stations.csv --> csv file containing stations data
│── LICENSE
│── README.md
