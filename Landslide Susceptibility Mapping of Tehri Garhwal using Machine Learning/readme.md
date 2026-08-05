# 🏔️ High-Resolution Landslide Susceptibility Mapping (LSM) — Tehri Garhwal, India

An end-to-end geospatial machine learning framework for **10m hyper-resolution Landslide Susceptibility Mapping (LSM)** across the **Tehri Garhwal district, Uttarakhand, India**. This project evaluates four computational architectures—**Logistic Regression (LR)**, **Random Forest (RF)**, **Extreme Gradient Boosting (XGBoost)**, and **Light Gradient Boosting Machine (LightGBM)**—integrating 14 multi-source geospatial factors to predict and delineate regional landslide hazards.

---

## 📌 Study Region & Spatial Resolution

* **Target Region:** Tehri Garhwal District, Uttarakhand (North-Western Himalayas, India).
* **Geographical Extent:** Latitudes $30^\circ 30'\text{ N}$ to $31^\circ 2'\text{ N}$, Longitudes $77^\circ 51'\text{ E}$ to $79^\circ 2'\text{ E}$ ($\approx 3,642\text{ km}^2$).
* **Spatial Resolution:** $10\text{ m} \times 10\text{ m}$ hyper-resolution pixel grid (a $9\times$ data density increase over conventional $30\text{ m}$ models).
* **Coordinate Reference System:** `WGS 84 / UTM Zone 44N` (`EPSG:32644`).
* **Landslide Inventory:** 2,591 verified historical landslide locations compiled from BHUKOSH-Geological Survey of India (GSI), paired with 2,591 pseudo-absence points ($1:1$ balanced dataset = 5,182 points total).
* **Data Partitioning:** 70% Training ($3,627\text{ points}$) / 30% Testing ($1,555\text{ points}$) with $5$-fold cross-validation.

---

## ✨ Key Features

* **10m Data Harmonization:** Downscaled and resampled raster feature stack utilizing Bilinear Interpolation for DEM-derived layers and Cubic Spline Resampling for IMD gridded daily rainfall data.
* **VIF Multicollinearity Screening:** Rigorous Variance Inflation Factor (VIF) verification ensuring all 14 conditioning factors remain independent ($1.013 \le \text{VIF} \le 2.458 < 2.5$).
* **Tree-Based & Gradient Boosting Architectures:** Benchmark comparison between baseline linear models and state-of-the-art boosting algorithms (XGBoost and LightGBM).
* **GIS-Ready Hazard Zoning:** Reclassification of predicted probabilities into 5 hazard levels (*Very Low, Low, Moderate, High, Very High*) using Natural Breaks (Jenks).

---

## 📊 Conditioning Factors & Feature Visualizations

The pipeline incorporates **14 conditioning factors** spanning topographic, geological, hydrological, environmental, and anthropogenic drivers:

| Category | Factors Included | Primary Data Source |
| :--- | :--- | :--- |
| **Morphometric** | Elevation, Slope Angle, Slope Aspect, Curvature, Topographic Wetness Index (TWI), Geomorphon | USGS SRTM DEM ($30\text{ m} \to 10\text{ m}$) |
| **Geological & Soil** | Lithology, Distance to Faults, Soil Type | BHUKOSH-GSI / FAO-UNESCO |
| **Hydrological & Climate** | Distance to Streams, Mean Annual Rainfall | BHUKOSH-GSI / IMD ($0.25^\circ \to 10\text{ m}$) |
| **Anthropogenic & Environmental**| Distance to Roads, NDVI, Land Use / Land Cover (LULC) | NGDR / Sentinel-2 / ESRI 10m |

<!-- REPLACE 'docs/features_visual.png' WITH YOUR ACTUAL IMAGE PATH -->
![Landslide Conditioning Factors](docs/features_visual.png)
*Figure 1: Visual layout of the 14 spatial conditioning factors across the Tehri Garhwal district.*

---

## ⚙️ Methodology & Pipeline Workflow

```text
┌───────────────────────────────┐    ┌───────────────────────────────┐    ┌───────────────────────────────┐
│ Multi-Source Spatial Data     │───>│ Resampling & Feature Stack    │───>│ Balanced Sampling Protocol    │
│ (USGS DEM, GSI, IMD, Sentinel)│    │ (10m Alignment, EPSG:32644)   │    │ (2,591 LS + 2,591 Non-LS)     │
└───────────────────────────────┘    └───────────────────────────────┘    └───────────────────────────────┘
                                                                                          │
                                                                                          ▼
┌───────────────────────────────┐    ┌───────────────────────────────┐    ┌───────────────────────────────┐
│ 5-Class Hazard Maps (GeoTIFF) │<───│ Performance Validation        │<───│ 5-Fold Cross Validation       │
│ (Jenks Natural Breaks)        │    │ (ROC-AUC, Precision, F1)      │    │ (LR, RF, XGBoost, LightGBM)   │
└───────────────────────────────┘    └───────────────────────────────┘    └───────────────────────────────┘
