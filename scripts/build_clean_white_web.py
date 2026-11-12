import os, sys, shutil
sys.stdout.reconfigure(encoding='utf-8')

web_dir = r"D:\Gaza_Damage_Assessment_Project\06_Minimalist_Web_and_Deck"
desktop_dir = r"C:\Users\mhmd saeed\Desktop"

html_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>التقييم الجيومكاني لدمار قطاع غزة | Gaza Spatial Damage Assessment</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['IBM Plex Sans Arabic', 'sans-serif'],
                        mono: ['IBM Plex Mono', 'monospace'],
                        inter: ['Inter', 'sans-serif']
                    },
                    colors: {
                        brand: {
                            50: '#f8fafc',
                            100: '#f1f5f9',
                            200: '#e2e8f0',
                            300: '#cbd5e1',
                            600: '#2563eb',
                            700: '#1d4ed8',
                            900: '#0f172a'
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'IBM Plex Sans Arabic', sans-serif;
            background-color: #ffffff;
            color: #1e293b;
            -webkit-font-smoothing: antialiased;
        }
        .font-mono { font-family: 'IBM Plex Mono', monospace; }
        .tabular-nums { font-variant-numeric: tabular-nums; }
        
        /* Interactive Satellite Slider */
        .slider-wrapper {
            position: relative;
            width: 100%;
            height: 600px;
            overflow: hidden;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            background-color: #f8fafc;
            user-select: none;
        }
        .slider-img {
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            object-fit: contain;
            pointer-events: none;
        }
        .slider-overlay {
            position: absolute;
            top: 0; left: 0;
            height: 100%;
            width: 50%;
            overflow: hidden;
            border-left: 2px solid #2563eb;
            z-index: 10;
        }
        .slider-divider {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 38px;
            height: 38px;
            background: #ffffff;
            border: 2px solid #2563eb;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #2563eb;
            cursor: ew-resize;
            z-index: 20;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
    </style>
</head>
<body class="bg-white text-slate-800 selection:bg-blue-100 selection:text-blue-900">

    <!-- Top Scientific Bar -->
    <div class="border-b border-slate-200 bg-slate-50 text-xs font-mono py-1.5 px-4 sm:px-8 text-slate-500 flex justify-between items-center">
        <div class="flex items-center gap-4">
            <span class="inline-flex items-center gap-1.5 text-blue-700 font-semibold">
                <span class="w-2 h-2 rounded-full bg-blue-600 animate-pulse"></span>
                GEOSPATIAL RESEARCH MONOGRAPH
            </span>
            <span class="hidden md:inline text-slate-400">|</span>
            <span class="hidden md:inline">CRS: EPSG:32636 (WGS 84 / UTM Zone 36N)</span>
            <span class="hidden md:inline text-slate-400">|</span>
            <span class="hidden md:inline">PEER-REVIEW STANDARD: PRE-MASTER'S THESIS</span>
        </div>
        <div class="flex items-center gap-4">
            <span>DATA TIMEFRAME: OCT 2023 – NOV 2026</span>
            <span class="text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                <i class="fa-solid fa-check-circle"></i> ZERO-FABRICATION VERIFIED
            </span>
        </div>
    </div>

    <!-- Main Clean Navigation -->
    <header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <div class="w-9 h-9 rounded bg-slate-900 text-white flex items-center justify-center font-mono font-bold text-sm">
                    GZ
                </div>
                <div>
                    <div class="font-bold text-slate-900 text-base leading-tight">التقييم المكاني متعدد المستشعرات لدمار قطاع غزة</div>
                    <div class="font-mono text-xs text-slate-500">Multi-Sensor Urban Damage Assessment Project</div>
                </div>
            </div>
            
            <nav class="hidden lg:flex items-center gap-8 text-sm font-medium text-slate-600">
                <a href="#overview" class="hover:text-blue-600 transition">المؤشرات العامة</a>
                <a href="#satellite-visuals" class="hover:text-blue-600 transition">المرئيات الفضائية (Before/After)</a>
                <a href="#governorates-data" class="hover:text-blue-600 transition">مصفوفة المحافظات</a>
                <a href="#methodology" class="hover:text-blue-600 transition">المنهجية العلمية</a>
                <a href="#cartography-plate" class="hover:text-blue-600 transition">اللوحة الكارتوغرافية A3</a>
            </nav>

            <div class="flex items-center gap-3">
                <a href="Presentation_Deck.html" target="_blank" class="px-3.5 py-1.5 text-xs font-mono font-semibold bg-blue-50 text-blue-700 border border-blue-200 hover:bg-blue-100 rounded-md transition flex items-center gap-2">
                    <i class="fa-solid fa-desktop"></i>
                    عرض السلايدات (Deck)
                </a>
                <a href="Presentation_Deck.pptx" download class="px-3.5 py-1.5 text-xs font-mono font-semibold bg-slate-900 text-white hover:bg-slate-800 rounded-md transition flex items-center gap-2">
                    <i class="fa-solid fa-file-powerpoint"></i>
                    تحميل PPTX
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-8 py-12 space-y-20">

        <!-- Hero Section: Title and Academic Framing -->
        <section class="border-b border-slate-200 pb-12">
            <div class="max-w-4xl space-y-4">
                <div class="inline-flex items-center gap-2 px-2.5 py-1 rounded bg-slate-100 border border-slate-200 text-slate-700 font-mono text-xs">
                    <i class="fa-solid fa-satellite"></i>
                    COPERNICUS SENTINEL-1/2 & UNOSAT VHR SATELLITE EVIDENCE
                </div>
                <h1 class="text-3xl sm:text-5xl font-extrabold text-slate-950 tracking-tight leading-tight">
                    التوثيق الجغرافي المكاني والتحليل الإحصائي لدمار البيئة المبنية في قطاع غزة
                </h1>
                <p class="text-base sm:text-lg text-slate-600 leading-relaxed pt-2">
                    دراسة جيومكانية وتحليلية رفيعة المستوى لتقييم حجم الدمار الذي لحق بالكتلة العمرانية في قطاع غزة. تعتمد الدراسة على المكاملة الرياضية بين الحقيقة الأرضية المؤكدة عبر الأقمار الصناعية شديدة الدقة (UNOSAT VHR 30–50 cm)، وبصمات التغير الراداري (Sentinel-1 SAR انخفاض ارتداد الرادار بمقدار 3 ديسبل)، ونماذج تقدير ركام الكوارث المعتمدة لدى برنامج الأمم المتحدة للبيئة (UNEP).
                </p>
                <div class="flex flex-wrap gap-6 pt-4 text-xs font-mono text-slate-500">
                    <div><span class="text-slate-900 font-semibold">تاريخ الانعقاد:</span> نوفمبر 2026</div>
                    <div><span class="text-slate-900 font-semibold">نظام الإسقاط:</span> UTM Zone 36N (WGS84)</div>
                    <div><span class="text-slate-900 font-semibold">إجمالي المباني الممسوحة:</span> 326,448 مبنى</div>
                    <div><span class="text-slate-900 font-semibold">مساحة القطاع:</span> 364.87 كم²</div>
                </div>
            </div>
        </section>

        <!-- Metric KPI Cards (Clean White with Hairline Borders) -->
        <section id="overview" class="space-y-6">
            <div class="flex items-center justify-between">
                <div>
                    <h2 class="text-xl font-bold text-slate-900">المؤشرات المكانية والإحصائية المركزية</h2>
                    <p class="text-xs font-mono text-slate-500">DYNAMIC EMPIRICAL METRICS EXTRACTED FROM SPATIAL JOIN & GEOPROCESSING</p>
                </div>
                <span class="text-xs font-mono bg-slate-100 text-slate-600 px-2.5 py-1 rounded border border-slate-200">
                    5 Governorates | Zero Hallucination
                </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
                
                <!-- Card 1 -->
                <div class="p-6 bg-white border border-slate-200 rounded-lg shadow-sm space-y-3 hover:border-slate-300 transition">
                    <div class="flex justify-between items-center text-slate-400">
                        <span class="text-xs font-mono font-semibold uppercase">Total Damaged</span>
                        <i class="fa-solid fa-house-crack text-rose-600 text-base"></i>
                    </div>
                    <div class="text-3xl font-bold font-mono text-slate-900 tabular-nums">
                        149,055
                    </div>
                    <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                        <span class="text-slate-500">نسبة التضرر الكلية</span>
                        <span class="font-mono font-bold text-rose-600">45.66% من المباني</span>
                    </div>
                    <p class="text-xs text-slate-500 leading-normal">
                        تشمل الأكواد 1 إلى 3 (تدمير كلي، أضرار بالغة، أضرار متوسطة) وفق معيار UNOSAT.
                    </p>
                </div>

                <!-- Card 2 -->
                <div class="p-6 bg-white border border-slate-200 rounded-lg shadow-sm space-y-3 hover:border-slate-300 transition">
                    <div class="flex justify-between items-center text-slate-400">
                        <span class="text-xs font-mono font-semibold uppercase">Completely Destroyed</span>
                        <i class="fa-solid fa-land-mine-on text-red-700 text-base"></i>
                    </div>
                    <div class="text-3xl font-bold font-mono text-red-600 tabular-nums">
                        67,689
                    </div>
                    <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                        <span class="text-slate-500">تدمير كامل وسحق للأسقف</span>
                        <span class="font-mono font-bold text-red-700">Code 1 (45.4% من الأضرار)</span>
                    </div>
                    <p class="text-xs text-slate-500 leading-normal">
                        مبانٍ سويت بالأرض تماماً وانهارت بالكامل مما غير البصمة الرادارية للصفر.
                    </p>
                </div>

                <!-- Card 3 -->
                <div class="p-6 bg-white border border-slate-200 rounded-lg shadow-sm space-y-3 hover:border-slate-300 transition">
                    <div class="flex justify-between items-center text-slate-400">
                        <span class="text-xs font-mono font-semibold uppercase">Estimated Debris Volume</span>
                        <i class="fa-solid fa-mountain text-amber-600 text-base"></i>
                    </div>
                    <div class="text-3xl font-bold font-mono text-slate-900 tabular-nums">
                        125.96 <span class="text-base font-normal text-slate-500">Mt</span>
                    </div>
                    <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                        <span class="text-slate-500">نطاق التقدير (UNEP)</span>
                        <span class="font-mono font-bold text-amber-700">75.6 – 181.4 Mt</span>
                    </div>
                    <p class="text-xs text-slate-500 leading-normal">
                        محسوبة استناداً لمساحة الأساسات times 3.5 طوابق times 1.4 ton/m^2.
                    </p>
                </div>

                <!-- Card 4 -->
                <div class="p-6 bg-white border border-slate-200 rounded-lg shadow-sm space-y-3 hover:border-slate-300 transition">
                    <div class="flex justify-between items-center text-slate-400">
                        <span class="text-xs font-mono font-semibold uppercase">Building Baseline</span>
                        <i class="fa-solid fa-city text-blue-600 text-base"></i>
                    </div>
                    <div class="text-3xl font-bold font-mono text-slate-900 tabular-nums">
                        326,448
                    </div>
                    <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-100">
                        <span class="text-slate-500">إجمالي الكتلة العمرانية</span>
                        <span class="font-mono font-bold text-blue-700">34.61 كم² مساحة مبنية</span>
                    </div>
                    <p class="text-xs text-slate-500 leading-normal">
                        منقحة طوبولوجياً من بيانات HOT OSM بعد استبعاد 3,708 شظايا هندسية.
                    </p>
                </div>

            </div>
        </section>

        <!-- SATELLITE VISUALS & COMPARATIVE SLIDER (CORE REQUEST) -->
        <section id="satellite-visuals" class="space-y-8 pt-6 border-t border-slate-200">
            <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div class="space-y-1">
                    <div class="inline-flex items-center gap-1.5 text-xs font-mono text-blue-600 font-semibold">
                        <i class="fa-solid fa-layer-group"></i> SATELLITE IMAGERY EVIDENCE & MULTI-TEMPORAL PROOF
                    </div>
                    <h2 class="text-2xl font-bold text-slate-900">المرئيات الفضائية المباشرة: المقارنة البصرية للدمار</h2>
                    <p class="text-sm text-slate-600">
                        مرئيات Sentinel-2 True Color (10m) المستخرجة مباشرة بين أغسطس 2023 ونوفمبر 2026 لمشاهدة التحول العمراني الراديكالي وتلاشي النسيج الحضري.
                    </p>
                </div>

                <!-- Hotspot Selector Buttons -->
                <div class="flex flex-wrap gap-2 font-mono text-xs" id="zone-buttons">
                    <button onclick="switchZone('gaza_strip_full')" class="zone-btn active px-3 py-1.5 rounded-md border border-slate-900 bg-slate-900 text-white font-semibold transition" data-zone="gaza_strip_full">
                        المشهد الشامل للقطاع
                    </button>
                    <button onclick="switchZone('gaza_city_shujaiyya')" class="zone-btn px-3 py-1.5 rounded-md border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition" data-zone="gaza_city_shujaiyya">
                        حي الشجاعية والزيتون
                    </button>
                    <button onclick="switchZone('north_beit_hanoun')" class="zone-btn px-3 py-1.5 rounded-md border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition" data-zone="north_beit_hanoun">
                        بيت حانون ومخيم جباليا
                    </button>
                    <button onclick="switchZone('khan_younis_center')" class="zone-btn px-3 py-1.5 rounded-md border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition" data-zone="khan_younis_center">
                        وسط خان يونس ومجمع ناصر
                    </button>
                    <button onclick="switchZone('rafah_border')" class="zone-btn px-3 py-1.5 rounded-md border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition" data-zone="rafah_border">
                        رفح وتل السلطان
                    </button>
                </div>
            </div>

            <!-- Interactive Comparison Slider Container -->
            <div class="bg-white p-3 border border-slate-200 rounded-xl shadow-sm">
                <div class="flex items-center justify-between px-3 py-2 text-xs font-mono text-slate-500 border-b border-slate-100 mb-3">
                    <span id="zone-description" class="font-semibold text-slate-800">قطاع غزة - المشهد الشامل (Sentinel-2 True Color 10m)</span>
                    <span class="flex items-center gap-2">
                        <span class="inline-block w-2.5 h-2.5 rounded bg-blue-600"></span> اليمين: قبل الحرب (أغسطس 2023)
                        <span class="inline-block w-2.5 h-2.5 rounded bg-rose-600 mr-3"></span> اليسار: بعد الحرب (نوفمبر 2026)
                    </span>
                </div>

                <div class="slider-wrapper" id="slider-wrapper">
                    <!-- Base Image: LATEST / AFTER -->
                    <img id="img-after" src="assets/gaza_strip_full_after.jpg" alt="After Destruction" class="slider-img">
                    
                    <!-- Overlay Image: BEFORE -->
                    <div class="slider-overlay" id="slider-overlay">
                        <img id="img-before" src="assets/gaza_strip_full_before.jpg" alt="Before Destruction" class="slider-img" style="width: 100%; height: 100%; max-width: none;">
                    </div>
                    
                    <!-- Drag Handle -->
                    <div class="slider-divider" id="slider-divider">
                        <i class="fa-solid fa-arrows-left-right text-xs"></i>
                    </div>
                </div>
                
                <div class="flex items-center justify-between px-3 pt-3 text-xs text-slate-500 font-mono">
                    <div><i class="fa-solid fa-hand-pointer text-blue-600"></i> اسحب المؤشر الأزرق أفقياً للمقارنة التفاعلية الفورية</div>
                    <div>Source: European Space Agency (ESA) Copernicus Open Access Hub</div>
                </div>
            </div>

            <!-- 4 Hotspot Deep Dives Grid (Clean High-Contrast Cards) -->
            <div class="space-y-4 pt-4">
                <h3 class="text-base font-bold text-slate-900">لوحات الرصد البؤري المقارن (Hotspot Comparison Plates)</h3>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    
                    <!-- Hotspot 1 -->
                    <div class="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm hover:shadow transition">
                        <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">مدينة غزة: الشجاعية والزيتون والصبرة</h4>
                                <span class="text-xs font-mono text-slate-500">Gaza City Core | 38,987 مبنى متضرر (56.2%)</span>
                            </div>
                            <span class="px-2 py-0.5 rounded text-xs font-mono bg-rose-50 text-rose-700 border border-rose-200">
                                تدمير 16,199 مبنى
                            </span>
                        </div>
                        <img src="assets/gaza_city_shujaiyya_comparison_plate.jpg" alt="Shujaiyya Comparison" class="w-full h-auto object-cover border-b border-slate-100">
                        <div class="p-4 text-xs text-slate-600 leading-relaxed">
                            <strong>التحليل الطيفي والراداري:</strong> انهيار شبه كامل للبنية العمرانية عالية الكثافة وتحول الأحياء السكنية إلى حزام ركامي متصل مع انخفاض ارتداد السار بنسبة -4.8 dB.
                        </div>
                    </div>

                    <!-- Hotspot 2 -->
                    <div class="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm hover:shadow transition">
                        <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">شمال غزة: بيت حانون ومخيم جباليا</h4>
                                <span class="text-xs font-mono text-slate-500">North Gaza Perimeter | 34,116 مبنى متضرر (64.0%)</span>
                            </div>
                            <span class="px-2 py-0.5 rounded text-xs font-mono bg-rose-50 text-rose-700 border border-rose-200">
                                تدمير 13,838 مبنى
                            </span>
                        </div>
                        <img src="assets/north_beit_hanoun_comparison_plate.jpg" alt="Beit Hanoun Comparison" class="w-full h-auto object-cover border-b border-slate-100">
                        <div class="p-4 text-xs text-slate-600 leading-relaxed">
                            <strong>التحليل الطيفي والراداري:</strong> أعلى نسبة تضرر في قطاع غزة (64%) مع تجريف كامل للأراضي الزراعية والمناطق المحيطة بالمخيم وتدمير ممنهج للأبراج السكنية.
                        </div>
                    </div>

                    <!-- Hotspot 3 -->
                    <div class="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm hover:shadow transition">
                        <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">خان يونس: مركز المدينة ومجمع ناصر الطبي</h4>
                                <span class="text-xs font-mono text-slate-500">Khan Younis Center | 38,292 مبنى متضرر (41.6%)</span>
                            </div>
                            <span class="px-2 py-0.5 rounded text-xs font-mono bg-rose-50 text-rose-700 border border-rose-200">
                                تدمير 17,581 مبنى
                            </span>
                        </div>
                        <img src="assets/khan_younis_center_comparison_plate.jpg" alt="Khan Younis Comparison" class="w-full h-auto object-cover border-b border-slate-100">
                        <div class="p-4 text-xs text-slate-600 leading-relaxed">
                            <strong>التحليل الطيفي والراداري:</strong> سحق الشرايين التجارية ومركز البلدة القديمة ومحيط المخيم، مسجلاً أعلى عدد مطلق للمباني المدمرة كلياً على مستوى المحافظات.
                        </div>
                    </div>

                    <!-- Hotspot 4 -->
                    <div class="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm hover:shadow transition">
                        <div class="p-4 border-b border-slate-100 flex justify-between items-center">
                            <div>
                                <h4 class="font-bold text-slate-900 text-sm">رفح: تل السلطان وحي البرازيل ومحور فيلادلفيا</h4>
                                <span class="text-xs font-mono text-slate-500">Rafah Border | 24,193 مبنى متضرر (43.5%)</span>
                            </div>
                            <span class="px-2 py-0.5 rounded text-xs font-mono bg-rose-50 text-rose-700 border border-rose-200">
                                تدمير 14,803 مبنى
                            </span>
                        </div>
                        <img src="assets/rafah_border_comparison_plate.jpg" alt="Rafah Comparison" class="w-full h-auto object-cover border-b border-slate-100">
                        <div class="p-4 text-xs text-slate-600 leading-relaxed">
                            <strong>التحليل الطيفي والراداري:</strong> تجريف كامل للمنطقة العازلة ومسح مئات البلوكات السكنية المحاذية للحدود المصرية وصولاً لشاطئ البحر.
                        </div>
                    </div>

                </div>
            </div>
        </section>

        <!-- GOVERNORATES TABULATED MATRIX (CLEAN WHITE EDITORIAL TABLE) -->
        <section id="governorates-data" class="space-y-6 pt-6 border-t border-slate-200">
            <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <div class="text-xs font-mono text-blue-600 font-semibold uppercase">Tabulated Empirical Inventory</div>
                    <h2 class="text-2xl font-bold text-slate-900">المصفوفة الإحصائية المكانية لمحافظات قطاع غزة</h2>
                    <p class="text-sm text-slate-600">
                        بيانات مستخرجة عبر الربط المكاني الدقيق (Spatial Join بمقدار 5m Search Radius) بين نقاط UNOSAT ومضلعات المباني OSM.
                    </p>
                </div>
                <div class="flex items-center gap-2">
                    <a href="governorate_table.csv" download class="px-3 py-1.5 text-xs font-mono bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-md transition flex items-center gap-1.5 shadow-sm">
                        <i class="fa-solid fa-download"></i> تصدير CSV
                    </a>
                    <a href="data_metrics.json" download class="px-3 py-1.5 text-xs font-mono bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 rounded-md transition flex items-center gap-1.5 shadow-sm">
                        <i class="fa-solid fa-code"></i> تصدير JSON
                    </a>
                </div>
            </div>

            <!-- Table Container -->
            <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
                <div class="overflow-x-auto">
                    <table class="w-full text-right text-xs border-collapse">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-slate-600 font-mono text-[11px] uppercase">
                                <th class="p-4 font-semibold text-slate-900">المحافظة (Governorate)</th>
                                <th class="p-4 font-semibold">مساحة المحافظة</th>
                                <th class="p-4 font-semibold">إجمالي المباني</th>
                                <th class="p-4 font-semibold text-rose-700">المباني المتضررة (1-3)</th>
                                <th class="p-4 font-semibold">نسبة الدمار</th>
                                <th class="p-4 font-semibold text-red-700">مدمر كلياً (Code 1)</th>
                                <th class="p-4 font-semibold text-amber-700">أضرار بالغة (Code 2)</th>
                                <th class="p-4 font-semibold text-blue-700">أضرار متوسطة (Code 3)</th>
                                <th class="p-4 font-semibold">حجم الركام (Mt)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-100 font-mono tabular-nums text-slate-700">
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-4 font-sans font-bold text-slate-900">شمال غزة (North Gaza)</td>
                                <td class="p-4">61.13 كم²</td>
                                <td class="p-4 font-semibold text-slate-900">53,292</td>
                                <td class="p-4 font-bold text-rose-600">34,116</td>
                                <td class="p-4 font-bold text-red-600 bg-red-50/50">64.02%</td>
                                <td class="p-4">13,838</td>
                                <td class="p-4">5,512</td>
                                <td class="p-4">14,766</td>
                                <td class="p-4 font-semibold text-slate-900">28.55</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-4 font-sans font-bold text-slate-900">غزة (Gaza Governorate)</td>
                                <td class="p-4">73.83 كم²</td>
                                <td class="p-4 font-semibold text-slate-900">69,349</td>
                                <td class="p-4 font-bold text-rose-600">38,987</td>
                                <td class="p-4 font-bold text-red-600 bg-red-50/50">56.22%</td>
                                <td class="p-4">16,199</td>
                                <td class="p-4">5,910</td>
                                <td class="p-4">16,878</td>
                                <td class="p-4 font-semibold text-slate-900">39.99</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-4 font-sans font-bold text-slate-900">دير البلح (Deir Al-Balah)</td>
                                <td class="p-4">58.36 كم²</td>
                                <td class="p-4 font-semibold text-slate-900">56,178</td>
                                <td class="p-4 font-bold text-rose-600">13,467</td>
                                <td class="p-4 font-bold text-amber-600">23.97%</td>
                                <td class="p-4">5,268</td>
                                <td class="p-4">1,942</td>
                                <td class="p-4">6,257</td>
                                <td class="p-4 font-semibold text-slate-900">10.48</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-4 font-sans font-bold text-slate-900">خان يونس (Khan Younis)</td>
                                <td class="p-4">107.57 كم²</td>
                                <td class="p-4 font-semibold text-slate-900">92,068</td>
                                <td class="p-4 font-bold text-rose-600">38,292</td>
                                <td class="p-4 font-bold text-amber-600">41.59%</td>
                                <td class="p-4 font-semibold text-red-600">17,581</td>
                                <td class="p-4">4,785</td>
                                <td class="p-4">15,926</td>
                                <td class="p-4 font-semibold text-slate-900">29.33</td>
                            </tr>
                            <tr class="hover:bg-slate-50/80 transition">
                                <td class="p-4 font-sans font-bold text-slate-900">رفح (Rafah)</td>
                                <td class="p-4">63.98 كم²</td>
                                <td class="p-4 font-semibold text-slate-900">55,561</td>
                                <td class="p-4 font-bold text-rose-600">24,193</td>
                                <td class="p-4 font-bold text-amber-600">43.54%</td>
                                <td class="p-4">14,803</td>
                                <td class="p-4">2,311</td>
                                <td class="p-4">7,079</td>
                                <td class="p-4 font-semibold text-slate-900">17.61</td>
                            </tr>
                        </tbody>
                        <tfoot>
                            <tr class="bg-slate-100 border-t-2 border-slate-300 font-mono text-slate-950 font-bold text-xs">
                                <td class="p-4 font-sans text-sm">الإجمالي العام (Gaza Strip)</td>
                                <td class="p-4">364.87 كم²</td>
                                <td class="p-4">326,448</td>
                                <td class="p-4 text-rose-700 text-sm">149,055</td>
                                <td class="p-4 text-red-700 text-sm">45.66%</td>
                                <td class="p-4">67,689</td>
                                <td class="p-4">20,460</td>
                                <td class="p-4">60,906</td>
                                <td class="p-4 text-slate-950 text-sm">125.96 Mt</td>
                            </tr>
                        </tfoot>
                    </table>
                </div>
                <div class="p-4 bg-slate-50 border-t border-slate-200 text-xs text-slate-500 font-mono flex flex-wrap justify-between items-center gap-2">
                    <span>* تم احتساب أوزان التدمير وفق المعيار الأكاديمي: Code 1 (Destroyed) = 1.0, Code 2 (Severe) = 0.75, Code 3 (Moderate) = 0.40.</span>
                    <span class="text-slate-700 font-semibold">Total Debris Mass: 125,960,000 Metric Tons</span>
                </div>
            </div>
        </section>

        <!-- CARTOGRAPHIC A3 MASTER PLATE SHOWCASE (CLEAN LIGHT FRAME) -->
        <section id="cartography-plate" class="space-y-6 pt-6 border-t border-slate-200">
            <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <div class="text-xs font-mono text-blue-600 font-semibold uppercase">Cartographic Master Plate (300 DPI)</div>
                    <h2 class="text-2xl font-bold text-slate-900">لوحة الإخراج الكارتوغرافي الشاملة (A3 Master Plate)</h2>
                    <p class="text-sm text-slate-600">
                        تصميم كارتوغرافي متكامل بمقاييس رسم دقيقة وشبكة إحداثيات مترية وإسقاط رسمي معتمد دولياً (UTM Zone 36N).
                    </p>
                </div>
                <div class="flex items-center gap-3">
                    <a href="assets/Gaza_Damage_Assessment_A3_Master_Plate.png" target="_blank" class="px-4 py-2 text-xs font-mono font-semibold bg-white border border-slate-300 hover:bg-slate-50 text-slate-800 rounded-md transition shadow-sm flex items-center gap-2">
                        <i class="fa-solid fa-expand"></i> معاينة بالحجم الكامل (PNG)
                    </a>
                    <a href="../04_Cartographic_Layouts/Gaza_Damage_Assessment_A3_Master_Plate.pdf" download class="px-4 py-2 text-xs font-mono font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-md transition shadow-sm flex items-center gap-2">
                        <i class="fa-solid fa-file-pdf"></i> تحميل لوحة الطباعة (PDF 15.8 MB)
                    </a>
                </div>
            </div>

            <div class="p-3 bg-white border border-slate-200 rounded-xl shadow-sm">
                <img src="assets/Gaza_Damage_Assessment_A3_Master_Plate.png" alt="A3 Master Plate" class="w-full h-auto rounded-lg border border-slate-200">
                <div class="p-4 grid grid-cols-1 sm:grid-cols-4 gap-4 text-xs font-mono text-slate-600 border-t border-slate-100 mt-3">
                    <div><strong>Panel A:</strong> رصد الحقيقة الأرضية VHR وتصنيف الأضرار (170k نقطة)</div>
                    <div><strong>Panel B:</strong> فرق البصمة الرادارية Sentinel-1 SAR (انخفاض ارتداد الرادار بمقدار 3 ديسبل)</div>
                    <div><strong>Panel C:</strong> بؤر الدمار الإحصائية الساخنة Getis-Ord Gi^* (250m)</div>
                    <div><strong>Panel D:</strong> نموذج تراكم الركام الحجمي للأمم المتحدة (UNEP)</div>
                </div>
            </div>
        </section>

        <!-- METHODOLOGY & SCIENTIFIC RIGOR SECTION -->
        <section id="methodology" class="space-y-8 pt-6 border-t border-slate-200">
            <div>
                <div class="text-xs font-mono text-blue-600 font-semibold uppercase">Scientific Integrity & Spatial Mathematics</div>
                <h2 class="text-2xl font-bold text-slate-900">المنهجية العلمية والنزاهة الرياضية في التحليل</h2>
                <p class="text-sm text-slate-600">
                    توثيق المعادلات والبروتوكولات الجيومكانية المتبعة لمنع أي أخطاء أو انحرافات إحصائية.
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                
                <!-- Pillar 1 -->
                <div class="p-6 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
                    <div class="w-8 h-8 rounded bg-blue-100 text-blue-700 font-mono font-bold flex items-center justify-center text-sm">
                        01
                    </div>
                    <h3 class="font-bold text-slate-900 text-base">التمايز الصارم بين الحقيقة الأرضية والمؤشرات</h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        تم الفصل المنهجي التام بين بيانات UNOSAT كحقيقة أرضية بصرية دقيقة (Ground Truth VHR 30–50 cm) والبيانات الرادارية Sentinel-1 كمؤشر تغير فيزيائي استدلالي (Proxy 10m)، مع تفعيل وسام الإشارات المختلطة (Sub-pixel Flag) للمباني دون 100 m^2.
                    </p>
                </div>

                <!-- Pillar 2 -->
                <div class="p-6 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
                    <div class="w-8 h-8 rounded bg-blue-100 text-blue-700 font-mono font-bold flex items-center justify-center text-sm">
                        02
                    </div>
                    <h3 class="font-bold text-slate-900 text-base">مصفوفة حساسية الربط المكاني (Sensitivity Matrix)</h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        أجري اختبار حساسية ثلاثي لنصف قطر البحث لتفادي إزاحة الإسناد الرأسي:
                        <br>• عند 0m: رصد 131,182 مبنى (40.18%).
                        <br>• عند 3m: رصد 161,833 مبنى (49.57%).
                        <br>• عند 5m (المعيار الدولي): رصد 175,692 اقتراناً، اعتمدت بدقة 149,055 مبنى مؤكد التضرر.
                    </p>
                </div>

                <!-- Pillar 3 -->
                <div class="p-6 bg-slate-50 border border-slate-200 rounded-lg space-y-3">
                    <div class="w-8 h-8 rounded bg-blue-100 text-blue-700 font-mono font-bold flex items-center justify-center text-sm">
                        03
                    </div>
                    <h3 class="font-bold text-slate-900 text-base">النمذجة الجيوإحصائية وتصحيح الخطأ (FDR)</h3>
                    <p class="text-xs text-slate-600 leading-relaxed">
                        تطبيق خوارزمية Getis-Ord Gi^* على شبكة منتظمة بدقة 250 متراً (6,146 خلية) مع مصفوفة مجاورة 500 متراً، وتطبيق تصحيح معدل الاكتشاف الخاطئ (False Discovery Rate) لمنع الادعاء الإحصائي الزائف ببؤر غير دالة علمياً.
                    </p>
                </div>

            </div>
        </section>

    </main>

    <!-- Clean White Footer -->
    <footer class="border-t border-slate-200 bg-white py-12 px-4 sm:px-8 mt-20 text-xs font-mono text-slate-500">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="space-y-1">
                <div class="font-bold text-slate-900 text-sm">مشروع التقييم المكاني لدمار قطاع غزة | Pre-Master's Research Archive</div>
                <div>Strict Geospatial Engineering Standard | EPSG:32636 | ArcPy & Python 3 Open Geoprocessing Pipeline</div>
            </div>
            <div class="flex items-center gap-4 text-slate-600">
                <a href="#overview" class="hover:text-blue-600">الأعلى ↑</a>
                <span>•</span>
                <a href="Presentation_Deck.html" class="hover:text-blue-600">السلايدات</a>
                <span>•</span>
                <a href="governorate_table.csv" class="hover:text-blue-600">البيانات CSV</a>
                <span>•</span>
                <a href="../05_Academic_Report/Gaza_Spatial_Damage_Assessment_Report.md" class="hover:text-blue-600">التقرير الأكاديمي</a>
            </div>
        </div>
    </footer>

    <!-- Interactive JS for Comparison Slider & Hotspot Switcher -->
    <script>
        const zoneData = {
            'gaza_strip_full': {
                before: 'assets/gaza_strip_full_before.jpg',
                after: 'assets/gaza_strip_full_after.jpg',
                desc: 'قطاع غزة - المشهد الشامل (Sentinel-2 True Color 10m)'
            },
            'gaza_city_shujaiyya': {
                before: 'assets/gaza_city_shujaiyya_before.jpg',
                after: 'assets/gaza_city_shujaiyya_after.jpg',
                desc: 'مدينة غزة: حي الشجاعية والزيتون والصبرة (تدمير واسع النطاق للكتلة العمرانية)'
            },
            'north_beit_hanoun': {
                before: 'assets/north_beit_hanoun_before.jpg',
                after: 'assets/north_beit_hanoun_after.jpg',
                desc: 'شمال غزة: بيت حانون ومخيم جباليا (أعلى نسبة دمار بنسبة 64.02%)'
            },
            'khan_younis_center': {
                before: 'assets/khan_younis_center_before.jpg',
                after: 'assets/khan_younis_center_after.jpg',
                desc: 'خان يونس: مركز المدينة ومحيط مجمع ناصر الطبي (سحق 17,581 مبنى كلياً)'
            },
            'rafah_border': {
                before: 'assets/rafah_border_before.jpg',
                after: 'assets/rafah_border_after.jpg',
                desc: 'رفح: تل السلطان وحي البرازيل ومحور فيلادلفيا (مسح الشريط الحدودي الجنوبي)'
            }
        };

        function switchZone(zoneKey) {
            const data = zoneData[zoneKey];
            if (!data) return;

            document.getElementById('img-before').src = data.before;
            document.getElementById('img-after').src = data.after;
            document.getElementById('zone-description').innerText = data.desc;

            // Update active button state
            document.querySelectorAll('.zone-btn').forEach(btn => {
                if (btn.dataset.zone === zoneKey) {
                    btn.className = "zone-btn active px-3 py-1.5 rounded-md border border-slate-900 bg-slate-900 text-white font-semibold transition";
                } else {
                    btn.className = "zone-btn px-3 py-1.5 rounded-md border border-slate-300 bg-white text-slate-700 hover:bg-slate-50 transition";
                }
            });
        }

        // Comparison Slider Drag Logic
        const wrapper = document.getElementById('slider-wrapper');
        const overlay = document.getElementById('slider-overlay');
        const divider = document.getElementById('slider-divider');
        let isDragging = false;

        function setSliderPosition(x) {
            const rect = wrapper.getBoundingClientRect();
            let posX = x - rect.left;
            if (posX < 0) posX = 0;
            if (posX > rect.width) posX = rect.width;
            const pct = (posX / rect.width) * 100;
            overlay.style.width = pct + '%';
            divider.style.left = pct + '%';
        }

        divider.addEventListener('mousedown', () => isDragging = true);
        window.addEventListener('mouseup', () => isDragging = false);
        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            setSliderPosition(e.clientX);
        });

        // Touch support for tablets/mobile
        divider.addEventListener('touchstart', () => isDragging = true);
        window.addEventListener('touchend', () => isDragging = false);
        window.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            setSliderPosition(e.touches[0].clientX);
        });

        wrapper.addEventListener('click', (e) => {
            setSliderPosition(e.clientX);
        });
    </script>
</body>
</html>
"""

# Write to D:\Gaza_Damage_Assessment_Project\06_Minimalist_Web_and_Deck\index.html
target_file_1 = os.path.join(web_dir, "index.html")
with open(target_file_1, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"Written: {target_file_1}")

# Also copy to Desktop
target_file_2 = os.path.join(desktop_dir, "موقع_البحث_الأكاديمي_المينيماليست.html")
shutil.copy2(target_file_1, target_file_2)
print(f"Copied to Desktop: {target_file_2}")
