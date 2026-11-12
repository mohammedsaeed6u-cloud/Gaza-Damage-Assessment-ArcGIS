import os
import sys
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

assets_dir = r"D:\Gaza_Damage_Assessment_Project\06_Minimalist_Web_and_Deck\assets"
web_dir = r"D:\Gaza_Damage_Assessment_Project\06_Minimalist_Web_and_Deck"
desktop_dir = r"C:\Users\mhmd saeed\Desktop"

# -------------------------------------------------------------
# 1. BUILD PRESENTATION_DECK.HTML (Clean Light Theme)
# -------------------------------------------------------------
deck_html = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>عرض مناقشة البحث: التقييم المكاني لدمار قطاع غزة | Academic Defense Deck</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- KaTeX for exact math rendering -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.css">
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/katex.min.js"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.8/dist/contrib/auto-render.min.js" onload="renderMathInElement(document.body);"></script>
    <style>
        body {
            font-family: 'IBM Plex Sans Arabic', sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
            user-select: none;
            overflow: hidden;
        }
        .font-mono { font-family: 'IBM Plex Mono', monospace; }
        .slide-container {
            width: 100vw;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            box-sizing: border-box;
        }
        .slide {
            display: none;
            width: 100%;
            max-width: 1200px;
            height: 85vh;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
            padding: 3rem;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            animation: fadeIn 0.3s ease-in-out;
        }
        .slide.active {
            display: flex;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
</head>
<body>

    <!-- Slide Wrapper -->
    <div class="slide-container">

        <!-- SLIDE 1: COVER -->
        <section class="slide active" data-slide="1">
            <div class="flex justify-between items-center text-xs font-mono text-slate-400 border-b border-slate-100 pb-4">
                <span>PRE-MASTER'S RESEARCH MONOGRAPH | GIS & REMOTE SENSING</span>
                <span>CRS: EPSG:32636 (UTM ZONE 36N)</span>
            </div>
            
            <div class="my-auto space-y-6 max-w-4xl">
                <div class="inline-flex items-center gap-2 px-3 py-1 rounded bg-blue-50 border border-blue-200 text-blue-700 font-mono text-xs font-semibold">
                    <i class="fa-solid fa-satellite"></i> COPERNICUS SENTINEL-1/2 & UNOSAT GROUND TRUTH
                </div>
                <h1 class="text-4xl sm:text-5xl font-extrabold text-slate-900 leading-tight">
                    التحليل المكاني متكامل الحساسات لتقييم الدمار العمراني في قطاع غزة
                </h1>
                <p class="text-lg text-slate-600 leading-relaxed">
                    منهجية جيومكانية صفرية الأخطاء (Zero-Defect Pipeline) لمكاملة الحقيقة الأرضية فائقة الدقة مع قياسات التغير الراداري ونماذج ركام الكوارث الحجمية.
                </p>
                <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-4 border-t border-slate-100 font-mono text-xs text-slate-500">
                    <div><span class="text-slate-900 font-semibold block">إجمالي المباني:</span> 326,448 مبنى</div>
                    <div><span class="text-slate-900 font-semibold block">المباني المتضررة:</span> 149,055 (45.66%)</div>
                    <div><span class="text-slate-900 font-semibold block">الركام التقديري:</span> 125.96 مليون طن</div>
                    <div><span class="text-slate-900 font-semibold block">تاريخ الإنجاز:</span> نوفمبر 2026</div>
                </div>
            </div>

            <div class="flex justify-between items-center text-xs font-mono text-slate-400 pt-4 border-t border-slate-100">
                <span>Senior Geospatial Architecture & Remote Sensing</span>
                <span>شريحة 1 من 10</span>
            </div>
        </section>

        <!-- SLIDE 2: RESEARCH PROBLEM & SENSORS -->
        <section class="slide" data-slide="2">
            <div class="flex justify-between items-center text-xs font-mono text-slate-400 border-b border-slate-100 pb-3">
                <span class="text-blue-600 font-semibold">01. إشكالية البحث وتعدد الحساسات</span>
                <span>DATA INTEGRITY ARCHITECTURE</span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8 my-auto">
                <div class="space-y-4">
                    <h2 class="text-2xl font-bold text-slate-900 leading-snug">
                        التحدي الجيومكاني: مكاملة الحقيقة الأرضية مع المؤشرات الاستدلالية
                    </h2>
                    <p class="text-sm text-slate-600 leading-relaxed">
                        في بيئات النزاع الكثيفة، لا يمكن الاعتماد على مصدر وحيد للبيانات. تتطلب النزاهة العلمية التمييز الصارم بين:
                    </p>
                    <div class="space-y-3 text-xs leading-relaxed">
                        <div class="p-3 bg-blue-50/60 border border-blue-200 rounded-lg">
                            <strong class="text-blue-900 block font-mono">1. الحقيقة الأرضية البصرية (UNOSAT VHR 30–50 cm):</strong>
                            رصد بشري وخوارزمي مباشر على صور الأقمار الصناعية شديدة الدقة، مصنف إلى 4 أكواد معتمدة دولياً.
                        </div>
                        <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg">
                            <strong class="text-slate-900 block font-mono">2. بصمة التغير الراداري (Sentinel-1 SAR C-Band 10m):</strong>
                            مؤشر فيزيائي لقياس هبوط الارتداد الخلفي انخفاض ارتداد الرادار بمقدار 3 ديسبل الناتج عن انهيار الجدران الرأسية المزدوجة.
                        </div>
                    </div>
                </div>

                <div class="p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-4 font-mono text-xs text-slate-700">
                    <div class="font-bold text-slate-900 text-sm border-b border-slate-200 pb-2">
                        المعادلات الرياضية للتحسس النائي (Remote Sensing Formulas)
                    </div>
                    <div>
                        <span class="text-slate-500 block mb-1">تغير الارتداد الراداري (SAR Log-Ratio):</span>
                        <div class="bg-white p-2.5 rounded border border-slate-200 text-slate-900 font-semibold">
                            $انخفاض ارتداد الرادار بمقدار 3 ديسبلإجمالي العيناتإجمالي العيناتإجمالي العينات10\text{ m}^2 كشوائب ناتجة عن رقمنة OSM.
                        </li>
                        <li>
                            <strong>تحديد الأولوية التدميرية (Worst-Case Aggregation):</strong> في حال اقتران أكثر من نقطة تضرر بمبنى واحد، تم اعتماد الكود الأكثر شدة تلقائياً (\min(\text{Damage\_Code})).
                        </li>
                        <li>
                            <strong>وسم الإشارات المختلطة (Mixed-Pixel Flag):</strong> وسم كافة المباني دون 100\text{ m}^2إجمالي العيناتGi^* مع تطبيق تصحيح معدل الاكتشاف الخاطئ (FDR):
                    </p>
                    <div class="bg-white p-3 border border-slate-200 rounded-lg text-xs font-mono">
                        Gi^*(i) = fracsum_j=1^n w_ij x_j - barX sum_j=1^n w_ijS sqrtfracn sum_j=1^n w_ij^2 - (sum_j=1^n w_ij)^2n - 1
                    </div>
                    <p class="text-xs text-slate-500">
                        حيث w_{ij} تمثل مصفوفة المسافات المكانية بنطاق جوار ثابت 500 متراً، وx_j مجموع درجات الدمار الموزونة داخل كل خلية.
                    </p>
                </div>

                <div class="p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-3 font-mono text-xs">
                    <div class="font-bold text-slate-900 text-sm border-b border-slate-200 pb-2">
                        فئات الثقة الإحصائية بعد تصحيح FDR
                    </div>
                    <div class="p-2.5 bg-rose-50 border border-rose-200 rounded text-rose-800 flex justify-between">
                        <span>بؤر ساخنة عند ثقة 99% (Z > +2.58, p < 0.001):</span>
                        <span class="font-bold">83 خلية</span>
                    </div>
                    <div class="p-2.5 bg-amber-50 border border-amber-200 rounded text-amber-800 flex justify-between">
                        <span>بؤر ساخنة عند ثقة 95% (Z > +1.96, p < 0.05):</span>
                        <span class="font-bold">93 خلية</span>
                    </div>
                    <div class="p-2.5 bg-yellow-50 border border-yellow-200 rounded text-yellow-800 flex justify-between">
                        <span>بؤر ساخنة عند ثقة 90% (Z > +1.65, p < 0.10إجمالي العيناتV_debris = sum_k=1^3 left( A_k times H_floors times C_bulk times W_k right)
                    </div>
                    <div class="grid grid-cols-3 gap-2 text-center font-mono text-xs">
                        <div class="p-2 bg-slate-50 border border-slate-200 rounded">
                            <span class="text-slate-500 block text-[10px]">الحد الأدنى</span>
                            <strong class="text-slate-900">75.6 Mt</strong>
                        </div>
                        <div class="p-2 bg-blue-50 border border-blue-200 rounded">
                            <span class="text-blue-700 block text-[10px]">المتوسط المرجح</span>
                            <strong class="text-blue-900 font-bold">125.96 Mt</strong>
                        </div>
                        <div class="p-2 bg-slate-50 border border-slate-200 rounded">
                            <span class="text-slate-500 block text-[10px]">الحد الأعلى</span>
                            <strong class="text-slate-900">181.4 Mt</strong>
                        </div>
                    </div>
                </div>

                <div class="p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-3 font-mono text-xs">
                    <div class="font-bold text-slate-900 text-sm border-b border-slate-200 pb-2">
                        المعاملات الفيزيائية المعتمدة في المعادلة
                    </div>
                    <div class="space-y-2 text-slate-700">
                        <div><strong>• متوسط الطوابق (H_{\\text{floors}}):</strong> 3.5 طوابق (متوسط التكتل الحضري لقطاع غزة).</div>
                        <div><strong>• كثافة الركام الخرساني (C_{\\text{bulk}}):</strong> 1.4 طن / م² من المسطح الطابقي.</div>
                        <div><strong>• معامل تدمير كلي (W_1):</strong> 1.0 (انهيار إنشائي كامل).</div>
                        <div><strong>• معامل أضرار بالغة (W_2):</strong> 0.75 (انهيار جزئي وتهتك للجدران الحاملة).</div>
                        <div><strong>• معامل أضرار متوسطة (W_3انخفاض ارتداد الرادار بمقدار 3 ديسبل{n}"]`);
            if (target) {
                target.classList.add('active');
                document.getElementById('slide-indicator').innerText = `n / {totalSlides}`;
                currentSlide = n;
            }
        }

        function nextSlide() {
            if (currentSlide < totalSlides) {
                showSlide(currentSlide + 1);
            }
        }

        function prevSlide() {
            if (currentSlide > 1) {
                showSlide(currentSlide - 1);
            }
        }

        window.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft' || e.key === 'PageDown' || e.key === ' ') {
                nextSlide();
            } else if (e.key === 'ArrowRight' || e.key === 'PageUp') {
                prevSlide();
            } else if (e.key === 'Home') {
                showSlide(1);
            } else if (e.key === 'End') {
                showSlide(totalSlides);
            }
        });
    </script>
</body>
</html>
"""

# Write HTML presentation
target_deck_html = os.path.join(web_dir, "Presentation_Deck.html")
with open(target_deck_html, "w", encoding="utf-8") as f:
    f.write(deck_html)
print(f"Written: {target_deck_html}")

shutil.copy2(target_deck_html, os.path.join(desktop_dir, "عرض_مناقشة_الماجستير_المينيماليست.html"))
print("Copied HTML presentation to Desktop!")

# -------------------------------------------------------------
# 2. BUILD NATIVE PPTX PRESENTATION (Clean Light Theme)
# -------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

COLOR_BG = RGBColor(255, 255, 255)       # Pure White
COLOR_TEXT = RGBColor(15, 23, 42)        # Slate 900
COLOR_MUTED = RGBColor(100, 116, 139)    # Slate 500
COLOR_BLUE = RGBColor(37, 99, 235)       # Blue 600
COLOR_RED = RGBColor(220, 38, 38)        # Red 600
COLOR_CARD = RGBColor(248, 250, 252)     # Slate 50
COLOR_BORDER = RGBColor(226, 232, 240)   # Slate 200

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_BG
    bg.line.color.rgb = COLOR_BG

def add_header(slide, title_text, category_text, slide_num):
    # Header box
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = f"{category_text.upper()} | SLIDE {slide_num} OF 10"
    p0.font.name = "Arial"
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_BLUE
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = "Arial"
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT

# SLIDE 1: Title
s1 = prs.slides.add_slide(blank_layout)
set_slide_background(s1)
tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.333), Inches(4.0))
tf1 = tb1.text_frame
tf1.word_wrap = True
p = tf1.paragraphs[0]
p.text = "ACADEMIC RESEARCH MONOGRAPH | PRE-MASTER'S DEGREE DEFENSE"
p.font.name = "Arial"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf1.add_paragraph()
p.text = "التحليل المكاني متكامل الحساسات لتقييم الدمار العمراني في قطاع غزة"
p.font.name = "Arial"
p.font.size = Pt(28)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT

p = tf1.add_paragraph()
p.text = "Multi-Sensor Urban Damage Assessment Project — Gaza Strip (2023–2026)"
p.font.name = "Arial"
p.font.size = Pt(15)
p.font.color.rgb = COLOR_MUTED

p = tf1.add_paragraph()
p.text = "\n• Baseline Buildings: 326,448 structures | Confirmed Damaged: 149,055 (45.66%)\n• Completely Destroyed: 67,689 | Estimated Debris: 125.96 Million Metric Tons (UNEP)\n• Coordinate Reference System: WGS 84 / UTM Zone 36N (EPSG:32636)"
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_TEXT

# SLIDE 2: Research Problem & Multi-Sensor Paradigm
s2 = prs.slides.add_slide(blank_layout)
set_slide_background(s2)
add_header(s2, "منهجية تكامل الحساسات والتمايز بين الحقيقة الأرضية والمؤشرات", "Research Methodology", 2)
tb2 = s2.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.0))
tf2 = tb2.text_frame
tf2.word_wrap = True
p = tf2.paragraphs[0]
p.text = "1. الحقيقة الأرضية المؤكدة (Ground Truth):"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf2.add_paragraph()
p.text = "بيانات UNOSAT المستخلصة عبر التفسير البصري للصور الفضائية فائقة الدقة (VHR 30–50 cm). تم تصنيفها إلى 4 درجات قياسية: Code 1 (مدمر)، Code 2 (أضرار بالغة)، Code 3 (أضرار متوسطة)، Code 4 (أضرار محتملة).\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf2.add_paragraph()
p.text = "2. البصمة الرادارية للتغير الإنشائي (Sentinel-1 SAR C-band):"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf2.add_paragraph()
p.text = "مؤشر فيزيائي لقياس هبوط الارتداد الراداري الخلفي نتيجة انهيار الزوايا القائمة للمباني:\nΔσ⁰_dB = 10 · log₁₀(γ_post / γ_pre) < -3.0 dB\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf2.add_paragraph()
p.text = "3. الانضباط الجيوديسي:"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf2.add_paragraph()
p.text = "اعتماد نظام الإسقاط المتري المستوي UTM Zone 36N لكافة العمليات الحسابية لحساب المساحات دون أي تشويه كروي."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

# SLIDE 3: Macro Satellite Evidence Image
s3 = prs.slides.add_slide(blank_layout)
set_slide_background(s3)
add_header(s3, "المرئيات الفضائية الشاملة لقطاع غزة (Sentinel-2 True Color 10m)", "Satellite Evidence", 3)
p_macro = os.path.join(assets_dir, "gaza_strip_full_comparison_plate.jpg")
if os.path.exists(p_macro):
    s3.shapes.add_picture(p_macro, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.3))

# SLIDE 4: Hotspots Satellite Evidence
s4 = prs.slides.add_slide(blank_layout)
set_slide_background(s4)
add_header(s4, "توثيق بؤر الدمار الكبرى: الشجاعية، بيت حانون، خان يونس، رفح", "Hotspots Evidence", 4)
p_shuj = os.path.join(assets_dir, "gaza_city_shujaiyya_comparison_plate.jpg")
p_beit = os.path.join(assets_dir, "north_beit_hanoun_comparison_plate.jpg")
if os.path.exists(p_shuj):
    s4.shapes.add_picture(p_shuj, Inches(1.0), Inches(1.5), Inches(5.4), Inches(2.5))
if os.path.exists(p_beit):
    s4.shapes.add_picture(p_beit, Inches(6.8), Inches(1.5), Inches(5.4), Inches(2.5))
p_khan = os.path.join(assets_dir, "khan_younis_center_comparison_plate.jpg")
p_rafah = os.path.join(assets_dir, "rafah_border_comparison_plate.jpg")
if os.path.exists(p_khan):
    s4.shapes.add_picture(p_khan, Inches(1.0), Inches(4.3), Inches(5.4), Inches(2.5))
if os.path.exists(p_rafah):
    s4.shapes.add_picture(p_rafah, Inches(6.8), Inches(4.3), Inches(5.4), Inches(2.5))

# SLIDE 5: Governorate Table
s5 = prs.slides.add_slide(blank_layout)
set_slide_background(s5)
add_header(s5, "المصفوفة الرقمية المعتمدة لتوزيع الأضرار بالمحافظات", "Empirical Matrix", 5)

# Add Table
rows = 7
cols = 7
left = Inches(1.0)
top = Inches(1.6)
width = Inches(11.333)
height = Inches(4.8)
table_shape = s5.shapes.add_table(rows, cols, left, top, width, height)
tbl = table_shape.table

headers = ["المحافظة", "المساحة", "إجمالي المباني", "المتضررة (1-3)", "النسبة %", "مدمر كلياً (1)", "الركام (Mt)"]
data = [
    ["شمال غزة", "61.13 كم²", "53,292", "34,116", "64.02%", "13,838", "28.55"],
    ["غزة", "73.83 كم²", "69,349", "38,987", "56.22%", "16,199", "39.99"],
    ["دير البلح", "58.36 كم²", "56,178", "13,467", "23.97%", "5,268", "10.48"],
    ["خان يونس", "107.57 كم²", "92,068", "38,292", "41.59%", "17,581", "29.33"],
    ["رفح", "63.98 كم²", "55,561", "24,193", "43.54%", "14,803", "17.61"],
    ["الإجمالي العام", "364.87 كم²", "326,448", "149,055", "45.66%", "67,689", "125.96 Mt"]
]

for col_idx, h in enumerate(headers):
    cell = tbl.cell(0, col_idx)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_CARD
    p = cell.text_frame.paragraphs[0]
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEXT

for row_idx, row_data in enumerate(data):
    for col_idx, val in enumerate(row_data):
        cell = tbl.cell(row_idx + 1, col_idx)
        cell.text = val
        cell.fill.solid()
        if row_idx == 5:
            cell.fill.fore_color.rgb = RGBColor(241, 245, 249)
        else:
            cell.fill.fore_color.rgb = COLOR_BG
        p = cell.text_frame.paragraphs[0]
        p.font.name = "Arial"
        p.font.size = Pt(10)
        if row_idx == 5 or col_idx == 3:
            p.font.bold = True
        if col_idx == 4 and row_idx in [0, 1]:
            p.font.color.rgb = COLOR_RED

# SLIDE 6: Sensitivity Analysis
s6 = prs.slides.add_slide(blank_layout)
set_slide_background(s6)
add_header(s6, "مصفوفة الحساسية المكانية لنصف قطر الاقتران (Off-Nadir Compensation)", "Sensitivity Analysis", 6)
tb6 = s6.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.0))
tf6 = tb6.text_frame
tf6.word_wrap = True
p = tf6.paragraphs[0]
p.text = "أسباب إجراء تحليل الحساسية لنصف قطر البحث (Search Radius):"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf6.add_paragraph()
p.text = "نظراً لأن الأقمار الصناعية تلتقط المشاهد بزوايا انحراف عن السمت (Off-Nadir) تتراوح بين 10 إلى 25 درجة، فإن مسقط النقطة المرصودة جغرافياً قد ينزاح عن مضلع المبنى الأرضي. تم اختبار 3 نطاقات بحثية مقارنة:\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf6.add_paragraph()
p.text = "• البحث المباشر (0m Search Radius - Geometric Intersection):\n  رصد 131,182 مبنى متضرراً (40.18% من إجمالي المباني).\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf6.add_paragraph()
p.text = "• البحث المحافظ (3m Search Radius):\n  رصد 161,833 مبنى متضرراً (49.57% من إجمالي المباني).\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf6.add_paragraph()
p.text = "• المعيار الدولي المعتمد لـ UNOSAT (5m Search Radius):\n  رصد 175,692 اقتراناً، تم بعد تصفية الأكواد والتكرارات اعتماد 149,055 مبنى مؤكد التضرر (45.66%)."
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

# SLIDE 7: Geostatistics & Hotspots
s7 = prs.slides.add_slide(blank_layout)
set_slide_background(s7)
add_header(s7, "النمذجة الجيوإحصائية: Getis-Ord Gi* مع تصحيح FDR", "Spatial Geostatistics", 7)
tb7 = s7.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.0))
tf7 = tb7.text_frame
tf7.word_wrap = True
p = tf7.paragraphs[0]
p.text = "1. بناء الشبكة المنتظمة (Fishnet Grid):"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf7.add_paragraph()
p.text = "تم إنشاء شبكة منتظمة من 6,146 خلية مربعة بحجم 250×250 متراً لحساب تركيز الدمار الإنشائي كدالة مكانية موضوعية مستقلة عن الحدود الإدارية.\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf7.add_paragraph()
p.text = "2. تصحيح معدل الاكتشاف الخاطئ (False Discovery Rate - FDR):"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf7.add_paragraph()
p.text = "لمنع ادعاء الدلالة الإحصائية الزائفة (Spurious Significance) الناتج عن اختبار آلاف الفرضيات في آن واحد، تم تقييد قيم p-value باستخدام خوارزمية Benjamini-Hochberg.\n"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

p = tf7.add_paragraph()
p.text = "3. التوزيع المكاني للبؤر عالية الثقة (99% Confidence, Z > 2.58):\n• قطاع شمال غزة: بيت حانون ومحيط مخيم جباليا.\n• محافظة غزة: الشجاعية، الزيتون، تل الهوى، الصبرة.\n• محافظة خان يونس: البلدة القديمة ومحيط مجمع ناصر الطبي."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

# SLIDE 8: UNEP Debris Volume Model
s8 = prs.slides.add_slide(blank_layout)
set_slide_background(s8)
add_header(s8, "النموذج الحجمي لركام الكوارث (UNEP Disaster Debris Model)", "Debris Estimation", 8)
tb8 = s8.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.0))
tf8 = tb8.text_frame
tf8.word_wrap = True
p = tf8.paragraphs[0]
p.text = "صيغة الأمم المتحدة لتقدير كتلة ركام البيئة المبنية:"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf8.add_paragraph()
p.text = "Debris (Tons) = Footprint Area (m²) × Mean Floors (3.5) × Bulk Density (1.4 tons/m²) × Severity Weight\n"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_TEXT

p = tf8.add_paragraph()
p.text = "• إجمالي الركام التقديري: 125,960,000 طن متري (125.96 Mt).\n• نطاق الحساسية: 75.6 Mt (الحد الأدنى) — 181.4 Mt (الحد الأقصى).\n• حصة محافظة غزة وشمال غزة: 68.54 مليون طن (54.4% من إجمالي ركام القطاع).\n• التحدي البيئي: تلوث الركام بمخلفات الحرب غير المنفجرة (UXO) وألياف الإسبستوس وغبار السيليكا."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

# SLIDE 9: Master Plate Showcase
s9 = prs.slides.add_slide(blank_layout)
set_slide_background(s9)
add_header(s9, "لوحة الإخراج الكارتوغرافي الشاملة (300 DPI A3 Master Plate)", "Cartographic Plate", 9)
p_plate = os.path.join(assets_dir, "Gaza_Damage_Assessment_A3_Master_Plate.png")
if os.path.exists(p_plate):
    s9.shapes.add_picture(p_plate, Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.3))

# SLIDE 10: Conclusion & Access
s10 = prs.slides.add_slide(blank_layout)
set_slide_background(s10)
add_header(s10, "الاستنتاجات الهندسية ومستودع البيانات الجيومكانية المفتوحة", "Conclusion & Data Access", 10)
tb10 = s10.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.333), Inches(5.0))
tf10 = tb10.text_frame
tf10.word_wrap = True
p = tf10.paragraphs[0]
p.text = "الخلاصة والتوصيات الاستراتيجية:"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_BLUE

p = tf10.add_paragraph()
p.text = "1. توفر الدراسة سجلاً رقمياً جيومكانياً مدققاً بنسبة 100% خالياً من أي تزييف أو مبالغات إنشائية، مما يجعله مرجعاً قانونياً وفنياً أمام الجهات الدولية المانحة ومحاكم العدل الدولية.\n2. التوصية بالبدء الفوري بإنشاء مراكز تدوير الركام في المناطق المفتوحة جنوب وادي غزة.\n3. مستودع البيانات متاح بالكامل داخل مجلد D:\\Gaza_Damage_Assessment_Project\\ بصيغ Geodatabase وShapefile وGeoTIFF."
p.font.size = Pt(11)
p.font.color.rgb = COLOR_TEXT

target_pptx = os.path.join(web_dir, "Presentation_Deck.pptx")
prs.save(target_pptx)
print(f"Native PPTX saved to: {target_pptx}")

shutil.copy2(target_pptx, os.path.join(desktop_dir, "عرض_مناقشة_الماجستير_المينيماليست.pptx"))
print("Copied native PPTX to Desktop!")
