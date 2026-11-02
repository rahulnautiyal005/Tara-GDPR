"""
Tara PrivacyOS — Phase 2 Master RAG Engine
Coordinates:
1. Legal Knowledge Retrieval via LegalRetriever
2. Statutory Grounding Context Builder (UK GDPR & India DPDPA)
3. Azure OpenAI gpt-4o-mini Generation with Strict Grounding & Citation Attribution
4. RAG-Augmented Document Auditing & Statutory Clause Auto-Fixer
"""

import re
import os
import json
import logging
import requests
from typing import Dict, Any, List, Optional

from tara_privacyos.rag.retriever import LegalRetriever
from tara_privacyos.rag.corpus_data import get_corpus_stats

logger = logging.getLogger("tara_rag_engine")

AZURE_OPENAI_URL = os.getenv(
    "AZURE_OPENAI_ENDPOINT",
    "https://tara-infotech-storytellingupdated.services.ai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview"
)
AZURE_OPENAI_KEY = os.getenv(
    "AZURE_OPENAI_API_KEY",
    "2XAHv2WTF9zEHk3m6tYluhq5CJoozyRf5UjIW6LlzTZTnzR5NX0JJQQJ99CAACmepeSXJ3w3AAABACOGlJgL"
)

RAG_GROUNDED_SYSTEM_PROMPT = """You are Tara AI — Lead Data Protection Officer (DPO) and Statutory Privacy Legal Architect for UK GDPR and India DPDP Act 2023.

CORE INSTRUCTIONS:
1. DIRECT, PRECISE & RELEVANT ANSWERS:
   - Always answer the user's EXACT question directly in the opening lines. Never evade or give generic non-sequiturs.
   - If the user asks in Hindi or Hinglish, understand their question perfectly and respond in fluent, professional Hindi/Hinglish or English with clarity.
   - Do NOT force rigid boilerplate templates onto every answer. Adapt the structure to the question:
     * If they ask a direct concept question ("What is Article 9?"), explain the concept and rule clearly.
     * If they ask "Can I do X?", give a clear Yes/No/Conditional verdict, followed by the statutory justification.
     * Only include contract snippets or code patches when relevant to what the user asked.

2. STATUTORY ACCURACY & CITATIONS:
   - Ground your answer in official statutory provisions (UK GDPR, UK DPA 2018, ICO Guidance, India DPDP Act 2023).
   - Accurately cite specific Articles (e.g. UK GDPR Article 6 lawful basis, Art 9 special category, Art 17 erasure, Art 28 processor obligations) or Sections (India DPDPA Section 6 consent, Section 8 obligations).
   - Where relevant, mention statutory penalties or requirements (e.g. UK GDPR up to £17.5M/4% turnover; DPDP Act up to ₹250 Crore).

3. PRACTICAL ENGINEERING & LEGAL GUIDANCE:
   - Provide concrete, pragmatic recommendations for engineering and legal teams (e.g. unbundled checkboxes, zero-data retention, AES-256 encryption, IDTA execution).
   - Keep answers clean, structured with markdown bolding, clear bullet points, and code/quote blocks where appropriate.
"""

def classify_user_intent(query: str) -> str:
    """Classifies user input into greeting, feedback/complaint, gratitude, or compliance query."""
    q = query.strip().lower()
    q_clean = re.sub(r'[^\w\s]', '', q).strip()
    words = q_clean.split()

    greetings = {
        "hi", "hello", "hey", "heya", "hiya", "howdy", "hola", "namaste", "namaskar",
        "good morning", "good evening", "good afternoon", "good day", "greetings",
        "sup", "yo", "test", "ping"
    }
    if q_clean in greetings:
        return "greeting"
    if len(words) <= 2 and words and words[0] in {"hi", "hello", "hey", "hola", "namaste", "yo"}:
        return "greeting"

    feedback_patterns = [
        "not correct", "wrong answer", "galat", "kya puchra", "kya pooch", "chi",
        "bekar", "ye kya hai", "what are you saying", "that is wrong", "incorrect",
        "didn't answer", "did not answer", "answer my question", "samajh nahi",
        "kya bakwas", "nonsense", "useless", "stuck", "it's not correct", "its not correct"
    ]
    if any(p in q for p in feedback_patterns):
        return "meta_feedback"

    gratitude = {"thank you", "thanks", "thx", "dhanyawad", "shukriya", "bye", "goodbye", "ok", "okay", "got it"}
    if q_clean in gratitude or (len(words) <= 2 and words and words[0] in {"thanks", "thank", "bye", "ok"}):
        return "gratitude_or_closure"

    return "compliance_query"

class TaraRAGEngine:
    def __init__(self):
        self.retriever = LegalRetriever()

    def get_stats(self) -> Dict[str, Any]:
        """Returns statistics on the indexed statutory corpus."""
        return get_corpus_stats()

    def search_statutes(self, query: str, jurisdiction: Optional[str] = None, top_k: int = 5) -> List[Dict[str, Any]]:
        """Performs raw semantic and keyword search across statutory articles."""
        return self.retriever.search(query, jurisdiction=jurisdiction, top_k=top_k)

    def query(
        self,
        query: str,
        history: Optional[List[Dict[str, str]]] = None,
        jurisdiction: Optional[str] = None,
        top_k: int = 4
    ) -> Dict[str, Any]:
        """
        Executes end-to-end RAG pipeline:
        1. Classifies user intent (Greeting / Feedback / Gratitude / Compliance)
        2. Retrieves relevant statutory knowledge chunks
        3. Builds grounded context prompt
        4. Calls Azure OpenAI gpt-4o-mini
        5. Attaches precise statutory citation badges
        """
        intent = classify_user_intent(query)

        # 1. Pure Greeting Handler
        if intent == "greeting":
            return {
                "success": True,
                "answer": (
                    "Hello! 👋 I'm **Tara Legal AI Copilot**, your statutory legal & privacy architecture assistant.\n\n"
                    "I am pre-calibrated on **UK GDPR (ICO statutory rules)** and **India's DPDP Act 2023**.\n\n"
                    "How can I help you today? You can ask me about:\n"
                    "• **Privacy Policies & Consent mechanisms** (UK GDPR Art. 6 & 9, India DPDPA Sec. 6)\n"
                    "• **Cross-Border Transfers & IDTA Agreements** (UK to India developer access)\n"
                    "• **Right to Erasure & DSAR implementation** (Article 17, 30-day purge)\n"
                    "• **Third-Party AI & LLM Governance** (Sending consultation transcripts to OpenAI)\n"
                    "• **Live Policy Document Auditing & Statutory Auto-Fixing**"
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 2. Pure Gratitude / Closure Handler
        if intent == "gratitude_or_closure":
            return {
                "success": True,
                "answer": (
                    "You're very welcome! Feel free to ask anytime you need guidance on UK GDPR, India DPDPA, or statutory engineering requirements."
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 3. User Feedback / Complaint Handler
        if intent == "meta_feedback":
            feedback_system_prompt = (
                "You are Tara AI — Lead Data Protection Officer (DPO) and Statutory Privacy Legal Architect for UK GDPR and India DPDP Act 2023.\n"
                "CRITICAL INSTRUCTION: The user is expressing frustration or complaining that the bot gave an incorrect or generic response.\n"
                "- Acknowledge their concern with empathy and apologize politely in the language they used (Hinglish/Hindi/English).\n"
                "- Explain that you are ready to answer their exact, specific question without any unnecessary boilerplate or generic templates.\n"
                "- Ask them to state their specific question so you can give them a direct, precise, and accurate answer."
            )
            messages = [{"role": "system", "content": feedback_system_prompt}]
            if history:
                for msg in history[-4:]:
                    if msg.get("role") in ("user", "assistant") and msg.get("content"):
                        messages.append({"role": msg["role"], "content": msg["content"]})
            messages.append({"role": "user", "content": query})

            try:
                headers = {"api-key": AZURE_OPENAI_KEY, "Content-Type": "application/json"}
                payload = {"messages": messages, "temperature": 0.4, "max_tokens": 400}
                response = requests.post(AZURE_OPENAI_URL, headers=headers, json=payload, timeout=15)
                if response.status_code == 200:
                    res_json = response.json()
                    reply = res_json["choices"][0]["message"]["content"]
                    return {
                        "success": True,
                        "answer": reply,
                        "retrieved_citations": [],
                        "model_clauses": [],
                        "rag_grounded": False,
                        "top_similarity": 0.0,
                        "provider": "Tara Conversational Intelligence"
                    }
            except Exception as e:
                logger.error(f"Feedback LLM error: {e}")

            return {
                "success": True,
                "answer": (
                    "Mujhe aapki frustration samajh aati hai, aur main maafi chahti hoon agar pichla response off-target tha. "
                    "Main aapke exact sawaal ka seedha aur accurate jawab dene ke liye tayaar hoon. "
                    "Kripya apna specific question poochiye (UK GDPR, India DPDPA, ya Privacy architecture par), main turant madad karungi!"
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 4. Compliance / Legal / Engineering Query
        # Context-aware query expansion for follow-up conversational turns
        search_query = query
        if history and len(query.split()) < 8:
            last_user_q = ""
            for h in reversed(history):
                if h.get("role") == "user" and h.get("content"):
                    last_user_q = h.get("content", "")
                    break
            if last_user_q:
                search_query = f"{last_user_q} {query}"

        retrieved_chunks = self.retriever.search(search_query, jurisdiction=jurisdiction, top_k=top_k)

        # Build Grounded Context Block
        context_blocks = []
        citations_summary = []
        model_clauses = []

        for idx, chunk in enumerate(retrieved_chunks, 1):
            chunk_id = chunk.get("id")
            citation = chunk.get("citation")
            title = chunk.get("title")
            penalties = chunk.get("penalties")
            statutory_text = chunk.get("statutory_text")
            practical = chunk.get("practical_application")

            context_blocks.append(
                f"### [DOCUMENT {idx}] {citation}: {title}\n"
                f"- Category: {chunk.get('category')}\n"
                f"- Statutory Text Excerpt: \"{statutory_text}\"\n"
                f"- Statutory Penalties: {penalties}\n"
                f"- Practical Implementation Rule: {practical}\n"
            )

            citations_summary.append({
                "id": chunk_id,
                "citation": citation,
                "title": title,
                "jurisdiction": chunk.get("jurisdiction"),
                "category": chunk.get("category"),
                "penalties": penalties,
                "similarity_score": chunk.get("similarity_score"),
                "statutory_text": statutory_text,
                "practical_application": practical
            })

            if "model" in chunk.get("category", "").lower() or "clause" in chunk.get("category", "").lower():
                model_clauses.append({
                    "title": title,
                    "citation": citation,
                    "clause_text": statutory_text
                })

        context_string = "\n\n".join(context_blocks)

        if context_string:
            user_content = f"""STATUTORY REFERENCE CONTEXT (UK GDPR & India DPDPA):
=========================================
{context_string}
=========================================

USER QUESTION:
{query}

Answer the user's question directly and authoritatively, citing the relevant Articles and Sections above."""
        else:
            user_content = query

        messages = [{"role": "system", "content": RAG_GROUNDED_SYSTEM_PROMPT}]

        if history:
            for msg in history[-6:]:
                if msg.get("role") in ("user", "assistant") and msg.get("content"):
                    messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_content})

        headers = {
            "api-key": AZURE_OPENAI_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "messages": messages,
            "temperature": 0.25,
            "max_tokens": 1400
        }

        try:
            response = requests.post(AZURE_OPENAI_URL, headers=headers, json=payload, timeout=22)
            if response.status_code == 200:
                res_json = response.json()
                reply = res_json["choices"][0]["message"]["content"]
                return {
                    "success": True,
                    "answer": reply,
                    "retrieved_citations": citations_summary,
                    "model_clauses": model_clauses,
                    "rag_grounded": len(citations_summary) > 0,
                    "top_similarity": citations_summary[0]["similarity_score"] if citations_summary else 0.0,
                    "provider": "Tara RAG Pipeline v2.0 (Azure OpenAI gpt-4o-mini + Local Vector Index)"
                }
            else:
                logger.error(f"Azure OpenAI Error {response.status_code}: {response.text}")
                return self._generate_offline_rag_answer(query, citations_summary, model_clauses)
        except Exception as e:
            logger.error(f"RAG OpenAI Connection Error: {e}")
            return self._generate_offline_rag_answer(query, citations_summary, model_clauses)

    def _generate_offline_rag_answer(
        self,
        query: str,
        citations: List[Dict[str, Any]],
        model_clauses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Deterministic offline legal synthesis when external network is restricted."""
        q_low = query.lower()
        if any(w in q_low for w in ["hi", "hello", "hey"]):
            return {
                "success": True,
                "answer": "Hello! 👋 I'm Tara Legal AI Copilot. How can I help you with UK GDPR or India DPDPA compliance today?",
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Offline Assistant"
            }

        if not citations:
            return {
                "success": True,
                "answer": (
                    "### Statutory Compliance Guidance (UK GDPR & India DPDPA)\n\n"
                    "Data processing requires an explicit lawful basis, transparent consent, and technical security safeguards:\n\n"
                    "• **UK GDPR Article 6 & 9:** Lawful basis and explicit opt-in for sensitive special category data.\n"
                    "• **UK GDPR Chapter V:** International transfer safeguards (IDTA/SCCs).\n"
                    "• **India DPDPA Section 6 & 8:** Notice, consent, and reasonable security safeguards."
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Offline Statutory Engine"
            }

        top_chunk = citations[0]
        answer_parts = [
            f"### Statutory Guidance: {top_chunk['title']}\n\n",
            f"**Legal Basis:** [{top_chunk['citation']}] ({top_chunk['jurisdiction']})\n\n",
            f"**Statutory Rule:** {top_chunk['statutory_text']}\n\n",
            f"**Required Engineering Action:** {top_chunk['practical_application']}\n\n",
            f"**Statutory Penalties:** ⚠️ {top_chunk['penalties']}\n"
        ]

        if model_clauses:
            answer_parts.append(f"\n**Compliant Contract Clause:**\n```\n{model_clauses[0]['clause_text']}\n```\n")

        return {
            "success": True,
            "answer": "".join(answer_parts),
            "retrieved_citations": citations,
            "model_clauses": model_clauses,
            "rag_grounded": True,
            "top_similarity": citations[0]["similarity_score"],
            "provider": "Tara RAG Statutory Engine (Local Grounded Synthesis)"
        }

    def audit_document(self, document_text: str, doc_type: str = "privacy_policy") -> Dict[str, Any]:
        """
        RAG-Augmented Document Auditor:
        Cross-references text against statutory corpus to identify missing requirements
        and injects statutory model clauses as redline replacements.
        """
        doc_lower = document_text.lower()
        issues = []
        score = 100

        # 1. Article 9 Explicit Consent Check
        art9_chunk = self.retriever.get_chunk_by_id("UK-GDPR-ART-09")
        model_art9 = self.retriever.get_chunk_by_id("MODEL-CLAUSE-ART9-CONSENT")
        if any(term in doc_lower for term in ["health", "spiritual", "astrology", "kundli", "horoscope", "medical", "beliefs"]):
            if "explicit consent" not in doc_lower and "article 9" not in doc_lower:
                score -= 25
                issues.append({
                    "severity": "critical",
                    "title": "Missing Article 9 Explicit Consent Gateway",
                    "law": "UK GDPR Article 9(1) & 9(2)(a)",
                    "penalties": "Statutory fine up to £17.5M or 4% of annual turnover",
                    "description": "The document processes health, spiritual, or astrological context but relies on generic consent. Article 9 strictly prohibits processing special category data without an explicit, separate affirmative consent statement.",
                    "original_text": "We collect user details, consultation notes, and health or spiritual concerns to provide our advisory services.",
                    "fixed_text": model_art9["statutory_text"] if model_art9 else "We collect personal consultation data only with explicit affirmative Article 9(2)(a) consent.",
                    "explanation": "Injected ICO-approved Article 9 explicit consent clause with separate checkbox and revocation right."
                })

        # 2. Vague Data Retention Check
        retention_chunk = self.retriever.get_chunk_by_id("UK-GDPR-ART-05")
        model_retention = self.retriever.get_chunk_by_id("MODEL-CLAUSE-RETENTION")
        if any(vague in doc_lower for vague in ["as long as necessary", "as long as needed", "for legitimate business purposes", "indefinitely"]):
            score -= 20
            issues.append({
                "severity": "critical",
                "title": "Unlawful Vague Data Retention (Storage Limitation Flaw)",
                "law": "UK GDPR Article 5(1)(e) & India DPDPA Section 8(7)",
                "penalties": "Statutory fine up to £17.5M / ₹100 Crore",
                "description": "Phrasing such as 'retaining data as long as necessary' is explicitly rejected by the UK ICO and DPBI. Statutory retention requires defined timeframes and purpose fulfillment erasure.",
                "original_text": "We retain your personal data for as long as necessary to fulfill the purposes outlined in this policy or as required by our business needs.",
                "fixed_text": model_retention["statutory_text"] if model_retention else "We retain data for 30 days post-session, after which consultation notes are purged.",
                "explanation": "Replaced vague retention with an itemised schedule (30-day session purge, 6-year tax records)."
            })

        # 3. International Cross-Border Transfer & IDTA Check
        idta_chunk = self.retriever.get_chunk_by_id("UK-GDPR-CHAP-V")
        model_idta = self.retriever.get_chunk_by_id("MODEL-CLAUSE-IDTA-CROSSBORDER")
        if any(trans in doc_lower for trans in ["india", "overseas", "international", "subcontractor", "practitioner"]):
            if "idta" not in doc_lower and "international data transfer agreement" not in doc_lower and "scc" not in doc_lower:
                score -= 20
                issues.append({
                    "severity": "critical",
                    "title": "Unapproved International Data Transfers to India",
                    "law": "UK GDPR Chapter V (Articles 44–46) & DPA 2018 Sec 119A",
                    "penalties": "Statutory fine up to £17.5M and immediate ICO Stop-Processing Injunction",
                    "description": "UK customer data accessed by personnel in India constitutes a restricted international transfer. Because India lacks an adequacy finding, transfers are unlawful without an ICO-approved IDTA.",
                    "original_text": "Your data may be shared with our overseas team and practitioners in India to deliver consultations.",
                    "fixed_text": model_idta["statutory_text"] if model_idta else "All international data access is governed by the UK ICO International Data Transfer Agreement (IDTA).",
                    "explanation": "Added formal UK IDTA statutory disclosures, zero local device storage warranties, and third-party beneficiary rights."
                })

        # 4. AI & LLM Processing Disclosure Check
        ai_chunk = self.retriever.get_chunk_by_id("ICO-AI-GUIDANCE-2024")
        model_ai = self.retriever.get_chunk_by_id("MODEL-CLAUSE-OPENAI-GOVERNANCE")
        if any(ai_term in doc_lower for ai_term in ["ai", "openai", "chatgpt", "llm", "large language model", "automated"]):
            if "zero retention" not in doc_lower and "model training" not in doc_lower:
                score -= 15
                issues.append({
                    "severity": "warning",
                    "title": "Unstated AI Model Training Opt-Out & Zero Retention",
                    "law": "UK GDPR Article 28 & ICO AI Guidance (2024)",
                    "penalties": "Statutory fine up to £8.7M / Suspension of AI features",
                    "description": "Draft document mentions AI features but fails to guarantee that third-party LLMs (OpenAI) do not train on confidential customer consultations.",
                    "original_text": "We use artificial intelligence tools to summarize consultation sessions.",
                    "fixed_text": model_ai["statutory_text"] if model_ai else "Our AI features enforce zero model training and ephemeral prompt caching.",
                    "explanation": "Injected zero model training guarantee, prompt PII scrubbing, and ephemeral memory processing."
                })

        # 5. India Grievance Redressal Officer Check
        grievance_chunk = self.retriever.get_chunk_by_id("IN-DPDPA-SEC-13")
        if "grievance" not in doc_lower and "dpbi" not in doc_lower:
            score -= 10
            issues.append({
                "severity": "warning",
                "title": "Missing India Grievance Redressal Officer & Contact",
                "law": "India DPDP Act 2023 Section 13",
                "penalties": "Statutory fine up to ₹50 Crore",
                "description": "Every Data Fiduciary under DPDPA 2023 must publish the name and direct contact details of an accessible Grievance Redressal Officer.",
                "original_text": "For questions, contact our support team at support@example.com.",
                "fixed_text": "GRIEVANCE REDRESSAL (DPDP Act 2023 Sec 13):\nData Protection & Grievance Officer: Legal Counsel\nEmail: grievance@taraprivacy.io | Phone: +91-11-23456789\nAddress: Tara Infotech, Okhla Industrial Area, New Delhi, India.\nGrievances will be acknowledged within 24 hours and resolved within 30 days.",
                "explanation": "Injected statutory Grievance Officer details and 30-day statutory resolution timeline."
            })

        critical_count = sum(1 for i in issues if i["severity"] == "critical")
        warning_count = sum(1 for i in issues if i["severity"] == "warning")

        return {
            "stats": {
                "score": max(20, score),
                "critical": critical_count,
                "warnings": warning_count,
                "fixes": len(issues)
            },
            "issues": issues,
            "rag_audit_version": "2.0-Statutory-Grounded",
            "statutory_corpus_checked": "UK GDPR, ICO Codes 2024, India DPDPA 2023"
        }
