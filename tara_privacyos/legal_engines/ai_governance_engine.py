"""
Tara PrivacyOS — AI & LLM Governance Engine
Statutory Risk Assessment, AI DPIA Generator, and Employee AI Acceptable Use Policy Engine
Complies with UK GDPR (ICO Guidance on AI and Data Protection) & India DPDP Act 2023.
"""

from typing import Dict, List, Any
from datetime import datetime

AI_TOOLS_CATALOG = {
    "chatgpt_consumer": {
        "id": "chatgpt_consumer",
        "name": "ChatGPT (Free / Plus Consumer)",
        "vendor": "OpenAI LLC",
        "category": "GenAI Web App",
        "jurisdiction": "United States (California)",
        "model_training_default": True,
        "zero_retention_supported": False,
        "dpa_available": False,
        "risk_tier": "HIGH",
        "icon": "🤖",
        "description": "Consumer web interface. Default terms permit OpenAI to use user conversations for model training unless opted out. Servers located in the US."
    },
    "openai_api": {
        "id": "openai_api",
        "name": "OpenAI API (Direct Developer Tier)",
        "vendor": "OpenAI LLC",
        "category": "API / SDK",
        "jurisdiction": "United States",
        "model_training_default": False,
        "zero_retention_supported": True,
        "dpa_available": True,
        "risk_tier": "MEDIUM",
        "icon": "⚡",
        "description": "API data is not used for model training by default. 30-day prompt retention applies unless Zero Data Retention (ZDR) is explicitly approved."
    },
    "azure_openai": {
        "id": "azure_openai",
        "name": "Azure OpenAI Service (Enterprise)",
        "vendor": "Microsoft Corporation",
        "category": "Cloud Enterprise AI",
        "jurisdiction": "UK / EU Data Boundary (e.g. UK South)",
        "model_training_default": False,
        "zero_retention_supported": True,
        "dpa_available": True,
        "risk_tier": "LOW",
        "icon": "🛡️",
        "description": "Governed by Microsoft Enterprise DPA. Data resides within chosen region (e.g. London). Zero prompt training. HIPAA and ISO 27001 certified."
    },
    "claude_anthropic": {
        "id": "claude_anthropic",
        "name": "Claude (Anthropic Web / Free)",
        "vendor": "Anthropic PBC",
        "category": "GenAI Web App",
        "jurisdiction": "United States",
        "model_training_default": False,
        "zero_retention_supported": False,
        "dpa_available": False,
        "risk_tier": "MEDIUM",
        "icon": "🧠",
        "description": "Commercial terms do not train on user data, but consumer web interface retains prompt history for up to 90 days for safety moderation."
    },
    "ms_copilot": {
        "id": "ms_copilot",
        "name": "Microsoft 365 Copilot (Enterprise)",
        "vendor": "Microsoft Corporation",
        "category": "Workplace AI",
        "jurisdiction": "Enterprise Tenant Boundary",
        "model_training_default": False,
        "zero_retention_supported": True,
        "dpa_available": True,
        "risk_tier": "LOW",
        "icon": "💼",
        "description": "Inherits existing M365 security, compliance, and privacy policies. User data does not leak into public LLM weights."
    },
    "google_gemini": {
        "id": "google_gemini",
        "name": "Google Gemini (Consumer Web)",
        "vendor": "Google LLC",
        "category": "GenAI Web App",
        "jurisdiction": "United States",
        "model_training_default": True,
        "zero_retention_supported": False,
        "dpa_available": False,
        "risk_tier": "HIGH",
        "icon": "🌐",
        "description": "Human reviewers may read, annotate, and process conversations for model improvement. Extreme risk if customer PII is entered."
    },
    "cursor_copilot": {
        "id": "cursor_copilot",
        "name": "Cursor / GitHub Copilot (Code Assistant)",
        "vendor": "Anysphere / GitHub (Microsoft)",
        "category": "Developer Tool",
        "jurisdiction": "United States",
        "model_training_default": False,
        "zero_retention_supported": True,
        "dpa_available": True,
        "risk_tier": "MEDIUM",
        "icon": "💻",
        "description": "Source code and embedded hardcoded API keys/passwords can be indexed or transmitted to remote inference clusters unless privacy mode is forced."
    },
    "midjourney_canva": {
        "id": "midjourney_canva",
        "name": "Midjourney & Canva AI (Design / Media)",
        "vendor": "Various",
        "category": "Generative Media",
        "jurisdiction": "United States",
        "model_training_default": True,
        "zero_retention_supported": False,
        "dpa_available": False,
        "risk_tier": "MEDIUM",
        "icon": "🎨",
        "description": "Marketing prompts and uploaded customer portrait images are publicly indexed on community channels by default."
    }
}

DATA_TYPES_CATALOG = {
    "customer_pii": {
        "id": "customer_pii",
        "name": "Customer Names & Contact Details",
        "gdpr_category": "Standard Personal Data (Article 6)",
        "sensitivity": "MEDIUM",
        "icon": "👤"
    },
    "consultation_health": {
        "id": "consultation_health",
        "name": "Consultation Transcripts & Health / Beliefs",
        "gdpr_category": "Special Category Data (Article 9)",
        "sensitivity": "CRITICAL",
        "icon": "🧬"
    },
    "financial_data": {
        "id": "financial_data",
        "name": "Financial Transactions & Bank / Card Details",
        "gdpr_category": "High Risk Confidential Data",
        "sensitivity": "CRITICAL",
        "icon": "💳"
    },
    "source_code": {
        "id": "source_code",
        "name": "Proprietary Source Code & DB Schemas",
        "gdpr_category": "Corporate IP & Security Asset",
        "sensitivity": "HIGH",
        "icon": "💻"
    },
    "employee_cvs": {
        "id": "employee_cvs",
        "name": "Employee CVs, Resumes & HR Records",
        "gdpr_category": "Employee Personal Data (Article 6/88)",
        "sensitivity": "HIGH",
        "icon": "📄"
    },
    "api_secrets": {
        "id": "api_secrets",
        "name": "API Keys, Credentials & Passwords",
        "gdpr_category": "Security Safeguard (Article 32 Violation)",
        "sensitivity": "CRITICAL",
        "icon": "🔑"
    }
}

class AIGovernanceEngine:
    def __init__(self):
        self.tools = AI_TOOLS_CATALOG
        self.data_types = DATA_TYPES_CATALOG

    def get_catalog(self) -> Dict[str, Any]:
        return {
            "tools": list(self.tools.values()),
            "data_types": list(self.data_types.values())
        }

    def audit_ai_footprint(self, selected_tool_ids: List[str], selected_data_ids: List[str], company_name: str = "Tara Infotech Ltd") -> Dict[str, Any]:
        """Calculates statutory risk score, identifies red flags, and constructs risk matrix."""
        tools = [self.tools[t] for t in selected_tool_ids if t in self.tools]
        data_types = [self.data_types[d] for d in selected_data_ids if d in self.data_types]

        if not tools:
            # Default to chatgpt consumer if none selected
            tools = [self.tools["chatgpt_consumer"]]
        if not data_types:
            data_types = [self.data_types["customer_pii"]]

        risk_score = 100
        red_flags = []
        high_risk_flows = []

        has_special_category = any(d["id"] in ["consultation_health", "financial_data", "api_secrets"] for d in data_types)
        has_consumer_ai = any(t["model_training_default"] for t in tools)
        has_cross_border_ai = any("United States" in t["jurisdiction"] for t in tools)

        # Check: Special category in consumer AI
        if has_special_category and has_consumer_ai:
            risk_score -= 40
            red_flags.append({
                "severity": "CRITICAL",
                "title": "Article 9 Breach: Special Category / Health Data in Model-Training AI",
                "statute": "UK GDPR Article 9 & Section 4 India DPDP Act 2023",
                "risk": "Employees uploading sensitive consultation notes or financial records into consumer AI models where conversations are harvested for public model retraining.",
                "remediation": "Immediately enforce zero-retention enterprise tier (e.g. Azure OpenAI) and disable consumer ChatGPT/Gemini for sensitive workflows.",
                "fine_exposure": "Up to £17,500,000 (ICO) or ₹250 Crore (DPDP Board of India)"
            })

        # Check: Unrestricted cross-border transfer to US AI clusters
        if has_cross_border_ai:
            risk_score -= 20
            red_flags.append({
                "severity": "HIGH",
                "title": "Unapproved International LLM Data Egress",
                "statute": "UK GDPR Chapter V (Articles 44–49) & ICO International Transfer Addendum",
                "risk": "Prompts containing UK/India citizen data egress to US inference clusters without International Data Transfer Agreement (IDTA) or SCCs.",
                "remediation": "Execute standard contractual addendum with AI vendors and enable UK-local Azure deployment.",
                "fine_exposure": "Up to £8,700,000 under ICO Enforcement Powers"
            })

        # Check: Missing mandatory DPIA
        if len(tools) >= 2 or has_special_category:
            risk_score -= 15
            red_flags.append({
                "severity": "HIGH",
                "title": "Mandatory Article 35 AI DPIA Missing",
                "statute": "UK GDPR Article 35(3) & ICO Guidance on Generative AI",
                "risk": "Conducting systematic processing using novel artificial intelligence without a prior documented Data Protection Impact Assessment.",
                "remediation": "Publish and register formal AI DPIA with company Data Protection Officer (DPO).",
                "fine_exposure": "Regulatory reprimand + operational audit mandate"
            })

        # Check: API secrets in AI prompts
        if any(d["id"] == "api_secrets" for d in data_types):
            risk_score -= 20
            red_flags.append({
                "severity": "CRITICAL",
                "title": "Security Inadequacy: System Credentials Exposed to Third-Party AI",
                "statute": "UK GDPR Article 32 & India DPDPA Section 8(5)",
                "risk": "Developers pasting database connection strings, JWT keys, or client secrets into LLM prompts creates direct exposure.",
                "remediation": "Deploy pre-commit git secret scanners and enforce strict prompt sanitization filter.",
                "fine_exposure": "Immediate security breach notification mandatory within 72 hours"
            })

        # Build risk matrix table
        matrix = []
        for t in tools:
            for d in data_types:
                is_high_risk = t["model_training_default"] or (d["sensitivity"] == "CRITICAL" and not t["zero_retention_supported"])
                status = "CRITICAL" if is_high_risk else ("WARNING" if d["sensitivity"] in ["HIGH", "MEDIUM"] and t["risk_tier"] != "LOW" else "COMPLIANT")
                matrix.append({
                    "tool_name": t["name"],
                    "data_name": d["name"],
                    "status": status,
                    "model_training": "YES (High Risk)" if t["model_training_default"] else "NO (Enterprise Protected)",
                    "action_required": "Block / Restrict" if is_high_risk else "Permit with Guidelines"
                })

        risk_score = max(15, min(100, risk_score))
        if risk_score >= 80:
            health_grade = "Grade A (Low Risk)"
        elif risk_score >= 60:
            health_grade = "Grade B (Moderate Risk)"
        elif risk_score >= 40:
            health_grade = "Grade C (High Exposure)"
        else:
            health_grade = "Grade D (Severe Breach Risk)"

        return {
            "company_name": company_name,
            "audit_timestamp": datetime.now().isoformat(),
            "overall_score": risk_score,
            "health_grade": health_grade,
            "tools_audited_count": len(tools),
            "data_types_audited_count": len(data_types),
            "red_flags": red_flags,
            "risk_matrix": matrix,
            "tools_summary": tools,
            "data_summary": data_types
        }

    def generate_ai_dpia(self, audit_result: Dict[str, Any]) -> str:
        """Generates statutory AI Data Protection Impact Assessment (UK GDPR Article 35)."""
        co = audit_result.get("company_name", "Tara Infotech Ltd")
        tools = ", ".join([t["name"] for t in audit_result.get("tools_summary", [])])
        data_types = ", ".join([d["name"] for d in audit_result.get("data_summary", [])])
        score = audit_result.get("overall_score", 65)
        grade = audit_result.get("health_grade", "C")
        now_str = datetime.now().strftime("%B %d, %Y")

        md = f"""# STATUTORY DATA PROTECTION IMPACT ASSESSMENT (DPIA)
## SYSTEMATIC PROCESSING OF PERSONAL DATA VIA GENERATIVE ARTIFICIAL INTELLIGENCE
**Governing Statute:** UK GDPR (Article 35), Data Protection Act 2018 & India DPDP Act 2023  
**Organization:** {co}  
**DPIA Assessment Reference:** DPIA-AI-{datetime.now().strftime('%Y%m%d')}-001  
**Assessment Date:** {now_str}  
**Compliance Rating:** {score}/100 (Grade: {grade})

---

### 1. Systematic Description of AI Processing
* **Deploying Entity:** {co}
* **Artificial Intelligence Technologies Evaluated:** {tools}
* **Categories of Ingested Data:** {data_types}
* **Operational Purpose:** Enhancement of software development, automated consultation record summarization, internal research, and customer communication workflows.
* **Model Inference Infrastructure:** Hybrid (Local/Cloud APIs & Consumer LLM Interfaces).

---

### 2. Assessment of Necessity & Proportionality (Article 35(7)(b))
1. **Lawful Basis:** Contractual Necessity (Article 6(1)(b)) for user-directed queries; Explicit Consent (Article 9(2)(a)) for special category consultation and health inferences.
2. **Data Minimization:** Prompts submitted to AI systems must be scrubbed of non-essential identifiers (names, national identity numbers, payment card tokens).
3. **Model Training Isolation:** Personal and business consultation data MUST NOT be incorporated into public foundation model parameter weights.

---

### 3. Statutory Risk Assessment & Severity Matrix

| Risk Factor | Statutory Article | Inherent Risk | Mitigated Risk | Mandatory Remediation Control |
| :--- | :--- | :---: | :---: | :--- |
| **Model Weight Poisoning / Leakage** | UK GDPR Art 5(1)(f) | 🔴 CRITICAL | 🟢 LOW | Disable consumer ChatGPT/Gemini; enforce Azure OpenAI / Enterprise Zero-Retention agreement. |
| **Special Category Article 9 Processing** | UK GDPR Art 9 & DPDPA Sec 4 | 🔴 CRITICAL | 🟡 MEDIUM | Implement client-side PII pseudonymization prior to inference dispatch. |
| **International Prompt Egress (UK to US)** | UK GDPR Chapter V (Art 44) | 🟡 HIGH | 🟢 LOW | Execute UK International Data Transfer Addendum (IDTA) with AI cloud providers. |
| **Hallucination & Inaccurate Legal/Health Advice** | UK GDPR Art 5(1)(d) (Accuracy) | 🟡 HIGH | 🟢 LOW | Human-in-the-loop review mandatory; automated output disclaimers enforced. |

---

### 4. Mandatory Statutory Action Plan for {co}
1. **Tool Sanctioning:** Immediately restrict unsanctioned consumer AI models on corporate networks.
2. **Zero-Retention API Contracts:** Migrate high-volume summarization workloads to Azure OpenAI with certified Zero Data Retention (ZDR).
3. **Employee Governance:** Promulgate the *Tara Employee AI Acceptable Use Policy* requiring staff sign-off within 14 calendar days.

---
**Approved by Data Protection Officer (DPO):** Certified Compliance Verification  
**Next Statutory Review Date:** {datetime.now().replace(year=datetime.now().year + 1).strftime('%B %d, %Y')}
"""
        return md

    def generate_employee_aup(self, audit_result: Dict[str, Any]) -> str:
        """Generates ready-to-sign Employee AI Acceptable Use Policy (AUP)."""
        co = audit_result.get("company_name", "Tara Infotech Ltd")
        now_str = datetime.now().strftime("%B %d, %Y")

        md = f"""# {co.upper()} — EMPLOYEE ARTIFICIAL INTELLIGENCE ACCEPTABLE USE POLICY (AUP)
**Version:** 2.0 (Statutory Compliance Update)  
**Effective Date:** {now_str}  
**Applies to:** All Employees, Contractors, Advisors, and Remote Practitioners

---

### 1. Purpose & Scope
This policy establishes mandatory operational rules for using Artificial Intelligence tools (including ChatGPT, Claude, Microsoft Copilot, Cursor, and internal LLMs) in connection with {co}'s business activities. Failure to comply exposes the company to statutory penalties up to £17.5M under the UK Data Protection Act 2018 and ₹250 Cr under the India DPDP Act 2023.

---

### 2. The 3 Golden Rules of Workplace AI

```
[ RULE 1: NO SPECIAL CATEGORY DATA ] ──► Never input customer consultation notes, health data, or religious beliefs into public AI.
[ RULE 2: NO SECRETS OR PASSWORDS   ] ──► Never paste API keys, AWS credentials, JWT tokens, or proprietary source algorithms.
[ RULE 3: VERIFY BEFORE PUBLISHING  ] ──► AI outputs can hallucinate. You remain 100% accountable for work delivered to clients.
```

---

### 3. Sanctioned vs. Prohibited AI Tools

* **🟢 Approved for Business Use:**
  * Company-provided **Azure OpenAI Enterprise** (Zero-Retention Enabled).
  * **Microsoft 365 Copilot** under company enterprise license.
  * **GitHub Copilot / Cursor** with telemetry collection strictly disabled.
* **🔴 Strictly Prohibited with Company Data:**
  * Personal, free, or unmanaged consumer ChatGPT, Google Gemini, or Claude accounts.
  * Public AI summarizers or third-party WhatsApp AI bots.

---

### 4. Permitted & Prohibited Data Ingestion

| Data Category | Permitted in Sanctioned AI? | Conditions / Requirements |
| :--- | :---: | :--- |
| **Marketing copy, general email drafts** | ✅ YES | Review for factual accuracy before sending. |
| **Public documentation & coding syntax** | ✅ YES | Permitted without restrictions. |
| **Customer Names, Emails & Phone Numbers** | ⚠️ CONDITIONAL | Must use pseudonymized / placeholder tokens (e.g. `User_A`). |
| **Consultation Transcripts & Wellness Records** | ❌ STRICTLY NO | Violates UK GDPR Article 9. Requires explicit DPO authorization. |
| **Passwords, DB Connections & API Keys** | ❌ STRICTLY NO | Immediate disciplinary action and incident report. |

---

### 5. Employee Acknowledgment & Undertaking
*I confirm that I have read, understood, and agree to abide by {co}'s Employee AI Acceptable Use Policy. I understand that non-compliance may result in disciplinary action up to termination of employment and personal regulatory referral.*

**Employee Signature:** ___________________________  
**Employee Name:** ______________________________  
**Date:** _______________________________________
"""
        return md

