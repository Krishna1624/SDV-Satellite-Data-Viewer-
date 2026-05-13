# SDV-Satellite-Data-Viewer-

# Project Description

    Satellite Data Viewer (SDV) is a web-based Ocean Forecasting and Visualization System developed during a Summer Internship at the Indian National Centre for       Ocean Information Services (INCOIS). The system is designed to provide interactive visualization and analysis of satellite-derived oceanographic data through      a modern geospatial web interface.

    The platform dynamically processes scientific satellite datasets stored in NetCDF format and visualizes them on an interactive map without relying on pre-         generated static imagery. The system integrates a Flask-based backend with THREDDS Data Server (TDS) infrastructure for accessing and processing                   multidimensional satellite datasets, while the frontend uses LeafletJS for geospatial rendering, temporal filtering, and animation support.

    The application enables users to explore ocean and atmospheric conditions spatially and temporally through map overlays, animation controls, product filters,      and date-based analysis. The system was designed with a modular architecture to support scalable scientific visualization workflows and efficient processing       of satellite products.

# Key Features
    Interactive geospatial visualization of satellite datasets
    Dynamic processing of NetCDF scientific data
    Temporal animation and time-series playback
    Real-time map-based rendering of oceanographic products
    Product-based filtering and date-range analysis
    THREDDS and NCSS-based scientific data access
    Flask + Leaflet integrated client-server architecture
    Visualization of satellite-derived environmental parameters
    Technologies Used
  Frontend
      HTML5
      CSS3
      JavaScript
      LeafletJS
      georaster-layer-for-leaflet
  Backend
      Python
      Flask
      xarray
      OpenCV
      Matplotlib
    
# Data & Infrastructure
    NetCDF
    THREDDS Data Server (TDS)
    Apache Tomcat 9
    NCSS (NetCDF Subset Service)
    WMS (Web Map Service)
    System Workflow
    Users select product type, satellite source, and date range through the web interface.
    The Flask backend retrieves corresponding NetCDF datasets from the THREDDS server.
    Scientific data bands are dynamically extracted and processed.
    Geospatial visualizations are generated using Matplotlib and Cartopy.
    Processed layers are rendered on an interactive Leaflet map.
    Users can animate, filter, and analyze temporal environmental variations.
# Future Enhancements
    Integration of advanced False Color Composite (FCC) rendering techniques for improved environmental interpretation
    Enhanced Cloud Top Temperature (CTT) analysis for weather and cloud monitoring applications
    Advanced Thermal Infrared Imagery (TIR) processing for surface heat and anomaly detection
    AI-assisted satellite image analytics and anomaly detection
    Real-time multi-satellite data streaming support
    Advanced geospatial forecasting and visualization modules
    Note on Dataset Access

# The datasets used in this project are part of organizational/government scientific infrastructure and are therefore not included in this repository.

# This repository contains only:

# Application source code
# Visualization workflows
# Processing logic
Frontend and backend integration modules
