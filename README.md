# 🗺️ GeoMap RJ — Synthetic Geospatial Analytics Dashboard

An interactive geospatial visualization platform for municipal-level election data in Rio de Janeiro, built using Python, GeoPandas, and Plotly.

This project demonstrates a production-style geospatial data pipeline using synthetic data while preserving the structure and logic of a real-world system.

---

## 🚀 Features

- Interactive municipal-level choropleth map
- Region-based aggregation layer (custom geographic grouping)
- Multi-year analysis: 2014, 2018, 2022, 2026
- Log-scaled visualization for skewed distributions
- Rich hover tooltips with:
  - Vote counts
  - Percentage metrics
- Dropdown selector for year switching
- Fully synthetic dataset (safe for public portfolio use)

---

## 🧱 Tech Stack

- Python
- Pandas / NumPy — data processing
- GeoPandas — geospatial operations
- Plotly — interactive visualization
- Requests — GeoJSON ingestion

---

## 📂 Project Structure

geomap-rj/  
├── synthetic_hover_municipios_export.csv  
├── geomap_script.py  
├── generic_logo.png  
├── requirements.txt  
└── README.md  

---

## ⚙️ How It Works

### 1. Data Input
The pipeline reads a synthetic CSV containing:
- Municipality names
- Vote counts per year
- Percentage metrics

### 2. Data Processing
- Text normalization for consistent joins
- Merge with official GeoJSON municipal boundaries
- Missing values safely handled

### 3. Feature Engineering
- Log transformation:
  log(value + 1)
- Region mapping based on predefined geography

### 4. Visualization
- Choropleth layers per year
- Region overlay polygons
- Interactive hover comparisons
- Dropdown year selector

---

## ▶️ Running the Project

### Install dependencies
pip install -r requirements.txt

### Run the script
python geopandas_synthetic_map.py

### Output
Synthetic_Municipal_Vote_Map_LogScaled.html

Open the HTML file in your browser to explore the interactive visualization.

---

## 📊 Data Notes

- Dataset is fully synthetic
- Maintains realistic statistical distribution
- Preserves geographic structure
- Safe for portfolio and public use

---

## 🧠 Engineering Highlights

- End-to-end ETL-style pipeline
- Robust geospatial normalization
- Multi-layer choropleth rendering
- Log-scaled distribution handling
- Modular and reproducible design

---

## 🔮 Future Improvements

- Dash web application interface
- Real-time data ingestion pipeline
- Data validation layer (schema enforcement)
- Dockerized deployment
- Fuzzy matching for municipality alignment

---

## 👤 Author

Marcelo Vieira Leão Nunes  
Ph.D. in Biomedical Engineering | Data Scientist  

LinkedIn: https://www.linkedin.com/in/marcelo-vieira-leao-nunes  
GitHub: https://github.com/MvleaoN  

---

## 📄 License

This project is intended for educational and portfolio purposes.
