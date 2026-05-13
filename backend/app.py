from flask import Flask, request, jsonify, render_template, send_file
import os
import re
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import datetime
import tempfile
import requests
import matplotlib
matplotlib.use('Agg') 

app = Flask(__name__, template_folder="templates", static_folder="static")

THREDDS_WMS_BASE = "http://localhost:8089/thredds/wms/"
THREDDS_NCSS_BASE = "http://localhost:8089/thredds/ncss/"
LOCAL_BASE = os.path.join("SatelliteDashboard", "thredds_content")
 
DATA_FOLDER_MAP = {
    "sst": "data/metop/level2_avhrr",
    "chlorophyll": "data/OCM3",
    "fcc": "data/metop/level1_nc",
    "ctt": "data/metop/level1_nc",
    "thermal": "data/metop/level1_nc",
}

@app.route("/")
def index():
    return render_template("ofs_d_n.html")

@app.route("/api/wms_links")
def get_wms_links():
    product = request.args.get("product")
    satellite = request.args.get("satellite")
    sensor = request.args.get("sensor")
    start = request.args.get("start")
    end = request.args.get("end")

    if not all([product, satellite, sensor, start, end]):
        return jsonify({"error": "Missing parameters"}), 400

    folder = DATA_FOLDER_MAP.get(product)
    if not folder:
        return jsonify({"error": f"Unsupported product: {product}"}), 400

    start_date = datetime.strptime(start, "%Y-%m-%d").date()
    end_date = datetime.strptime(end, "%Y-%m-%d").date()

    local_path = os.path.join(LOCAL_BASE, *folder.split("/"))
    if not os.path.exists(local_path):
        return jsonify({"error": "Local folder not found."}), 404

    links = []
    for fname in os.listdir(local_path):
        if not fname.endswith(".nc"):
            continue

        try:
            if product == "chlorophyll":
                if not fname.startswith("OCM_"):
                    continue
                date_str = fname.replace("OCM_", "").replace(".nc", "")
                file_date = datetime.strptime(date_str, "%d%b%Y").date()
            else:
                if satellite not in fname or sensor not in fname:
                    continue
                match = re.search(r"(\d{8})[_-](\d{6})", fname)
                if not match:
                    continue
                file_date = datetime.strptime(match.group(1), "%Y%m%d").date()
        except Exception as e:
            print(f"[PARSE ERROR] {fname}: {e}")
            continue

        if start_date <= file_date <= end_date:
            if product in ["fcc", "ctt", "thermal"]:
                links.append(fname) 
            else:
                wms_url = f"{THREDDS_WMS_BASE}{folder}/{fname}"
                links.append(wms_url)

    return jsonify({"wms_links": sorted(links)})

import tempfile
import requests
import os

def fetch_bands_from_ncss(fname, bands):
    url = f"{THREDDS_NCSS_BASE}data/metop/level1_nc/{fname}"
    params = {
        "var": bands,
        "disableLLSubset": "on",
        "disableProjSubset": "on",
        "horizStride": 1,
        "addLatLon": "true"
    }

    print("[NCSS FETCH]", url, params)
    tmp_path = None
    try:
    
        with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as tmp:
            tmp_path = tmp.name
            r = requests.get(url, params=params)
            print(f"[HTTP] Status code: {r.status_code}")
            r.raise_for_status()
            tmp.write(r.content)

        ds = xr.open_dataset(tmp_path)
        arrays = [ds[b].squeeze().values for b in bands]
        ds.close()

        return arrays
    except Exception as e:
        print(f"[FETCH ERROR] {e}")
        raise
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


def normalize(arr):
    try:
        arr = np.ma.masked_invalid(arr)
        arr = arr.copy()
        if np.all(np.isnan(arr)):
            print("[NORMALIZE WARNING] Entire array is NaN.")
            return np.zeros_like(arr, dtype=np.uint8)

        min_val = np.nanpercentile(arr, 2)
        max_val = np.nanpercentile(arr, 98)

        arr = np.clip(arr, min_val, max_val)

        norm = (arr - min_val) / (max_val - min_val)
        norm_uint8 = (255 * norm).astype(np.uint8).copy()

        return norm_uint8

    except Exception as e:
        print(f"[NORMALIZE ERROR] {e}")
        return np.zeros_like(arr, dtype=np.uint8)



def render_rgb_image(bands):
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature

        if len(bands) != 3:
            raise ValueError("Three bands required for RGB image.")

        norm_bands = [normalize(b) for b in bands]
        rgb = np.dstack(norm_bands)

        height, width, _ = rgb.shape
        lon_min, lon_max = 68, 98   
        lat_min, lat_max = 6, 38    
        extent = [lon_min, lon_max, lat_min, lat_max]

        fig = plt.figure(figsize=(10, 8), dpi=150)
        ax = plt.axes(projection=ccrs.PlateCarree())

        im = ax.imshow(rgb, extent=extent, transform=ccrs.PlateCarree(), origin='upper')

        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        gl.right_labels = gl.top_labels = False
        gl.xlabel_style = {'size': 8}
        gl.ylabel_style = {'size': 8}

        ax.set_title("FCC - RGB Composite", fontsize=12, loc='left')
        ax.text(0.01, -0.08, "Source: INCOIS Ground Station", transform=ax.transAxes, fontsize=10)

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1, facecolor='white')
        plt.close(fig)
        buf.seek(0)
        return buf

    except Exception as e:
        print(f"[RENDER_RGB ERROR] {e}")
        raise



def render_ctt_image(band4):
    try:
        print(f"[CTT] Band4 shape: {band4.shape}")
        band_celsius = band4 - 273.15
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
        im = ax.imshow(band_celsius, cmap="nipy_spectral", vmin=-100, vmax=0)
        plt.colorbar(im, ax=ax, shrink=0.6, label="°C")
        ax.axis('off')
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"[RENDER_CTT ERROR] {e}")
        raise

def render_thermal_image(band4):
    try:
        import cartopy.crs as ccrs
        import cartopy.feature as cfeature

        band_celsius = band4 - 273.15
        print("[THERMAL] band4 min (°C):", np.nanmin(band_celsius), "max:", np.nanmax(band_celsius))

        vmin = np.nanpercentile(band_celsius, 2)
        vmax = np.nanpercentile(band_celsius, 98)
        if abs(vmax - vmin) < 1:
            vmin, vmax = np.nanmin(band_celsius), np.nanmax(band_celsius)

        fig = plt.figure(figsize=(10, 8), dpi=150)
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())  

        im = ax.imshow(
            band_celsius,
            cmap="gray",
            vmin=vmin,
            vmax=vmax,
            origin="upper",
            extent=[50, 105, -5, 45],
            transform=ccrs.PlateCarree()
        )

        ax.coastlines(resolution='10m', color='black')
        ax.add_feature(cfeature.BORDERS, edgecolor='black', linewidth=0.5)
        gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5)
        gl.top_labels = gl.right_labels = False

        ax.set_title("MAP: Thermal Product", loc='left', fontsize=12)
        ax.text(0.01, -0.08, "Source: INCOIS Ground Station", transform=ax.transAxes, fontsize=10)

        cbar = fig.colorbar(im, ax=ax, shrink=0.6, label="Brightness Temp (°C)")

        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)
        buf.seek(0)
        return buf

    except Exception as e:
        print(f"[RENDER_THERMAL ERROR] {e}")
        raise

@app.route("/api/fcc_image")
def fcc_image():
    fname = request.args.get("filename")
    if not fname:
        return "Filename required", 400
    try:
        print(f"[FCC] Processing: {fname}")
        try:
            bands = fetch_bands_from_ncss(fname, ["band2", "band1", "band1"])
            print("[FCC] Used band2/band1/band1")
        except Exception as e1:
            print(f"[FCC Fallback] band2/band1 failed: {e1}")
            bands = fetch_bands_from_ncss(fname, ["band4", "band5", "band5"])
            print("[FCC] Used fallback band4/band5/band5")
        for i, b in enumerate(bands):
            print(f"[FCC] Band {i+1} shape: {b.shape}, min: {np.nanmin(b)}, max: {np.nanmax(b)}")
        buf = render_rgb_image(bands)
        return send_file(buf, mimetype="image/png")
    except Exception as e:
        print(f"[FCC ERROR] {e}")
        return f"Failed to generate FCC: {e}", 500

@app.route("/api/ctt_image")
def ctt_image():
    fname = request.args.get("filename")
    if not fname:
        return "Filename required", 400
    try:
        print(f"[CTT] Processing: {fname}")
        band4, = fetch_bands_from_ncss(fname, ["band4"])
        print(f"[CTT] band4 min: {np.nanmin(band4)}, max: {np.nanmax(band4)}")
        buf = render_ctt_image(band4)
        return send_file(buf, mimetype="image/png")
    except Exception as e:
        print(f"[CTT ERROR] {e}")
        return f"Failed to generate CTT: {e}", 500

@app.route("/api/thermal_image")
def thermal_array():
    fname = request.args.get("filename")
    if not fname:
        return "Filename required", 400

    try:
        print(f"[THERMAL] Processing: {fname}")
        band4, = fetch_bands_from_ncss(fname, ["band4"])
        print(f"[THERMAL] band4 min: {np.nanmin(band4)}, max: {np.nanmax(band4)}")

        band_celsius = band4 - 273.15
        print("[THERMAL] band4 min (K):", np.nanmin(band4), "max:", np.nanmax(band4))
        print("[THERMAL] band4 min (°C):", np.nanmin(band_celsius), "max:", np.nanmax(band_celsius))

        vmin = np.nanpercentile(band_celsius, 2)
        vmax = np.nanpercentile(band_celsius, 98)
        if abs(vmax - vmin) < 1:
            vmin, vmax = np.nanmin(band_celsius), np.nanmax(band_celsius)
        print(f"[THERMAL] Using vmin={vmin}, vmax={vmax}")
        
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
        im = ax.imshow(band_celsius, cmap="inferno", vmin=180, vmax=320)
        plt.colorbar(im, ax=ax, shrink=0.6, label="Brightness Temp (°C)")
        ax.axis('off')

        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        print(f"[THERMAL ERROR] {e}")
        return f"Failed to generate Thermal: {e}", 500

import matplotlib
matplotlib.use('Agg')  

import matplotlib.pyplot as plt

@app.route("/api/ctt_image_old")
def ctt_image_old():
    fname = request.args.get("filename")
    if not fname:
        return "Filename required", 400

    try:
        print(f"[CTT] Requested file: {fname}")
        band4, = fetch_bands_from_ncss(fname, ["band4"])
        print(f"[CTT] band4 shape: {band4.shape}, min: {np.nanmin(band4)}, max: {np.nanmax(band4)}")

        buf = render_ctt_image(band4)

        
        response = send_file(buf, mimetype="image/png")
        response.headers['X-Bounds'] = "6.0,68.0,37.0,97.0"  
        return response

    except Exception as e:
        print(f"[CTT ERROR] {e}")
        return f"Failed to generate CTT: {e}", 500
    
@app.route("/api/stats")
def get_stats():
    filename = request.args.get("filename")
    product = request.args.get("product")
    
    if not filename or not product:
        return jsonify({"error": "Missing filename or product"}), 400

    var_map = {
        "sst": ("sst", "data/metop/level2_avhrr"),
        "chlorophyll": ("chlor_a", "data/OCM3"),
        "ctt": ("band4", "data/metop/level1_nc"),
        "thermal": ("band4", "data/metop/level1_nc")
    }

    if product not in var_map:
        return jsonify({"error": "Unsupported product"}), 400

    var_name, relative_path = var_map[product]
    local_path = os.path.join("SatelliteDashboard", "thredds_content", relative_path, filename)

    if not os.path.exists(local_path):
        return jsonify({"error": "File not found."}), 404

    try:
        ds = xr.open_dataset(local_path)
        data = ds[var_name].values
        ds.close()

        data = np.ma.masked_invalid(data)

        if product in ["sst", "ctt", "thermal"]:
            data = data - 273.15

        min_val = float(np.nanpercentile(data, 2))
        max_val = float(np.nanpercentile(data, 98))

        return jsonify({
            "min": round(min_val, 2),
            "max": round(max_val, 2)
        })

    except Exception as e:
        print(f"[STATS ERROR] {e}")
        return jsonify({"error": str(e)}), 500

    
if __name__ == "__main__":
    app.run(debug=True)
