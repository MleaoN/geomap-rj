import pandas as pd
import numpy as np
import geopandas as gpd
import plotly.graph_objects as go
import requests
import base64

# ============================================================
# CONFIG
# ============================================================

INPUT_CSV = "synthetic_hover_municipios_export.csv"

YEARS = ["2014", "2018", "2022", "2026"]

SYMBOLS = {
    "2014": "🔶",
    "2018": "🔷",
    "2022": "🔺",
    "2026": "🟢"
}

# ============================================================
# HELPERS
# ============================================================

def normalize_text(series):
    return (
        series.astype(str)
        .str.upper()
        .str.normalize("NFKD")
        .str.encode("ascii", "ignore")
        .str.decode("utf-8")
    )

# ============================================================
# 1. LOAD SYNTHETIC DATA
# ============================================================

df = pd.read_csv(INPUT_CSV)

if "municipality" not in df.columns:
    raise ValueError("CSV must contain 'municipality' column")

df["municipality"] = normalize_text(df["municipality"])

# ============================================================
# 2. LOAD GEOJSON
# ============================================================

url = "https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-33-mun.json"
geojson = requests.get(url).json()

gdf = gpd.GeoDataFrame.from_features(geojson["features"])
gdf["municipality"] = normalize_text(gdf["name"])
gdf["id"] = gdf["id"].astype(str)

# ============================================================
# 3. MERGE
# ============================================================

gdf = gdf.merge(df, on="municipality", how="left")

# Merge validation (important)
missing = gdf["2014_VALUE"].isna().sum()
print(f"[DEBUG] Missing matches after merge: {missing}")

for col in ["2014_VALUE", "2018_VALUE", "2022_VALUE", "2026_VALUE"]:
    gdf[col] = pd.to_numeric(gdf[col], errors="coerce").fillna(0)

# ============================================================
# 4. LOG TRANSFORMATION
# ============================================================

for col in ["2014_VALUE", "2018_VALUE", "2022_VALUE", "2026_VALUE"]:
    gdf[col + "_LOG"] = np.log1p(gdf[col])

# ============================================================
# 5. LOAD LOGO
# ============================================================

with open("generic_logo.png", "rb") as f:
    encoded = base64.b64encode(f.read()).decode("utf-8")

# ============================================================
# 6. REGION MAPPING
# ============================================================

municipality_to_region = {
    # (keep your full mapping here unchanged)
}

gdf["region"] = gdf["municipality"].map(municipality_to_region)

# ============================================================
# 7. REGION POLYGONS
# ============================================================

gdf["geometry"] = gdf["geometry"].buffer(0)

region_gdf = gdf.dropna(subset=["region"]).dissolve(by="region", as_index=False)

region_codes = {
    name: i for i, name in enumerate(sorted(region_gdf["region"].dropna().unique()))
}
region_gdf["region_code"] = region_gdf["region"].map(region_codes)

REGION_COLORSCALE = [
    [0.0, "#fbb4ae"], [0.16, "#b3cde3"], [0.33, "#ccebc5"],
    [0.5, "#decbe4"], [0.66, "#fed9a6"], [0.83, "#ffffcc"], [1.0, "#e5d8bd"]
]

# ============================================================
# 8. BUILD FIGURE
# ============================================================

fig = go.Figure()

# Region layer
fig.add_choropleth(
    geojson=region_gdf.__geo_interface__,
    locations=region_gdf["region"],
    z=region_gdf["region_code"],
    colorscale=REGION_COLORSCALE,
    marker=dict(line=dict(width=1.5, color="black")),
    featureidkey="properties.region",
    showscale=False,
    hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
    customdata=np.stack([
        region_gdf["region"],
        region_gdf["region_code"]
    ], axis=-1)
)

# Global zmax
zmax_global = max(gdf[f"{y}_VALUE_LOG"].max() for y in YEARS)

# Municipal layers
for year in YEARS:
    fig.add_choropleth(
        geojson=geojson,
        locations=gdf["id"],
        z=gdf[f"{year}_VALUE_LOG"],
        colorscale="Viridis",
        marker=dict(line=dict(width=0.2, color="black"), opacity=0.55),
        featureidkey="properties.id",
        visible=(year == "2014"),
        zmin=0,
        zmax=zmax_global,
        colorbar=dict(
            title="Votes (log-scaled)",
            tickvals=[np.log1p(v) for v in [1,10,50,100,500,1000,5000,10000]],
            ticktext=["1","10","50","100","500","1k","5k","10k"]
        ),
        hovertemplate="<b>%{customdata[0]}</b><br>" +
                      f"{SYMBOLS['2014']} 2014: %{{customdata[1]:,}} votes (%{{customdata[5]:.2f}}%)<br>" +
                      f"{SYMBOLS['2018']} 2018: %{{customdata[2]:,}} votes (%{{customdata[6]:.2f}}%)<br>" +
                      f"{SYMBOLS['2022']} 2022: %{{customdata[3]:,}} votes (%{{customdata[7]:.2f}}%)<br>" +
                      f"{SYMBOLS['2026']} 2026: %{{customdata[4]:,}} votes (%{{customdata[8]:.2f}}%)<br>" +
                      "<extra></extra>",
        customdata=gdf[[
            "municipality",
            "2014_VALUE","2018_VALUE","2022_VALUE","2026_VALUE",
            "2014_PERCENT","2018_PERCENT","2022_PERCENT","2026_PERCENT"
        ]],
        showscale=True
    )

# ============================================================
# 9. DROPDOWN + LAYOUT
# ============================================================

buttons = []
for i, year in enumerate(YEARS):
    visibility = [True] + [False] * len(YEARS)
    visibility[1 + i] = True

    buttons.append(dict(
        label=f"{SYMBOLS[year]} {year}",
        method="update",
        args=[{"visible": visibility},
              {"title": f"Municipal Vote Map — {year} (Synthetic Data)"}]
    ))

fig.update_layout(
    title=dict(
        text="<b>Interactive Municipal Vote Map — Synthetic Data (Log-Scaled)</b>",
        x=0.5
    ),
    geo=dict(fitbounds="locations", visible=False),
    margin=dict(r=0, t=60, l=0, b=0),
    updatemenus=[dict(buttons=buttons, x=0.02, y=0.95)]
)

fig.add_layout_image(dict(
    source="data:image/png;base64," + encoded,
    xref="paper", yref="paper",
    x=1, y=0,
    sizex=0.18, sizey=0.18,
    xanchor="right", yanchor="bottom"
))

# ============================================================
# 10. OUTPUT
# ============================================================

fig.write_html("Synthetic_Municipal_Vote_Map_LogScaled.html")
fig.show()