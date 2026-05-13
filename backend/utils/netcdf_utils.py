import os
import xarray as xr
from datetime import datetime, timedelta
from flask import jsonify

THREDDS_OPENDAP_BASE = "http://localhost:8089/thredds/dodsC/"
DATA_PATHS = {
    "sst": "data/metop/level2_avhrr",
    "fcc": "data/metop/level1_nc"
}

def daterange(start_date, end_date):
    for n in range((end_date - start_date).days + 1):
        yield start_date + timedelta(n)

def find_opendap_urls(product, start_date, end_date, satellite, sensor):
    folder = DATA_PATHS[product]
    base_path = f"C:/Satellite_capturing/SatelliteDashboard/thredds_content/{folder.replace('/', os.sep)}"
    urls = []

    for date in daterange(start_date, end_date):
        day_str = date.strftime("%Y%m%d")
        for filename in os.listdir(base_path):
            if filename.endswith(".nc") and filename.startswith(f"{satellite}_{sensor}") and day_str in filename:
                urls.append(f"{THREDDS_OPENDAP_BASE}{folder}/{filename}")

    return urls

def get_sst_data(start, end, satellite, sensor):
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        urls = find_opendap_urls("sst", start_dt, end_dt, satellite, sensor)

        data = []
        for url in urls:
            try:
                ds = xr.open_dataset(url)
                if 'sst' in ds:
                    sst = ds['sst'].values
                    data.append(sst.tolist())
            except Exception as e:
                print(f"Skipping {url} due to error:", e)

        if not data:
            return jsonify({"message": "No SST data found."}), 404
        return jsonify({"sst": data})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

def get_fcc_rgb(start, end, satellite, sensor):
    try:
        start_dt = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        urls = find_opendap_urls("fcc", start_dt, end_dt, satellite, sensor)

        frames = []
        for url in urls:
            try:
                ds = xr.open_dataset(url)
                if all(b in ds for b in ["band1", "band2"]):
                    r = ds["band2"].values
                    g = ds["band1"].values
                    b = ds["band1"].values
                    rgb = [[[int(r[i][j]), int(g[i][j]), int(b[i][j])]
                            for j in range(r.shape[1])]
                            for i in range(r.shape[0])]
                    frames.append(rgb)
                else:
                    print(f"Skipping {url} — missing required FCC bands")
            except Exception as e:
                print(f"Error processing {url}: {e}")

        if not frames:
            return jsonify({"message": "No FCC data found."}), 404
        return jsonify({"fcc": frames})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
