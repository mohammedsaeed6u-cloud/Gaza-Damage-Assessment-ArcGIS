import shapefile
import json
import math
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# WGS84 Ellipsoid
a = 6378137.0
f = 1 / 298.257223563
b = a * (1 - f)
e_sq = 1 - (b / a)**2
k0 = 0.9996
lon0 = math.radians(33.0)

def utm36n_to_latlon(e, n):
    x = e - 500000.0
    y = n
    m = y / k0
    mu = m / (a * (1 - e_sq/4 - 3*e_sq**2/64 - 5*e_sq**3/256))
    e1 = (1 - math.sqrt(1 - e_sq)) / (1 + math.sqrt(1 - e_sq))
    j1 = 3*e1/2 - 27*e1**3/32
    j2 = 21*e1**2/16 - 55*e1**4/32
    j3 = 151*e1**3/96
    j4 = 1097*e1**4/512
    fp = mu + j1*math.sin(2*mu) + j2*math.sin(4*mu) + j3*math.sin(6*mu) + j4*math.sin(8*mu)
    e1sq = e_sq / (1 - e_sq)
    c1 = e1sq * (math.cos(fp))**2
    t1 = (math.tan(fp))**2
    r1 = a * (1 - e_sq) / ((1 - e_sq * (math.sin(fp))**2)**1.5)
    n1 = a / math.sqrt(1 - e_sq * (math.sin(fp))**2)
    d = x / (n1 * k0)
    lat = fp - (n1 * math.tan(fp) / r1) * (d**2 / 2 - (5 + 3*t1 + 10*c1 - 4*c1**2 - 9*e1sq)*d**4 / 24)
    lon = lon0 + (d - (1 + 2*t1 + c1)*d**3 / 6) / math.cos(fp)
    
    # Apply calibrated geodetic alignment shift
    calib_lon = math.degrees(lon) - 0.000082
    calib_lat = math.degrees(lat) + 0.000010
    
    return round(calib_lat, 6), round(calib_lon, 6)

# Neighborhood Bounding Boxes [min_lat, min_lon, max_lat, max_lon]
neighborhoods_config = {
    'rimal_shifa': {
        'name': 'حي الرمال ومجمع الشفاء',
        'bounds': [31.5170, 34.4340, 31.5320, 34.4530],
        'center': [31.524, 34.444],
        'zoom': 17
    },
    'rimal_south': {
        'name': 'الرمال الجنوبي وتل الهوى',
        'bounds': [31.5000, 34.4280, 31.5160, 34.4480],
        'center': [31.508, 34.438],
        'zoom': 17
    },
    'old_city': {
        'name': 'البلدة القديمة وعمر المختار',
        'bounds': [31.4980, 34.4530, 31.5140, 34.4750],
        'center': [31.505, 34.464],
        'zoom': 17
    },
    'jabalia_camp': {
        'name': 'مخيم جباليا وساحة الشهداء',
        'bounds': [31.5280, 34.4880, 31.5450, 34.5090],
        'center': [31.536, 34.498],
        'zoom': 17
    },
    'khan_younis_center': {
        'name': 'وسط خان يونس والقلعة',
        'bounds': [31.3360, 34.2920, 31.3520, 34.3120],
        'center': [31.344, 34.302],
        'zoom': 17
    },
    'rafah_shaboura': {
        'name': 'وسط رفح ومخيم الشابورة',
        'bounds': [31.2760, 34.2460, 31.2930, 34.2660],
        'center': [31.284, 34.256],
        'zoom': 17
    },
    'deir_balah_center': {
        'name': 'دير البلح ومخيم النصيرات',
        'bounds': [31.4100, 34.3440, 31.4260, 34.3640],
        'center': [31.418, 34.354],
        'zoom': 17
    }
}

shp_path = r"D:\Gaza_Damage_Assessment_Project\02_Geodatabase\Gaza_Buildings_Clean.shp"
print("Reading Shapefile:", shp_path)
sf = shapefile.Reader(shp_path)
total_records = len(sf)
print(f"Total features in dataset: {total_records:,}")

neighborhood_features = {k: [] for k in neighborhoods_config}
neighborhood_areas = {k: 0.0 for k in neighborhoods_config}

print("Filtering and calibrating geometries...")
for idx, shape_rec in enumerate(sf.iterShapeRecords()):
    if idx % 50000 == 0 and idx > 0:
        print(f"  Processed {idx:,} / {total_records:,}...")
    
    sh = shape_rec.shape
    rec = shape_rec.record
    
    # Rough filter by UTM bounding boxes
    bbox = sh.bbox
    center_utm_x = (bbox[0] + bbox[2]) / 2.0
    center_utm_y = (bbox[1] + bbox[3]) / 2.0
    
    c_lat, c_lon = utm36n_to_latlon(center_utm_x, center_utm_y)
    
    # Check which neighborhood contains this center
    matched_key = None
    for k, conf in neighborhoods_config.items():
        b = conf['bounds']
        if b[0] <= c_lat <= b[2] and b[1] <= c_lon <= b[3]:
            matched_key = k
            break
            
    if not matched_key:
        continue
        
    bld_id = int(rec['Building_I'])
    footprint = round(float(rec['Bld_Footpr']), 1)
    gov_e = rec['Gov_Name_E']
    gov_a = rec['Gov_Name_A']
    
    # Convert points with calibrated alignment
    parts = list(sh.parts) + [len(sh.points)]
    rings = []
    for p_idx in range(len(sh.parts)):
        p_start = parts[p_idx]
        p_end = parts[p_idx + 1]
        ring_pts = []
        for p in sh.points[p_start:p_end]:
            p_lat, p_lon = utm36n_to_latlon(p[0], p[1])
            ring_pts.append([p_lon, p_lat]) # GeoJSON is [lon, lat]
        if ring_pts:
            # Ensure closed
            if ring_pts[0] != ring_pts[-1]:
                ring_pts.append(ring_pts[0])
            rings.append(ring_pts)
            
    if not rings:
        continue
        
    feature = {
        'type': 'Feature',
        'id': bld_id,
        'properties': {
            'id': bld_id,
            'area': footprint,
            'gov_e': gov_e,
            'gov_a': gov_a,
            'status': 'قائم وسليم 100% (أكتوبر 2023)'
        },
        'geometry': {
            'type': 'Polygon',
            'coordinates': rings
        }
    }
    
    neighborhood_features[matched_key].append(feature)
    neighborhood_areas[matched_key] += footprint

# Output directories
out_dirs = [
    r"C:\Users\mhmd saeed\.gemini\antigravity\scratch\gaza-deploy\data",
    r"C:\Users\mhmd saeed\Desktop\data",
    r"C:\Users\mhmd saeed\Desktop\مشروع_تقييم_أضرار_غزة_ArcGIS_الشامل\08_المنظومة_التفاعلية_Web_GIS_أوفلاين\data"
]

for d in out_dirs:
    os.makedirs(d, exist_ok=True)

manifest = {}

for k, feats in neighborhood_features.items():
    conf = neighborhoods_config[k]
    count = len(feats)
    total_area = round(neighborhood_areas[k])
    print(f"\nNeighborhood '{k}' ({conf['name']}):")
    print(f"  Count: {count:,} buildings")
    print(f"  Total Area: {total_area:,} m²")
    
    fc = {
        'type': 'FeatureCollection',
        'name': f"gaza_buildings_{k}",
        'crs': { 'type': 'name', 'properties': { 'name': 'urn:ogc:def:crs:OGC:1.3:CRS84' } },
        'features': feats
    }
    
    geojson_str = json.dumps(fc, ensure_ascii=False, separators=(',', ':'))
    js_str = f"window.onNeighborhoodLoaded('{k}', {geojson_str});"
    
    for d in out_dirs:
        geojson_path = os.path.join(d, f"neighborhood_{k}.geojson")
        js_path = os.path.join(d, f"neighborhood_{k}.js")
        with open(geojson_path, 'w', encoding='utf-8') as f:
            f.write(geojson_str)
        with open(js_path, 'w', encoding='utf-8') as f:
            f.write(js_str)
            
    manifest[k] = {
        'name': conf['name'],
        'count': count,
        'area_sqm': total_area,
        'center': conf['center'],
        'zoom': conf['zoom'],
        'geojson': f"data/neighborhood_{k}.geojson",
        'js': f"data/neighborhood_{k}.js"
    }

for d in out_dirs:
    manifest_path = os.path.join(d, "neighborhoods_manifest.json")
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

print("\nAll 7 calibrated neighborhoods successfully generated and synced across all directories!")
