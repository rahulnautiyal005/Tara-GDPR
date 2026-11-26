"""
Tara PrivacyOS — Phase 2 Master Legal RAG Engine
Coordinates:
1. Legal Knowledge Retrieval via LegalRetriever (Hybrid BM25 + Vector Cosine + Citation Boosts)
2. Authoritative Statutory Grounding (UK GDPR, EU GDPR & India DPDP Act 2023)
3. Multi-Turn Scenario Continuity & Context-Aware Fact Retention
4. Strict Legal Nuance: Profiling (Art 4(4)/22), Purpose Compatibility (Art 6(4)),
   Legitimate Uses (DPDP Sec 7 vs GDPR Art 6(1)(f)), Access (Sec 11), Erasure (Sec 12),
   Grievance (Sec 13), Nominee (Sec 14), Duties (Sec 15), and Schedule Penalties.
5. Domain-Aware Dynamic Document Auditing & Statutory Remediation
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

RAG_GROUNDED_SYSTEM_PROMPT = """You are Tara AI — Lead Data Protection Officer (DPO) and Senior Privacy Legal Counsel specialising in the UK GDPR, EU GDPR (2016/679), and India's Digital Personal Data Protection Act, 2023 (DPDP Act 2023).

### CORE PERSONA & CONVERSATIONAL DELIVERY:
1. Act as an intelligent, conversational, and highly experienced Lead DPO and Legal Counsel speaking directly with the user.
2. NEVER sound like a broken robotic template or form generator. DO NOT output rigid repetitive numbered section headers (such as '### 1. Applicable Legal Provisions', '### 2. Legal Interpretation & Analysis', etc.) on every single turn.
3. Answer the user's specific question or scenario directly in the opening sentence. If the user mentions their company (e.g. "Law AI"), address that company by name immediately.
4. Integrate statutory citations smoothly and naturally into your prose and bullet points (e.g., "Under UK GDPR Article 3(2)...", "Under Section 11 of the DPDP Act 2023...").
5. Seamlessly support multi-turn conversations: Remember facts established earlier (such as company name, target audience, business model, jurisdictions, previous consent questions), and build upon them fluidly.
6. If the user asks in Hindi or Hinglish, understand fully and reply with natural, clear, professional language.

### MANDATORY STATUTORY REASONING DIRECTIVES:

1. STATUTORY PRECISION & JURISDICTION SEPARATION:
   - Never conflate GDPR and DPDP Act provisions. They are distinct legal frameworks with different thresholds, lawful bases, and statutory mechanics.
   - Correctly cite exact Articles (GDPR) and Sections (DPDP Act):
     * India DPDP Act 2023:
       - Section 4 & 5: Grounds for processing and mandatory itemised multilingual notice.
       - Section 6: Consent conditions, unconditional mandate (Sec 6(2)), and withdrawal (Sec 6(4)-(6)).
       - Section 7: CERTAIN LEGITIMATE USES (Strict exhaustive statutory list: employment, state subsidies, court orders, medical emergencies). CRITICAL: The DPDP Act does NOT have a general commercial 'legitimate interests' ground like GDPR Art. 6(1)(f)! Commercial profiling and targeted ads CANNOT rely on Section 7; they require valid Section 6 consent.
       - Section 8: Fiduciary obligations — Sec 8(5) reasonable security safeguards; Sec 8(6) mandatory breach notification to Board and affected principals; Sec 8(7) mandatory erasure upon purpose fulfillment or consent withdrawal.
       - Section 9: Children's data (under 18) — verifiable parental consent, absolute ban on tracking/behavioural monitoring/targeted ads directed at children.
       - Section 10: Significant Data Fiduciaries (resident DPO in India, independent auditor, DPIA).
       - Section 11: Right to ACCESS information about personal data (summary of data, identities of all fiduciaries/processors shared with, description of shared data).
       - Section 12: Right to CORRECTION, completion, updating, and ERASURE (fiduciary must erase unless retention necessary for purpose or legal compliance).
       - Section 13: Right of GRIEVANCE REDRESSAL (mandatory internal redressal, Grievance Officer, data principal must exhaust internal remedies before complaining to DPBI).
       - Section 14: Right to NOMINATE representative in event of death or incapacity.
       - Section 15: Duties of Data Principal (duty not to impersonate or register false/frivolous complaints, penalty up to ₹10,000).
     * DPDP Act Penalties (The Schedule):
       - Breach of Sec 8(5) security safeguards: Up to ₹250 Crore.
       - Failure to notify breach under Sec 8(6): Up to ₹200 Crore.
       - Breach of Sec 9 child obligations: Up to ₹200 Crore.
       - Breach of Sec 10 SDF obligations: Up to ₹150 Crore.
       - Breach of Sec 15 Data Principal duties: Up to ₹10,000.
       - Any other general breach: Up to ₹50 Crore.
       - Never invent penalty numbers.

2. BALANCED, NUANCED LEGAL INTERPRETATION (NO OVERSIMPLIFICATIONS):
   - PROFILING & TARGETED ADVERTISING UNDER GDPR:
     * Profiling is defined under Article 4(4).
     * Explicit consent is NOT always necessary for profiling. Standard consent (Art 6(1)(a)) or Legitimate Interests (Art 6(1)(f)) may be used for standard direct marketing profiling, provided Article 21(2)-(3) absolute right to object is provided.
     * Explicit consent is required ONLY if Special Category Data (Art 9) is processed, or if Article 22 solely automated decision-making produces legal or similarly significant effects.
     * Article 22 is NOT automatically triggered by all profiling. Standard marketing and personalized product recommendations do not typically have legal or similarly significant effects under EDPB guidelines.
   - PURPOSE LIMITATION & FURTHER PROCESSING (GDPR Art 6(4)):
     * If data was collected for marketing and subsequently used for profiling/analytics, analyze compatibility under Article 6(4) using the 5 statutory criteria: (a) purpose link, (b) context/expectations, (c) nature of data, (d) consequences, (e) safeguards. If incompatible, fresh Article 6(1)(a) consent is required.
   - CONSENT WITHDRAWAL & STATUTORY RETENTION (GDPR Art 7(3)/17 & DPDP Sec 6(4)/8(7)/12):
     * Withdrawal does NOT affect the lawfulness of past processing based on consent prior to withdrawal.
     * Future processing based on that consent must halt immediately.
     * Data collected solely for that purpose must be erased, EXCEPT data that MUST or MAY be retained under statutory legal obligations (e.g. financial/tax records for 6-7 years under HMRC/GST) or for defense of legal claims (limitation periods), plus maintaining a minimal suppression list.
   - MULTI-JURISDICTION UNIFIED PRIVACY POLICY:
     * A company CAN use a unified global privacy policy across UK/EU and India if structured modularly (Global Core + Regional Schedules for UK/EU GDPR and India DPDP Act). Claiming it is strictly prohibited is legally incorrect.

3. MULTI-TURN SCENARIO CONTINUITY:
   - When answering follow-up questions, PRESERVE and EXPLICITLY BUILD UPON previously established facts (e.g. company collecting customer emails for marketing, subsequent profiling, withdrawal of consent, multi-jurisdiction operations).
   - Address specific entities and scenarios established in prior turns rather than regressing into generic abstract lectures.
"""

def classify_user_intent(query: str) -> str:
    """Classifies user input into greeting, feedback/complaint, gratitude, out-of-scope trivia, or compliance query."""
    q = query.strip().lower()
    q_clean = re.sub(r'[^\w\s]', '', q).strip()
    words = q_clean.split()
    first_word = words[0] if words else ""

    # Common greetings (English, Hindi, Hinglish, informal slang, typos)
    greeting_exact = {
        "hi", "hello", "hey", "heya", "hiya", "howdy", "hola", "namaste", "namaskar",
        "namashkar", "pranam", "pranaam", "good morning", "good evening", "good afternoon",
        "good day", "greetings", "sup", "yo", "test", "ping", "hlo", "hlw", "hii", "hiii",
        "heyy", "heyyy", "kaise ho", "kya haal hai", "kya hal hai", "kya chal raha hai",
        "suno", "sun rhe ho", "listen", "bhai", "bro", "oye", "ram ram", "salaam", "adaab",
        "wassup", "what's up", "whats up"
    }

    # Regex check for variations like hloooo, heyyyy, hiiiii, etc.
    if re.match(r'^(?:h+[li]+[ow]+|h+e+y+|h+i+|h+e+l+o+|y+o+|s+u+p+|w+a+s+u+p+)\b', q_clean):
        if len(words) <= 3:
            return "greeting"

    if q_clean in greeting_exact:
        return "greeting"

    if len(words) <= 3 and first_word in {
        "hi", "hello", "hey", "hola", "namaste", "yo", "hlo", "hlw", "hii", "heyy", "bhai", "bro", "oye", "suno"
    } and not any(w in q for w in ["gdpr", "dpdp", "privacy", "data", "law", "act", "section", "article"]):
        return "greeting"

    # Out of scope / General Knowledge Trivia check (e.g. "pm of india ?", "who is president", "capital of")
    trivia_patterns = [
        r'\bpm of india\b', r'\bprime minister\b', r'\bpresident of\b', r'\bchief minister\b',
        r'\bwho is the pm\b', r'\bcapital of\b', r'\bweather in\b', r'\bwho won\b',
        r'\bcricket score\b', r'\btell me a joke\b', r'\bwrite a poem\b'
    ]
    if any(re.search(pat, q) for pat in trivia_patterns) and not any(w in q for w in ["gdpr", "dpdp", "privacy", "data", "consent", "audit"]):
        return "out_of_scope_trivia"

    # Meta-Feedback / Frustration patterns
    feedback_patterns = [
        "not correct", "wrong answer", "galat", "kya puchra", "kya pooch", "chi",
        "bekar", "ye kya hai", "what are you saying", "that is wrong", "incorrect",
        "didn't answer", "did not answer", "answer my question", "samajh nahi",
        "kya bakwas", "nonsense", "useless", "stuck", "it's not correct", "its not correct",
        "kya mooh dikhaunga", "working very poor"
    ]
    if any(p in q for p in feedback_patterns):
        return "meta_feedback"

    gratitude = {"thank you", "thanks", "thx", "dhanyawad", "shukriya", "bye", "goodbye", "ok", "okay", "got it", "fine"}
    if q_clean in gratitude or (len(words) <= 2 and words and words[0] in {"thanks", "thank", "bye", "ok"}):
        return "gratitude_or_closure"

    return "compliance_query"

def extract_scenario_keywords(history: List[Dict[str, str]]) -> str:
    """Extracts key factual scenario elements across previous conversational turns."""
    if not history:
        return ""
    scenario_terms = []
    combined_history = " ".join(m.get("content", "") for m in history if m.get("role") in ("user", "assistant")).lower()
    
    key_signals = [
        ("email", "email marketing"),
        ("marketing", "direct marketing"),
        ("profiling", "profiling targeted advertising"),
        ("withdraw", "consent withdrawal"),
        ("erasure", "right to erasure retention"),
        ("controller", "controller processor"),
        ("processor", "processor obligations"),
        ("india", "india dpdp act 2023"),
        ("uk", "uk gdpr"),
        ("unified", "unified privacy policy"),
        ("section 11", "section 11 access"),
        ("section 12", "section 12 correction erasure"),
        ("section 13", "section 13 grievance"),
        ("section 7", "section 7 legitimate uses"),
        ("article 22", "article 22 automated decision"),
        ("article 6(4)", "article 6(4) compatibility")
    ]
    for trigger, tag in key_signals:
        if trigger in combined_history:
            scenario_terms.append(tag)
            
    return " ".join(scenario_terms)

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
        top_k: int = 6
    ) -> Dict[str, Any]:
        """
        Executes statutory grounded RAG pipeline with multi-turn scenario continuity:
        1. Classifies user intent
        2. Resolves conversational scenario context across previous messages
        3. Retrieves authoritative primary statutory chunks
        4. Constructs grounded prompt enforcing legal precision and nuanced analysis
        5. Calls Azure OpenAI gpt-4o-mini (or deterministic legal fallback)
        6. Returns structured answer with traceable citation badges
        """
        intent = classify_user_intent(query)

        # 1. Pure Greeting Handler
        if intent == "greeting":
            q_lower = query.lower()
            if any(w in q_lower for w in ["kaise", "haal", "hal", "suno", "bhai", "namaste", "pranam", "kya", "oye"]):
                ans = (
                    "नमस्ते! 👋 Main hoon **Tara Legal AI Copilot**, aapka Data Protection Officer (DPO) & Privacy Legal Architect.\n\n"
                    "Main **UK GDPR, EU GDPR (2016/679)**, aur **India ke Digital Personal Data Protection Act, 2023 (DPDP Act 2023)** "
                    "ke statutory compliance me help karta hoon.\n\n"
                    "Aap mujhse pooch sakte hain:\n"
                    "• Kya aapki company/app par GDPR ya India DPDP Act apply hota hai?\n"
                    "• Consent policies, email marketing aur profiling ke statutory rules\n"
                    "• Data Principal ke Rights (Section 11 Access, Section 12 Erasure, Section 13 Grievance)\n"
                    "• Cross-border data transfers aur IDTA agreements\n\n"
                    "Bataiye, aapke project ya company ke baare me kya query hai?"
                )
            else:
                ans = (
                    "Hello! 👋 I'm **Tara Legal AI Copilot**, Lead Data Protection Officer (DPO) and Statutory Privacy Legal Architect.\n\n"
                    "I provide authoritative, practical legal counsel on **UK GDPR, EU GDPR (2016/679)**, and **India's Digital Personal Data Protection Act, 2023 (DPDP Act 2023)**.\n\n"
                    "How can I help you or your team today? You can ask me:\n"
                    "• **Applicability Checks:** Does GDPR or India DPDP Act apply to your startup, SaaS, or app?\n"
                    "• **Marketing & Profiling Rules:** Lawful grounds under GDPR Art 6/21 vs India DPDP Sec 6/7\n"
                    "• **Statutory Rights in India:** Section 11 (Access), Section 12 (Erasure), Section 13 (Grievance Redressal)\n"
                    "• **Data Retention & Exceptions:** Mandatory erasures vs statutory tax/limitation period retentions\n"
                    "• **Cross-Border Transfers:** UK-to-India IDTA and EU SCC requirements\n\n"
                    "Feel free to ask any question or tell me about your app!"
                )
            return {
                "success": True,
                "answer": ans,
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 2. Out of Scope / General Knowledge Trivia Handler
        if intent == "out_of_scope_trivia":
            q_lower = query.lower()
            if "pm of india" in q_lower or "prime minister" in q_lower:
                trivia_ans = "The Prime Minister of India is **Shri Narendra Modi**."
            elif "president of" in q_lower and "india" in q_lower:
                trivia_ans = "The President of India is **Smt. Droupadi Murmu**."
            else:
                trivia_ans = "I noted your question."

            return {
                "success": True,
                "answer": (
                    f"{trivia_ans}\n\n"
                    "*(Note: As **Tara Legal AI**, my primary role and specialization is in **Data Protection, UK/EU GDPR, and India's DPDP Act 2023**. "
                    "If you have any privacy compliance, legal policy, consent framework, or regulatory architecture questions for your company or application, I'm here to help!)*"
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 3. Pure Gratitude / Closure Handler
        if intent == "gratitude_or_closure":
            return {
                "success": True,
                "answer": (
                    "You're very welcome! Feel free to ask anytime you need guidance on UK GDPR, EU GDPR, or India's DPDP Act 2023 statutory obligations."
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 4. User Feedback / Complaint Handler
        if intent == "meta_feedback":
            return {
                "success": True,
                "answer": (
                    "I hear you, and I apologize if my previous response felt too rigid, repetitive, or off-target. "
                    "I am calibrated to give direct, conversational, and legally accurate counsel tailored to your specific application and business scenario without boilerplates. "
                    "Please state your specific scenario or question, and I will address it directly!"
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Conversational Intelligence"
            }

        # 5. Compliance / Legal Scenario Query with Multi-Turn Scenario Context Expansion
        scenario_context = extract_scenario_keywords(history) if history else ""
        search_query = f"{query} {scenario_context}".strip()

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
                f"### [STATUTORY SOURCE {idx}] {citation}: {title}\n"
                f"- Jurisdiction: {chunk.get('jurisdiction')}\n"
                f"- Statutory Text: \"{statutory_text}\"\n"
                f"- Statutory Penalties: {penalties}\n"
                f"- Application Rule: {practical}\n"
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

        user_content = f"""USER QUESTION:
{query}

STATUTORY REFERENCE CONTEXT (UK/EU GDPR & INDIA DPDP ACT 2023):
======================================================================
{context_string}
======================================================================

RESPONSE GUIDELINES:
- Conversational & Direct: Answer the user's specific inquiry directly in the opening sentence in an intelligent, conversational tone.
- Scenario-Specific: If the user names their company (e.g. Law AI), address them directly by name.
- Avoid Template Clutter: DO NOT format your response with repetitive rigid headers like '(1) Applicable Legal Provisions, (2) Legal Interpretation & Analysis'. Use natural prose with clean bullet points.
- Multi-Turn Continuity: If this builds on earlier questions in the conversation, maintain context and refer back naturally.
- Statutory Accuracy: Seamlessly embed exact statutory Articles (UK/EU GDPR) and Sections (India DPDP Act 2023) inline with explanations.
- Clarify GDPR vs DPDP Act: Distinguish GDPR legitimate interests (Art 6(1)(f)) from India's DPDP Act (Section 7 has exhaustive legitimate uses; commercial profiling/marketing requires Section 6 consent).
- Correct DPDP Sections: Section 11 (Access), Section 12 (Correction/Erasure), Section 13 (Grievance Redressal).
- If the user writes in Hinglish, seamlessly understand and respond in clear, professional language."""

        messages = [{"role": "system", "content": RAG_GROUNDED_SYSTEM_PROMPT}]

        # Inject conversation history to maintain scenario continuity
        if history:
            for msg in history[-8:]:
                if msg.get("role") in ("user", "assistant") and msg.get("content"):
                    messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({"role": "user", "content": user_content})

        headers = {
            "api-key": AZURE_OPENAI_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 1600
        }

        try:
            response = requests.post(AZURE_OPENAI_URL, headers=headers, json=payload, timeout=25)
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
                    "provider": "Tara Grounded Legal Intelligence Engine (Azure OpenAI gpt-4o-mini + Authoritative Statutory Corpus)"
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
        """Comprehensive, legally verified deterministic offline synthesis when external LLM is unreachable."""
        if not citations:
            return {
                "success": True,
                "answer": (
                    "### Statutory Compliance Architecture (UK GDPR & India DPDP Act 2023)\n\n"
                    "Data processing requires an explicit statutory ground, purpose transparency, and technical security safeguards:\n\n"
                    "• **UK GDPR Article 6 & 9:** Lawful bases (consent, contract, legal obligation, legitimate interests) and explicit consent for special categories.\n"
                    "• **UK GDPR Article 21 & 22:** Absolute right to object to direct marketing profiling; Article 22 solely automated decision threshold.\n"
                    "• **India DPDP Act 2023 Sections 4, 5, 6:** Lawful processing based on itemised notice and unconditional consent.\n"
                    "• **India DPDP Act 2023 Section 7:** Exhaustive 'Certain Legitimate Uses' (no general commercial legitimate interests).\n"
                    "• **India DPDP Act 2023 Sections 11, 12, 13:** Data principal rights to Access (Sec 11), Correction & Erasure (Sec 12), and Grievance Redressal (Sec 13)."
                ),
                "retrieved_citations": [],
                "model_clauses": [],
                "rag_grounded": False,
                "top_similarity": 0.0,
                "provider": "Tara Offline Statutory Engine"
            }

        top_chunk = citations[0]
        answer_parts = [
            f"### Statutory Legal Guidance: {top_chunk['title']}\n\n",
            f"**1. Governing Statute & Citation:**\n[{top_chunk['citation']}] ({top_chunk['jurisdiction']})\n\n",
            f"**2. Authoritative Statutory Rule:**\n{top_chunk['statutory_text']}\n\n",
            f"**3. Legal Application & Key Requirements:**\n{top_chunk['practical_application']}\n\n",
            f"**4. Statutory Penalties:**\n⚠️ {top_chunk['penalties']}\n"
        ]

        if model_clauses:
            answer_parts.append(f"\n**5. Model Statutory Clause:**\n```\n{model_clauses[0]['clause_text']}\n```\n")

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
        Dynamic, domain-aware statutory document auditor:
        First attempts AI-driven audit via Azure OpenAI (JSON schema mode) so the analysis
        reflects the user's ACTUAL document and business domain.
        Falls back to a domain-aware rule engine (zero astrology contamination).
        """
        # Attempt AI-driven audit first for 100% dynamic, tailored results
        try:
            from tara_privacyos.core.azure_llm import audit_document_with_ai
            ai_res = audit_document_with_ai(document_text, doc_type)
            if ai_res and ai_res.get("success"):
                return ai_res
        except Exception as e:
            logger.warning(f"Live AI document audit failed, using domain-aware fallback: {e}")

        # Domain-aware rule-based statutory auditor (sanitized, zero astrology contamination)
        doc_lower = document_text.lower()
        issues = []
        score = 100

        # Infer company name or domain from document
        c_name_match = re.search(r'(?:company|organization|entity|we|us|platform|app|service)\s*(?:called|named|known as)?\s*([A-Z][A-Za-z0-9_\s]{2,30})', document_text)
        detected_cname = c_name_match.group(1).strip() if c_name_match else "Our Organization"

        # 0. Special Category Data Check (Article 9)
        if any(sc_term in doc_lower for sc_term in ["health", "spiritual", "biometric", "medical", "religious", "philosophical", "special category"]):
            if "explicit consent" not in doc_lower and "article 9" not in doc_lower:
                score -= 20
                issues.append({
                    "severity": "critical",
                    "title": "Unlawful Processing of Special Category Data Without Explicit Consent (Article 9 Flaw)",
                    "law": "UK GDPR Article 9(1) & 9(2)(a) & DPDP Act 2023 Section 6",
                    "penalties": "Statutory fine up to £17.5M (GDPR) / ₹250 Crore (DPDPA)",
                    "description": "Processing special category data (such as health, biometric, or religious/philosophical beliefs) is strictly prohibited under UK GDPR Article 9(1) unless explicit, unbundled opt-in consent is obtained under Article 9(2)(a).",
                    "original_text": "We collect user sensitive concerns to deliver consultations.",
                    "fixed_text": f"EXPLICIT CONSENT FOR SPECIAL CATEGORY DATA (UK GDPR Art 9(2)(a) & DPDP Act Sec 6):\n'By checking this box, you expressly and affirmatively consent to our collection and processing of special category personal data solely to provide the requested service. You may withdraw this explicit consent at any time through your account privacy settings.'",
                    "explanation": "Injected mandatory unbundled explicit consent gate under Article 9(2)(a)."
                })

        # 1. Unlawful Vague Retention Check
        if any(vague in doc_lower for vague in ["as long as necessary", "as long as needed", "for legitimate business purposes", "indefinitely"]):
            score -= 20
            issues.append({
                "severity": "critical",
                "title": "Unlawful Vague Data Retention (Storage Limitation Flaw)",
                "law": "UK GDPR Article 5(1)(e) & India DPDP Act 2023 Section 8(7)",
                "penalties": "Statutory fine up to £17.5M (GDPR) / ₹50 Crore (DPDPA Schedule Item 6)",
                "description": "Phrasing such as 'retaining data as long as necessary' violates statutory storage limitation principles. Both UK GDPR and India DPDP Act mandate explicit, purpose-linked retention schedules and mandatory erasure once purpose is fulfilled.",
                "original_text": "We retain your personal data for as long as necessary to fulfill the purposes outlined in this policy or as required by our business needs.",
                "fixed_text": f"DATA RETENTION SCHEDULE (UK GDPR Art 5(1)(e) & DPDP Act Sec 8(7)):\n'{detected_cname} enforces strict data minimisation: 1. User Account Data is retained for the active lifecycle of the account + 30 days following verified account closure; 2. Customer inquiries and support logs are purged 90 days post-resolution; 3. Financial and billing transaction records are retained for statutory periods mandated by applicable tax and accounting laws (6 years under UK HMRC / 7 years under Indian GST); 4. Marketing data is purged immediately upon consent withdrawal under DPDP Sec 6(4) / GDPR Art 7(3).'\nUpon expiration of designated periods, data is permanently erased or irreversibly anonymized.",
                "explanation": "Replaced vague indefinite retention with explicit purpose-specific timetables and statutory tax retention exceptions."
            })

        # 2. International Transfer / Cross-Border Safeguards Check
        if any(trans in doc_lower for trans in ["india", "overseas", "international", "subcontractor", "cross-border", "transfer outside"]):
            if "idta" not in doc_lower and "international data transfer agreement" not in doc_lower and "scc" not in doc_lower and "standard contractual clauses" not in doc_lower:
                score -= 20
                issues.append({
                    "severity": "critical",
                    "title": "Unapproved International Cross-Border Data Transfer",
                    "law": "UK GDPR Chapter V (Articles 44–46) & DPA 2018 Section 119A",
                    "penalties": "Statutory fine up to £17.5M and ICO Stop-Processing Injunction",
                    "description": "Cross-border transfers between the UK/EU and overseas technical teams or processors without citing UK ICO-approved International Data Transfer Agreements (IDTA) or Standard Contractual Clauses (SCCs) are unlawful.",
                    "original_text": "Your data may be transferred to or accessed by our overseas team and international affiliates.",
                    "fixed_text": f"INTERNATIONAL DATA TRANSFERS (UK GDPR Chapter V):\n'Personal data processed by {detected_cname} may be accessed by technical personnel and cloud administrators located overseas (including in the Republic of India). In the absence of an adequacy regulation, all cross-border access is strictly governed by the official UK ICO International Data Transfer Agreement (IDTA) pursuant to Section 119A of the Data Protection Act 2018, ensuring equivalent safeguards, encryption in transit, and enforceable third-party beneficiary rights.'",
                    "explanation": "Injected statutory UK IDTA safeguards, encryption warranties, and enforceable third-party beneficiary rights."
                })

        # 3. India Grievance Redressal Officer Check
        if "grievance" not in doc_lower and "dpbi" not in doc_lower:
            score -= 15
            issues.append({
                "severity": "warning",
                "title": "Missing India Grievance Redressal Officer & Contact Details",
                "law": "India DPDP Act 2023 Section 13",
                "penalties": "Statutory fine up to ₹50 Crore under Item 6 of the Schedule",
                "description": "Every Data Fiduciary under DPDP Act 2023 must publish the name and direct contact details of an accessible Grievance Redressal Officer, and resolve grievances within prescribed statutory timelines.",
                "original_text": "For questions, contact our support team at support@example.com.",
                "fixed_text": f"GRIEVANCE REDRESSAL MECHANISM (India DPDP Act 2023 Section 13):\n'Data Protection & Grievance Redressal Officer: Legal & Compliance Counsel\nEmail: grievance@taraprivacy.io | Contact: +91-11-23456789\nAddress: {detected_cname}, Compliance Division, New Delhi, India.\nGrievances will be acknowledged within 24 hours and resolved within statutory timelines (30 days). Under Section 13(3), Data Principals must exhaust this redressal mechanism before filing a complaint with the Data Protection Board of India (DPBI).'",
                "explanation": "Injected designated Grievance Officer, contact email/phone, 30-day statutory resolution timeline, and DPBI escalation pathway."
            })

        # 4. Consent Withdrawal Mechanism Check
        if "withdraw" not in doc_lower and "revoc" not in doc_lower:
            score -= 15
            issues.append({
                "severity": "critical",
                "title": "Missing Explicit Consent Withdrawal Mechanism",
                "law": "UK GDPR Article 7(3) & India DPDP Act 2023 Section 6(4)",
                "penalties": "Statutory fine up to £17.5M (GDPR) / ₹50 Crore (DPDPA Schedule)",
                "description": "Both UK GDPR Article 7(3) and DPDP Act Section 6(4) mandate that data subjects must have the right to withdraw consent at any time, with ease of withdrawal being comparable to the ease with which consent was given.",
                "original_text": "By signing up, you agree to our processing of your personal data.",
                "fixed_text": "RIGHT TO WITHDRAW CONSENT (GDPR Art 7(3) & DPDP Act Sec 6(4)):\n'You have the statutory right to withdraw your consent at any time with the same ease with which it was provided, via your account privacy settings or by emailing privacy@taraprivacy.io. Consent withdrawal takes effect immediately and halts future processing. Pursuant to law, withdrawal does not affect the legality of processing carried out prior to withdrawal, nor does it preclude retention required for compliance with statutory tax, financial, or legal defense obligations.'",
                "explanation": "Added self-service withdrawal mechanism, clarification of past lawfulness, and statutory retention exceptions."
            })

        # 5. AI / Automated Processing Disclosure (if AI/automated terms present)
        if any(ai_term in doc_lower for ai_term in ["ai", "openai", "chatgpt", "llm", "large language model", "automated processing", "algorithm"]):
            if "zero model training" not in doc_lower and "model training" not in doc_lower and "human oversight" not in doc_lower:
                score -= 15
                issues.append({
                    "severity": "warning",
                    "title": "Unstated AI Model Training Opt-Out & Ephemeral Processing",
                    "law": "UK GDPR Article 28 & ICO Guidance on Generative AI (2024)",
                    "penalties": "Statutory fine up to £8.7M / Suspension of AI processing",
                    "description": "Where third-party Large Language Model (LLM) APIs are integrated, controllers must guarantee that customer data is not used for public model training and that prompts are processed ephemerally.",
                    "original_text": "We utilize artificial intelligence to process inputs and provide automated responses.",
                    "fixed_text": f"ARTIFICIAL INTELLIGENCE & THIRD-PARTY LLM PROCESSING:\n'To provide automated intelligent features, {detected_cname} integrates enterprise AI APIs (such as OpenAI LLC and Microsoft Azure OpenAI). We enforce strict contractual safeguards: 1. Zero Model Training: Your application inputs, prompts, and personal data are never used to train, retrain, or fine-tune public foundational AI models; 2. Ephemeral Processing: Inputs are processed ephemerally in volatile memory and not retained on AI vendor servers; 3. Human in the Loop: AI outputs provide automated recommendations and do not make sole decisions producing legal or similarly significant effects under GDPR Article 22.'",
                    "explanation": "Injected zero model training warranty, ephemeral prompt processing, and Article 22 human-in-the-loop safeguards."
                })

        critical_count = sum(1 for i in issues if i["severity"] == "critical")
        warning_count = sum(1 for i in issues if i["severity"] == "warning")

        return {
            "stats": {
                "score": max(25, score),
                "critical": critical_count,
                "warnings": warning_count,
                "fixes": len(issues)
            },
            "issues": issues,
            "rag_audit_version": "2.4-Domain-Aware-Statutory",
            "statutory_corpus_checked": "UK GDPR, EU GDPR 2016/679, India DPDP Act 2023"
        }
