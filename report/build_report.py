# -*- coding: utf-8 -*-
"""Build the final-project report PDF (Traditional Chinese, embedded fonts)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, KeepTogether, HRFlowable,
)

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(os.path.dirname(HERE), "期末專題報告書.pdf")

# ---- Fonts: embed Microsoft JhengHei (Traditional Chinese) + Consolas ----
pdfmetrics.registerFont(TTFont("JH", r"C:\Windows\Fonts\msjh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("JHB", r"C:\Windows\Fonts\msjhbd.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("Mono", r"C:\Windows\Fonts\consola.ttf"))
pdfmetrics.registerFont(TTFont("Sym", r"C:\Windows\Fonts\seguisym.ttf"))  # for ▶ play glyph
pdfmetrics.registerFontFamily("JH", normal="JH", bold="JHB", italic="JH", boldItalic="JHB")

INK = colors.HexColor("#1e293b")
MUTE = colors.HexColor("#475569")
INDIGO = colors.HexColor("#4f46e5")
SLATE = colors.HexColor("#334155")
LINE = colors.HexColor("#cbd5e1")
RED = colors.HexColor("#ef4444")
BLUE = colors.HexColor("#0ea5e9")
GREEN = colors.HexColor("#10b981")
HEADBG = colors.HexColor("#eef2ff")
ZEBRA = colors.HexColor("#f1f5f9")

def S(name, **kw):
    base = dict(fontName="JH", fontSize=10.5, leading=17, textColor=INK,
                wordWrap="CJK", alignment=TA_JUSTIFY, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(name, **base)

st_title   = S("title", fontName="JHB", fontSize=26, leading=34, alignment=TA_CENTER, textColor=SLATE, spaceAfter=0)
st_sub     = S("sub", fontSize=14, leading=22, alignment=TA_CENTER, textColor=INDIGO, spaceAfter=0)
st_h1      = S("h1", fontName="JHB", fontSize=16, leading=24, textColor=INDIGO, spaceBefore=14, spaceAfter=8)
st_h2      = S("h2", fontName="JHB", fontSize=12.5, leading=20, textColor=SLATE, spaceBefore=8, spaceAfter=4)
st_body    = S("body")
st_bullet  = S("bullet", leftIndent=16, bulletIndent=4, spaceAfter=3)
st_code    = S("code", fontName="Mono", fontSize=9, leading=14, textColor=colors.HexColor("#0f172a"),
               backColor=colors.HexColor("#f8fafc"), borderColor=LINE, borderWidth=0.5,
               borderPadding=6, leftIndent=4, rightIndent=4, alignment=TA_LEFT, wordWrap=None)
st_caption = S("caption", fontSize=9, leading=13, alignment=TA_CENTER, textColor=MUTE, spaceBefore=3)
st_eq      = S("eq", fontSize=11, leading=18, alignment=TA_CENTER, textColor=SLATE, spaceAfter=4)
st_cell    = S("cell", fontSize=9.5, leading=13, alignment=TA_CENTER, spaceAfter=0)
st_cellL   = S("cellL", fontSize=9.5, leading=13, alignment=TA_LEFT, spaceAfter=0)
st_cellH   = S("cellH", fontName="JHB", fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.white, spaceAfter=0)
st_meta    = S("meta", fontSize=12, leading=22, alignment=TA_CENTER, textColor=MUTE, spaceAfter=0)

story = []

def h1(t): story.append(Paragraph(t, st_h1))
def h2(t): story.append(Paragraph(t, st_h2))
def p(t):  story.append(Paragraph(t, st_body))
def sp(h=6): story.append(Spacer(1, h))
def bullets(items):
    for it in items:
        story.append(Paragraph(it, st_bullet, bulletText="•"))
def code(lines):
    txt = "<br/>".join(lines)
    story.append(Paragraph(txt, st_code)); sp(6)
def eq(t): story.append(Paragraph(t, st_eq))

def figure(fname, width_cm, caption):
    path = os.path.join(ASSETS, fname)
    from PIL import Image as PImage
    iw, ih = PImage.open(path).size
    w = width_cm * cm
    h = w * ih / iw
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    story.append(KeepTogether([img, Paragraph(caption, st_caption)]))
    sp(8)

def datatable(data, col_widths, header=True, zebra=True):
    rows = []
    for r, row in enumerate(data):
        styled = []
        for cell in row:
            if r == 0 and header:
                styled.append(Paragraph(str(cell), st_cellH))
            else:
                styled.append(Paragraph(str(cell), st_cell))
        rows.append(styled)
    t = Table(rows, colWidths=[c * cm for c in col_widths], hAlign="CENTER")
    ts = [
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        ts.append(("BACKGROUND", (0, 0), (-1, 0), INDIGO))
    if zebra:
        for r in range(1, len(data)):
            if r % 2 == 0:
                ts.append(("BACKGROUND", (0, r), (-1, r), ZEBRA))
    t.setStyle(TableStyle(ts))
    story.append(t); sp(8)

# ============================ COVER ============================
story.append(Spacer(1, 3.2 * cm))
story.append(Paragraph("邏輯設計　期末專題報告書", st_sub))
sp(20)
story.append(HRFlowable(width="62%", thickness=1.2, color=LINE, spaceBefore=2, spaceAfter=18, hAlign="CENTER"))
story.append(Paragraph("循序電路設計", st_title))
story.append(Paragraph("自動化系統", st_title))
sp(10)
story.append(Paragraph("Sequential Circuit Design Automation System", st_sub))
sp(26)
story.append(HRFlowable(width="62%", thickness=1.2, color=LINE, spaceBefore=2, spaceAfter=22, hAlign="CENTER"))
story.append(Paragraph("學號　1140503", st_meta))
story.append(Paragraph("姓名　張昱謙", st_meta))
sp(16)
story.append(Paragraph("中華民國 115 年 6 月", st_meta))
sp(20)
story.append(Paragraph(
    '線上展示：<a href="https://doremi0614.github.io/logic/">'
    '<font name="Mono" size="10" color="#4f46e5">https://doremi0614.github.io/logic/</font></a>',
    st_meta))
sp(16)

# Prominent demo-video callout (placed below the website link).
VIDEO_URL = "https://youtu.be/cPSF_NMRxQI"
vid_title = ParagraphStyle("vidTitle", fontName="JHB", fontSize=15, leading=22,
                           alignment=TA_CENTER, textColor=colors.white)
vid_link = ParagraphStyle("vidLink", fontName="Mono", fontSize=12, leading=20,
                          alignment=TA_CENTER, textColor=colors.white)
vid = Table(
    [[Paragraph('<font name="Sym">&#9654;</font>&nbsp;&nbsp;這是示範影片連結（點我觀看）', vid_title)],
     [Paragraph('<a href="%s"><font color="#ffffff">%s</font></a>' % (VIDEO_URL, VIDEO_URL), vid_link)]],
    colWidths=[12 * cm])
vid.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#dc2626")),
    ("ROUNDEDCORNERS", [10, 10, 10, 10]),
    ("TOPPADDING", (0, 0), (-1, 0), 12),
    ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
    ("TOPPADDING", (0, 1), (-1, 1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
    ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ("RIGHTPADDING", (0, 0), (-1, -1), 10),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]))
vid.hAlign = "CENTER"
story.append(vid)
story.append(PageBreak())

# ============================ TOC (manual) ============================
h1("目錄")
toc = [
    ("一、專題簡介與動機", "1"),
    ("二、系統功能總覽", "2"),
    ("三、理論背景", "3"),
    ("四、完整製作流程", "4"),
    ("五、系統架構與技術細節", "5"),
    ("六、操作說明與實作範例", "6"),
    ("七、成果展示", "7"),
    ("八、開發過程遭遇的問題與解決", "8"),
    ("九、結論與心得", "9"),
    ("十、參考資料", "10"),
]
for name, _ in toc:
    story.append(Paragraph(name, S("toc", fontSize=11.5, leading=24, spaceAfter=2)))
story.append(PageBreak())

# ============================ 1. 簡介 ============================
h1("一、專題簡介與動機")
h2("1.1　專題動機")
p("在數位邏輯設計課程中，「循序電路（Sequential Circuit）」的設計流程相當繁瑣：從狀態表（State Table）開始，"
  "需要依序完成狀態指定、查激勵表、填卡諾圖、化簡布林方程式，最後才能畫出電路圖。整個過程不僅費時，"
  "人工化簡時也很容易出錯。本專題的動機，便是希望把這一連串「機械化」的設計步驟自動化，"
  "讓使用者只要輸入狀態表，系統就能即時算出結果並視覺化呈現，作為學習與驗算的輔助工具。")
h2("1.2　專題目標")
bullets([
    "以網頁形式（單頁式應用程式 SPA）實作，免安裝、跨平台、可直接於瀏覽器使用。",
    "支援 Mealy 與 Moore 兩種模型，以及 JK、T、D 三種正反器。",
    "由狀態表自動推導：狀態指定 → 激勵表 → 卡諾圖化簡 → 正反器輸入方程式。",
    "將結果視覺化：即時卡諾圖、自動佈線的電路圖、狀態轉換泡泡圖。",
    "可匯出設計報告，並部署到網際網路供任何人使用。",
])
h2("1.3　系統概觀")
p("系統採用現代、乾淨的淺色系工程軟體風格，畫面分為三個直行：左欄為輸入區（淡紅邊框）、"
  "中欄為運算結果區（淡藍邊框）、右欄為電路圖區（淡綠邊框），最下方為操作列。整體具備響應式設計（RWD），"
  "在較小螢幕時會自動由三欄變為單欄垂直排列。")
figure("app-overview.png", 16.5, "圖 1　系統整體介面（三欄式佈局，頂部與底部皆顯示作者學號姓名）")
story.append(PageBreak())

# ============================ 2. 功能總覽 ============================
h1("二、系統功能總覽")
h2("2.1　輸入區（左欄）")
bullets([
    "<b>Model Type</b>：選擇 Mealy 或 Moore 模型。",
    "<b>Flip-Flop Type</b>：選擇 JK、T 或 D 正反器。",
    "<b>State Table Input</b>：可自由命名輸入／輸出變數，並以可編輯的表格輸入狀態轉移，"
    "支援新增列、刪除列、清空、載入範例等操作。",
])
h2("2.2　運算結果區（中欄）")
bullets([
    "<b>State Transition Diagram</b>：將狀態表即時轉換為泡泡圖，圓圈代表狀態、箭頭代表轉換條件，"
    "不需按下 GENERATE 即時更新。",
    "<b>Flip-Flop Input Equations</b>：顯示化簡後的正反器輸入方程式與輸出方程式，並列出狀態編碼。",
    "<b>K-Map（Live）</b>：可下拉切換任一函數，以格雷碼排列並用顏色標示化簡所選的質含項群組。",
])
h2("2.3　電路圖區（右欄）")
bullets([
    "<b>Sequential Circuit Diagram</b>：依化簡後的方程式自動繪製電路圖，"
    "包含正反器、AND／OR 邏輯閘與接線，邏輯閘數量與佈線皆隨方程式自動調整。",
    "提供放大、縮小、全螢幕、下載 SVG 等工具按鈕。",
])
h2("2.4　底部操作列")
bullets([
    "左側顯示作者資訊（學號 1140503、姓名 張昱謙）。",
    "中央為 GENERATE 主按鈕；當輸入變更後按鈕會轉為琥珀色，提示需重新產生。",
    "右側為 EXPORT REPORT（匯出純文字設計報告）與 About。",
])
story.append(PageBreak())

# ============================ 3. 理論背景 ============================
h1("三、理論背景")
h2("3.1　Mealy 與 Moore 模型")
p("Mealy 模型的輸出為「現態」與「輸入」的函數，輸出可能在輸入改變的當下立即變化；"
  "Moore 模型的輸出僅為「現態」的函數，輸出只在狀態改變時變化。本系統在 Mealy 模式下，"
  "輸出方程式包含輸入變數；在 Moore 模式下，系統會檢查同一狀態的輸出是否一致，並把輸出標示在狀態泡泡內。")
h2("3.2　正反器激勵表（Excitation Table）")
p("「激勵」是指要讓正反器從現態 Q(t) 轉移到次態 Q(t+1) 所需的輸入值。三種正反器的激勵表如下"
  "（d 表示 don't care）：")

sp(2)

def excit_table(cols, data, widths):
    rows = [[Paragraph(c, st_cellH) for c in cols]]
    rows += [[Paragraph(x, st_cell) for x in row] for row in data]
    t = Table(rows, colWidths=[w * cm for w in widths])
    t.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, LINE),
        ("BACKGROUND", (0, 0), (-1, 0), INDIGO),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]))
    return t

jk_t = excit_table(["Q(t)→Q(t+1)", "J", "K"],
                   [["0 → 0", "0", "d"], ["0 → 1", "1", "d"], ["1 → 0", "d", "1"], ["1 → 1", "d", "0"]],
                   [2.5, 1.0, 1.0])
t_t = excit_table(["Q(t)→Q(t+1)", "T"],
                  [["0 → 0", "0"], ["0 → 1", "1"], ["1 → 0", "1"], ["1 → 1", "0"]],
                  [2.5, 1.0])
d_t = excit_table(["Q(t)→Q(t+1)", "D"],
                  [["0 → 0", "0"], ["0 → 1", "1"], ["1 → 0", "0"], ["1 → 1", "1"]],
                  [2.5, 1.0])

two = Table([[jk_t, t_t, d_t]], colWidths=[5.3 * cm, 4.1 * cm, 4.1 * cm])
two.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
]))
story.append(two)
story.append(Paragraph("表 1　JK／T／D 正反器激勵表", st_caption))
sp(8)
p("由此可知：D 正反器最單純，其激勵 D = Q(t+1)，也就是「次態值」本身；T 正反器的激勵為 "
  "T = Q(t) ⊕ Q(t+1)；JK 正反器則因含有 don't care，化簡後常能得到最精簡的邏輯。")

h2("3.3　卡諾圖與 Quine–McCluskey 化簡法")
p("卡諾圖（Karnaugh Map）適合人工化簡 2～4 個變數的布林函數；而本系統內部採用 "
  "<b>Quine–McCluskey（QM）演算法</b>進行化簡，原因是 QM 為表格式、步驟明確、易於程式化，"
  "且能正確處理任意變數數量與 don't care。其流程為：(1) 將最小項與 don't care 反覆兩兩合併，"
  "找出所有「質含項（Prime Implicants）」；(2) 以「必要質含項」優先，再用貪婪法選取最少數量的質含項，"
  "覆蓋所有必須為 1 的最小項。中欄的卡諾圖即把 QM 所選的質含項以不同顏色圈選標示，方便對照。")
story.append(PageBreak())

# ============================ 4. 完整製作流程 ============================
h1("四、完整製作流程")
p("本章依實際開發順序，完整說明本專題從零到部署上線的每一個步驟。")

h2("4.1　需求分析與規劃")
p("先確認系統要解決的核心問題：把「狀態表 → 正反器輸入方程式 → 電路圖」的人工流程自動化。"
  "據此規劃三欄式版面（輸入／結果／電路圖），並列出必備功能：模型與正反器選擇、可編輯狀態表、"
  "化簡方程式、卡諾圖、電路圖與狀態圖。")

h2("4.2　技術選型")
bullets([
    "<b>React 19</b>：以元件化方式管理 UI 與狀態，輸入改變即自動重繪。",
    "<b>Tailwind CSS v4</b>：以 utility class 快速打造一致的工程軟體風格。",
    "<b>Vite 6</b>：開發伺服器啟動快、支援熱更新（HMR），打包輕量。",
    "<b>Lucide React</b>：提供乾淨的線條圖示。",
    "全部以純前端實作，化簡與佈線皆於瀏覽器端計算，無需後端伺服器。",
])

h2("4.3　開發環境建置")
p("開發初期本機尚未安裝 Node.js。為了能立即預覽，先製作了一份免安裝的 "
  "<font name='Mono' size='9'>standalone.html</font>（透過 CDN 載入 React／Tailwind／Babel），"
  "可直接用瀏覽器開啟。之後再正式安裝 Node.js LTS 並建立 Vite 專案：")
code([
    "winget install OpenJS.NodeJS.LTS      # 安裝 Node.js 24 LTS",
    "npm install                            # 安裝專案相依套件",
    "npm run dev                            # 啟動開發伺服器 (localhost:5173)",
])

h2("4.4　介面實作")
p("依規劃建立三欄式版面與卡片元件，抽出共用的 Card、Radio、IconButton 等小元件，"
  "並以 Tailwind 的 lg 斷點實作 RWD：螢幕寬度不足時三欄自動改為單欄垂直排列。"
  "左欄輸入、中欄結果、右欄電路圖分別以淡紅、淡藍、淡綠邊框作視覺區分。")

h2("4.5　核心演算法實作")
p("這是系統的心臟，依序完成下列步驟：")
bullets([
    "<b>狀態指定</b>：依狀態出現順序給定二進位編碼（如 A=00、B=01、C=10），"
    "並自動決定所需正反器數量 n = ⌈log₂(狀態數)⌉。",
    "<b>建立激勵表</b>：逐列依現態與次態，按 JK／T／D 的激勵規則填入各正反器輸入的真值表；"
    "凡未出現的（狀態, 輸入）組合一律視為 don't care。",
    "<b>布林化簡</b>：以 Quine–McCluskey 演算法求出每個輸入函數的最簡「積之和（SOP）」。",
    "<b>輸出方程式</b>：Mealy 由現態與輸入決定；Moore 僅由現態決定，並檢查輸出一致性。",
])

h2("4.6　視覺化實作")
bullets([
    "<b>卡諾圖</b>：以格雷碼排列產生 2～4 變數的網格，並把化簡所選的質含項以顏色圈選。",
    "<b>電路圖</b>：依方程式的每個乘積項自動佈置 AND 閘，再以 OR 閘合併，"
    "並把輸入變數拉成左側匯流排、正反器輸出回授，全部以 SVG 動態繪製、可縮放與下載。",
    "<b>狀態轉換圖</b>：把狀態排成圓形佈局，依轉移畫出箭頭，"
    "自我迴圈與雙向轉換會自動彎曲避開，初始狀態加上起始箭頭。",
])

h2("4.7　測試與驗證")
p("每完成一項功能，便在瀏覽器預覽中以實際操作驗證：切換模型／正反器、編輯狀態表、按下 GENERATE，"
  "並核對輸出方程式是否與手算結果一致（如後述第六章範例）。也測試了錯誤情況，"
  "例如空狀態、未定義的次態、重複的（狀態, 輸入）列、Moore 模型輸出不一致等，系統皆會顯示對應的錯誤或警告。")

h2("4.8　版本控制與部署")
p("以 Git 進行版本控制，並推送至 GitHub。專案附帶 GitHub Actions 工作流程，"
  "每次 push 到 main 分支即自動建置（npm run build）並部署到 GitHub Pages：")
code([
    "git add -A",
    "git commit -m \"...\"",
    "git push                               # 觸發 Actions 自動部署",
])
p("部署完成後，網站即可於下列網址公開使用：")
eq("<font name='Mono' color='#4f46e5'>https://doremi0614.github.io/logic/</font>")

h2("4.9　後續功能擴充")
p("在基本系統完成並上線後，又陸續加入三項擴充：(1) 即時<b>狀態轉換圖</b>；"
  "(2) 新增 <b>D 型正反器</b>（D = 次態值，激勵最單純）；"
  "(3) 將底部的 Settings 改為顯示作者<b>學號姓名（1140503 張昱謙）</b>。")
story.append(PageBreak())

# ============================ 5. 架構 ============================
h1("五、系統架構與技術細節")
h2("5.1　檔案結構")
code([
    "logic/",
    "├─ index.html              # 進入點",
    "├─ src/",
    "│  ├─ main.jsx             # React 掛載點",
    "│  ├─ App.jsx              # 主程式（UI + 演算法，單一檔案）",
    "│  └─ index.css            # Tailwind 進入點",
    "├─ standalone.html         # 免安裝 CDN 預覽版（由 App.jsx 產生）",
    "├─ vite.config.js          # Vite 設定",
    "├─ package.json            # 相依套件與指令",
    "└─ .github/workflows/deploy.yml   # GitHub Pages 自動部署",
])
h2("5.2　資料流")
p("使用者輸入（狀態表、模型、正反器）儲存在 React 的 state 中。按下 GENERATE 時呼叫核心函數 "
  "<font name='Mono' size='9'>designCircuit()</font>，回傳狀態編碼、化簡後方程式與各函數的真值表；"
  "中欄與右欄的卡諾圖、電路圖元件再依此結果繪製。狀態轉換圖則直接讀取狀態表，"
  "因此不需按 GENERATE 即可即時更新。當輸入與上次產生的內容不同時，系統會標記為 stale 並提示重新產生。")
h2("5.3　關鍵技術點")
bullets([
    "Quine–McCluskey 化簡同時支援 don't care，能對應正反器激勵表中的無關項。",
    "電路圖以遞迴方式依乘積項數量計算 AND／OR 閘的位置與接線座標，達成自動佈線。",
    "所有圖形皆為 SVG，可無損縮放並下載，方便放入報告或投影片。",
])
story.append(PageBreak())

# ============================ 6. 操作說明與範例 ============================
h1("六、操作說明與實作範例")
h2("6.1　操作步驟")
bullets([
    "於左欄選擇模型（Mealy／Moore）與正反器（JK／T／D）。",
    "在 State Table 輸入狀態轉移；可按「Load Example」載入內建範例。",
    "按下 GENERATE，中欄與右欄即顯示方程式、卡諾圖與電路圖。",
    "需要時可下載電路圖／狀態圖 SVG，或按 EXPORT REPORT 匯出文字報告。",
])
h2("6.2　範例：以內建狀態表驗證")
p("以系統內建範例（Mealy 模型、JK 正反器）為例，其狀態表如下：")
datatable(
    [["現態 (Present)", "X", "次態 (Next)", "Z"],
     ["A", "0", "A", "0"],
     ["A", "1", "B", "0"],
     ["B", "0", "C", "0"],
     ["B", "1", "B", "1"],
     ["C", "0", "A", "1"],
     ["C", "1", "B", "0"]],
    col_widths=[4.2, 2.2, 4.2, 2.2])
p("系統自動指定狀態編碼 <b>A=00、B=01、C=10</b>（狀態變數 Q<sub>1</sub>Q<sub>0</sub>），"
  "經激勵表與 Quine–McCluskey 化簡後，得到下列結果：")
eq("J<sub>1</sub> = Q<sub>0</sub>·X′　　K<sub>1</sub> = 1　　J<sub>0</sub> = X　　K<sub>0</sub> = X′")
eq("Z = Q<sub>0</sub>·X + Q<sub>1</sub>·X′　（Mealy 輸出）")
p("（註：X′ 表示 X 的反相 NOT X。）此結果與人工查激勵表、填卡諾圖化簡所得完全一致，驗證系統正確。")
story.append(PageBreak())

# ============================ 7. 成果展示 ============================
h1("七、成果展示")
p("下列為上述範例由系統自動產生的狀態轉換圖與循序電路圖。")
figure("state-diagram.png", 9.5, "圖 2　狀態轉換圖：圓圈為狀態、箭頭標示「輸入／輸出」，含自我迴圈與起始箭頭")
figure("circuit-diagram.png", 13.0,
       "圖 3　循序電路圖：兩個 JK 正反器、自動佈置的 AND／OR 閘與接線，右側輸出 Z")
p("系統已部署上線，任何人皆可於瀏覽器開啟下列網址實際操作："
  "<font name='Mono' size='9.5' color='#4f46e5'>https://doremi0614.github.io/logic/</font>")
story.append(PageBreak())

# ============================ 8. 問題與解決 ============================
h1("八、開發過程遭遇的問題與解決")
def qa(title, problem, solution):
    h2(title)
    story.append(Paragraph("<b>問題：</b>" + problem, st_body))
    story.append(Paragraph("<b>解決：</b>" + solution, st_body))
qa("8.1　本機尚未安裝 Node.js",
   "開發初期環境沒有 Node.js／npm，無法立即建立 Vite 專案預覽。",
   "先以 CDN 製作免安裝的 standalone.html 快速預覽；之後再用 winget 安裝 Node.js LTS 建立正式專案。")
qa("8.2　standalone.html 中文亂碼",
   "由程式自動產生 standalone.html 時，中文與 ·、′ 等符號出現亂碼。",
   "改以明確的 UTF-8（無 BOM）讀寫檔案，確保特殊字元正確保存。")
qa("8.3　git push 被拒（fast-forward）",
   "在 GitHub 網頁上操作後，遠端多出本機沒有的提交，導致 push 被拒。",
   "先 git pull 整合遠端變更後再 push。")
qa("8.4　兩個部署工作流程衝突",
   "從 GitHub 頁面套用了 Static HTML 範本，產生的 static.yml 會把未建置的原始碼直接上傳，"
   "與自訂的 deploy.yml（會先 build）互相競爭，可能導致網站壞掉。",
   "刪除多餘的 static.yml，只保留會先建置 Vite 專案的 deploy.yml。")
qa("8.5　Tailwind v4 色彩與截圖工具相容性",
   "Tailwind v4 預設使用 oklch() 色彩，傳統截圖函式庫無法解析。",
   "改用支援 oklch 的 html2canvas-pro 擷取介面，並把 SVG 圖以瀏覽器 canvas 轉為高解析 PNG。")
story.append(PageBreak())

# ============================ 9. 結論 ============================
h1("九、結論與心得")
p("本專題完成了一套可實際運作的「循序電路設計自動化系統」，"
  "把課堂上繁瑣的人工設計流程——狀態指定、激勵表、卡諾圖化簡、繪製電路圖——"
  "整合為輸入狀態表即可一鍵完成，並支援 Mealy／Moore 模型與 JK／T／D 三種正反器。")
p("在製作過程中，我把課本的理論（激勵表、Quine–McCluskey 化簡）實際寫成程式，"
  "對演算法的理解比單純做習題更深刻；也學到完整的前端工程流程：從環境建置、元件化開發、"
  "瀏覽器驗證，到使用 Git 與 GitHub Actions 自動部署上線。過程中遇到的種種問題與排解，"
  "更是一次完整的工程實戰經驗。")
p("未來可再擴充的方向包括：支援多個輸入／輸出變數、自動狀態化簡（state minimization）、"
  "提供電路時序模擬，以及匯出標準的 Verilog／VHDL 程式碼。")

h1("十、參考資料")
bullets([
    "M. Morris Mano, Michael D. Ciletti, <i>Digital Design</i>.",
    "Quine–McCluskey algorithm — 布林函數最小化演算法。",
    "React 官方文件　https://react.dev/",
    "Tailwind CSS 官方文件　https://tailwindcss.com/",
    "Vite 官方文件　https://vite.dev/",
    "專案原始碼　https://github.com/doremi0614/logic",
    "線上展示　https://doremi0614.github.io/logic/",
    "示範影片　https://youtu.be/cPSF_NMRxQI",
])

# ============================ Build ============================
def footer(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        canvas.setFont("JH", 8.5)
        canvas.setFillColor(MUTE)
        canvas.drawString(2 * cm, 1.2 * cm, "循序電路設計自動化系統　—　期末專題報告書")
        canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, "第 %d 頁" % (doc.page - 1))
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(2 * cm, 1.5 * cm, A4[0] - 2 * cm, 1.5 * cm)
    canvas.restoreState()

frame = Frame(2 * cm, 1.8 * cm, A4[0] - 4 * cm, A4[1] - 3.4 * cm, id="main")
doc = BaseDocTemplate(OUT, pagesize=A4, title="循序電路設計自動化系統 — 期末專題報告書",
                      author="1140503 張昱謙")
doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])
doc.build(story)
print("PDF written:", OUT, os.path.getsize(OUT), "bytes")
