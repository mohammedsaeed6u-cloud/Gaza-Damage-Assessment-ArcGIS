# Multi-Sensor Urban Damage Assessment of the Gaza Strip (2023–2026)
## تقييم الاستشعار عن بعد والتحليل المكاني للدمار العمراني في قطاع غزة

[![ArcGIS Pro](https://img.shields.io/badge/ArcGIS_Pro-3.x-007AC2?logo=esri&logoColor=white)](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Copernicus Sentinel-2](https://img.shields.io/badge/Copernicus-Sentinel--2_L2A-003399)](https://sentinels.copernicus.eu/)
[![UNOSAT](https://img.shields.io/badge/UNOSAT-Satellite_Analysis-1E40AF)](https://unosat.org/)
[![Spatial Reference](https://img.shields.io/badge/CRS-EPSG%3A32636_(UTM_36N)-10B981)](#spatial-reference)

---

## 📌 نبذة عامة عن المشروع (Executive Summary)

يمثل هذا المشروع دراسة أكاديمية متقدمة في مجال **نظم المعلومات الجغرافية (GIS) والاستشعار عن بعد (Remote Sensing)** توثق التغيرات المكانية والدمار العمراني الشامل في **قطاع غزة ومدينة غزة (2023 - 2026)** بدقة تحليلية 10 أمتار، اعتماداً على مرئيات القمر الصناعي الأوروبي **Copernicus Sentinel-2 L2A** وقواعد بيانات مركز الأمم المتحدة للأقمار الصناعية (**UNOSAT CDA**) ومكتب تنسيق الشؤون الإنسانية (**OCHA**).

This repository contains the complete, reproducible **ArcGIS Pro project (`.aprx`)**, **File Geodatabase (`.gdb`)**, **spatial analysis scripts (Python / ArcPy)**, **interactive web-based presentation**, and **high-resolution cartographic layouts (A3 Landscape at 300 DPI)** for the multi-temporal damage assessment of the Gaza Strip.

---

## 🔬 المنهجية العلمية ومصادر البيانات (Methodology & Data)

1. **المرئيات الفضائية (Copernicus Sentinel-2 L2A):**
   - استخراج 4 مراحل زمنية متتالية خالية تماماً من الغيوم بنسبة **`0.0%` غيوم ودخان**:
     - **خط الأساس (Baseline):** 17 سبتمبر 2023 (سماء صافية 0.02% غيوم).
     - **المرحلة الأولى (Phase 1):** 26 ديسمبر 2023 (صورة نقية خالية تماماً من أعمدة الدخان).
     - **المرحلة الثانية (Phase 2):** 11 سبتمبر 2024 (بعد عام كامل، توثق تسوية المربعات السكنية).
     - **الوضع الراهن (Present):** 10 نوفمبر 2026 (معايرة لونية طبيعية لمياه البحر بلون كحلي أردوازي `#0E2A47`).
2. **قاعدة بيانات التدمير (UNOSAT Comprehensive Damage Assessment):**
   - حصر وتصنيف **46,687 موقعاً متضرراً** في مدينة غزة و**326,448 مبنى** على مستوى قطاع غزة.
   - تصنيف الدمار كارتوغرافياً إلى 4 مستويات:
     - 🔴 **مدمر كلياً (Destroyed):** `#B91C1C`
     - 🟠 **دمار شديد (Severely Damaged):** `#EA580C`
     - 🟡 **دمار متوسط (Moderately Damaged):** `#F59E0B`
     - ⚪ **سليم / أضرار طفيفة:** `#CBD5E1`
3. **النطاق المكاني والإسقاط الجغرافي:**
   - **المرجع الجيوديسي:** WGS 1984
   - **المسقط:** Universal Transverse Mercator (UTM) Zone 36N (`EPSG:32636`)

---

## 📊 النتائج والإحصائيات المعتمدة (Validated Statistics)

### مدينة غزة (Gaza City Focus - 73.83 km²)
- **إجمالي المواقع المتضررة الموثقة:** `46,687` موقعاً (UNOSAT)
- **إجمالي الكتلة العمرانية الحضرية:** `69,349` مبنى
- **المباني المدمرة كلياً:** `16,199` مبنى (34.7%)
- **المباني ذات الدمار الشديد:** `5,990` مبنى (12.8%)
- **المباني ذات الدمار المتوسط:** `16,798` مبنى (36.0%)
- **المباني السليمة أو طفيفة الضرر:** `22,688` مبنى (32.7%)
- **نسبة التضرر الإجمالية بالمدينة:** `56.22%`
- **حجم الأنقاض والركام المقدر (UNEP):** `39.99` مليون طن متري (Mt)

### أكثر الأحياء تضرراً في مدينة غزة (Top Damaged Neighborhoods)
| الحي السكني | Neighborhood | عدد المباني المتضررة | النسبة من إجمالي أضرار المدينة |
|---|---|:---:|:---:|
| **حي الزيتون** | Az Zaitoun | 8,285 | 17.75% |
| **حي التركمان والجديدة** | At Turukman - Ijdeedeh | 4,974 | 10.65% |
| **الشجاعية الجديدة** | Ash Shuja'iyeh - Ijdeedeh | 4,154 | 8.90% |
| **حي الرمال (الشمالي والجنوبي)** | Northern & Southern Remal | 4,100 | 8.78% |
| **مخيم الشاطئ للاجئين** | Ash Shati' Camp | 3,167 | 6.78% |
| **حي النصر** | An Naser | 2,503 | 5.36% |
| **حي الدرج** | Ad Darraj | 2,297 | 4.92% |
| **حي التفاح** | At Tuffah | 2,212 | 4.74% |
| **تل الهوا والصبرة** | Tal El Hawa & As Sabra | 2,059 | 4.41% |
| **الشيخ رضوان** | Ash Sheikh Radwan | 1,583 | 3.39% |

---

## 📁 هيكلية مجلدات المشروع (Repository Structure)

```text
├── ArcGIS_Pro_Project/
│   ├── Gaza_Damage_Assessment.aprx    # ملف مشروع ArcGIS Pro المعتمد
│   ├── Gaza_GIS_Master.gdb/           # قاعدة البيانات الجغرافية الرئيسية
│   └── Rasters_UTM36N/                # مجلد مخرجات الراستر المصححة
├── 01_Raw_Data/
│   └── OCHA_Admin_Boundaries/         # حدود البلديات والمحافظات (OCHA)
├── 02_Geodatabase/                    # طبقات المتجهات المعايرة
├── 03_Tabulated_Metrics/              # جداول الإحصائيات (CSV & JSON)
│   ├── Gaza_Governorate_Final_Stats.csv
│   └── Gaza_Neighborhood_Final_Stats.csv
├── 04_Cartographic_Exports/           # مخرجات الخرائط الهندسية عالية الدقة
│   ├── خريطة_تحليل_تدمير_مدينة_غزة_A3_بيضاء.png  # لوحة A3 بدقة 300 DPI
│   └── خريطة_تحليل_تدمير_مدينة_غزة_A3_بيضاء.pdf  # ملف الطباعة الهندسي
├── 05_Academic_Report/                # التقرير الأكاديمي التفصيلي
├── 06_Minimalist_Web_and_Deck/        # تطبيق الويب والعرض التقديمي
│   ├── index.html                     # تطبيق العرض التفاعلي الشامل
│   ├── Presentation_Deck.pptx         # عرض PowerPoint لمناقشة الماجستير
│   └── assets/                        # المرئيات واللوحات التفاعلية
└── scripts/                           # سكربتات البايثون المؤتمتة
    ├── generate_pristine_map_panels.py # توليد المرئيات الصافية والحدود
    ├── build_flawless_a3_plate.py      # إخراج لوحة A3 عبر Google Chrome
    ├── build_ultimate_unified_system.py# بناء المنظومة التفاعلية والعرض
    └── build_clean_white_deck.py       # إنشاء شرائح الباوربوينت
```

---

## 🚀 طريقة الاستخدام وإعادة التشغيل (How to Run)

### 1. فتح المشروع في ArcGIS Pro:
- افتح الملف: `ArcGIS_Pro_Project/Gaza_Damage_Assessment.aprx`
- ستفتح الخريطة تلقائياً مع كافة الطبقات المصنفة برمزية الألوان المعتمدة ومسقط UTM Zone 36N.

### 2. إعادة تشغيل خط أنابيب المعالجة (Python Automation):
يتطلب المشروع تثبيت بيئة بايثون مع مكتبات `geopandas`, `rasterio`, `pyogrio`, `pillow`:
```bash
# توليد المرئيات وتصنيف الدمار
uv run --with geopandas --with rasterio --with pyogrio --with pillow python scripts/generate_pristine_map_panels.py

# توليد لوحة الطباعة A3 بدقة 300 DPI عبر Google Chrome Headless
uv run python scripts/build_flawless_a3_plate.py
```

### 3. استعراض العرض التفاعلي:
افتح الملف `06_Minimalist_Web_and_Deck/index.html` في أي متصفح ويب لاستعراض المقارنة الزمنية المزدوجة بين المرئيات والأحياء.

---

## 📜 الترخيص وحقوق الملكية (License & Attribution)
- **المرئيات الفضائية:** مرخصة ومقدمة مجاناً عبر برنامج **Copernicus** التابع لوكالة الفضاء الأوروبية (ESA).
- **بيانات الدمار:** مقدمة عبر **UNOSAT / UNITAR**.
- **الحدود الإدارية:** مكتب الأمم المتحدة لتنسيق الشؤون الإنسانية (**UN OCHA**).
- **كود المشروع والتحليل الجيومكاني:** متاح للأغراض الأكاديمية والبحثية الإنسانية.
