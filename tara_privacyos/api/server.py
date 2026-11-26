"""
Tara PrivacyOS — FastAPI REST Service
Provides HTTP endpoints for:
1. Code-to-GDPR scans, statutory audit reports, and Article 30 RoPA tables
2. Azure OpenAI GDPR Legal Copilot Chatbot (/api/chat)
3. Live Document Legal Auditing & Auto-Fixing (/api/audit-live)
4. Azure Connection Diagnostics (/api/azure-status)
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any, List

from tara_privacyos.privacyos_engine import PrivacyOSEngine
from tara_privacyos.core.azure_llm import ask_gdpr_copilot, audit_document_with_ai, test_azure_connection
from tara_privacyos.rag.rag_engine import TaraRAGEngine
from tara_privacyos.rag.corpus_data import get_corpus, get_corpus_stats
from tara_privacyos.core.github_extractor import GitHubRepoExtractor, PrivateRepoError
from tara_privacyos.legal_engines.use_based_gdpr_gen import UseBasedGDPRGenerator

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

app = FastAPI(
    title="Tara PrivacyOS & GDPR AI Copilot API",
    description="Statutory Code-to-GDPR, DPDPA Compliance & Azure OpenAI Legal Chatbot Service with Phase 2 RAG Intelligence",
    version="2.0.0"
)

# Enable CORS for dashboard and copilot frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

NO_CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store, must-revalidate, max-age=0",
    "Pragma": "no-cache",
    "Expires": "0"
}

@app.middleware("http")
async def add_no_cache_middleware(request, call_next):
    response = await call_next(request)
    content_type = response.headers.get("content-type", "")
    if "text/html" in content_type or "application/json" in content_type:
        for k, v in NO_CACHE_HEADERS.items():
            response.headers[k] = v
    return response

engine = PrivacyOSEngine()
rag_engine = TaraRAGEngine()
github_extractor = GitHubRepoExtractor()
use_based_gdpr_gen = UseBasedGDPRGenerator()
latest_report: Optional[Dict[str, Any]] = None

class GitHubScanRequest(BaseModel):
    repo_url: str = "https://github.com/tara-infotech/consultation-platform-backend"
    branch: Optional[str] = None
    company_name: Optional[str] = None

class GitHubGenerateGDPRRequest(BaseModel):
    extraction_data: Dict[str, Any]
    company_name: Optional[str] = None

class GitHubExportRequest(BaseModel):
    markdown_content: str
    export_format: str = "markdown" # markdown, html, json
    document_title: Optional[str] = "Statutory_Privacy_Policy"

class ScanRequest(BaseModel):
    target_path_or_url: str = "./tara_privacyos/benchmarks/sample_consultation_app"

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = None

class AuditLiveRequest(BaseModel):
    document_text: str
    doc_type: Optional[str] = "privacy_policy"

class RAGSearchRequest(BaseModel):
    query: str
    jurisdiction: Optional[str] = None
    top_k: Optional[int] = 5

class RAGQueryRequest(BaseModel):
    query: str
    history: Optional[List[Dict[str, str]]] = None
    jurisdiction: Optional[str] = None
    top_k: Optional[int] = 4

class RAGAuditRequest(BaseModel):
    document_text: str
    doc_type: Optional[str] = "privacy_policy"


@app.get("/")
def home():
    login_path = os.path.join(BASE_DIR, "login.html")
    if os.path.exists(login_path):
        return FileResponse(login_path, headers=NO_CACHE_HEADERS)
    copilot_path = os.path.join(BASE_DIR, "Tara-GDPR-AI-Copilot.html")
    if os.path.exists(copilot_path):
        return FileResponse(copilot_path, headers=NO_CACHE_HEADERS)
    return {
        "status": "online",
        "service": "Tara PrivacyOS Phase 1 Engine",
        "supported_regulations": ["UK GDPR (ICO)", "India DPDP Act 2023"]
    }

@app.get("/copilot")
def get_copilot():
    return RedirectResponse(url="/dashboard?phase=chatbot")

@app.get("/login")
def get_login():
    login_path = os.path.join(BASE_DIR, "login.html")
    if os.path.exists(login_path):
        return FileResponse(login_path, headers=NO_CACHE_HEADERS)
    raise HTTPException(status_code=404, detail="Login file not found")

@app.get("/dashboard")
def get_dashboard():
    demo_path = os.path.join(BASE_DIR, "AI-PrivacyOS-Production-Demo.html")
    if os.path.exists(demo_path):
        return FileResponse(demo_path, headers=NO_CACHE_HEADERS)
    raise HTTPException(status_code=404, detail="Demo file not found")

@app.get("/scan-details")
def get_scan_details():
    return RedirectResponse(url="/dashboard?phase=github")

@app.get("/privacyos_audit_report.json")
def get_audit_json():
    rep_path = os.path.join(BASE_DIR, "privacyos_audit_report.json")
    if os.path.exists(rep_path):
        return FileResponse(rep_path)
    raise HTTPException(status_code=404, detail="Audit report not found")

@app.get("/plan")
def get_plan():
    plan_path = os.path.join(BASE_DIR, "AI_Accelerator_Project_Execution_Plan_Viewer.html")
    if os.path.exists(plan_path):
        return FileResponse(plan_path)
    raise HTTPException(status_code=404, detail="Plan viewer file not found")

@app.get("/guardrails")
def get_guardrails():
    guardrails_path = os.path.join(BASE_DIR, "LawAi-Guardrails-Charter.html")
    if os.path.exists(guardrails_path):
        return FileResponse(guardrails_path)
    raise HTTPException(status_code=404, detail="Guardrails charter file not found")

@app.get("/rag-guide")
def get_rag_guide():
    rag_path = os.path.join(BASE_DIR, "How-RAG-Works-In-Tara-LawAi.html")
    if os.path.exists(rag_path):
        return FileResponse(rag_path)
    raise HTTPException(status_code=404, detail="RAG client guide not found")

@app.get("/features-guide")
def get_features_guide():
    guide_path = os.path.join(BASE_DIR, "Tara-PrivacyOS-3-Features-Architecture-Guide.html")
    if os.path.exists(guide_path):
        return FileResponse(guide_path)
    raise HTTPException(status_code=404, detail="Features architecture guide not found")

@app.get("/lawyer-guide")
def get_lawyer_guide():
    lawyer_path = os.path.join(BASE_DIR, "Tara-PrivacyOS-Lawyer-Client-Guide.html")
    if os.path.exists(lawyer_path):
        return FileResponse(lawyer_path)
    raise HTTPException(status_code=404, detail="Lawyer client guide not found")

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "service": "Tara PrivacyOS Legal Engine & Azure Copilot",
        "supported_regulations": ["UK GDPR (ICO)", "India DPDP Act 2023"],
        "azure_model": "gpt-4o-mini"
    }

@app.get("/api/azure-status")
def check_azure():
    return test_azure_connection()

@app.post("/api/chat")
def chat_with_copilot(req: ChatRequest):
    """Answers any GDPR/DPDPA question using Azure OpenAI gpt-4o-mini."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    return ask_gdpr_copilot(req.message, req.history)

@app.post("/api/audit-live")
def audit_live_document(req: AuditLiveRequest):
    """Performs live AI audit and statutory clause rewriting on uploaded/pasted text."""
    if not req.document_text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty")
    result = audit_document_with_ai(req.document_text, req.doc_type or "privacy_policy")
    return result

@app.post("/api/scan")
def run_scan(req: ScanRequest):
    global latest_report
    try:
        report = engine.scan(req.target_path_or_url)
        latest_report = report
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/benchmarks/sample")
def run_benchmark():
    global latest_report
    sample_path = "./tara_privacyos/benchmarks/sample_consultation_app"
    report = engine.scan(sample_path)
    latest_report = report
    return report

@app.get("/api/reports/latest")
def get_latest_report():
    if not latest_report:
        sample_path = "./tara_privacyos/benchmarks/sample_consultation_app"
        return engine.scan(sample_path)
    return latest_report

@app.get("/api/ropa")
def get_ropa():
    rep = get_latest_report()
    return rep["uk_gdpr_compliance_package"]["article_30_ropa"]

@app.get("/api/checklist")
def get_checklist():
    rep = get_latest_report()
    return {
        "uk_gdpr_dev_checklist": rep["uk_gdpr_compliance_package"]["developer_remediation_checklist"],
        "india_dpdpa_dev_checklist": rep["india_dpdpa_compliance_package"]["developer_action_points"]
    }

# ==============================================================
# PHASE 2: STATUTORY RAG LEGAL INTELLIGENCE ENDPOINTS
# ==============================================================

@app.get("/api/rag/stats")
def get_rag_statistics():
    """Returns statutory corpus stats: total chunks, articles, jurisdictions, categories."""
    return rag_engine.get_stats()

@app.get("/api/rag/corpus")
def get_full_corpus():
    """Returns the full statutory legal database for explorer and citation lookups."""
    return get_corpus()

@app.get("/api/rag/citation/{citation_id}")
def get_citation_by_id(citation_id: str):
    """Retrieves full statutory text, requirements, and penalties for a specific citation ID."""
    chunk = rag_engine.retriever.get_chunk_by_id(citation_id)
    if not chunk:
        raise HTTPException(status_code=404, detail=f"Statutory citation '{citation_id}' not found.")
    return chunk

@app.post("/api/rag/search")
def search_statutes(req: RAGSearchRequest):
    """Hybrid semantic vector & lexical keyword search over UK GDPR and India DPDPA statutes."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")
    return rag_engine.search_statutes(
        query=req.query,
        jurisdiction=req.jurisdiction,
        top_k=req.top_k or 5
    )

@app.post("/api/rag/query")
def grounded_rag_query(req: RAGQueryRequest):
    """Executes RAG pipeline: retrieves statutory articles, injects grounded context, queries Azure OpenAI."""
    if not req.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    return rag_engine.query(
        query=req.query,
        history=req.history,
        jurisdiction=req.jurisdiction,
        top_k=req.top_k or 4
    )

@app.post("/api/rag/audit")
def rag_audit_document(req: RAGAuditRequest):
    """RAG-augmented document audit: finds statutory gaps and injects model statutory clauses as redlines."""
    if not req.document_text.strip():
        raise HTTPException(status_code=400, detail="Document text cannot be empty")
    return rag_engine.audit_document(
        document_text=req.document_text,
        doc_type=req.doc_type or "privacy_policy"
    )

# ==============================================================
# PHASE 3: GITHUB REPOSITORY EXTRACTION & USE-BASED GDPR ENGINE
# ==============================================================

@app.get("/api/github/presets")
def get_github_presets():
    """Returns curated repository presets representing diverse industry use cases."""
    return [
        {
            "id": "zenauraa-live",
            "name": "ZenAuraa Consultation App & Backend (Live Public Repo)",
            "repo_url": "https://github.com/rahulnautiyal005/Zenauracl",
            "domain": "Astrology & Spiritual Consultation",
            "description": "Prisma + Node.js backend handling consultation bookings, astrologer profiles, chat messages, and Razorpay/Stripe payments.",
            "tech_stack": ["Node.js", "Prisma ORM", "PostgreSQL", "Stripe", "Razorpay"],
            "statutory_risk": "CRITICAL (UK GDPR Article 9 Special Category Data & DPDPA Mandatory Consent)"
        },
        {
            "id": "medconnect-telehealth",
            "name": "MedConnect Telemedicine & Patient EHR",
            "repo_url": "https://github.com/medconnect-health/ehr-backend-service",
            "domain": "Telehealth & Medical Diagnostics",
            "description": "Express.js + Prisma service managing patient diagnoses, doctor consultations, NHS identifiers, and prescription dispatch.",
            "tech_stack": ["Node.js", "Express", "Prisma ORM", "AWS S3", "SendGrid"],
            "statutory_risk": "CRITICAL (UK GDPR Art 9 Health Data, DPIA Mandated, AES-256 KMS)"
        },
        {
            "id": "payflow-saas",
            "name": "PayFlow Enterprise B2B Billing & Invoicing",
            "repo_url": "https://github.com/payflow-systems/billing-gateway",
            "domain": "FinTech & Payment Services",
            "description": "Python service processing customer tax identifiers (PAN, NI number), Stripe webhooks, and HMRC financial audit trails.",
            "tech_stack": ["Python", "FastAPI", "Stripe SDK", "Razorpay", "PostgreSQL"],
            "statutory_risk": "HIGH (Financial Credentials, RBI Localisation, 6-Year HMRC Retention)"
        },
        {
            "id": "ai-knowledge-agent",
            "name": "CognitoAI SaaS Document Copilot",
            "repo_url": "https://github.com/cognito-ai/rag-enterprise-copilot",
            "domain": "AI Platform & LLM Copilot",
            "description": "Next.js + Python microservices indexing company documents with vector embeddings and third-party LLMs.",
            "tech_stack": ["Next.js", "Pinecone", "Azure OpenAI", "PostHog", "Redis"],
            "statutory_risk": "HIGH (LLM Data Egress, Article 28 DPA, Zero-Retention Agreements)"
        }
    ]

@app.post("/api/github/scan")
def scan_github_repository(req: GitHubScanRequest):
    """
    Clones or analyzes a GitHub repository or codebase, extracts data models,
    PII classifications, API routes, and infers business domain/use case.
    """
    if not req.repo_url.strip():
        raise HTTPException(status_code=400, detail="Repository URL or path cannot be empty")
    try:
        extraction_result = github_extractor.extract_from_repo(req.repo_url, branch=req.branch)
        return extraction_result
    except PrivateRepoError as pre:
        return JSONResponse(
            status_code=403,
            content={
                "status": "ERROR",
                "error_type": "PRIVATE_REPOSITORY",
                "message": str(pre)
            }
        )
    except Exception as e:
        err_str = str(e)
        if any(w in err_str.lower() for w in ["private", "authentication", "not found", "terminal prompts disabled"]):
            return JSONResponse(
                status_code=403,
                content={
                    "status": "ERROR",
                    "error_type": "PRIVATE_REPOSITORY",
                    "message": f"Repository '{req.repo_url}' is Private or inaccessible. Tara PrivacyOS requires the repository to be Public on GitHub to scan data models and routes."
                }
            )
        raise HTTPException(status_code=500, detail=f"Failed to extract from repository: {err_str}")

@app.post("/api/github/generate-gdpr")
def generate_use_based_gdpr(req: GitHubGenerateGDPRRequest):
    """
    Generates tailored statutory Privacy Policy, RoPA table, DPIA assessment,
    and developer remediation code patches based on extracted GitHub data.
    """
    if not req.extraction_data:
        raise HTTPException(status_code=400, detail="Extraction data is required")
    try:
        compliance_package = use_based_gdpr_gen.generate_full_package(
            extraction_data=req.extraction_data,
            company_name=req.company_name
        )
        return compliance_package
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate GDPR package: {str(e)}")

@app.post("/api/github/extract-and-generate")
def extract_and_generate_gdpr(req: GitHubScanRequest):
    """
    Single all-in-one pipeline:
    1. Extracts AST, data models, routes, dependencies & infers use case from GitHub repo.
    2. Dynamically generates statutory Use-Based GDPR package.
    """
    if not req.repo_url.strip():
        raise HTTPException(status_code=400, detail="Repository URL cannot be empty")
    try:
        # Step 1: Extract from repo
        extraction_data = github_extractor.extract_from_repo(req.repo_url, branch=req.branch)
        
        # Step 2: Generate use-based compliance package
        compliance_package = use_based_gdpr_gen.generate_full_package(
            extraction_data=extraction_data,
            company_name=req.company_name
        )

        return {
            "status": "SUCCESS",
            "extraction": extraction_data,
            "compliance_package": compliance_package
        }
    except PrivateRepoError as pre:
        return JSONResponse(
            status_code=403,
            content={
                "status": "ERROR",
                "error_type": "PRIVATE_REPOSITORY",
                "message": str(pre)
            }
        )
    except Exception as e:
        err_str = str(e)
        if any(w in err_str.lower() for w in ["private", "authentication", "not found", "terminal prompts disabled"]):
            return JSONResponse(
                status_code=403,
                content={
                    "status": "ERROR",
                    "error_type": "PRIVATE_REPOSITORY",
                    "message": f"Repository '{req.repo_url}' is Private or inaccessible. Tara PrivacyOS requires the repository to be Public on GitHub to scan data models and routes."
                }
            )
        raise HTTPException(status_code=500, detail=f"Pipeline error: {err_str}")

@app.post("/api/github/export")
def export_gdpr_document(req: GitHubExportRequest):
    """Exports generated GDPR document as Markdown or standalone HTML."""
    content = req.markdown_content
    fmt = req.export_format.lower()

    if fmt == "html":
        # Wrap markdown in clean, publication-ready CSS HTML document
        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{req.document_title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.7;
            color: #1E293B;
            background: #F8FAFC;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 880px;
            margin: 0 auto;
            background: #FFFFFF;
            padding: 50px 60px;
            border-radius: 12px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.06);
            border: 1px solid #E2E8F0;
        }}
        h1 {{ font-size: 26px; color: #0F172A; border-bottom: 2px solid #3B82F6; padding-bottom: 12px; }}
        h2 {{ font-size: 20px; color: #1E293B; margin-top: 32px; border-bottom: 1px solid #E2E8F0; padding-bottom: 8px; }}
        h3 {{ font-size: 16px; color: #334155; margin-top: 24px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
        th, td {{ padding: 10px 14px; border: 1px solid #CBD5E1; text-align: left; }}
        th {{ background: #F1F5F9; color: #0F172A; font-weight: 600; }}
        tr:nth-child(even) {{ background: #F8FAFC; }}
        code {{ background: #F1F5F9; padding: 2px 6px; border-radius: 4px; font-size: 13px; color: #2563EB; }}
        pre {{ background: #0F172A; color: #F8FAFC; padding: 16px; border-radius: 8px; overflow-x: auto; }}
        hr {{ border: none; border-top: 1px solid #E2E8F0; margin: 30px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <pre style="background:transparent; color:#1E293B; font-family:inherit; white-space:pre-wrap;">{content}</pre>
    </div>
</body>
</html>"""
        return HTMLResponse(content=html_doc, headers={"Content-Disposition": f"attachment; filename={req.document_title}.html"})

    return HTMLResponse(content=content, media_type="text/markdown", headers={"Content-Disposition": f"attachment; filename={req.document_title}.md"})

# ==============================================================
# PHASE 4: AI & LLM GOVERNANCE COPILOT ENDPOINTS
# ==============================================================

from tara_privacyos.legal_engines.ai_governance_engine import AIGovernanceEngine
from tara_privacyos.legal_engines.data_flow_engine import DataFlowEngine

ai_gov_engine = AIGovernanceEngine()
data_flow_engine = DataFlowEngine()

class AIAuditRequest(BaseModel):
    selected_tools: List[str]
    selected_data_types: List[str]
    company_name: Optional[str] = "Tara Infotech Ltd"

class AIDocGenRequest(BaseModel):
    audit_result: Dict[str, Any]
    company_name: Optional[str] = "Tara Infotech Ltd"

class TopologyRequest(BaseModel):
    preset_id: str

class IDTARequest(BaseModel):
    company_name: Optional[str] = "Tara Infotech Ltd"
    overseas_entity: Optional[str] = "Tara Infotech India Pvt Ltd"

@app.get("/api/ai-governance/tools-catalog")
def get_ai_tools_catalog():
    return ai_gov_engine.get_catalog()

@app.post("/api/ai-governance/audit")
def audit_ai_governance(req: AIAuditRequest):
    return ai_gov_engine.audit_ai_footprint(
        selected_tool_ids=req.selected_tools,
        selected_data_ids=req.selected_data_types,
        company_name=req.company_name or "Tara Infotech Ltd"
    )

@app.post("/api/ai-governance/generate-dpia")
def generate_ai_dpia_endpoint(req: AIDocGenRequest):
    content = ai_gov_engine.generate_ai_dpia(req.audit_result)
    return {"content": content, "format": "markdown"}

@app.post("/api/ai-governance/generate-aup")
def generate_ai_aup_endpoint(req: AIDocGenRequest):
    content = ai_gov_engine.generate_employee_aup(req.audit_result)
    return {"content": content, "format": "markdown"}

# ==============================================================
# PHASE 5: DATA FLOW & CROSS-BORDER TRANSFER ENDPOINTS
# ==============================================================

@app.get("/api/data-flow/presets")
def get_data_flow_presets():
    return data_flow_engine.get_presets_list()

@app.post("/api/data-flow/topology")
def get_data_flow_topology(req: TopologyRequest):
    return data_flow_engine.get_topology(req.preset_id)

@app.post("/api/data-flow/generate-idta")
def generate_idta_endpoint(req: IDTARequest):
    content = data_flow_engine.generate_idta_schedule(
        company_name=req.company_name or "Tara Infotech Ltd",
        overseas_entity=req.overseas_entity or "Tara Infotech India Pvt Ltd"
    )
    return {"content": content, "format": "markdown"}
