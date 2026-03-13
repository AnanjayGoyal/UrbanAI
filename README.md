# UrbanAI — India Location Intelligence
### A Python + Streamlit Data Analytics Platform

---

## Project Structure

```
urbanai/
├── app.py               ← Main Streamlit application
├── requirements.txt     ← Python dependencies
├── cities.csv           ← City-level data (19 cities)
├── neighborhoods.csv    ← Neighborhood scores & rent data (108 areas)
└── rentals.csv          ← Property listings (90 listings)
```

---

## Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## How It Works

### Data Flow
All three CSV files are loaded at startup and drive every feature:

| File | Used For |
|------|----------|
| `cities.csv` | City comparison charts, cost of living breakdown |
| `neighborhoods.csv` | Scoring engine, map heatmap, rankings |
| `rentals.csv` | Rental listings tab with filters |

### Scoring Engine
The scoring algorithm is a **weighted average** of 8 dimensions:

```
overall_score = Σ (dimension_score × preference_weight) / total_weight
```

Your sidebar choices (chips + sliders) act as multipliers:
- Toggling a preference **on** → boosts that dimension's weight by 1.3–1.5×
- Toggling it **off** → reduces weight to 0.5–0.7×

### Pages / Tabs
| Tab | What's Inside |
|-----|---------------|
| 🗺 Map | Folium heatmap with top-12 pins, switchable layers |
| 🏘 Rankings | Sortable neighborhood cards with scores |
| 📊 Insights | Bar charts, scatter, radar, correlation heatmap, CoL cards |
| 🏠 Rentals | Filtered property listings with rent distribution chart |
| 🏙 City Compare | Multi-city side-by-side comparison across all CSV metrics |

---

## Updating Your Data

### Option 1 — Replace CSV files directly
Edit `cities.csv`, `neighborhoods.csv`, or `rentals.csv` and restart the app.

### Option 2 — Upload in the app
Use the **"📂 Update Data Files"** panel in the sidebar to upload new CSVs while the app is running. No restart needed.

### Adding New Cities
1. Add a row to `cities.csv` with the city name and metrics
2. Add neighborhood rows to `neighborhoods.csv` with the same city name
3. Optionally add listings to `rentals.csv`
4. Restart the app (or re-upload files)

### Required Column Names

**cities.csv** — key columns:
`city, state, latitude, longitude, cost_of_living_index, avg_monthly_expenses_single, quality_of_life_score, pollution_index`

**neighborhoods.csv** — key columns:
`city, neighborhood, latitude, longitude, safety_score, transport_score, greenery_score, market_score, healthcare_score, schools_score, lifestyle_score, avg_rent_1bhk, avg_rent_2bhk, avg_rent_3bhk, cost_of_living_index, known_for`

**rentals.csv** — key columns:
`city, neighborhood, property_name, property_type, bedrooms, bathrooms, area_sqft, rent_per_month, furnishing, floor, total_floors, parking, amenities, listing_url, source, contact, description`

---

## Deploy to Streamlit Cloud (Free)

1. Push this folder to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the main file
4. Deploy — you get a public URL instantly

---

## Deploy to Vercel / Railway / Render

Not recommended — Streamlit apps are better hosted on Streamlit Cloud or Railway.
For Railway: add a `Procfile` with `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
