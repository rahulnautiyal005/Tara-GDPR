import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Create workbook
wb = openpyxl.Workbook()

# ==============================================================
# PREMIUM COLOR PALETTE & STYLES
# ==============================================================
NAVY_PRIMARY = "0B132B"       # Midnight Navy
NAVY_ACCENT = "1C2541"        # Slate Navy
NAVY_LIGHT = "263655"         # Table Header Navy
HEADER_TEXT = "FFFFFF"

FILL_CRITICAL = PatternFill(start_color="FFE4E6", end_color="FFE4E6", fill_type="solid")  # Rose
FONT_CRITICAL = Font(name="Segoe UI", size=10, bold=True, color="9F1239")

FILL_HIGH = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")      # Amber
FONT_HIGH = Font(name="Segoe UI", size=10, bold=True, color="92400E")

FILL_MEDIUM = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")    # Sky Blue
FONT_MEDIUM = Font(name="Segoe UI", size=10, bold=True, color="0369A1")

FILL_LOW = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")       # Slate
FONT_LOW = Font(name="Segoe UI", size=10, color="475569")

FILL_COMPLETED = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid") # Emerald
FONT_COMPLETED = Font(name="Segoe UI", size=10, bold=True, color="166534")

# Legend Task Fills
FILL_LEG_STATIC = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")  # Blue
FONT_LEG_STATIC = Font(name="Segoe UI", size=10, bold=True, color="0369A1")

FILL_LEG_DOC = PatternFill(start_color="EDE9FE", end_color="EDE9FE", fill_type="solid")     # Purple
FONT_LEG_DOC = Font(name="Segoe UI", size=10, bold=True, color="5B21B6")

FILL_LEG_VM = PatternFill(start_color="FFE4E6", end_color="FFE4E6", fill_type="solid")      # Rose
FONT_LEG_VM = Font(name="Segoe UI", size=10, bold=True, color="9F1239")

FILL_LEG_BE = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")      # Emerald
FONT_LEG_BE = Font(name="Segoe UI", size=10, bold=True, color="166534")

FILL_LEG_UI = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid")      # Amber
FONT_LEG_UI = Font(name="Segoe UI", size=10, bold=True, color="92400E")

FILL_ZEBRA = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
FILL_KPI_BOX = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")

# Fonts
font_main_title = Font(name="Segoe UI", size=16, bold=True, color=HEADER_TEXT)
font_main_sub = Font(name="Segoe UI", size=10, italic=True, color="94A3B8")
font_sec_hdr = Font(name="Segoe UI", size=11, bold=True, color=HEADER_TEXT)
font_tbl_hdr = Font(name="Segoe UI", size=10, bold=True, color=HEADER_TEXT)
font_body = Font(name="Segoe UI", size=10, color="1E293B")
font_body_bold = Font(name="Segoe UI", size=10, bold=True, color="0F172A")

# Borders
border_light_gray = Side(border_style="thin", color="E2E8F0")
cell_border = Border(left=border_light_gray, right=border_light_gray, top=border_light_gray, bottom=border_light_gray)

border_navy_thick = Side(border_style="medium", color=NAVY_PRIMARY)
header_border = Border(left=border_light_gray, right=border_light_gray, top=border_light_gray, bottom=border_navy_thick)

# ==============================================================
# TAB 1: OVERVIEW (3-Track Architecture)
# ==============================================================
ws_over = wb.active
ws_over.title = "Overview"
ws_over.views.sheetView[0].showGridLines = True

# Row Heights
ws_over.row_dimensions[1].height = 14
ws_over.row_dimensions[2].height = 36
ws_over.row_dimensions[3].height = 22
ws_over.row_dimensions[4].height = 12

# Title Banner
ws_over.merge_cells("B2:I2")
t_cell = ws_over["B2"]
t_cell.value = "TARA PRIVACYOS — 3-Tier AI Compliance & Security Platform"
t_cell.font = font_main_title
t_cell.fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
t_cell.alignment = Alignment(horizontal="center", vertical="center")

ws_over.merge_cells("B3:I3")
s_cell = ws_over["B3"]
s_cell.value = "1. GitHub Code Analysis • 2. Document Review & Fix • 3. VM Sandbox Runtime Security • 45-Day Delivery"
s_cell.font = font_main_sub
s_cell.fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
s_cell.alignment = Alignment(horizontal="center", vertical="center")

for r in [2, 3]:
    for c in range(2, 10):
        ws_over[f"{get_column_letter(c)}{r}"].fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")

# Row 5: KPI Executive Cards
ws_over.row_dimensions[5].height = 42
kpi_data = [
    ("B5:C5", "TOTAL ROADMAP", "45 Working Days"),
    ("D5:E5", "CORE PILLARS", "3 Dedicated Tracks"),
    ("F5:G5", "DELIVERABLES", "34 Production Tasks"),
    ("H5:I5", "TARGET MVP", "Phase 1 by Day 15")
]

for merge_range, label, val in kpi_data:
    ws_over.merge_cells(merge_range)
    start_col = merge_range.split(":")[0]
    cell = ws_over[start_col]
    cell.value = f"{label}:  {val}"
    cell.font = font_body_bold
    cell.fill = FILL_KPI_BOX
    cell.alignment = Alignment(horizontal="center", vertical="center")
    
    start_c, end_c = merge_range.split(":")[0][0], merge_range.split(":")[1][0]
    r_idx = int(start_col[1:])
    for c_letter in [start_c, end_c]:
        ws_over[f"{c_letter}{r_idx}"].border = cell_border

ws_over.row_dimensions[6].height = 14

# Row 7: Section Header - 3 TRACK SUMMARY
ws_over.row_dimensions[7].height = 28
ws_over.merge_cells("B7:I7")
ps_hdr = ws_over["B7"]
ps_hdr.value = "  THE 3 CORE FUNCTIONAL TRACKS"
ps_hdr.font = font_sec_hdr
ps_hdr.fill = PatternFill(start_color=NAVY_ACCENT, end_color=NAVY_ACCENT, fill_type="solid")
ps_hdr.alignment = Alignment(horizontal="left", vertical="center")

# Row 8: Table Headers
ws_over.row_dimensions[8].height = 26
headers_overview = ["Operational Track", "Duration", "Sprint Window", "Core Value Proposition", "Assigned Lead", "Tasks", "Launch Status", "Risk Profile"]
cols = ["B", "C", "D", "E", "F", "G", "H", "I"]

for idx, h in enumerate(headers_overview):
    c_letter = cols[idx]
    cell = ws_over[f"{c_letter}8"]
    cell.value = h
    cell.font = font_tbl_hdr
    cell.fill = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = header_border

# Rows 9-11: Phase Data Rows
three_tracks_data = [
    ("Track 1 — Code-to-GDPR Generator (GitHub)", "15 Days", "Day 1 – Day 15", "'Give us your code, and we will tell you what GDPR requirements you need to follow'", "AI Lead + Dev", 12, "Completed", "Low"),
    ("Track 2 — Document Review & Statutory RAG Engine", "15 Days", "Day 16 – Day 30", "'Give us your existing GDPR docs, and we will find gaps and auto-correct them with grounded statutes'", "Legal AI Lead", 7, "Completed", "Low"),
    ("Track 3 — VM Sandbox Runtime Security Monitor", "15 Days", "Day 31 – Day 45", "'Run the app in a VM sandbox to detect suspicious activity, bulk access & data theft'", "Security Lead + DevOps", 11, "Planned", "High")
]

for row_offset, rdata in enumerate(three_tracks_data, start=9):
    ws_over.row_dimensions[row_offset].height = 32
    for col_idx, val in enumerate(rdata):
        c_letter = cols[col_idx]
        cell = ws_over[f"{c_letter}{row_offset}"]
        cell.value = val
        cell.font = font_body
        cell.border = cell_border
        
        if col_idx in [0, 3]:
            cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        else:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            
        if row_offset % 2 == 1:
            cell.fill = FILL_ZEBRA
            
        if col_idx == 6:
            if val == "Completed":
                cell.fill = FILL_COMPLETED
                cell.font = FONT_COMPLETED
            elif val == "Critical":
                cell.fill = FILL_CRITICAL
                cell.font = FONT_CRITICAL
            else:
                cell.fill = FILL_MEDIUM
                cell.font = FONT_MEDIUM
                
        if col_idx == 7:
            if val == "High":
                cell.fill = FILL_CRITICAL
                cell.font = FONT_CRITICAL
            else:
                cell.fill = FILL_HIGH
                cell.font = FONT_HIGH

ws_over.row_dimensions[12].height = 18

# Row 13: Section Header - WORKSTREAM LEGEND
ws_over.row_dimensions[13].height = 28
ws_over.merge_cells("B13:I13")
leg_hdr = ws_over["B13"]
leg_hdr.value = "  WORKSTREAM LEGEND — CORE CAPABILITIES"
leg_hdr.font = font_sec_hdr
leg_hdr.fill = PatternFill(start_color=NAVY_ACCENT, end_color=NAVY_ACCENT, fill_type="solid")
leg_hdr.alignment = Alignment(horizontal="left", vertical="center")

track_legends = [
    ("Static Code Analysis", "Track 1: AST parsing, database schema inspection, API route scanning, automated requirements", FILL_LEG_STATIC, FONT_LEG_STATIC),
    ("Document AI Review", "Track 2: NLP clause auditing, gap detection, Article 9 checks, statutory auto-rewriting", FILL_LEG_DOC, FONT_LEG_DOC),
    ("VM Sandbox Security", "Track 3: Isolated virtual machine, eBPF telemetry, bulk query anomaly detection, socket drop", FILL_LEG_VM, FONT_LEG_VM),
    ("Backend Architecture", "FastAPI / Node.js, pgvector knowledge base, LangGraph orchestrator, regulatory datasets", FILL_LEG_BE, FONT_LEG_BE),
    ("Frontend UI / UX", "Next.js executive console, diff viewers, live telemetry terminal, simulator dashboards", FILL_LEG_UI, FONT_LEG_UI)
]

for row_offset, (tname, tdesc, tfill, tfont) in enumerate(track_legends, start=14):
    ws_over.row_dimensions[row_offset].height = 26
    
    ws_over.merge_cells(f"B{row_offset}:C{row_offset}")
    c_cat = ws_over[f"B{row_offset}"]
    c_cat.value = tname
    c_cat.font = tfont
    c_cat.fill = tfill
    c_cat.alignment = Alignment(horizontal="center", vertical="center")
    c_cat.border = cell_border
    ws_over[f"C{row_offset}"].border = cell_border
    
    ws_over.merge_cells(f"D{row_offset}:I{row_offset}")
    c_desc = ws_over[f"D{row_offset}"]
    c_desc.value = tdesc
    c_desc.font = font_body
    c_desc.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    c_desc.border = cell_border
    for ci in ["E", "F", "G", "H", "I"]:
        ws_over[f"{ci}{row_offset}"].border = cell_border

col_widths_overview = {
    "A": 4,
    "B": 38,
    "C": 16,
    "D": 18,
    "E": 68,
    "F": 24,
    "G": 12,
    "H": 16,
    "I": 16
}
for c, w in col_widths_overview.items():
    ws_over.column_dimensions[c].width = w

# ==============================================================
# DETAIL TAB BUILDER
# ==============================================================
detail_headers = ["Task ID", "Workstream", "Task Description", "Assigned Owner", "Priority", "Est. Days", "Progress", "Status", "Deliverable / Production Output"]
detail_cols = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]

def build_spacious_detail_tab(ws, tab_title, banner_sub, tasks):
    ws.views.sheetView[0].showGridLines = True
    
    ws.row_dimensions[1].height = 14
    ws.row_dimensions[2].height = 34
    ws.row_dimensions[3].height = 22
    ws.row_dimensions[4].height = 14
    ws.row_dimensions[5].height = 28
    
    ws.merge_cells("A2:I2")
    tcell = ws["A2"]
    tcell.value = f"TARA PRIVACYOS — {tab_title}"
    tcell.font = font_main_title
    tcell.fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
    tcell.alignment = Alignment(horizontal="center", vertical="center")
    
    ws.merge_cells("A3:I3")
    scell = ws["A3"]
    scell.value = banner_sub
    scell.font = font_main_sub
    scell.fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
    scell.alignment = Alignment(horizontal="center", vertical="center")
    
    for r in [2, 3]:
        for c in range(1, 10):
            ws[f"{get_column_letter(c)}{r}"].fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
            
    for idx, h in enumerate(detail_headers):
        col_letter = detail_cols[idx]
        cell = ws[f"{col_letter}5"]
        cell.value = h
        cell.font = font_tbl_hdr
        cell.fill = PatternFill(start_color=NAVY_LIGHT, end_color=NAVY_LIGHT, fill_type="solid")
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border
        
    for row_idx, task in enumerate(tasks, start=6):
        ws.row_dimensions[row_idx].height = 28
        for col_idx, val in enumerate(task):
            col_letter = detail_cols[col_idx]
            cell = ws[f"{col_letter}{row_idx}"]
            cell.value = val
            cell.font = font_body
            cell.border = cell_border
            
            if col_idx in [2, 8]:
                cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
            elif col_idx in [1, 3]:
                cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
            else:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                
            if row_idx % 2 == 1:
                cell.fill = FILL_ZEBRA
                
            if col_idx == 4:
                if val == "Critical":
                    cell.fill = FILL_CRITICAL
                    cell.font = FONT_CRITICAL
                elif val == "High":
                    cell.fill = FILL_HIGH
                    cell.font = FONT_HIGH
                elif val == "Medium":
                    cell.fill = FILL_MEDIUM
                    cell.font = FONT_MEDIUM
                else:
                    cell.fill = FILL_LOW
                    cell.font = FONT_LOW
                    
            if col_idx == 7:
                if val == "Completed":
                    cell.fill = FILL_COMPLETED
                    cell.font = FONT_COMPLETED
                elif val == "In Progress":
                    cell.fill = FILL_MEDIUM
                    cell.font = FONT_MEDIUM
                elif val == "Planned":
                    cell.fill = FILL_HIGH
                    cell.font = FONT_HIGH
                    
    col_widths_detail = {
        "A": 14,
        "B": 24,
        "C": 58,
        "D": 22,
        "E": 14,
        "F": 12,
        "G": 12,
        "H": 16,
        "I": 42
    }
    for c, w in col_widths_detail.items():
        ws.column_dimensions[c].width = w

# ==============================================================
# TAB 2: Track 1 — Code-to-GDPR (GitHub)
# ==============================================================
ws_p1 = wb.create_sheet(title="Track 1 — Code to GDPR")
track_1_tasks = [
    ("CODE-101", "Static Code Analysis", "Build GitHub Repository Cloner & AST Syntax Tree Parser", "Backend Lead", "Critical", 2, "100%", "Completed", "tara_privacyos/core/repo_ast_parser.py"),
    ("CODE-102", "Static Code Analysis", "Develop ORM & Database Schema PII Identifier (detects Aadhaar, PAN, NI, NHS)", "Legal AI Lead", "Critical", 2, "100%", "Completed", "tara_privacyos/core/pii_schema_detector.py"),
    ("CODE-103", "Static Code Analysis", "Build API Route & Controller Data-Flow Tracer (finds unconsented collection)", "Backend Dev", "Critical", 3, "100%", "Completed", "tara_privacyos/core/api_route_tracer.py"),
    ("CODE-104", "Static Code Analysis", "Detect Third-Party SDK & LLM Calls (OpenAI API, Stripe, Firebase, AWS)", "Backend Dev", "Critical", 2, "100%", "Completed", "tara_privacyos/core/subprocessor_detector.py"),
    ("CODE-105", "Static Code Analysis", "Generate Tailored UK GDPR Statutory Mandates (Article 6, 9, 28, 32)", "Legal AI Lead", "Critical", 3, "100%", "Completed", "tara_privacyos/legal_engines/uk_gdpr_mandates_gen.py"),
    ("CODE-106", "Static Code Analysis", "Generate Tailored India DPDP Act 2023 Mandates (Section 6, 8, 16)", "Legal AI Lead", "Critical", 2, "100%", "Completed", "tara_privacyos/legal_engines/india_dpdpa_mandates_gen.py"),
    ("CODE-107", "Frontend UI / UX", "Build Repository Scan Results Dashboard with Checklist & Dev Action Items", "Frontend Dev", "High", 3, "100%", "Completed", "RepoScanDashboard.html"),
    ("CODE-108", "QA & Compliance", "Run code scanner against open-source & benchmark backend repos to benchmark accuracy", "QA Lead", "High", 2, "100%", "Completed", "privacyos_audit_report.json")
]
build_spacious_detail_tab(ws_p1, "Track 1: Generate GDPR from Code (Days 1–15)", "'Give us your code, and we will tell you what GDPR requirements you need to follow'", track_1_tasks)

# ==============================================================
# TAB 3: Track 2 — Document Review & Statutory RAG
# ==============================================================
ws_p2 = wb.create_sheet(title="Track 2 — Document Review & RAG")
track_2_tasks = [
    ("DOC-201", "Document AI Review", "Build Multi-Format Document Ingestion Engine & Statutory Legal Corpus", "Backend Dev", "Critical", 3, "100%", "Completed", "tara_privacyos/rag/corpus_data.py"),
    ("DOC-202", "Document AI Review", "Implement Hybrid Semantic Vector & BM25 Legal Retriever", "Legal AI Lead", "Critical", 3, "100%", "Completed", "tara_privacyos/rag/retriever.py"),
    ("DOC-203", "Document AI Review", "Build Master Statutory RAG Pipeline & Azure OpenAI Grounding", "Legal AI Lead", "Critical", 3, "100%", "Completed", "tara_privacyos/rag/rag_engine.py"),
    ("DOC-204", "Document AI Review", "Develop Automated Statutory Clause Re-writer & Model Clause Inserter", "Legal AI Lead", "Critical", 2, "100%", "Completed", "tara_privacyos/rag/rag_engine.py:audit_document"),
    ("DOC-205", "Backend Architecture", "Expose REST RAG API Endpoints (/api/rag/query, /api/rag/search, /api/rag/audit)", "Backend Dev", "Critical", 2, "100%", "Completed", "tara_privacyos/api/server.py"),
    ("DOC-206", "Frontend UI / UX", "Build Interactive Statutory RAG Explorer & Grounding Citation Badges", "Frontend Dev", "High", 3, "100%", "Completed", "Tara-GDPR-AI-Copilot.html"),
    ("DOC-207", "QA & Compliance", "Develop and Execute Phase 2 RAG Comprehensive Test Suite (7/7 Passed)", "QA Lead", "High", 2, "100%", "Completed", "tara_privacyos/tests/test_phase2_rag.py")
]
build_spacious_detail_tab(ws_p2, "Track 2: Review & Correct Existing Docs with RAG (Days 16–30)", "'Give us your existing GDPR docs, and we will find gaps, cite exact statutes, and auto-correct them'", track_2_tasks)


# ==============================================================
# TAB 4: Track 3 — VM Sandbox Monitor
# ==============================================================
ws_p3 = wb.create_sheet(title="Track 3 — VM Sandbox Monitor")
track_3_tasks = [
    ("VM-301", "VM Sandbox Security", "Provision Isolated Ubuntu Sandbox VM with automated container execution", "DevOps Lead", "Critical", 3, "30%", "In Progress", "sandbox_vm_provisioner.sh"),
    ("VM-302", "VM Sandbox Security", "Implement eBPF Kernel Probe to trace openat(), read(), and socket() syscalls", "Security Lead", "Critical", 4, "20%", "Planned", "ebpf_kernel_probe.c"),
    ("VM-303", "VM Sandbox Security", "Build Database Query Anomaly Detector (flags sudden 1,000+ record bulk dumps)", "Backend Dev", "Critical", 3, "25%", "Planned", "db_anomaly_detector.py"),
    ("VM-304", "VM Sandbox Security", "Build Network Egress Guardrail (detects unapproved outbound IP/port connections)", "Security Lead", "Critical", 3, "20%", "Planned", "egress_guardrail.py"),
    ("VM-305", "VM Sandbox Security", "Automate Active Defense Kill-Switch (drops socket & sends SIGSTOP to process)", "Security Lead", "High", 2, "10%", "Planned", "auto_killswitch.sh"),
    ("VM-306", "Frontend UI / UX", "Develop Live Sandbox Telemetry Terminal & Real-Time Alert Toast Feed", "Frontend Dev", "High", 3, "100%", "Completed", "SandboxTerminalView.tsx"),
    ("VM-307", "QA & Compliance", "Simulate 5 real-world data-theft attack vectors to verify 100% interception rate", "QA Lead", "High", 3, "0%", "Planned", "data_theft_pentest_report.pdf")
]
build_spacious_detail_tab(ws_p3, "Track 3: VM Sandbox Runtime Monitor (Days 31–45)", "'Run the app in a controlled VM sandbox to detect suspicious activity & data theft'", track_3_tasks)

# Save Workbook
output_path = r"c:\Users\Rahul\OneDrive\Desktop\LawAi\AI_Accelerator_Project_Execution_Plan.xlsx"
wb.save(output_path)
print("Updated 3-Track Excel Workbook successfully created at:", output_path)
