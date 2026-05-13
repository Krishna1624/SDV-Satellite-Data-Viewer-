### Video Demo : " https://github.com/user-attachments/assets/c537dcaa-da1f-4b75-9588-06d0f0e8c157 "

<div align="center">

# 🛰️ Satellite Data Viewer (SDV)

### Ocean Forecasting & Geospatial Visualization System

Developed during a Summer Internship at the Indian National Centre for Ocean Information Services (INCOIS)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=flat-square&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![LeafletJS](https://img.shields.io/badge/LeafletJS-Geospatial-199900?style=flat-square&logo=leaflet&logoColor=white)
![NetCDF](https://img.shields.io/badge/NetCDF-Scientific%20Data-0073CF?style=flat-square)

</div>

---

## 📌 Overview

Satellite Data Viewer (SDV) is a full-stack, web-based platform for the interactive visualization and temporal analysis of satellite-derived oceanographic data.

Built on a modern geospatial architecture, the platform dynamically processes scientific datasets in NetCDF format and renders them as interactive map overlays without relying on pre-generated static imagery.

The system integrates:
- Flask backend for scientific processing
- THREDDS Data Server (TDS) for multidimensional data access
- LeafletJS frontend for browser-based geospatial rendering and animation

> **Note:** The datasets powering this system are part of INCOIS government scientific infrastructure and are not included in this repository.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🗺️ Interactive Geospatial Visualization | Render satellite datasets as dynamic map overlays using LeafletJS |
| 🌊 NetCDF Scientific Data Processing | Real-time extraction and processing of multidimensional oceanographic datasets |
| 🎞️ Temporal Animation & Playback | Animate time-series environmental data |
| 📅 Date-Range & Product Filtering | Query datasets by satellite source and date range |
| 🔬 THREDDS / NCSS Integration | Scientific data retrieval using NCSS and WMS protocols |
| ⚡ Real-Time Map Rendering | Dynamic layer generation from raw satellite datasets |
| 🧱 Modular Architecture | Scalable component-based visualization workflow |

---

## 🏗️ System Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                      Web Browser                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ LeafletJS Map + Geospatial Controls                │ │
│ │ Product Selector · Animation UI · Date Filters     │ │
│ └──────────────────────┬──────────────────────────────┘ │
└────────────────────────│────────────────────────────────┘
                         │ HTTP / REST
┌────────────────────────▼────────────────────────────────┐
│                    Flask Backend                       │
│ ┌──────────────┐ ┌──────────────┐ ┌─────────────────┐ │
│ │ API Layer    │▶│ xarray       │▶│ Visualization   │ │
│ │ Request Flow │ │ NetCDF Logic │ │ Engine          │ │
│ └──────────────┘ └──────────────┘ └─────────────────┘ │
└────────────────────────┬───────────────────────────────┘
                         │ NCSS / WMS
┌────────────────────────▼────────────────────────────────┐
│              THREDDS Data Server (TDS)                 │
│             Apache Tomcat 9 · NetCDF Data              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔄 System Workflow

```text
1. USER INPUT
   └─▶ Select product type, satellite source, and date range

2. DATA RETRIEVAL
   └─▶ Flask backend requests datasets from THREDDS via NCSS/WMS

3. SCIENTIFIC PROCESSING
   └─▶ NetCDF bands extracted and processed using xarray

4. VISUALIZATION GENERATION
   └─▶ Geospatial layers rendered using Matplotlib and OpenCV

5. MAP RENDERING
   └─▶ Processed layers displayed on LeafletJS interactive maps

6. USER EXPLORATION
   └─▶ Users animate and analyze temporal environmental variations
```

---

## 🛠️ Technology Stack

### Frontend

| Technology | Role |
|---|---|
| HTML5 / CSS3 | Structure and styling |
| JavaScript | Client-side interactivity |
| LeafletJS | Interactive geospatial rendering |
| georaster-layer-for-leaflet | Raster overlay support |

### Backend

| Technology | Role |
|---|---|
| Python | Core processing language |
| Flask | REST API and application server |
| xarray | NetCDF dataset processing |
| Matplotlib | Scientific visualization |
| OpenCV | Image processing |

### Data & Infrastructure

| Technology | Role |
|---|---|
| NetCDF | Scientific multidimensional data format |
| THREDDS Data Server | Scientific dataset serving |
| Apache Tomcat 9 | TDS hosting infrastructure |
| NCSS | NetCDF Subset Service |
| WMS | Web Map Service |

---

## 🗂️ Project Structure

```text
SatelliteDashboard/
├── backend/
│   ├── app.py                          # Flask application
│
├── Frontend/
│   └── ofs_d_n.html                    # Main frontend dashboard UI
│
├── static/
│   ├── india_ocean_clip.geojson        # Indian Ocean boundary clipping layer
│   ├── logo.png                   # Runtime-generated visualization outputs
│
├── utils/
│   ├── geospatial_utils.py             # Coordinate & projection helpers
│   ├── netcdf_utils.py                 # NetCDF processing utilities
│   └── animation_utils.py              # Animation helper functions
│
├── thredds_content/
│   ├── catalogs/
│   │   └── catalog.xml                 # THREDDS catalog configuration
│   │
│   ├── data/
│   │   ├── metop/
│   │   │   ├── level1_nc/              # FCC / CTT / TIR source datasets
│   │   │   └── level2_avhrr/           # SST datasets
│   │   │
│   │   └── OCM3/
│   │       └── chlorophyll/            # Chlorophyll datasets
│   │
│   └── thredds/
│       ├── catalogs/
│       └── logs/
│
├── Apache Software Foundation/
│   └── Tomcat 9.0/
│       ├── bin/
│       ├── conf/
│       ├── content/
│       ├── lib/
│       ├── logs/
│       ├── temp/
│       ├── webapps/
│       └── work/
│
├── README.md
├── requirements.txt
└── sdv.mp4                             # Project demonstration video
```

> Later, the frontend architecture was consolidated into a single integrated frontend file for simplified deployment and management.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Access to a THREDDS Data Server instance
- Oceanographic NetCDF datasets

## 🔮 Future Enhancements

- Advanced False Color Composite (FCC) rendering
- Enhanced Cloud Top Temperature (CTT) analytics
- Thermal Infrared Imagery (TIR) anomaly detection
- AI-assisted satellite analytics
- Multi-satellite real-time streaming
- Advanced environmental forecasting modules

---

## 📂 Note on Repository Contents

Some files and datasets used during development are intentionally not included in this repository due to the following reasons:

- Large satellite datasets and NetCDF files exceed GitHub storage limitations.
- Government-provided oceanographic datasets used during the internship are restricted and cannot be publicly redistributed.
- THREDDS server data directories contain dynamically generated scientific datasets intended for local deployment environments.
- Runtime-generated visualization outputs, logs, cache files, and temporary media files were excluded to keep the repository lightweight and maintainable.
- Apache Tomcat binaries and server files are external dependencies that can be installed separately using official distributions.
- Virtual environments, compiled cache files (`__pycache__`), and generated outputs were omitted following standard software engineering practices.
- Some configuration files and deployment-specific settings were excluded for portability and security reasons.

The repository includes:
- Source code
- Processing pipelines
- Visualization logic
- Frontend/backend integration
- Documentation and project structure

This ensures the project remains reproducible while maintaining repository efficiency and compliance with dataset usage policies.

---

## 🏛️ Acknowledgements

Developed during a Summer Internship at the Indian National Centre for Ocean Information Services (INCOIS), Hyderabad, India.

---

<div align="center">

Built with 🌊 for ocean science.

</div>
