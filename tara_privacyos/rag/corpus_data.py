"""
Tara PrivacyOS — Phase 2 Statutory Legal Corpus
High-fidelity, authoritative legal knowledge base covering:
1. UK General Data Protection Regulation (UK GDPR) & Data Protection Act 2018 (DPA 2018)
2. EU General Data Protection Regulation (EU GDPR 2016/679)
3. UK Information Commissioner's Office (ICO) Statutory Guidance & Codes (2024)
4. India Digital Personal Data Protection Act, 2023 (DPDP Act 2023, Act No. 22 of 2023)
5. The Schedule to the DPDP Act 2023 (Statutory Penalties Matrix)
6. Multi-Jurisdictional Privacy Architecture (UK/EU GDPR + India DPDP Act)
7. Statutory Model Clauses for Automated Redlining & Gap Remediation
"""

from typing import List, Dict, Any

STATUTORY_CORPUS: List[Dict[str, Any]] = [
    # =========================================================================
    # PART 1: UK / EU GDPR — CORE ARTICLES, PRINCIPLES & GOVERNANCE
    # =========================================================================
    {
        "id": "UK-GDPR-ART-04-CONTROLLER-PROCESSOR",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation & EU GDPR",
        "citation": "GDPR Article 4(7) & Article 4(8)",
        "category": "Roles & Governance",
        "title": "Definitions & Statutory Division between Data Controller and Data Processor",
        "summary": "Article 4(7) defines a Data Controller as the natural or legal person, public authority, agency or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data. Article 4(8) defines a Data Processor as a natural or legal person, public authority, agency or other body which processes personal data on behalf of the controller.",
        "key_requirements": [
            "Controller determines 'Why' (purpose) and 'How' (essential means) personal data is processed",
            "Processor acts strictly on the documented instructions of the controller and cannot process data for its own independent commercial purposes",
            "Controllers bear primary accountability under Article 5(2) and Article 24 for compliance with data subject rights, legal bases, DPIAs, and transparency",
            "Processors have direct statutory duties under Article 28(3) (maintain contracts), Article 29 (processing under authority), Article 30(2) (records of processing categories), Article 32 (security measures), Article 33(2) (breach notification to controller without undue delay), and Article 44 (cross-border transfers)"
        ],
        "penalties": "Infringements of controller/processor governance obligations under Articles 28, 30, and 32 carry statutory fines up to £8,700,000 / €10,000,000 or 2% of annual worldwide turnover (Article 83(4)).",
        "statutory_text": "Article 4(7): 'controller' means the natural or legal person, public authority, agency or other body which, alone or jointly with others, determines the purposes and means of the processing of personal data. Article 4(8): 'processor' means a natural or legal person, public authority, agency or other body which processes personal data on behalf of the controller.",
        "practical_application": "A SaaS vendor hosting customer data as a database infrastructure provider is a Processor. A company collecting user signups and deciding to run targeted advertising or marketing campaigns is the Controller.",
        "keywords": ["controller", "processor", "article 4", "purposes and means", "on behalf of", "governance", "role allocation", "joint controllers"]
    },
    {
        "id": "UK-GDPR-ART-24-CONTROLLER-OBLIGATIONS",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 24(1) & 24(2)",
        "category": "Controller Obligations",
        "title": "Responsibility of the Controller & Accountability Measures",
        "summary": "Taking into account the nature, scope, context and purposes of processing as well as the risks of varying likelihood and severity for the rights and freedoms of natural persons, the controller shall implement appropriate technical and organisational measures to ensure and to be able to demonstrate that processing is performed in accordance with this Regulation. Those measures shall be reviewed and updated where necessary.",
        "key_requirements": [
            "Implement technical and organisational measures proportionate to risk",
            "Maintain comprehensive documentation demonstrating GDPR compliance (Accountability)",
            "Adopt formal internal data protection policies (Art 24(2)) where proportionate",
            "Adhere to approved codes of conduct (Art 40) or certification mechanisms (Art 42)"
        ],
        "penalties": "Statutory fine up to £8,700,000 or 2% of annual worldwide turnover under Article 83(4)(a).",
        "statutory_text": "Article 24(1): Taking into account the nature, scope, context and purposes of processing as well as the risks of varying likelihood and severity for the rights and freedoms of natural persons, the controller shall implement appropriate technical and organisational measures to ensure and to be able to demonstrate that processing is performed in accordance with this Regulation.",
        "practical_application": "Controllers cannot outsource core accountability. Even when using AWS or Stripe, the controller remains legally responsible for determining lawful basis and honoring DSARs.",
        "keywords": ["article 24", "controller responsibility", "accountability", "technical measures", "organisational measures"]
    },
    {
        "id": "UK-GDPR-ART-28",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 28(1)-(4)",
        "category": "Processor Obligations",
        "title": "Processor Contracts & Mandatory Data Processing Addendum (DPA) Clauses",
        "summary": "Where processing is carried out on behalf of a controller, the controller shall use only processors providing sufficient guarantees. Processing by a processor shall be governed by a binding contract setting out subject matter, duration, nature and purpose, type of personal data, categories of data subjects, and the obligations and rights of the controller.",
        "key_requirements": [
            "Must have a legally binding written Data Processing Agreement (DPA)",
            "Processor must process data ONLY on documented instructions from the controller (Art 28(3)(a))",
            "Persons authorised to process data must be committed to confidentiality (Art 28(3)(b))",
            "Processor must implement technical security measures pursuant to Article 32 (Art 28(3)(c))",
            "Prior specific or general written authorization required before engaging sub-processors (Art 28(2) & 28(4))",
            "Processor must assist controller by appropriate technical measures in responding to DSARs (Art 28(3)(e))",
            "Processor must assist controller with breach notifications (Art 33/34) and DPIAs (Art 35) (Art 28(3)(f))",
            "Processor must delete or return all personal data at the end of the provision of services (Art 28(3)(g))",
            "Processor must make available to controller all information necessary to demonstrate compliance and allow for audits (Art 28(3)(h))"
        ],
        "penalties": "Statutory fine up to £8,700,000 or 2% of annual worldwide turnover under Article 83(4)(a).",
        "statutory_text": "Article 28(3): Processing by a processor shall be governed by a contract or other legal act under Union or Member State law, that is binding on the processor with regard to the controller and that sets out the subject-matter and duration of the processing, the nature and purpose of the processing, the type of personal data and categories of data subjects and the obligations and rights of the controller.",
        "practical_application": "Every vendor integration (Stripe, Twilio, OpenAI, AWS) requires a verified Article 28 DPA with documented instructions, confidentiality, subprocessor terms, and audit clauses.",
        "keywords": ["article 28", "processor", "dpa", "data processing agreement", "documented instructions", "subprocessor", "return or delete"]
    },
    {
        "id": "UK-GDPR-ART-05",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 5(1) & 5(2)",
        "category": "Core Principles",
        "title": "Principles Relating to Processing of Personal Data",
        "summary": "Personal data must be processed lawfully, fairly, and transparently; collected for specified, explicit, and legitimate purposes (purpose limitation); adequate, relevant, and limited to what is necessary (data minimisation); accurate; kept in a form which permits identification for no longer than necessary (storage limitation); and processed with appropriate security (integrity and confidentiality). The controller is accountable for demonstrating compliance.",
        "key_requirements": [
            "Lawfulness, fairness, and transparency (Art 5(1)(a))",
            "Purpose limitation: no processing incompatible with declared purpose (Art 5(1)(b))",
            "Data minimisation: strictly limited to what is necessary (Art 5(1)(c))",
            "Accuracy and rectification obligation (Art 5(1)(d))",
            "Storage limitation: indefinite retention is strictly illegal (Art 5(1)(e))",
            "Integrity and confidentiality via technical and organisational security (Art 5(1)(f))",
            "Accountability principle: controller must maintain audit proof of compliance (Art 5(2))"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide annual turnover, whichever is higher under Article 83(5)(a).",
        "statutory_text": "Personal data shall be: (a) processed lawfully, fairly and in a transparent manner; (b) collected for specified, explicit and legitimate purposes; (c) adequate, relevant and limited to what is necessary; (d) accurate; (e) kept in a form which permits identification for no longer than is necessary; (f) processed in a manner that ensures appropriate security of the personal data.",
        "practical_application": "Establish explicit data retention schedules (e.g. 30 days for telemetry logs, 6 years for statutory tax/financial records). Storing customer prompts or telemetry forever violates Article 5(1)(e).",
        "keywords": ["principles", "data minimisation", "storage limitation", "purpose limitation", "accuracy", "integrity", "accountability", "article 5"]
    },
    {
        "id": "UK-GDPR-ART-06",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 6(1)",
        "category": "Lawful Bases",
        "title": "Lawfulness of Processing (The Six Legal Bases)",
        "summary": "Processing of personal data is lawful only if at least one of the six legal bases applies: (a) Consent, (b) Contract performance or pre-contractual steps, (c) Legal obligation, (d) Vital interests, (e) Public task, or (f) Legitimate interests (balanced against data subject fundamental rights and freedoms, particularly where data subject is a child).",
        "key_requirements": [
            "Identify and document the specific lawful basis prior to commencing data processing",
            "Cannot retroactively swap lawful bases if the original basis becomes invalid",
            "Consent must satisfy strict Article 7 conditions (unbundled, freely given, revocable)",
            "Legitimate interests (Art 6(1)(f)) requires a documented 3-part balancing test: Purpose test, Necessity test, and Balancing test",
            "For direct marketing and profiling under legitimate interests, data subject has an absolute right to object under Article 21"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(a).",
        "statutory_text": "Article 6(1): Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent; (b) processing is necessary for the performance of a contract; (c) processing is necessary for compliance with a legal obligation; (d) processing is necessary in order to protect vital interests; (e) processing is necessary for public interest; (f) processing is necessary for the purposes of legitimate interests.",
        "practical_application": "User registration requires Contract (Art 6(1)(b)). Basic email newsletter marketing may rely on Consent (Art 6(1)(a)) or soft opt-in Legitimate Interests (Art 6(1)(f)) subject to PECR and absolute right to object.",
        "keywords": ["article 6", "lawful basis", "consent", "contractual necessity", "legitimate interests", "legal obligation"]
    },
    {
        "id": "UK-GDPR-ART-06-4-COMPATIBILITY",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 6(4)",
        "category": "Purpose Compatibility",
        "title": "Compatibility Test for Further Processing (Purpose Limitation)",
        "summary": "Where processing for a purpose other than that for which the personal data have been collected is not based on the data subject's consent or on Union or Member State law, the controller shall, in order to ascertain whether processing for another purpose is compatible with the original purpose, take into account five statutory criteria.",
        "key_requirements": [
            "Criteria (a): Any link between the purposes for which the personal data have been collected and the purposes of the intended further processing",
            "Criteria (b): The context in which the personal data have been collected, in particular regarding the relationship between data subjects and the controller (reasonable expectations)",
            "Criteria (c): The nature of the personal data, in particular whether special categories of personal data (Art 9) or criminal convictions data (Art 10) are processed",
            "Criteria (d): The possible consequences of the intended further processing for data subjects",
            "Criteria (e): The existence of appropriate safeguards, which may include encryption or pseudonymisation",
            "If further processing is INCOMPATIBLE with the original collection purpose, fresh valid consent under Article 6(1)(a) is mandatory"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(a).",
        "statutory_text": "Article 6(4): Where processing for a purpose other than that for which personal data have been collected is not based on consent or Union/Member State law, the controller shall, in order to ascertain whether processing for another purpose is compatible with the purpose for which personal data are initially collected, take into account: (a) any link between the purposes; (b) the context of collection and relationship with data subject; (c) the nature of personal data; (d) possible consequences for data subjects; (e) the existence of appropriate safeguards.",
        "practical_application": "If customer email addresses were collected solely to send product updates/receipts, subsequent detailed behavioural profiling or targeted advertising across third-party ad networks constitutes an incompatible new purpose requiring fresh, affirmative consent under Article 6(4).",
        "keywords": ["article 6(4)", "compatibility test", "further processing", "purpose limitation", "reasonable expectations", "incompatible purpose", "profiling"]
    },
    {
        "id": "UK-GDPR-ART-21-RIGHT-TO-OBJECT",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 21(1)-(3)",
        "category": "Data Subject Rights",
        "title": "Right to Object to Processing & Absolute Right to Halt Direct Marketing Profiling",
        "summary": "The data subject shall have the right to object, on grounds relating to his or her particular situation, at any time to processing based on legitimate interests (Art 6(1)(f)). Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing, including profiling to the extent that it is related to such direct marketing. Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.",
        "key_requirements": [
            "General objection under Article 21(1): Controller must stop processing unless it demonstrates compelling legitimate grounds overriding data subject interests, or for legal claims",
            "Direct marketing objection under Article 21(2) & 21(3): ABSOLUTE RIGHT. No balancing test or compelling grounds can override an objection to direct marketing or direct marketing profiling",
            "Must explicitly present this right to data subject at the latest at time of first communication and clearly separate it from other information (Art 21(4))",
            "Upon objection, marketing profiling must halt immediately across all systems"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(b).",
        "statutory_text": "Article 21(2): Where personal data are processed for direct marketing purposes, the data subject shall have the right to object at any time to processing of personal data concerning him or her for such marketing, which includes profiling to the extent that it is related to such direct marketing. Article 21(3): Where the data subject objects to processing for direct marketing purposes, the personal data shall no longer be processed for such purposes.",
        "practical_application": "Every marketing email must include an instant 1-click unsubscribe. When clicked, all promotional emailing and associated advertising profiling must immediately terminate.",
        "keywords": ["article 21", "right to object", "direct marketing", "profiling objection", "absolute right", "opt-out", "unsubscribe"]
    },
    {
        "id": "UK-GDPR-ART-22-AUTOMATED-DECISION-MAKING",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 22(1)-(4) & Article 4(4)",
        "category": "Automated Decisions & Profiling",
        "title": "Automated Individual Decision-Making, Profiling & The Legal/Significant Effect Threshold",
        "summary": "Article 4(4) defines profiling as any form of automated processing of personal data evaluating personal aspects relating to a natural person. Article 22(1) grants the data subject the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her. Article 22 does NOT apply to all profiling—only profiling meeting this high statutory threshold.",
        "key_requirements": [
            "Profiling under Art 4(4) does not automatically trigger Article 22. Standard marketing profiling or basic product recommendations do NOT produce legal or similarly significant effects under EDPB guidelines",
            "Article 22 threshold is triggered when decisions produce 'legal effects' (e.g. cancellation of contract, denial of legal right) or 'similarly significantly affect' the individual (e.g. automated denial of credit/loan, exclusion from job interview, dynamic differential pricing that prevents access to basic goods)",
            "Where Art 22 is triggered, it is prohibited UNLESS: (a) necessary for entering into or performance of a contract; (b) authorized by Union/Member State law; or (c) based on explicit consent (Art 22(2))",
            "Where exceptions (a) or (c) apply, controller must implement suitable safeguards: at least the right to obtain human intervention, to express his or her point of view, and to contest the decision (Art 22(3))",
            "Automated decisions cannot be based on Special Category Data (Art 9) unless Art 9(2)(a) explicit consent or substantial public interest applies, and suitable measures are in place (Art 22(4))"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(b).",
        "statutory_text": "Article 22(1): The data subject shall have the right not to be subject to a decision based solely on automated processing, including profiling, which produces legal effects concerning him or her or similarly significantly affects him or her. Article 22(3): ...the data controller shall implement suitable measures to safeguard the data subject's rights and freedoms and legitimate interests, at least the right to obtain human intervention on the part of the controller, to express his or her point of view and to contest the decision.",
        "practical_application": "Using customer purchase history to recommend similar software tools is standard profiling (Art 4(4)) governed by Art 6 and Art 21, but does NOT trigger Art 22. Using an automated AI algorithm to deny a user credit or cancel their account solely based on automated risk scoring triggers Art 22 and mandates human review mechanisms.",
        "keywords": ["article 22", "article 4(4)", "profiling", "automated decision making", "legal effect", "similarly significantly affects", "human intervention", "contest decision"]
    },
    {
        "id": "UK-GDPR-ART-07",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 7(1)-(4)",
        "category": "Consent Conditions",
        "title": "Conditions for Consent & The Right to Withdraw Consent",
        "summary": "Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented. The request for consent must be clearly distinguishable, intelligible, and easily accessible using clear and plain language. The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal.",
        "key_requirements": [
            "Burden of proof on controller to demonstrate affirmative consent was given (Art 7(1))",
            "Consent requests must be separate from generic terms of service (Art 7(2))",
            "Right to withdraw at any time; it must be as easy to withdraw consent as it is to give it (Art 7(3))",
            "CRITICAL PRINCIPLE: Withdrawal of consent does NOT retroactively make prior processing unlawful; it terminates lawful basis for future processing",
            "Freely given test: Assessing whether performance of contract is made conditional on consent to processing not necessary for that contract (Art 7(4))"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(a).",
        "statutory_text": "Article 7(3): The data subject shall have the right to withdraw his or her consent at any time. The withdrawal of consent shall not affect the lawfulness of processing based on consent before its withdrawal. Prior to giving consent, the data subject shall be informed thereof. It shall be as easy to withdraw as to give consent.",
        "practical_application": "When a customer unchecks marketing consent, past newsletter deliveries remain lawful, but all future marketing blasts must cease instantly. If consent was given via a 1-click toggle, withdrawal cannot require a phone call or written letter.",
        "keywords": ["article 7", "consent conditions", "consent withdrawal", "prior lawfulness", "as easy to withdraw", "freely given"]
    },
    {
        "id": "UK-GDPR-ART-17",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 17(1)-(3)",
        "category": "Data Subject Rights",
        "title": "Right to Erasure ('Right to be Forgotten') & Statutory Retention Exceptions",
        "summary": "The data subject shall have the right to obtain from the controller the erasure of personal data without undue delay. The controller has the obligation to erase personal data without undue delay where grounds apply (e.g. data no longer necessary for purpose, consent withdrawn and no other legal ground). Crucially, Article 17(3) contains explicit exceptions where data MUST NOT or NEED NOT be erased.",
        "key_requirements": [
            "Grounds for erasure (Art 17(1)): (a) data no longer necessary for purpose; (b) consent withdrawn and no other legal basis; (c) data subject objects under Art 21; (d) unlawful processing",
            "MANDATORY EXCEPTIONS (Art 17(3)): Erasure does NOT apply to the extent processing is necessary for: (b) compliance with a legal obligation under Union/Member State law (e.g. statutory tax, accounting, or corporate record keeping); (e) for the establishment, exercise or defence of legal claims (statutory limitation periods)",
            "Suppression / Opt-out lists: Controller may retain minimal identification data (e.g. hashed email) strictly to maintain a suppression register preventing accidental future marketing re-contact",
            "Timeframe: Erasure must be executed within one month of receiving the request (Article 12(3)) across primary databases and backup lifecycles"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(b).",
        "statutory_text": "Article 17(1): The data subject shall have the right to obtain from the controller the erasure of personal data without undue delay... Article 17(3): Paragraphs 1 and 2 shall not apply to the extent that processing is necessary: (b) for compliance with a legal obligation which requires processing by Union or Member State law...; (e) for the establishment, exercise or defence of legal claims.",
        "practical_application": "If a user withdraws marketing consent and requests erasure, delete their marketing profile and behavioral telemetry immediately. However, retain their invoice billing records for 6 years pursuant to UK HMRC / Indian GST tax laws and maintain their email on a suppression list.",
        "keywords": ["article 17", "right to erasure", "right to be forgotten", "retention exceptions", "statutory retention", "legal obligation", "defence of legal claims", "suppression list"]
    },
    {
        "id": "UK-GDPR-ART-15-16",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 15 & Article 16",
        "category": "Data Subject Rights",
        "title": "Right of Access (DSAR) & Right to Rectification",
        "summary": "Article 15 gives data subjects the right to obtain confirmation as to whether personal data concerning them are being processed, access to the personal data, and detailed information on purposes, categories, recipients, retention period, and source. Article 16 gives the right to obtain the rectification of inaccurate personal data without undue delay, and to have incomplete data completed.",
        "key_requirements": [
            "Controller must provide a copy of the personal data undergoing processing free of charge (Art 15(3))",
            "Must provide information on purposes, categories, recipients, retention, rights to rectify/erase/object, and right to lodge complaint with ICO",
            "Rectification must be executed without undue delay (Art 16)",
            "Response must be delivered within one month of receipt (Art 12(3)), extendable by two months for complex requests"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(b).",
        "statutory_text": "Article 15(1): The data subject shall have the right to obtain from the controller confirmation as to whether or not personal data concerning him or her are being processed, and, where that is the case, access to the personal data... Article 16: The data subject shall have the right to obtain from the controller without undue delay the rectification of inaccurate personal data concerning him or her.",
        "practical_application": "Automate DSAR export generating a machine-readable JSON/PDF summary of all customer database records within 30 days.",
        "keywords": ["article 15", "article 16", "dsar", "right of access", "rectification", "correction", "copy of data"]
    },
    {
        "id": "UK-GDPR-ART-09",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 9(1) & 9(2)(a)",
        "category": "Special Category Data",
        "title": "Processing of Special Categories of Personal Data (Strict Prohibition & Exceptions)",
        "summary": "Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health or data concerning a natural person's sex life or sexual orientation shall be prohibited. Processing is permitted ONLY if an Article 9(2) exception applies, such as explicit consent (Art 9(2)(a)).",
        "key_requirements": [
            "General rule: Special category data processing is PROHIBITED by default",
            "Article 9(2)(a) exception requires EXPLICIT consent (higher standard than Article 6 standard consent)",
            "Explicit consent requires an express statement, standalone affirmation, separate checkbox, and clear explanation of the specific sensitive data risks",
            "Cannot rely on standard contractual necessity (Art 6(1)(b)) or legitimate interests (Art 6(1)(f)) for Article 9 data"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of worldwide turnover under Article 83(5)(a).",
        "statutory_text": "Article 9(1): Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs... genetic data, biometric data... data concerning health or data concerning a natural person's sex life or sexual orientation shall be prohibited. Article 9(2)(a): Paragraph 1 shall not apply if the data subject has given explicit consent...",
        "practical_application": "If an app processes health metrics, biometric scans, or religious affiliations, a separate explicit opt-in checkbox with clear risk warnings is mandatory prior to ingestion.",
        "keywords": ["article 9", "special category data", "health data", "biometrics", "explicit consent", "religious beliefs"]
    },

    # =========================================================================
    # PART 2: INDIA DIGITAL PERSONAL DATA PROTECTION ACT, 2023 (ACT NO. 22 OF 2023)
    # =========================================================================
    {
        "id": "IN-DPDPA-SEC-04-05",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 4 & Section 5",
        "category": "Notice & Grounds for Processing",
        "title": "Grounds for Processing & Mandatory Itemised Notice",
        "summary": "Under Section 4, personal data may be processed only in accordance with the provisions of the Act and for a lawful purpose for which the Data Principal has given consent (Sec 6) or for certain legitimate uses (Sec 7). Under Section 5, on or before requesting consent, the Data Fiduciary must give an itemised notice in clear and plain language.",
        "key_requirements": [
            "Section 4: Processing permissible ONLY for: (a) consent, or (b) certain legitimate uses under Section 7",
            "Section 5(1): Statutory Itemised Notice must specify: (i) personal data to be processed and purpose; (ii) manner of exercising right of withdrawal of consent and grievance redressal under Sec 13; (iii) manner of making complaint to the Data Protection Board of India (DPBI)",
            "Section 5(3): Notice must be accessible in English or any of the 22 languages specified in the Eighth Schedule to the Constitution of India",
            "Section 5(2): For consent given prior to commencement of Act, notice must be given as soon as reasonably practicable"
        ],
        "penalties": "Breach of notice obligations falls under the general penalty provision: May extend to ₹50 Crore (~£5 Million) under Item 6 of the Schedule.",
        "statutory_text": "Section 4(1): A person may process the personal data of a Data Principal only in accordance with the provisions of this Act and for a lawful purpose: (a) for which the Data Principal has given her consent; or (b) for certain legitimate uses. Section 5(1): On or before requesting consent, the Data Fiduciary shall give to the Data Principal an itemised notice in clear and plain language...",
        "practical_application": "Registration screen for Indian users must provide a language selector (Hindi, Bengali, Tamil, etc.) and an itemised notice stating exact personal data collected, grievance officer contact, and right to complain to DPBI.",
        "keywords": ["dpdpa 2023", "section 4", "section 5", "itemised notice", "22 scheduled languages", "grounds for processing", "data fiduciary"]
    },
    {
        "id": "IN-DPDPA-SEC-06",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 6(1)-(9)",
        "category": "Consent Architecture",
        "title": "Consent Conditions, Unconditional Mandate & Consent Managers",
        "summary": "Consent given by the Data Principal must be free, specific, informed, unconditional and unambiguous with a clear affirmative action, signifying agreement to processing for the specified purpose, limited to necessary data. Crucially, Section 6(2) provides that consent cannot be made a condition for providing services if the data is not necessary for that purpose.",
        "key_requirements": [
            "Section 6(1): Consent must be free, specific, informed, unconditional, and unambiguous with clear affirmative action",
            "Section 6(2): Unconditional requirement: Data Fiduciary cannot condition the provision of goods/services on consent to process data not necessary for that purpose",
            "Section 6(4): Right to withdraw consent at any time; withdrawal takes effect immediately. Crucially: withdrawal shall not affect the lawfulness of processing based on consent before its withdrawal",
            "Section 6(6): Upon withdrawal, Data Fiduciary and its Data Processors MUST cease processing personal data, unless required or authorised under the Act or any other law",
            "Section 6(7)-(9): Data Principal may give, manage, review or withdraw consent through an accessible, registered Consent Manager",
            "Section 6(10): Burden of proof is on the Data Fiduciary to prove that valid notice was given and consent obtained"
        ],
        "penalties": "Unlawful processing without valid consent falls under Item 6 of the Schedule: May extend to ₹50 Crore (~£5 Million).",
        "statutory_text": "Section 6(1): The consent given by the Data Principal shall be free, specific, informed, unconditional and unambiguous with a clear affirmative action... Section 6(4): The Data Principal shall have the right to withdraw her consent at any time, with the ease of doing so being comparable to the ease with which consent was given. Section 6(6): The consequence of the withdrawal of consent shall be that the Data Fiduciary shall, within a reasonable time, cease and cause its Data Processors to cease processing personal data...",
        "practical_application": "Unbundle marketing checkboxes. A user buying an e-commerce item cannot be forced to consent to marketing profiling as a condition of checkout. Implement instant consent withdrawal hooks.",
        "keywords": ["section 6", "unconditional consent", "clear affirmative action", "consent withdrawal", "consent manager", "burden of proof"]
    },
    {
        "id": "IN-DPDPA-SEC-07-LEGITIMATE-USES",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 7",
        "category": "Certain Legitimate Uses",
        "title": "Certain Legitimate Uses (Strict Statutory Exhaustive Grounds — NO General Legitimate Interests)",
        "summary": "Section 7 specifies the exhaustive statutory situations where personal data may be processed without consent for 'Certain Legitimate Uses'. Unlike the GDPR which provides a broad, open-ended 'legitimate interests' ground under Article 6(1)(f), India's DPDP Act 2023 does NOT permit general commercial or business legitimate interests. Processing under Section 7 is strictly confined to the statutory grounds enumerated.",
        "key_requirements": [
            "CRITICAL DISTINCTION FROM GDPR: India DPDP Act 2023 DOES NOT have a general 'legitimate interests' basis like GDPR Article 6(1)(f)",
            "Commercial marketing, customer profiling, and behavioural targeted advertising CANNOT be justified under Section 7; they require valid Section 6 consent",
            "Exhaustive Section 7 grounds include: (a) specified purpose for which Data Principal voluntarily provided personal data without indicating withholding of consent; (b) state subsidies, benefits, certificates; (c) performance of function under Indian law or sovereignty/security; (d) compliance with judgment/order under law; (e) medical emergency involving threat to life/health; (f) taking measures to provide medical treatment during epidemic/disaster; (g) employment purposes and safeguarding employer from loss/liability",
            "Any processing outside Section 7 requires affirmative Section 6 consent"
        ],
        "penalties": "Processing without consent and outside Section 7 legitimate uses carries penalties up to ₹50 Crore under Item 6 of the Schedule.",
        "statutory_text": "Section 7: A Data Fiduciary may process personal data of a Data Principal for any of following certain legitimate uses: (a) for the specified purpose for which the Data Principal has voluntarily provided her personal data to the Data Fiduciary, and in respect of which she has not indicated to the Data Fiduciary that she does not consent to the use of her personal data; (b) for the State to provide subsidy, benefit, service; (c) for the performance by the State of any function under any law; (d) for compliance with any judgment/order; (e) for responding to a medical emergency; (g) for the purposes of employment...",
        "practical_application": "Never tell an Indian client that they can rely on 'legitimate interests' to run targeted advertising or marketing profiling. In India, targeted commercial marketing strictly requires Section 6 consent.",
        "keywords": ["section 7", "certain legitimate uses", "no legitimate interests", "voluntary provision", "employment purpose", "medical emergency", "state benefits"]
    },
    {
        "id": "IN-DPDPA-SEC-08",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 8(1)-(11)",
        "category": "Fiduciary Obligations & Security",
        "title": "General Obligations of Data Fiduciary: Security Safeguards, Breach Reporting & Mandatory Erasure",
        "summary": "Section 8 sets out the fundamental obligations of a Data Fiduciary: ensuring accuracy of data (Sec 8(3)), implementing reasonable security safeguards to prevent personal data breach (Sec 8(5)), giving intimation of personal data breaches to the Board and affected Data Principals (Sec 8(6)), and mandatory erasure of personal data upon withdrawal of consent or purpose fulfillment (Sec 8(7)).",
        "key_requirements": [
            "Section 8(5): Must protect personal data by taking REASONABLE SECURITY SAFEGUARDS to prevent personal data breach (e.g. encryption, access control, audit logs)",
            "Section 8(6): In event of a personal data breach, MUST give intimation of breach to the Data Protection Board of India (DPBI) and to EACH affected Data Principal in prescribed form",
            "Section 8(7): MANDATORY ERASURE: Must erase personal data as soon as Data Principal withdraws consent or it is reasonable to assume specified purpose is no longer being served (purpose fulfillment)",
            "Section 8(8): Must publish business contact details of Data Protection Officer (if SDF) or person who can answer questions on behalf of Data Fiduciary",
            "Section 8(9): Must establish effective grievance redressal mechanism",
            "Section 8(2): Data Fiduciary may engage a Data Processor only under a valid contract, and remains responsible for processor compliance"
        ],
        "penalties": "SCHEDULE PENALTIES: Section 8(5) failure to take reasonable security safeguards to prevent personal data breach carries up to ₹250 CRORE (Item 1). Section 8(6) failure to notify Board/affected individuals carries up to ₹200 CRORE (Item 2). Other Section 8 breaches carry up to ₹50 Crore (Item 6).",
        "statutory_text": "Section 8(5): A Data Fiduciary shall protect personal data in its possession or under its control, including in respect of any processing undertaken by it or on its behalf by a Data Processor, by taking reasonable security safeguards to prevent personal data breach. Section 8(6): In the event of a personal data breach, the Data Fiduciary shall give the Board and each affected Data Principal, intimation of such breach... Section 8(7): A Data Fiduciary shall, upon a Data Principal withdrawing her consent, or as soon as it is reasonable to assume that the specified purpose is no longer being served, erase personal data...",
        "practical_application": "Enforce field-level encryption (AES-256) on sensitive database columns. Implement automated 30-day retention purge routines. Formulate a 24-hour breach response runbook notifying DPBI and users.",
        "keywords": ["section 8", "section 8(5)", "section 8(6)", "section 8(7)", "reasonable security safeguards", "breach notification", "mandatory erasure", "250 crore", "200 crore"]
    },
    {
        "id": "IN-DPDPA-SEC-09",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 9(1)-(3)",
        "category": "Children & Disability Protection",
        "title": "Verifiable Parental Consent & Absolute Prohibition on Tracking/Targeted Advertising to Children",
        "summary": "Section 9 mandates that before processing any personal data of a child (defined as an individual who has not completed 18 years of age) or a person with disability with a lawful guardian, the Data Fiduciary must obtain verifiable parental consent. Section 9(2) strictly prohibits tracking, behavioural monitoring, or targeted advertising directed at children.",
        "key_requirements": [
            "Child definition: Under Section 2(f), an individual who has not completed 18 years of age",
            "Section 9(1): Mandatory verifiable parental consent before processing any personal data of a child",
            "Section 9(2): ABSOLUTE STATUTORY PROHIBITION on tracking or behavioural monitoring of children or targeted advertising directed at children",
            "Section 9(3): Prohibition on processing personal data that is likely to cause any detrimental effect on the well-being of a child"
        ],
        "penalties": "SCHEDULE PENALTIES: Breach in observance of additional obligations in relation to children under Section 9 carries a statutory penalty up to ₹200 CRORE (~£20 Million) under Item 3 of the Schedule.",
        "statutory_text": "Section 9(1): The Data Fiduciary shall, before processing any personal data of a child or a person with disability who has a lawful guardian, obtain verifiable consent of the parent of such child or the lawful guardian... Section 9(2): A Data Fiduciary shall not undertake tracking or behavioural monitoring of children or targeted advertising directed at children. Section 9(3): A Data Fiduciary shall not undertake any processing of personal data that is likely to cause any detrimental effect on the well-being of a child.",
        "practical_application": "Any platform accessible to minors must implement an age-verification gate. If user is under 18, all advertising tracking, profiling cookies, and recommendation algorithms must be completely disabled.",
        "keywords": ["section 9", "children's data", "under 18", "verifiable parental consent", "prohibition on tracking", "targeted advertising to children", "200 crore"]
    },
    {
        "id": "IN-DPDPA-SEC-10",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 10(1)-(2)",
        "category": "Significant Data Fiduciary",
        "title": "Additional Obligations of Significant Data Fiduciary (SDF)",
        "summary": "The Central Government may notify any Data Fiduciary as a Significant Data Fiduciary (SDF) based on volume and sensitivity of data, risk to rights, sovereignty, security of State, or public order. SDFs have heightened statutory compliance burdens.",
        "key_requirements": [
            "Section 10(2)(a): Must appoint a Data Protection Officer (DPO) who shall be an individual based in India, representing the SDF and reporting to Board of Directors",
            "Section 10(2)(b): Must appoint an Independent Data Auditor to evaluate compliance audits",
            "Section 10(2)(c): Must undertake periodic Data Protection Impact Assessment (DPIA) and periodic compliance audits",
            "Section 10(2)(d): Must undertake other measures including algorithmic audits and security testing"
        ],
        "penalties": "SCHEDULE PENALTIES: Breach of SDF obligations under Section 10 carries a penalty up to ₹150 CRORE (~£15 Million) under Item 4 of the Schedule.",
        "statutory_text": "Section 10(2): The Significant Data Fiduciary shall: (a) appoint a Data Protection Officer who shall: (i) represent the Significant Data Fiduciary; and (ii) be an individual based in India; (b) appoint an independent data auditor to evaluate compliance; (c) undertake Data Protection Impact Assessment and periodic audits...",
        "practical_application": "Large tech platforms and high-volume data processors in India must recruit a resident Indian DPO and conduct formal DPIAs with independent auditors.",
        "keywords": ["section 10", "significant data fiduciary", "sdf", "resident dpo india", "independent data auditor", "dpia india", "150 crore"]
    },
    {
        "id": "IN-DPDPA-SEC-11-ACCESS",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 11",
        "category": "Data Principal Rights",
        "title": "Right to Access Information about Personal Data",
        "summary": "Section 11 grants the Data Principal the right to obtain from the Data Fiduciary to whom she has previously given consent or with whom data was processed under Section 7: (a) a summary of personal data being processed and processing activities; (b) identities of all other Data Fiduciaries and Data Processors with whom personal data has been shared, along with description of data shared; and (c) any other prescribed information.",
        "key_requirements": [
            "Section 11(1)(a): Right to receive a summary of personal data being processed and the processing activities undertaken",
            "Section 11(1)(b): Right to know the identities of ALL other Data Fiduciaries and Data Processors with whom personal data has been shared by the Data Fiduciary, and description of the data shared",
            "Section 11(1)(c): Right to any other information as may be prescribed by Central Government",
            "Exception (Sec 11(2)): Sharing details do not apply to data shared with another Data Fiduciary authorized by law for prevention, detection, or investigation of offenses or cyber incidents"
        ],
        "penalties": "Failure to honor Section 11 access rights carries statutory penalties up to ₹50 Crore under Item 6 of the Schedule.",
        "statutory_text": "Section 11(1): The Data Principal shall have the right to obtain from the Data Fiduciary to whom she has previously given consent...: (a) a summary of personal data which is being processed by such Data Fiduciary and the processing activities undertaken by that Data Fiduciary with respect to such personal data; (b) the identities of all other Data Fiduciaries and Data Processors with whom the personal data has been shared by such Data Fiduciary, along with a description of the personal data so shared; and (c) any other information as may be prescribed.",
        "practical_application": "Indian applications must provide a privacy dashboard where users can see exactly what data is held and a list of all third-party vendors (Stripe, AWS, analytics) with whom their data has been shared.",
        "keywords": ["section 11", "right to access information", "identities of processors", "summary of processing", "shared personal data", "data principal rights"]
    },
    {
        "id": "IN-DPDPA-SEC-12-CORRECTION-ERASURE",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 12",
        "category": "Data Principal Rights",
        "title": "Right to Correction, Completion, Updating and Erasure of Personal Data",
        "summary": "Section 12 gives the Data Principal the right to correction, completion, updating, and erasure of her personal data. The Data Fiduciary is mandated to correct inaccurate data, complete incomplete data, update outdated data, and erase personal data unless retention is necessary for the specified purpose or for compliance with any law.",
        "key_requirements": [
            "Section 12(1): Right to correction, completion, updating, and erasure of personal data",
            "Section 12(2)(a): Data Fiduciary shall correct inaccurate or misleading personal data",
            "Section 12(2)(b): Data Fiduciary shall complete incomplete personal data",
            "Section 12(2)(c): Data Fiduciary shall update personal data",
            "Section 12(2)(d): Data Fiduciary shall erase personal data that is no longer necessary for the specified purpose or upon withdrawal of consent",
            "Section 12(3): RETENTION EXCEPTION: Data Fiduciary is NOT required to erase personal data if retention is necessary for the specified purpose or for compliance with any law in force"
        ],
        "penalties": "Failure to honor Section 12 correction/erasure duties carries statutory penalties up to ₹50 Crore under Item 6 of the Schedule.",
        "statutory_text": "Section 12(1): A Data Principal shall have the right to correction, completion, updating and erasure of her personal data for the processing of which she has previously given consent... Section 12(2): The Data Fiduciary shall, upon receiving a request: (a) correct the inaccurate or misleading personal data; (b) complete the incomplete personal data; (c) update the personal data; (d) erase the personal data... Section 12(3): A Data Fiduciary shall not be required to erase personal data under sub-section (2) where retention of such personal data is necessary for the specified purpose or for compliance with any law for the time being in force.",
        "practical_application": "Provide self-service profile updating and account deletion in app settings. If user requests deletion, wipe marketing and tracking data, but retain statutory tax invoices for the 7-year GST limitation period.",
        "keywords": ["section 12", "correction", "completion", "updating", "erasure", "deletion", "retention exception", "compliance with law"]
    },
    {
        "id": "IN-DPDPA-SEC-13",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 13(1)-(3)",
        "category": "Grievance Redressal",
        "title": "Right of Grievance Redressal, Grievance Officer & Mandatory Exhaustion of Internal Remedies",
        "summary": "Section 13 establishes the Data Principal's right of grievance redressal regarding acts or omissions of the Data Fiduciary or Consent Manager. The Fiduciary must establish an easily accessible redressal mechanism. Crucially, Section 13(3) provides that the Data Principal must exhaust the opportunity of redressal provided by the Fiduciary before making a complaint to the Data Protection Board of India (DPBI).",
        "key_requirements": [
            "Section 13(1): Right of grievance redressal in respect of any act or omission of the Data Fiduciary regarding obligations under the Act",
            "Section 13(2): Data Fiduciary / Consent Manager MUST establish an effective grievance redressal mechanism and publish Grievance Officer details",
            "Section 13(3): MANDATORY EXHAUSTION: Data Principal must first exhaust internal grievance redressal before making a complaint to the Data Protection Board of India (DPBI)",
            "Grievances must be resolved within the timeline prescribed by the Central Government"
        ],
        "penalties": "Breach of grievance redressal obligations carries statutory penalties up to ₹50 Crore under Item 6 of the Schedule.",
        "statutory_text": "Section 13(1): A Data Principal shall have the right of grievance redressal in respect of any act or omission of Data Fiduciary or Consent Manager regarding performance of its obligations... Section 13(2): The Data Fiduciary or Consent Manager shall establish an effective redressal mechanism... Section 13(3): The Data Principal shall exhaust the opportunity of redressal provided by Data Fiduciary or Consent Manager before making a complaint to the Board.",
        "practical_application": "Designate a Grievance Redressal Officer with name, official email, phone, and address clearly displayed in the privacy policy and settings footer.",
        "keywords": ["section 13", "grievance redressal", "grievance officer", "complaint to board", "dpbi", "exhaustion of remedies"]
    },
    {
        "id": "IN-DPDPA-SEC-14-NOMINATE",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 14",
        "category": "Data Principal Rights",
        "title": "Right to Nominate Representative in Event of Death or Incapacity",
        "summary": "Section 14 grants the Data Principal the right to nominate any other individual who shall, in the event of death or incapacity of the Data Principal, exercise the rights of the Data Principal under the Act.",
        "key_requirements": [
            "Right to nominate another individual in event of death or incapacity of Data Principal",
            "'Incapacity' means inability to exercise rights due to unsoundness of mind or physical infirmity",
            "Nominee can exercise access, correction, and erasure rights on behalf of deceased or incapacitated individual"
        ],
        "penalties": "Statutory fine up to ₹50 Crore under Item 6 of the Schedule.",
        "statutory_text": "Section 14(1): A Data Principal shall have the right to nominate, in such manner as may be prescribed, any other individual, who shall, in the event of death or incapacity of the Data Principal, exercise the rights of the Data Principal in accordance with the provisions of this Act.",
        "practical_application": "Include an optional 'Digital Nominee' field in account security settings where users can name an emergency contact or representative.",
        "keywords": ["section 14", "right to nominate", "nominee", "death or incapacity", "digital inheritance", "data principal rights"]
    },
    {
        "id": "IN-DPDPA-SEC-15-DUTIES",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 15",
        "category": "Duties of Data Principal",
        "title": "Statutory Duties of Data Principal & Penalty for Frivolous Complaints",
        "summary": "Section 15 establishes that a Data Principal has statutory duties while exercising rights or providing information: not to impersonate, not to suppress material information, not to register false or frivolous grievances or complaints with the Board.",
        "key_requirements": [
            "Section 15(a): Comply with the provisions of all applicable laws while exercising rights",
            "Section 15(b): Ensure not to impersonate another person while providing personal data",
            "Section 15(c): Ensure not to suppress any material information while providing personal data for state document/identifier/service",
            "Section 15(d): Ensure not to register a false or frivolous grievance or complaint with Data Fiduciary or the Board"
        ],
        "penalties": "SCHEDULE PENALTIES: Breach in observance of the duties of Data Principal under Section 15 carries a statutory penalty up to ₹10,000 (Rupees Ten Thousand) under Item 5 of the Schedule.",
        "statutory_text": "Section 15: A Data Principal shall perform the following duties, namely: (a) comply with provisions of all applicable laws; (b) ensure not to impersonate another person; (c) ensure not to suppress any material information; (d) ensure not to register a false or frivolous grievance or complaint with Data Fiduciary or the Board.",
        "practical_application": "Display user notice during signup: 'Users are legally bound under Section 15 of DPDP Act 2023 not to furnish false details or impersonate others, subject to statutory penalties.'",
        "keywords": ["section 15", "duties of data principal", "impersonation", "false grievance", "frivolous complaint", "10000 rupees penalty"]
    },
    {
        "id": "IN-DPDPA-SCHEDULE-PENALTIES",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 The Schedule (Penalties Matrix)",
        "category": "Statutory Penalties",
        "title": "The Schedule to DPDP Act 2023: Complete Statutory Penalties Matrix",
        "summary": "Section 33(1) read with The Schedule to the Digital Personal Data Protection Act, 2023 prescribes the exact monetary penalties that may be imposed by the Data Protection Board of India (DPBI) for specific violations.",
        "key_requirements": [
            "Item 1: Breach in observing obligation to take reasonable security safeguards to prevent personal data breach under sub-section (5) of section 8 -> Significant penalty may extend to 250 CRORE RUPEES (₹250 Crore)",
            "Item 2: Breach in observing obligation to give the Board or affected Data Principal intimation of personal data breach under sub-section (6) of section 8 -> May extend to 200 CRORE RUPEES (₹200 Crore)",
            "Item 3: Breach in observance of additional obligations in relation to children under section 9 -> May extend to 200 CRORE RUPEES (₹200 Crore)",
            "Item 4: Breach in observance of additional obligations of Significant Data Fiduciary under section 10 -> May extend to 150 CRORE RUPEES (₹150 Crore)",
            "Item 5: Breach in observance of the duties of Data Principal under section 15 -> May extend to 10,000 RUPEES (₹10,000)",
            "Item 6: Breach of any other provision of this Act or the rules made thereunder -> May extend to 50 CRORE RUPEES (₹50 Crore)"
        ],
        "penalties": "Maximum penalties range up to ₹250 Crore. The Board considers nature, gravity, duration, repetitive nature, and mitigation steps taken under Section 33(2).",
        "statutory_text": "THE SCHEDULE [See section 33(1)]: (1) Breach in observing obligation to take reasonable security safeguards under section 8(5): up to 250 crore rupees; (2) Breach in observing obligation to give intimation of breach under section 8(6): up to 200 crore rupees; (3) Breach in observance of additional obligations in relation to children under section 9: up to 200 crore rupees; (4) Breach in observance of additional obligations of Significant Data Fiduciary under section 10: up to 150 crore rupees; (5) Breach in observance of duties under section 15: up to 10,000 rupees; (6) Breach of any other provision: up to 50 crore rupees.",
        "practical_application": "Ensure legal and security executives understand: Failing to prevent a breach is up to ₹250 Crore; failing to notify is up to ₹200 Crore; child tracking is up to ₹200 Crore; any other general breach is up to ₹50 Crore.",
        "keywords": ["the schedule", "penalties", "250 crore", "200 crore", "150 crore", "50 crore", "10000 rupees", "section 33", "dpbi fines"]
    },

    # =========================================================================
    # PART 2B: PECR (COOKIES & TELEMETRY REGULATIONS)
    # =========================================================================
    {
        "id": "ICO-PECR-REG-06",
        "jurisdiction": "PECR",
        "statute": "Privacy and Electronic Communications Regulations 2003",
        "citation": "PECR Regulation 6 & ICO Guidance on Cookies and Mobile App Tracking",
        "category": "Cookies & Mobile Telemetry",
        "title": "Consent for Storing or Accessing Information on User Devices",
        "summary": "Storing information, or gaining access to information stored, in the terminal equipment of a subscriber or user is only permitted if the subscriber or user is provided with clear and comprehensive information about the purposes and has given consent, unless strictly necessary for the delivery of an explicitly requested service.",
        "key_requirements": [
            "Applies equally to website cookies AND mobile application SDK telemetry (e.g. Firebase, PostHog, AppsFlyer)",
            "Strict opt-in consent: Analytics, advertising, and session replay trackers must remain OFF until user clicks Accept",
            "No cookie walls or forced consent banners",
            "Strictly Necessary exemption: ONLY applies to essential technical features (login session cookie, shopping basket, security)",
            "Must provide granular choice to reject non-essential cookies and revoke consent at any time"
        ],
        "penalties": "UK ICO statutory enforcement notices and fines up to £500,000 under PECR, plus UK GDPR Article 6/7 fines up to £17.5M for unconsented personal data tracking.",
        "statutory_text": "A person shall not store or gain access to information stored, in the terminal equipment of a subscriber or user, unless the subscriber or user of that terminal equipment: (a) is provided with clear and comprehensive information about the purposes of the storage of, or access to, that information; and (b) has given his or her consent. Paragraph (1) does not apply to the technical storage of, or access to, information: (a) for the sole purpose of carrying out the transmission of a communication; or (b) strictly necessary in order for the service provider to deliver a service explicitly requested by the subscriber.",
        "practical_application": "Deploy an unticked cookie banner. Ensure Google Analytics, PostHog, or tracking SDKs are initialized ONLY after the user clicks 'Accept Non-Essential Cookies'.",
        "keywords": ["pecr", "regulation 6", "cookies", "tracking", "sdk telemetry", "device storage", "opt-in consent", "cookie banner", "mobile tracking", "posthog", "analytics consent"]
    },

    # =========================================================================
    # PART 3: CROSS-JURISDICTIONAL POLICY ARCHITECTURE & MODEL CLAUSES
    # =========================================================================
    {
        "id": "UNIFIED-PRIVACY-POLICY-ARCHITECTURE",
        "jurisdiction": "CROSS_BORDER",
        "statute": "UK/EU GDPR & India DPDP Act 2023",
        "citation": "Multi-Jurisdictional Privacy Policy Architecture",
        "category": "Corporate Governance",
        "title": "Design Principles for Unified Global Privacy Policy across UK/EU & India",
        "summary": "A multinational company operating in both the UK/EU and India CAN use a unified privacy policy, provided it is structured modularly. A single generic policy that merges or dilutes statutory distinctions violates transparency. The compliant approach is a Global Core Privacy Statement accompanied by distinct, legally tailored Regional Addenda / Schedules for UK/EU GDPR and India DPDPA.",
        "key_requirements": [
            "Companies CAN maintain a unified global privacy policy architecture; claiming it is strictly prohibited is legally false",
            "Modular Structure: Core Global Section (data collected, general security, cookies, company identity) + Jurisdiction-Specific Addenda",
            "UK/EU Schedule must specify: Article 6 lawful bases (distinguishing consent from legitimate interests), Article 9 explicit consent, Article 21 right to object, Chapter V transfer mechanisms (IDTA/SCCs), and ICO/supervisory authority rights",
            "India DPDP Schedule must specify: Section 5 itemised notice, multilingual access (22 scheduled languages), Section 6 unconditional consent, Section 7 legitimate uses (no commercial legitimate interests), Section 13 Grievance Redressal Officer contact details and escalation to DPBI, Section 14 right to nominate, Section 9 child consent verification",
            "Consent UI: Consent mechanisms cannot be bundled together across jurisdictions where statutory standards differ (e.g. India requires unconditional standalone consent without bundled marketing)"
        ],
        "penalties": "Misleading or unbundled policy notices violate GDPR Article 12/13 (£17.5M fine) and DPDP Act Section 5/6 (₹50 Crore fine).",
        "statutory_text": "A unified policy is legally permissible provided it transparently informs data subjects in each jurisdiction of their distinct statutory rights and lawful grounds without conflating separate legal requirements.",
        "practical_application": "Structure website privacy policy as: 'Global Privacy Policy', with expandable tabs for 'UK & EU Data Protection Addendum' and 'India DPDP Act 2023 Addendum'.",
        "keywords": ["unified privacy policy", "multi-jurisdiction policy", "global policy", "uk gdpr and dpdp act", "regional addenda", "modular privacy notice"]
    },
    {
        "id": "MODEL-CLAUSE-RETENTION",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 5(1)(e) & DPDPA Sec 8(7)",
        "citation": "Statutory Model Clause: Storage Limitation & Data Retention",
        "category": "Model Clause",
        "title": "Compliant Data Retention & Statutory Erasure Clause",
        "summary": "Universal statutory model clause establishing purpose-specific retention schedules and legal retention exceptions.",
        "key_requirements": [
            "Itemised retention by purpose (not indefinite)",
            "Clear erasure triggers upon consent withdrawal or purpose fulfillment",
            "Explicit exceptions for statutory legal obligations (tax, financial records) and legal claims"
        ],
        "penalties": "Protects against ICO Article 5(1)(e) and DPBI Section 8(7) enforcement actions.",
        "statutory_text": "DATA RETENTION & PURPOSE-FULFILLMENT ERASURE:\n'We retain personal data strictly for as long as necessary to fulfill the purposes for which it was collected or to comply with applicable statutory obligations:\n1. User Account Data: Retained for the active duration of your account and erased within 30 days of verified deletion request or account closure.\n2. Customer Service & Communications: Retained for 90 days following inquiry resolution, then permanently purged.\n3. Marketing & Profiling Telemetry: Retained until consent is withdrawn or an objection under GDPR Article 21 / DPDP Act Section 6 is received, upon which marketing data is purged and your identifier is placed on a minimal suppression list.\n4. Billing, Invoicing & Financial Transactions: Retained for statutory periods mandated by applicable tax and accounting laws (e.g. 6 years under UK HMRC regulations and 7 years under Indian GST and Income Tax Acts).\n5. Dispute Resolution & Legal Claims: Retained as necessary for statutory limitation periods to establish, exercise or defend legal claims pursuant to GDPR Article 17(3)(e) and DPDP Act Section 12(3).'\nUpon expiration of the retention schedule, personal data is permanently deleted or irreversibly anonymised.",
        "practical_application": "Replace any clause stating 'we retain data for as long as necessary for our business needs' with this statutory model clause.",
        "keywords": ["model clause", "retention schedule", "storage limitation", "erasure timeline", "hmrc 6 years", "gst retention", "legal claims"]
    },
    {
        "id": "MODEL-CLAUSE-OPENAI-GOVERNANCE",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 28 & ICO AI Guidance (2024)",
        "citation": "Statutory Model Clause: Artificial Intelligence & Subprocessor Safeguards",
        "category": "Model Clause",
        "title": "Compliant AI / LLM Data Processing Disclosure Clause",
        "summary": "Universal statutory disclosure explaining how customer queries are processed by AI/LLM providers with zero model training and ephemeral retention.",
        "key_requirements": [
            "Disclose use of Large Language Model subprocessors",
            "Guarantee zero training on user personal prompts",
            "Confirm automated PII scrubbing before API transit",
            "Human oversight in the loop"
        ],
        "penalties": "Mitigates AI transparency and processor DPA violations under Articles 13, 14, and 28.",
        "statutory_text": "ARTIFICIAL INTELLIGENCE & THIRD-PARTY LLM PROCESSING:\n'To provide accelerated automated summaries, data synthesis, and AI-assisted workflows, our platform integrates enterprise AI Large Language Model APIs (specifically OpenAI LLC and Microsoft Azure OpenAI). We enforce strict technical and contractual guardrails under our Data Processing Addendum:\n1. Zero Model Training: Your queries, documents, prompts, and application inputs are never used to train, retrain, or improve public foundational AI models.\n2. Prompt Redaction: Direct personal identifiers (full name, phone number, email address, physical address) are scrubbed or tokenized prior to dispatching prompts to AI endpoints where applicable.\n3. Ephemeral Processing: Prompts are processed ephemerally in volatile memory and not retained on external AI servers beyond technical response generation.\n4. Human Oversight: AI outputs provide automated recommendations and do not make automated decisions producing legal or similarly significant effects without qualified human review.'",
        "practical_application": "Auto-inject into any draft privacy policy or SaaS Terms where OpenAI or Anthropic SDKs are detected.",
        "keywords": ["model clause", "ai disclosure", "openai zero retention", "subprocessor dpa", "human oversight", "ai governance"]
    },
    {
        "id": "MODEL-CLAUSE-ART9-CONSENT",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 9(2)(a) & DPDPA Sec 6",
        "citation": "Statutory Model Clause: Article 9 Explicit Consent",
        "category": "Model Clause",
        "title": "Compliant Explicit Consent Clause for Sensitive / Special Category Data",
        "summary": "Legally binding model clause satisfying UK GDPR Article 9 explicit consent and India DPDP Act Section 6 requirement for health, biometric, or sensitive personal data.",
        "key_requirements": [
            "Separate affirmative checkbox",
            "Clear identification of specific sensitive categories",
            "Explicit statement of processing purpose",
            "Clear revocation instructions"
        ],
        "penalties": "Protects against maximum Article 9 GDPR enforcement fines up to £17.5M.",
        "statutory_text": "EXPLICIT SPECIAL CATEGORY CONSENT (UK GDPR Art 9(2)(a) & DPDP Act 2023 Sec 6):\n'By checking this box, you expressly and affirmatively consent to our collection and processing of sensitive personal data (such as health information, biometric data, or other special category data) strictly for the specific purpose of providing the requested service. You may withdraw this explicit consent at any time through your account privacy settings or by contacting our Privacy Office, without affecting the lawfulness of processing carried out prior to withdrawal.'",
        "practical_application": "Use as a standalone unbundled checkbox whenever sensitive personal data is collected.",
        "keywords": ["model clause", "explicit consent", "special category consent", "article 9 clause"]
    },
    {
        "id": "MODEL-CLAUSE-IDTA-CROSSBORDER",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 46 & DPA 2018 Section 119A",
        "citation": "Statutory Model Clause: UK International Data Transfer Agreement (IDTA)",
        "category": "Model Clause",
        "title": "Compliant UK-to-India Cross-Border Data Transfer Disclosure",
        "summary": "Statutory model clause governing international data transfers between the UK and overseas teams/processors in India under the ICO IDTA.",
        "key_requirements": [
            "Cite lack of UK adequacy finding for India",
            "Incorporate official UK ICO International Data Transfer Agreement (IDTA)",
            "Confirm technical safeguards (encryption, role-based access, zero local export)",
            "Confer third-party beneficiary rights"
        ],
        "penalties": "Protects against cross-border data export injunctions by the UK Information Commissioner.",
        "statutory_text": "INTERNATIONAL DATA TRANSFERS & OVERSEAS PROCESSING (UK GDPR Chapter V):\n'Personal data collected in the United Kingdom may be accessed by our technical engineering, customer support, and cloud administration teams located in the Republic of India. Because India has not received a formal adequacy regulation from the UK Secretary of State, all overseas data access is strictly governed by the official UK Information Commissioner\'s Office (ICO) International Data Transfer Agreement (IDTA) pursuant to Section 119A of the Data Protection Act 2018.\nUnder our IDTA and supplementary technical safeguards: (i) all data access occurs via encrypted remote sessions with zero local device download permissions; (ii) direct personal identifiers are masked or tokenized where technically feasible; (iii) overseas personnel are bound by statutory confidentiality and DPA obligations; and (iv) UK data subjects retain fully enforceable third-party beneficiary rights.'",
        "practical_application": "Auto-replace vague clauses stating 'we may share data with international affiliates from time to time'.",
        "keywords": ["model clause", "idta clause", "international transfer clause", "uk to india transfer", "chapter v disclosure"]
    }
]

import os
import json

LAWYER_CORPUS_FILE = os.path.join(os.path.dirname(__file__), "lawyer_corpus.json")

def get_corpus() -> List[Dict[str, Any]]:
    """Returns the full statutory legal corpus including ingested lawyer PDFs."""
    combined = list(STATUTORY_CORPUS)
    if os.path.exists(LAWYER_CORPUS_FILE):
        try:
            with open(LAWYER_CORPUS_FILE, "r", encoding="utf-8") as f:
                lawyer_chunks = json.load(f)
                combined.extend(lawyer_chunks)
        except Exception:
            pass
    return combined

def get_corpus_stats() -> Dict[str, Any]:
    """Computes high-level statistics of the loaded legal corpus."""
    corpus = get_corpus()
    jurisdictions = {}
    categories = {}
    total_articles = len(corpus)
    
    for chunk in corpus:
        j = chunk.get("jurisdiction", "OTHER")
        c = chunk.get("category", "General")
        jurisdictions[j] = jurisdictions.get(j, 0) + 1
        categories[c] = categories.get(c, 0) + 1

    return {
        "total_chunks": total_articles,
        "jurisdictions": jurisdictions,
        "categories": categories,
        "supported_frameworks": [
            "UK Data Protection Act 2018 (DPA 2018 - Official Legislation)",
            "UK General Data Protection Regulation (UK GDPR)",
            "EU General Data Protection Regulation (EU GDPR 2016/679)",
            "India Digital Personal Data Protection Act, 2023 (DPDP Act 2023)",
            "The Schedule to the DPDP Act 2023 (Penalties Matrix)",
            "UK ICO AI & Generative AI Statutory Guidance (2024)",
            "PECR (Cookies & Telemetry Regulations)",
            "RBI Payment Data Localisation Directives",
            "Cross-Jurisdictional Privacy Policy Architecture"
        ]
    }
