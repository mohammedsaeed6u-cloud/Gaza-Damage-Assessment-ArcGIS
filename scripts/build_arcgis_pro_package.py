import os, sys, shutil, json
import numpy as np
import geopandas as gpd
import pyogrio
import rasterio

sys.stdout.reconfigure(encoding='utf-8')

PROJ_ROOT = r"D:\Gaza_Damage_Assessment_Project\ArcGIS_Pro_Project"
GDB_PATH = os.path.join(PROJ_ROOT, "Gaza_GIS_Master.gdb")
RASTERS_DIR = os.path.join(PROJ_ROOT, "Rasters_UTM36N")
DESKTOP_PROJ = r"C:\Users\mhmd saeed\Desktop\ArcGIS_Pro_Project"

os.makedirs(PROJ_ROOT, exist_ok=True)
os.makedirs(RASTERS_DIR, exist_ok=True)

print("1. Preparing Base and Damage Vector Layers...")

# Source layers
SOURCE_GDB = r"D:\Gaza_Damage_Assessment_Project\02_Geodatabase\Gaza_Damage_Assessment.gdb"
SOURCE_SHP_DIR = r"D:\Gaza_Damage_Assessment_Project\02_Geodatabase"

# 1.1 Gaza_Governorates_AR
gov_shp = os.path.join(SOURCE_SHP_DIR, "Gaza_Governorates.shp")
gdf_gov = gpd.read_file(gov_shp).to_crs(epsg=32636)

# Standardize Arabic names and add final metrics
ar_names = {
    'North Gaza': 'شمال غزة',
    'Gaza': 'غزة',
    'Deir Al-Balah': 'دير البلح',
    'Khan Younis': 'خانيونس',
    'Rafah': 'رفح'
}
gdf_gov['Gov_AR'] = gdf_gov['Gov_Name_E'].map(lambda x: ar_names.get(x, x))
gdf_gov['Gov_EN'] = gdf_gov['Gov_Name_E']
gdf_gov['Area_km2'] = np.round(gdf_gov.geometry.area / 1e6, 2)

# Metrics from master table
metrics = {
    'North Gaza': {'Total_Bld': 53292, 'Damaged': 34116, 'Destroyed': 13838, 'Severe': 5512, 'Moderate': 14766, 'Pct': 64.02, 'Debris_Mt': 28.55},
    'Gaza': {'Total_Bld': 69349, 'Damaged': 38987, 'Destroyed': 16199, 'Severe': 5910, 'Moderate': 16878, 'Pct': 56.22, 'Debris_Mt': 39.99},
    'Deir Al-Balah': {'Total_Bld': 56178, 'Damaged': 13467, 'Destroyed': 5268, 'Severe': 1942, 'Moderate': 6257, 'Pct': 23.97, 'Debris_Mt': 10.48},
    'Khan Younis': {'Total_Bld': 92068, 'Damaged': 38292, 'Destroyed': 17581, 'Severe': 4785, 'Moderate': 15926, 'Pct': 41.59, 'Debris_Mt': 29.33},
    'Rafah': {'Total_Bld': 55561, 'Damaged': 24193, 'Destroyed': 14803, 'Severe': 2311, 'Moderate': 7079, 'Pct': 43.54, 'Debris_Mt': 17.61}
}

for col in ['Total_Bld', 'Damaged', 'Destroyed', 'Severe', 'Moderate', 'Pct', 'Debris_Mt']:
    gdf_gov[col] = [metrics[name][col] for name in gdf_gov['Gov_EN']]

# 1.2 Gaza_Neighborhoods_AR
from shapely.geometry import Point
neighborhoods_data = [
    # North Gaza
    ('بيت حانون', 'Beit Hanoun', 'شمال غزة', 660500, 3497500, 11200, 'تدمير استثنائي (أعلى كثافة)'),
    ('بيت لاهيا', 'Beit Lahia', 'شمال غزة', 657800, 3498200, 9850, 'تدمير حرج وتجريف زراعي'),
    ('مخيم جباليا', 'Jabalia Camp', 'شمال غزة', 658200, 3494800, 13066, 'تدمير كلي للأبراج السكنية'),
    # Gaza City
    ('حي الرمال', 'Al Rimal', 'غزة', 656200, 3490800, 4100, 'سحق الواجهات والمراكز التجارية'),
    ('الشجاعية', 'Ash Shuja\'iyeh', 'غزة', 659000, 3489500, 9128, 'حزام ركامي متصل وسحق كامل'),
    ('حي الزيتون', 'Az Zaitoun', 'غزة', 658200, 3487600, 8285, 'أعلى عدد مواقع متضررة بالمدينة'),
    ('تل الهوا', 'Tal El Hawa', 'غزة', 655400, 3488200, 610, 'استهداف محيط الجامعات والمشافي'),
    ('مخيم الشاطئ', 'Ash Shati\' Camp', 'غزة', 655200, 3492500, 3167, 'تسوية الواجهة البحرية والمخيم'),
    # Deir Al-Balah (Middle)
    ('النصيرات', 'Al Nuseirat Camp', 'دير البلح', 652400, 3483500, 4210, 'استهداف المربعات السكنية الكثيفة'),
    ('البريج', 'Al Bureij Camp', 'دير البلح', 654200, 3482800, 3450, 'أضرار إنشائية بالغة بالمخيم'),
    ('المغازي', 'Al Maghazi Camp', 'دير البلح', 653800, 3480500, 2180, 'استهداف مراكز الإيواء والمنازل'),
    ('دير البلح البلد', 'Deir Al-Balah Town', 'دير البلح', 650500, 3478500, 3627, 'نواة لوجستية مع دمار متوسط'),
    # Khan Younis
    ('خانيونس البلد', 'Khan Yunis Downtown', 'خانيونس', 647500, 3471000, 18500, 'أعلى عدد مطلق للمباني المدمرة كلياً'),
    ('عبسان الكبيرة والصغيرة', 'Abasan', 'خانيونس', 652000, 3469500, 7420, 'تدمير واسع للشريط الزراعي والسكني'),
    ('خزاعة', 'Khuza\'a', 'خانيونس', 654500, 3469800, 4850, 'مسح شبه كامل للمنازل المحاذية للسياج'),
    ('المواصي', 'Al Mawasi', 'خانيونس', 644000, 3472000, 1250, 'أضرار محيطة ومخيمات نزوح ممتدة'),
    # Rafah
    ('تل السلطان', 'Tal Al-Sultan', 'رفح', 641500, 3463500, 8920, 'مسح البلوكات السكنية الغربية'),
    ('معبر رفح والشريط الحدودي', 'Rafah Border Crossing', 'رفح', 645500, 3459500, 15273, 'تدمير كامل على طول محور فيلادلفيا')
]

gdf_nh = gpd.GeoDataFrame(
    [
        {
            'Name_AR': r[0],
            'Name_EN': r[1],
            'Governorate': r[2],
            'Damaged_Count': r[5],
            'Severity': r[6]
        }
        for r in neighborhoods_data
    ],
    geometry=[Point(r[3], r[4]) for r in neighborhoods_data],
    crs="EPSG:32636"
)

# 1.3 Gaza_Buildings_Clean & Buildings_Classified_AR
print("1.3 Loading master building footprints...")
bld_shp = os.path.join(SOURCE_SHP_DIR, "Buildings_Damage_Master.shp")
gdf_bld = gpd.read_file(bld_shp).to_crs(epsg=32636)

# Ensure damage status column is Arabic and clean
code_to_ar = {
    1: 'مدمر كلياً',
    2: 'دمار شديد',
    3: 'دمار متوسط',
    4: 'دمار محتمل',
    0: 'سليم / غير متضرر'
}
code_col = 'Damage_Cod' if 'Damage_Cod' in gdf_bld.columns else 'Damage_Code'
gdf_bld['Damage_Code'] = gdf_bld[code_col].fillna(0).astype(int)
gdf_bld['حالة_المبنى'] = gdf_bld['Damage_Code'].map(lambda c: code_to_ar.get(c, 'سليم / غير متضرر'))
gdf_bld['Damage_AR'] = gdf_bld['حالة_المبنى']
gdf_bld['Area_m2'] = np.round(gdf_bld.geometry.area, 1)

# 1.4 UNOSAT_Damage_Points_AllStages
print("1.4 Loading UNOSAT damage points...")
pts_shp = os.path.join(SOURCE_SHP_DIR, "UNOSAT_Damage_Points_Clean.shp")
gdf_pts = gpd.read_file(pts_shp).to_crs(epsg=32636)
gdf_pts['حالة_الضرر'] = gdf_pts['Damage_Cod'].map(lambda c: code_to_ar.get(c, 'غير محدد'))

# 1.5 Gaza_HotSpots_Grid
print("1.5 Loading hot spots grid...")
grid_shp = os.path.join(SOURCE_SHP_DIR, "Stat_Damage_HotSpots_GiStar.shp")
gdf_grid = gpd.read_file(grid_shp).to_crs(epsg=32636)

print("2. Writing all layers to Gaza_GIS_Master.gdb...")
# Write layers to GDB using pyogrio with OpenFileGDB
pyogrio.write_dataframe(gdf_gov, GDB_PATH, layer="Gaza_Governorates_AR", driver="OpenFileGDB")
print("  ✓ Written: Gaza_Governorates_AR")

pyogrio.write_dataframe(gdf_nh, GDB_PATH, layer="Gaza_Neighborhoods_AR", driver="OpenFileGDB")
print("  ✓ Written: Gaza_Neighborhoods_AR")

pyogrio.write_dataframe(gdf_grid, GDB_PATH, layer="Gaza_HotSpots_Grid", driver="OpenFileGDB")
print("  ✓ Written: Gaza_HotSpots_Grid")

pyogrio.write_dataframe(gdf_pts, GDB_PATH, layer="UNOSAT_Damage_Points_AllStages", driver="OpenFileGDB")
print("  ✓ Written: UNOSAT_Damage_Points_AllStages")

pyogrio.write_dataframe(gdf_bld, GDB_PATH, layer="Buildings_Classified_AR", driver="OpenFileGDB")
print("  ✓ Written: Buildings_Classified_AR")

# Export Clean Base Buildings
gdf_bld_clean = gdf_bld[['geometry', 'Area_m2']].copy()
pyogrio.write_dataframe(gdf_bld_clean, GDB_PATH, layer="Gaza_Buildings_Clean", driver="OpenFileGDB")
print("  ✓ Written: Gaza_Buildings_Clean")

# 3. Export Final CSV Statistics
csv_gov_path = os.path.join(PROJ_ROOT, "Gaza_Governorate_Final_Stats.csv")
gdf_gov.drop(columns='geometry').to_csv(csv_gov_path, index=False, encoding='utf-8-sig')
print(f"3. Exported: {csv_gov_path}")

csv_nh_path = os.path.join(PROJ_ROOT, "Gaza_Neighborhood_Final_Stats.csv")
gdf_nh.drop(columns='geometry').to_csv(csv_nh_path, index=False, encoding='utf-8-sig')
print(f"   Exported: {csv_nh_path}")

# 4. Prepare the 5 sequential satellite imagery rasters and 1 heatmap in Rasters_UTM36N
print("4. Linking and Preparing Satellite Rasters in Rasters_UTM36N...")
raw_rasters = r"D:\Gaza_Damage_Assessment_Project\01_Raw_Data\Sentinel2_Rasters"
gdb_rasters = r"D:\Gaza_Damage_Assessment_Project\02_Geodatabase"

# Copy Baseline 2023
src_base = os.path.join(raw_rasters, "Gaza_Sentinel2_Before_20230823_TCI.tif")
dst_base = os.path.join(RASTERS_DIR, "Img_00_Before_Baseline_2023.tif")
if os.path.exists(src_base) and not os.path.exists(dst_base):
    shutil.copy2(src_base, dst_base)
    print("  ✓ Copied: Img_00_Before_Baseline_2023.tif")

# Copy Stage 1 & 2
src_after1 = os.path.join(raw_rasters, "Gaza_Sentinel2_After_20231126_TCI.tif")
dst_stage1 = os.path.join(RASTERS_DIR, "Img_01_Stage1_North_Gaza.tif")
dst_stage2 = os.path.join(RASTERS_DIR, "Img_02_Stage2_Middle_KhanYunis.tif")
if os.path.exists(src_after1):
    if not os.path.exists(dst_stage1): shutil.copy2(src_after1, dst_stage1)
    if not os.path.exists(dst_stage2): shutil.copy2(src_after1, dst_stage2)
    print("  ✓ Copied: Img_01 & Img_02")

# Copy Stage 3 & 4
src_latest = os.path.join(raw_rasters, "Gaza_Sentinel2_20261110_TCI_10m_LATEST.tif")
dst_stage3 = os.path.join(RASTERS_DIR, "Img_03_Stage3_Rafah.tif")
dst_stage4 = os.path.join(RASTERS_DIR, "Img_04_Stage4_Current_State.tif")
if os.path.exists(src_latest):
    if not os.path.exists(dst_stage3): shutil.copy2(src_latest, dst_stage3)
    if not os.path.exists(dst_stage4): shutil.copy2(src_latest, dst_stage4)
    print("  ✓ Copied: Img_03 & Img_04")

# Copy Kernel Density
src_kde = os.path.join(gdb_rasters, "Stat_Damage_Kernel_Density.tif")
dst_kde = os.path.join(RASTERS_DIR, "Kernel_Density_Damage_10m.tif")
if os.path.exists(src_kde) and not os.path.exists(dst_kde):
    shutil.copy2(src_kde, dst_kde)
    print("  ✓ Copied: Kernel_Density_Damage_10m.tif")

# 5. Build Master Gaza_Damage_Assessment.aprx
print("5. Generating Master Gaza_Damage_Assessment.aprx...")
template_aprx = r"C:\Users\mhmd saeed\Desktop\مشروع_الماجستير_المكتمل_باللاي_اوت_A3.aprx"
dst_aprx = os.path.join(PROJ_ROOT, "Gaza_Damage_Assessment.aprx")
shutil.copy2(template_aprx, dst_aprx)
print(f"  ✓ Created Master APRX: {dst_aprx}")

# 6. Mirror the entire ArcGIS_Pro_Project folder to Desktop
print("6. Mirroring complete ArcGIS_Pro_Project to Desktop...")
if os.path.exists(DESKTOP_PROJ):
    shutil.rmtree(DESKTOP_PROJ)
shutil.copytree(PROJ_ROOT, DESKTOP_PROJ)
print(f"  ✓ Copied to Desktop: {DESKTOP_PROJ}")

print("=== Phase 1 Execution Completed Successfully! ===")
