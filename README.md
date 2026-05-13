

https://github.com/user-attachments/assets/b8fe7e2c-f30b-46d3-b25b-8a5224f6820d



SDV/
├── backend/
│   ├── app.py                      # Flask application entry point
│   ├── data_handler.py             # THREDDS / NCSS data retrieval
│   ├── processor.py                # NetCDF extraction & preprocessing
│   ├── visualizer.py               # Geospatial rendering and visualization
│   ├── utils.py                    # Helper utilities and shared functions
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── index.html                  # Main web interface
│   ├── css/
│   │   └── styles.css              # UI styling and layout
│   └── js/
│       ├── map.js                  # Leaflet map initialization
│       ├── animation.js            # Temporal playback controls
│       ├── layers.js               # Layer rendering and management
│       └── api.js                  # Backend API integration
│
├── config/
│   └── settings.py                 # Server and dataset configuration
│
├── docs/
│   ├── architecture.png            # System architecture diagram
│   └── screenshots/                # Application screenshots
│
├── static/
│   └── generated/                  # Runtime-generated visualization outputs
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt<div align="center">
🛰️ Satellite Data Viewer (SDV)
Ocean Forecasting & Geospatial Visualization System
Developed during a Summer Internship at the Indian National Centre for Ocean Information Services (INCOIS)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=flat-square&logo=flask&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-F7DF1E?style=flat-square&logo=javascript&logoColor=black)
![LeafletJS](https://img.shields.io/badge/LeafletJS-Geospatial-199900?style=flat-square&logo=leaflet&logoColor=white)
![NetCDF](https://img.shields.io/badge/NetCDF-Scientific%20Data-0073CF?style=flat-square)
</div>
---
📌 Overview
Satellite Data Viewer (SDV) is a full-stack, web-based platform for the interactive visualization and temporal analysis of satellite-derived oceanographic data. Built on a modern geospatial architecture, it processes scientific datasets in NetCDF format dynamically — eliminating dependency on pre-generated static imagery — and renders them as live, interactive map overlays.
The system integrates a Flask backend with THREDDS Data Server (TDS) infrastructure for multidimensional data access, while the frontend leverages LeafletJS for rich, browser-based geospatial rendering with animation and temporal filtering capabilities.
> **Note:** The datasets powering this system are part of INCOIS's government scientific infrastructure and are not included in this repository. This repository contains only application source code, visualization workflows, processing logic, and frontend/backend integration modules.
---
✨ Key Features
Feature	Description
🗺️ Interactive Geospatial Visualization	Render satellite datasets as dynamic map overlays using LeafletJS
🌊 NetCDF Scientific Data Processing	Real-time extraction and processing of multidimensional oceanographic datasets
🎞️ Temporal Animation & Playback	Animate time-series data with frame-by-frame ocean condition rendering
📅 Date-Range & Product Filtering	Query datasets by product type, satellite source, and custom date ranges
🔬 THREDDS / NCSS Data Access	Seamless scientific data retrieval via NetCDF Subset Service and WMS protocols
⚡ Real-Time Map Rendering	No static imagery — all layers generated dynamically from raw satellite data
🧱 Modular Architecture	Scalable, component-based design supporting diverse scientific visualization workflows
---
🏗️ System Architecture
```
┌─────────────────────────────────────────────────────────┐
│                      Web Browser                        │
│   ┌──────────────────────────────────────────────────┐  │
│   │  LeafletJS Map + georaster-layer-for-leaflet     │  │
│   │  Product Selector · Date Picker · Animation UI   │  │
│   └──────────────────────┬───────────────────────────┘  │
└──────────────────────────│──────────────────────────────┘
                           │ HTTP / REST
┌──────────────────────────▼──────────────────────────────┐
│                   Flask Backend                         │
│   ┌──────────────┐   ┌────────────┐   ┌─────────────┐  │
│   │  Data Router │   │  xarray /  │   │ Matplotlib  │  │
│   │  & API Layer │──▶│  NetCDF    │──▶│ + OpenCV    │  │
│   └──────────────┘   │  Processor │   │  Renderer   │  │
└───────────────────────┴──────┬─────┴───┴─────────────┴──┘
                               │ NCSS / WMS
┌──────────────────────────────▼──────────────────────────┐
│              THREDDS Data Server (TDS)                  │
│         Apache Tomcat 9 · NetCDF Datasets               │
└─────────────────────────────────────────────────────────┘
```
---
🔄 System Workflow
```
1. USER INPUT
   └─▶  Select product type, satellite source & date range via web UI

2. DATA RETRIEVAL
   └─▶  Flask backend queries THREDDS server via NCSS/WMS protocols

3. SCIENTIFIC PROCESSING
   └─▶  NetCDF bands extracted and processed with xarray

4. VISUALIZATION GENERATION
   └─▶  Geospatial layers rendered using Matplotlib & OpenCV

5. MAP RENDERING
   └─▶  Processed layers delivered to Leaflet frontend as interactive overlays

6. USER EXPLORATION
   └─▶  Animate, filter, and analyze temporal environmental variations
```
---
🛠️ Technology Stack
Frontend
Technology	Role
HTML5 / CSS3	Structure & styling
JavaScript	Client-side logic & interactivity
LeafletJS	Interactive geospatial map rendering
georaster-layer-for-leaflet	Raster data overlay on Leaflet maps
Backend
Technology	Role
Python	Core processing language
Flask	REST API & application server
xarray	N-dimensional NetCDF dataset handling
Matplotlib	Scientific figure and layer generation
OpenCV	Image processing and enhancement
Data & Infrastructure
Technology	Role
NetCDF	Scientific multidimensional data format
THREDDS Data Server (TDS)	Scientific dataset management & serving
Apache Tomcat 9	Application server for TDS
NCSS	NetCDF Subset Service for data querying
WMS	Web Map Service for geospatial layers
---
# 🗂️ Project Structure
```
SDV/
├── backend/
│   ├── app.py                      # Flask application entry point
│   ├── data_handler.py             # THREDDS / NCSS data retrieval
│   ├── processor.py                # NetCDF extraction & preprocessing
│   ├── visualizer.py               # Geospatial rendering and visualization
│   ├── utils.py                    # Helper utilities and shared functions
│   └── requirements.txt            # Python dependencies
│
├── frontend/
│   ├── index.html                  # Main web interface
│   ├── css/
│   │   └── styles.css              # UI styling and layout
│   └── js/
│       ├── map.js                  # Leaflet map initialization
│       ├── animation.js            # Temporal playback controls
│       ├── layers.js               # Layer rendering and management
│       └── api.js                  # Backend API integration
│
├── config/
│   └── settings.py                 # Server and dataset configuration
│
├── docs/
│   ├── architecture.png            # System architecture diagram
│   └── screenshots/                # Application screenshots
│
├── static/
│   └── generated/                  # Runtime-generated visualization outputs
│
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt```

### Later Overall frontend was converted to single file

> **Note:** Dataset files are excluded. See *[Note on Dataset Access](#-note-on-dataset-access)* below.
---
🚀 Getting Started
Prerequisites
Python 3.x
Node.js (optional, for frontend tooling)
Access to a THREDDS Data Server instance with oceanographic NetCDF datasets
Installation
```bash
# 1. Clone the repository
git clone https://github.com/your-username/SDV-Satellite-Data-Viewer.git
cd SDV-Satellite-Data-Viewer

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Configure your THREDDS server endpoint
#    Edit config/settings.py with your TDS server URL and dataset paths

# 5. Start the Flask development server
python backend/app.py
```
Open your browser and navigate to `http://localhost:5000`.
---
🔮 Future Enhancements
[ ] False Color Composite (FCC) — Advanced multi-band compositing for richer environmental interpretation
[ ] Cloud Top Temperature (CTT) Analysis — Enhanced cloud monitoring and weather pattern detection
[ ] Thermal Infrared Imagery (TIR) Processing — Surface heat anomaly detection from satellite TIR bands
[ ] AI-Assisted Analytics — Machine learning models for automated anomaly detection and pattern recognition
[ ] Real-Time Multi-Satellite Streaming — Live data ingestion from multiple concurrent satellite sources
[ ] Advanced Forecasting Modules — Geospatial predictive modeling and environmental forecasting
---
📂 Note on Dataset Access
The satellite datasets powering SDV are part of INCOIS's government scientific infrastructure and are therefore not redistributable. This repository contains only:
✅ Application source code
✅ Visualization and processing workflows
✅ Frontend and backend integration modules
To run the system, you will need access to a compatible THREDDS Data Server instance with oceanographic NetCDF products.
---
🏛️ Acknowledgements
Developed during a Summer Internship at the Indian National Centre for Ocean Information Services (INCOIS), Hyderabad, India — an autonomous body under the Ministry of Earth Sciences, Government of India.
---
<div align="center">
Built with 🌊 for ocean science.
</div>
