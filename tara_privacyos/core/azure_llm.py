"""
Tara PrivacyOS — Azure OpenAI Legal Intelligence Engine
Integrates Azure OpenAI (gpt-4o-mini) for:
1. Conversational GDPR Legal Copilot (Q&A on UK GDPR & India DPDPA 2023)
2. Live Document Legal Auditing & Statutory Auto-Fixing
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional
import requests

logger = logging.getLogger("tara_azure_llm")

# Default Azure credentials from verified deployment
AZURE_OPENAI_URL = os.getenv(
    "AZURE_OPENAI_ENDPOINT",
    "https://tara-infotech-storytellingupdated.services.ai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview"
)
AZURE_OPENAI_KEY = os.getenv(
    "AZURE_OPENAI_API_KEY",
    "2XAHv2WTF9zEHk3m6tYluhq5CJoozyRf5UjIW6LlzTZTnzR5NX0JJQQJ99CAACmepeSXJ3w3AAABACOGlJgL"
)
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")

GDPR_SYSTEM_PROMPT = """You are Tara AI — Lead Data Protection Officer (DPO) and Statutory Privacy Legal Architect.
You specialize in:
1. UK GDPR & Data Protection Act 2018 (Information Commissioner's Office - ICO statutory codes).
2. India Digital Personal Data Protection Act 2023 (DPDP Act 2023 & statutory guidelines).
3. AI & LLM Data Governance (OpenAI/Azure AI data-flow compliance, zero-retention policies, DPIA).
4. Cross-Border Data Transfers (UK-to-India IDTA, Standard Contractual Clauses SCCs).
5. Data Subject Rights (DSAR Article 15-22, Article 17 Right to Erasure, Article 20 Portability).

Your advice is:
- Highly authoritative, precise, and practical for engineering and legal teams.
- Cites specific Articles (e.g. UK GDPR Art 6 lawful basis, Art 9 special category, Art 28 processor obligations, Art 30 RoPA, Art 35 DPIA) and Sections (e.g. India DPDPA Sec 6 consent, Sec 8 data fiduciary obligations).
- Structured with clear headings, bullet points, and code/contract clause snippets when helpful.
- Pragmatic for tech startups, SMEs, and consulting platforms.
"""

_rag_engine_instance = None

def _get_rag_engine():
    global _rag_engine_instance
    if _rag_engine_instance is None:
        try:
            from tara_privacyos.rag.rag_engine import TaraRAGEngine
            _rag_engine_instance = TaraRAGEngine()
        except Exception as e:
            logger.error(f"Failed to initialize RAG engine: {e}")
            _rag_engine_instance = None
    return _rag_engine_instance

def ask_gdpr_copilot(query: str, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    """Answers any GDPR, DPDPA, or privacy engineering query using Grounded RAG + Azure OpenAI."""
    rag_eng = _get_rag_engine()
    if rag_eng:
        try:
            return rag_eng.query(query, history=history)
        except Exception as e:
            logger.error(f"RAG execution failed, falling back to direct prompt: {e}")

    # Fallback to direct prompt if RAG pipeline raises an unexpected exception
    messages = [{"role": "system", "content": GDPR_SYSTEM_PROMPT}]

    if history:
        for msg in history[-8:]:  # Keep recent context window
            if msg.get("role") in ("user", "assistant") and msg.get("content"):
                messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": query})

    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 1200
    }

    try:
        response = requests.post(AZURE_OPENAI_URL, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            res_json = response.json()
            reply = res_json["choices"][0]["message"]["content"]
            return {
                "success": True,
                "answer": reply,
                "model": "Tara Legal AI Core v2.4",
                "provider": "Tara Proprietary Legal Intelligence Engine",
                "rag_grounded": False
            }
        else:
            logger.error(f"Azure OpenAI Error {response.status_code}: {response.text}")
            return _generate_fallback_answer(query, error_msg=f"Azure HTTP {response.status_code}")
    except Exception as e:
        logger.error(f"Azure OpenAI Connection Error: {e}")
        return _generate_fallback_answer(query, error_msg=str(e))

def audit_document_with_ai(document_text: str, doc_type: str = "privacy_policy") -> Dict[str, Any]:
    """Audits arbitrary draft document text using Azure OpenAI and returns structured compliance fixes."""
    audit_system_prompt = f"""You are the Tara PrivacyOS Statutory Legal Audit Engine.
Analyze the following user-supplied {doc_type} text against UK GDPR (ICO rules) and India DPDP Act 2023.

Return ONLY a valid JSON object matching this exact schema:
{{
  "stats": {{
    "score": <integer 0-100>,
    "critical": <integer count>,
    "warnings": <integer count>,
    "fixes": <integer count>
  }},
  "issues": [
    {{
      "severity": "critical" | "warning",
      "title": "<Concise issue title>",
      "law": "<Statutory citation, e.g. UK GDPR Article 6, Article 9, or India DPDP Act 2023 Section 6/8/12/13>",
      "description": "<Detailed explanation of the compliance flaw>",
      "fixed_text": "<Exact statutory remediation applied>"
    }}
  ],
  "fixed_document_html": "<Complete, professional HTML markup of the rewritten compliant document with <div class='clause-added'><span class='clause-label'>ADDED COMPLIANT CLAUSE:</span>...</div> highlighting where statutory clauses were injected>"
}}
"""

    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {"role": "system", "content": audit_system_prompt},
            {"role": "user", "content": f"AUDIT THIS DRAFT DOCUMENT ({doc_type}):\n\n{document_text[:6000]}"}
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0.2,
        "max_tokens": 2500
    }

    try:
        response = requests.post(AZURE_OPENAI_URL, headers=headers, json=payload, timeout=30)
        if response.status_code == 200:
            res_json = response.json()
            content = res_json["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            for iss in parsed.get("issues", []):
                if "fixed_text" not in iss and "fix" in iss:
                    iss["fixed_text"] = iss["fix"]
                if "fix" not in iss and "fixed_text" in iss:
                    iss["fix"] = iss["fixed_text"]
            parsed["success"] = True
            parsed["engine"] = "Tara PrivacyOS Legal Engine v2.4"
            return parsed
        else:
            logger.error(f"Azure Audit HTTP {response.status_code}: {response.text}")
            return {"success": False, "error": f"Azure returned {response.status_code}"}
    except Exception as e:
        logger.error(f"Azure Audit Exception: {e}")
        return {"success": False, "error": str(e)}

def test_azure_connection() -> Dict[str, Any]:
    """Tests live connectivity to Azure OpenAI."""
    headers = {
        "api-key": AZURE_OPENAI_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "messages": [{"role": "user", "content": "ping"}],
        "max_tokens": 5
    }
    try:
        r = requests.post(AZURE_OPENAI_URL, headers=headers, json=payload, timeout=6)
        return {
            "online": r.status_code == 200,
            "status_code": r.status_code,
            "deployment": AZURE_DEPLOYMENT,
            "endpoint": AZURE_OPENAI_URL.split("?")[0]
        }
    except Exception as e:
        return {
            "online": False,
            "error": str(e),
            "deployment": AZURE_DEPLOYMENT
        }

def _generate_fallback_answer(query: str, error_msg: str) -> Dict[str, Any]:
    """Local legal knowledge fallback if external API is unreachable."""
    q = query.lower()
    if "article 9" in q or "special category" in q or "health" in q:
        ans = (
            "### UK GDPR Article 9: Special Category Data Compliance\n\n"
            "Under **UK GDPR Article 9(1)**, processing special category data (health data, biometrics, religious or philosophical beliefs) "
            "is strictly prohibited unless you have both a **lawful basis under Article 6** AND a **specific condition under Article 9(2)**.\n\n"
            "**Key Requirements for Organizations:**\n"
            "1. **Explicit Consent (Art. 9(2)(a)):** Must be an affirmative opt-in separate from standard Terms of Service.\n"
            "2. **Granular Notice:** State clearly what special category data is collected and why.\n"
            "3. **Zero-Retention for AI:** Prompts sent to third-party LLM APIs must have zero-data retention clauses with sub-processors."
        )
    elif "retention" in q or "delete" in q or "erasure" in q:
        ans = (
            "### Data Retention & Right to Erasure (Article 17)\n\n"
            "Under **ICO Statutory Guidance**:\n"
            "- Stating *'We keep data as long as necessary'* is **unlawful** under Article 5(1)(e).\n"
            "- You must specify definitive timeframes (e.g., *Application logs: 90 days; Invoices & financial transactions: 6 years for HMRC*).\n"
            "- You must offer an automated or documented DSAR erasure endpoint (`/api/v1/user/dsar-delete`)."
        )
    elif "india" in q or "dpdp" in q or "cross border" in q or "transfer" in q:
        ans = (
            "### UK-to-India Cross-Border Data Transfers\n\n"
            "Under **UK GDPR Chapter V (Articles 44-49)** and **India DPDP Act 2023 (Section 16)**:\n"
            "1. India does not currently possess an ICO adequacy regulation.\n"
            "2. Any UK customer data accessed by India tech/QA teams requires an **International Data Transfer Agreement (IDTA)** or UK Addendum to EU SCCs.\n"
            "3. Article 28 Data Processing Agreement must bind overseas sub-processors to technical security safeguards."
        )
    else:
        ans = (
            f"### Statutory Privacy & Data Protection Guidance\n\n"
            f"Under UK GDPR (ICO guidelines) and India DPDP Act 2023, data processing must strictly adhere to Purpose Limitation, "
            f"Data Minimization (Art 5(1)(c)), and Lawful Consent (Art 6 / Sec 6).\n\n"
            f"*Note: Operating in local legal knowledge cache mode.*"
        )

    return {
        "success": True,
        "answer": ans,
        "model": "Tara Legal Engine (Local Cache Fallback)",
        "provider": "Tara In-House Legal Rulebook"
    }
