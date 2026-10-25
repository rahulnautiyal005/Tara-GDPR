"""
Tara PrivacyOS — Phase 2 Statutory Legal Corpus
High-fidelity legal knowledge base covering:
1. UK General Data Protection Regulation (UK GDPR) & Data Protection Act 2018 (DPA 2018)
2. UK Information Commissioner's Office (ICO) Statutory Codes & AI Guidance (2024)
3. India Digital Personal Data Protection Act, 2023 (DPDPA 2023) & Rules
4. AI & LLM Data Governance Standards (OpenAI/Azure AI Zero-Retention & PII Safeguards)
5. Statutory Model Clauses for Automated Redlining & Gap Remediation
"""

from typing import List, Dict, Any

STATUTORY_CORPUS: List[Dict[str, Any]] = [
    # =========================================================================
    # UK GDPR: CORE ARTICLES & RECITALS
    # =========================================================================
    {
        "id": "UK-GDPR-ART-05",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 5(1) & 5(2)",
        "category": "Core Principles",
        "title": "Principles Relating to Processing of Personal Data",
        "summary": "Personal data must be processed lawfully, fairly, and transparently; collected for specified, explicit, and legitimate purposes; adequate, relevant, and limited to what is necessary (data minimisation); accurate; kept in a form which permits identification for no longer than necessary (storage limitation); and processed with appropriate security (integrity and confidentiality). The controller is accountable for demonstrating compliance.",
        "key_requirements": [
            "Lawfulness, fairness, and transparency (Art 5(1)(a))",
            "Purpose limitation: no processing incompatible with declared purpose (Art 5(1)(b))",
            "Data minimisation: strictly limited to what is necessary (Art 5(1)(c))",
            "Accuracy and rectification obligation (Art 5(1)(d))",
            "Storage limitation: indefinite retention is strictly illegal (Art 5(1)(e))",
            "Integrity and confidentiality via technical and organisational security (Art 5(1)(f))",
            "Accountability principle: controller must maintain audit proof of compliance (Art 5(2))"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide annual turnover, whichever is higher.",
        "statutory_text": "Personal data shall be: (a) processed lawfully, fairly and in a transparent manner in relation to the data subject; (b) collected for specified, explicit and legitimate purposes; (c) adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed; (d) accurate and, where necessary, kept up to date; (e) kept in a form which permits identification of data subjects for no longer than is necessary; (f) processed in a manner that ensures appropriate security of the personal data.",
        "practical_application": "Web and mobile apps must establish explicit retention schedules (e.g. 30 days for chat queries, 6 years for tax receipts). Storing user prompts or chats forever directly violates Article 5(1)(e).",
        "keywords": ["principles", "data minimisation", "storage limitation", "purpose limitation", "accuracy", "integrity", "accountability", "article 5"]
    },
    {
        "id": "UK-GDPR-ART-06",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 6(1)",
        "category": "Lawful Bases",
        "title": "Lawfulness of Processing (The Six Legal Bases)",
        "summary": "Processing of personal data is lawful only if at least one of the six bases applies: (a) Consent, (b) Contract performance or pre-contractual steps, (c) Legal obligation, (d) Vital interests, (e) Public task, or (f) Legitimate interests (balanced against data subject fundamental rights).",
        "key_requirements": [
            "Identify and document the lawful basis prior to commencing data processing",
            "Cannot retroactively swap lawful bases if the original basis becomes invalid",
            "Consent must satisfy strict Article 7 conditions (unbundled, freely given)",
            "Legitimate interests require a documented 3-part Legitimate Interests Assessment (LIA): Purpose, Necessity, and Balancing test",
            "Direct marketing and non-essential cookies require Consent, not Legitimate Interests"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide annual turnover.",
        "statutory_text": "Processing shall be lawful only if and to the extent that at least one of the following applies: (a) the data subject has given consent to the processing of his or her personal data for one or more specific purposes; (b) processing is necessary for the performance of a contract to which the data subject is party; (c) processing is necessary for compliance with a legal obligation to which the controller is subject; (d) vital interests; (e) public interest or official authority; (f) legitimate interests pursued by the controller or by a third party, except where overridden by the interests or fundamental rights and freedoms of the data subject.",
        "practical_application": "User account authentication and service delivery rely on Contract (Art 6(1)(b)). Tracking cookies and marketing emails require Consent (Art 6(1)(a)). Fraud monitoring relies on Legitimate Interests (Art 6(1)(f)).",
        "keywords": ["lawful basis", "article 6", "consent", "contract", "legitimate interests", "legal obligation", "processing bases"]
    },
    {
        "id": "UK-GDPR-ART-07",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 7",
        "category": "Consent Conditions",
        "title": "Conditions for Lawful Consent",
        "summary": "Where processing is based on consent, the controller must be able to demonstrate that the data subject has consented. Pre-ticked boxes, bundled terms, or conditional access to services are strictly unlawful. The data subject has the right to withdraw consent at any time, as easily as it was given.",
        "key_requirements": [
            "Controller must maintain verifiable audit log of consent (timestamp, identity, version of notice)",
            "Consent request must be clearly distinguishable from other matters in plain language",
            "Pre-ticked consent checkboxes are prohibited under UK and EU caselaw (Planet49)",
            "Tying service provision to consent for unnecessary secondary processing is invalid (Art 7(4))",
            "Withdrawal of consent must be as easy as giving consent (one-click toggle in settings)"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide turnover.",
        "statutory_text": "1. Where processing is based on consent, the controller shall be able to demonstrate that the data subject has consented to processing of his or her personal data. 2. If the data subject's consent is given in the context of a written declaration which also concerns other matters, the request for consent shall be presented in a manner which is clearly distinguishable from the other matters, in an intelligible and easily accessible form, using clear and plain language. 3. The data subject shall have the right to withdraw his or her consent at any time. It shall be as easy to withdraw as to give consent. 4. When assessing whether consent is freely given, utmost account shall be taken of whether the performance of a contract is conditional on consent to the processing of personal data that is not necessary for the performance of that contract.",
        "practical_application": "Registration and checkout forms must never bundle marketing or analytics consent into Terms of Service. Checkboxes must remain unticked by default, and user profile settings must provide a live 'Withdraw Consent' toggle.",
        "keywords": ["consent", "article 7", "unbundled consent", "withdraw consent", "pre-ticked boxes", "freely given", "planet49"]
    },
    {
        "id": "UK-GDPR-ART-09",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 9(1) & 9(2)(a)",
        "category": "Special Category Data",
        "title": "Processing of Special Categories of Personal Data",
        "summary": "Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, genetic data, biometric data, data concerning health, or data concerning a natural person's sex life or sexual orientation is strictly prohibited, unless a specific exemption under Article 9(2) applies, most notably explicit consent under Article 9(2)(a).",
        "key_requirements": [
            "General prohibition on processing special category data without an Article 9(2) gateway",
            "Article 9(2)(a) requires EXPLICIT consent: a separate, specific affirmative statement expressly naming the sensitive data category",
            "Standard Article 6 consent is insufficient for health, spiritual, astrological, or relationship data",
            "Mandatory Data Protection Impact Assessment (DPIA) under Article 35 before collecting special category data at scale",
            "Enhanced security: field-level encryption, role-based masking, strict access logs"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide annual turnover. UK ICO treats unconsented Article 9 processing as an existential regulatory violation.",
        "statutory_text": "1. Processing of personal data revealing racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, and the processing of genetic data, biometric data for the purpose of uniquely identifying a natural person, data concerning health or data concerning a natural person's sex life or sexual orientation shall be prohibited. 2. Paragraph 1 shall not apply if one of the following applies: (a) the data subject has given explicit consent to the processing of those personal data for one or more specified purposes...",
        "practical_application": "Apps collecting spiritual queries, astrology charts, medical symptoms, or relationship advice MUST present an unticked checkbox: 'I explicitly consent to Tara processing my sensitive health and spiritual consultation data in accordance with the Privacy Notice.'",
        "keywords": ["article 9", "special category data", "explicit consent", "health data", "religious beliefs", "philosophical beliefs", "sexual orientation", "sensitive data", "dpia"]
    },
    {
        "id": "UK-GDPR-ART-17",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 17",
        "category": "Data Subject Rights",
        "title": "Right to Erasure ('Right to be Forgotten')",
        "summary": "The data subject has the right to obtain from the controller the erasure of personal data without undue delay where data is no longer necessary for original purposes, consent is withdrawn, or data was unlawfully processed. Controllers must also notify third-party processors and subprocessors to erase all copies, caches, and backups.",
        "key_requirements": [
            "Must respond and execute statutory erasure requests within one calendar month (Art 12(3))",
            "Erasure is mandatory when consent is withdrawn (Art 17(1)(b)) or processing lacks lawful basis",
            "Controller must cascade deletion instructions to all subprocessors (OpenAI, AWS, analytics, CRM)",
            "Statutory exceptions apply: tax/financial audit records (HMRC 6-year retention), legal defense claims",
            "Engineering implementation: Soft-delete + cryptographic purge of personal identifiers within 30 days"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide turnover.",
        "statutory_text": "1. The data subject shall have the right to obtain from the controller the erasure of personal data concerning him or her without undue delay and the controller shall have the obligation to erase personal data without undue delay where: (a) the personal data are no longer necessary in relation to the purposes for which they were collected or otherwise processed; (b) the data subject withdraws consent... and where there is no other legal ground for the processing; (c) the data subject objects to the processing... 2. Where the controller has made the personal data public and is obliged pursuant to paragraph 1 to erase the personal data, the controller... shall take reasonable steps, including technical measures, to inform controllers which are processing the personal data that the data subject has requested the erasure by such controllers of any links to, or copy or replication of, those personal data.",
        "practical_application": "Backend must expose automated self-service account deletion (e.g. DELETE /api/user/account) and automated webhooks to purge cached transcripts across external AI models and cloud database shards.",
        "keywords": ["right to erasure", "right to be forgotten", "article 17", "data deletion", "dsar", "account deletion", "subprocessor purge"]
    },
    {
        "id": "UK-GDPR-ART-20",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 20",
        "category": "Data Subject Rights",
        "title": "Right to Data Portability",
        "summary": "The data subject has the right to receive personal data concerning them, which they provided to a controller, in a structured, commonly used, and machine-readable format (e.g. JSON or CSV), and have the right to transmit those data to another controller without hindrance.",
        "key_requirements": [
            "Applies to data processed by automated means based on Consent or Contract (Art 6(1)(b))",
            "Must provide export in standard formats: JSON, XML, or CSV",
            "Must be delivered free of charge within one calendar month",
            "Where technically feasible, data subject can request direct controller-to-controller transmission"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of turnover.",
        "statutory_text": "1. The data subject shall have the right to receive the personal data concerning him or her, which he or she has provided to a controller, in a structured, commonly used and machine-readable format and have the right to transmit those data to another controller without hindrance from the controller to which the personal data have been provided...",
        "practical_application": "Platform should provide a 'Download My Data' button in user settings generating a password-protected zip file containing profile info, consultation notes, and payment receipts in structured JSON.",
        "keywords": ["data portability", "article 20", "machine readable", "json export", "data download", "dsar"]
    },
    {
        "id": "UK-GDPR-ART-28",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 28(3)",
        "category": "Vendor & Processor Governance",
        "title": "Processor Obligations & Mandatory Data Processing Agreements (DPAs)",
        "summary": "Where processing is to be carried out on behalf of a controller, the controller shall use only processors providing sufficient guarantees. Processing must be governed by a legally binding contract (DPA) setting out the subject matter, duration, nature and purpose, types of personal data, and categories of data subjects.",
        "key_requirements": [
            "Execute signed Data Processing Agreement (DPA) prior to transferring any user data to vendors",
            "Processor may only process personal data on documented instructions from controller",
            "Processor personnel must be committed to confidentiality",
            "Mandatory technical & organisational security measures (Art 32)",
            "Processor cannot engage a sub-processor without prior written specific or general consent",
            "Processor must assist controller with DSAR responses and security breach notifications",
            "Processor must delete or return all personal data at the end of service provision",
            "Processor must submit to audits and inspections conducted by the controller"
        ],
        "penalties": "Standard maximum fine tier: Up to £8,700,000 or 2% of total worldwide annual turnover.",
        "statutory_text": "Processing by a processor shall be governed by a contract or other legal act under domestic law, that is binding on the processor with regard to the controller and that sets out the subject-matter and duration of the processing, the nature and purpose of the processing, the type of personal data and categories of data subjects and the obligations and rights of the controller. That contract shall stipulate, in particular, that the processor: (a) processes personal data only on documented instructions; (b) ensures confidentiality; (c) takes Art 32 measures; (d) respects sub-processor rules; (e) assists with DSARs; (f) assists with compliance and security; (g) deletes/returns data; (h) makes available information to demonstrate compliance and allows audits.",
        "practical_application": "Every vendor used in code (OpenAI, AWS, Twilio, Stripe, PostHog, practitioner contractors) MUST have an active signed DPA containing statutory Article 28(3) warranties.",
        "keywords": ["article 28", "dpa", "data processing agreement", "processor", "subprocessor", "vendor risk", "documented instructions", "confidentiality"]
    },
    {
        "id": "UK-GDPR-ART-30",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 30",
        "category": "Accountability & Documentation",
        "title": "Records of Processing Activities (RoPA)",
        "summary": "Each controller and processor must maintain a written record of processing activities under its responsibility. This inventory must document processing purposes, data subject categories, personal data categories, recipient categories, international transfer safeguards, retention limits, and general technical security measures.",
        "key_requirements": [
            "Maintain comprehensive live register of all data flows across web, mobile, and backend",
            "SME exemption under Art 30(5) DOES NOT APPLY if processing is not occasional, includes special category data (Art 9), or poses risk to data subjects' rights",
            "Must be readily available to the Information Commissioner's Office (ICO) upon request",
            "Must document third-party vendors and cloud storage jurisdictions"
        ],
        "penalties": "Standard maximum fine tier: Up to £8,700,000 or 2% of annual turnover.",
        "statutory_text": "1. Each controller and, where applicable, the controller's representative, shall maintain a record of processing activities under its responsibility. That record shall contain all of the following information: (a) name and contact details; (b) purposes of processing; (c) description of categories of data subjects and personal data; (d) categories of recipients; (e) transfers to third countries and documentation of safeguards; (f) time limits for erasure; (g) general description of technical and organisational security measures.",
        "practical_application": "Tara must maintain an Article 30 RoPA mapping User Account Registration, Consultation Booking, AI/LLM Summarization, and Stripe Invoicing.",
        "keywords": ["article 30", "ropa", "record of processing activities", "data inventory", "data mapping", "accountability", "ico inspection"]
    },
    {
        "id": "UK-GDPR-ART-32",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 32",
        "category": "Technical Security",
        "title": "Security of Processing (Encryption & Access Controls)",
        "summary": "Taking into account state of the art, implementation costs, nature, scope, context, and risks, controller and processor must implement technical and organisational measures to ensure a level of security appropriate to the risk, including pseudonymisation, encryption, ongoing confidentiality, integrity, availability, and resilience.",
        "key_requirements": [
            "Mandatory TLS 1.3 encryption in transit for all web and API traffic",
            "Field-level AES-256 encryption at rest for sensitive consultation notes, health, and spiritual questions",
            "Role-Based Access Control (RBAC): practitioners must only view assigned clients",
            "Data masking: Practitioners must NEVER receive raw customer phone numbers or personal emails",
            "Regular vulnerability scanning and penetration testing of APIs and databases"
        ],
        "penalties": "Standard maximum fine tier: Up to £8,700,000 or 2% of turnover (and up to £17.5M if linked to Article 5(1)(f) breach).",
        "statutory_text": "1. Taking into account the state of the art, the costs of implementation and the nature, scope, context and purposes of processing as well as the risk of varying likelihood and severity for the rights and freedoms of natural persons, the controller and the processor shall implement appropriate technical and organisational measures to ensure a level of security appropriate to the risk, including inter alia as appropriate: (a) pseudonymisation and encryption of personal data; (b) confidentiality, integrity, availability and resilience; (c) ability to restore access; (d) regular testing and assessing effectiveness of technical measures.",
        "practical_application": "Customer phone numbers must be masked using virtual numbers / in-app WebRTC so astrologers or support staff in India cannot copy personal phone numbers to personal WhatsApp or external devices.",
        "keywords": ["article 32", "security of processing", "encryption", "aes-256", "tls 1.3", "masking", "data leak", "practitioner poaching", "rbac"]
    },
    {
        "id": "UK-GDPR-ART-33-34",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Articles 33 & 34",
        "category": "Incident Response",
        "title": "Notification of Personal Data Breaches (72-Hour Rule)",
        "summary": "In the case of a personal data breach, the controller must without undue delay and, where feasible, not later than 72 hours after becoming aware of it, notify the Information Commissioner's Office (ICO), unless the breach is unlikely to result in a risk to individuals. If high risk, affected individuals must also be notified without undue delay.",
        "key_requirements": [
            "Notify UK ICO within strict 72-hour window from the moment breach is confirmed",
            "Processors must notify controller without undue delay upon becoming aware of a breach",
            "Breach notice must state: nature of breach, categories and approximate number of individuals, DPO contact, likely consequences, and remediation measures taken",
            "Internal Breach Register must document all security incidents, even non-reportable minor leaks"
        ],
        "penalties": "Standard maximum fine tier: Up to £8,700,000 or 2% of worldwide turnover.",
        "statutory_text": "In the case of a personal data breach, the controller shall without undue delay and, where feasible, not later than 72 hours after having become aware of it, notify the personal data breach to the Commissioner... When the personal data breach is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall communicate the personal data breach to the data subject without undue delay.",
        "practical_application": "Engineering team must maintain an incident runbook. If an S3 bucket leaks or an API key is exposed on GitHub, clock starts immediately for ICO 72-hour notification.",
        "keywords": ["article 33", "article 34", "data breach", "72 hours", "ico notification", "breach reporting", "security incident"]
    },
    {
        "id": "UK-GDPR-ART-35",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Article 35",
        "category": "Risk Governance",
        "title": "Data Protection Impact Assessment (DPIA)",
        "summary": "Where a type of processing in particular using new technologies is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data.",
        "key_requirements": [
            "Statutory requirement for AI / Large Language Models (LLMs) analyzing personal text",
            "Statutory requirement for processing Special Category Data (Art 9) at scale",
            "DPIA must describe processing systematically, assess necessity and proportionality, evaluate risks to data subjects, and document mitigation safeguards",
            "Must consult the Data Protection Officer (DPO) and seek ICO prior consultation if high risks cannot be mitigated"
        ],
        "penalties": "Standard maximum fine tier: Up to £8,700,000 or 2% of annual turnover.",
        "statutory_text": "1. Where a type of processing in particular using new technologies, and taking into account the nature, scope, context and purposes of the processing, is likely to result in a high risk to the rights and freedoms of natural persons, the controller shall, prior to the processing, carry out an assessment of the impact of the envisaged processing operations on the protection of personal data... 3. A data protection impact assessment shall in particular be required in the case of: (a) systematic and extensive evaluation of personal aspects based on automated processing... (b) processing on a large scale of special categories of data referred to in Article 9(1)...",
        "practical_application": "Launching an LLM-powered astrology or spiritual consultation chat feature without an executed DPIA is an immediate ICO enforcement trigger.",
        "keywords": ["article 35", "dpia", "data protection impact assessment", "ai governance", "high risk", "new technologies", "ico prior consultation"]
    },
    {
        "id": "UK-GDPR-CHAP-V",
        "jurisdiction": "UK_GDPR",
        "statute": "UK General Data Protection Regulation",
        "citation": "UK GDPR Chapter V (Articles 44–46)",
        "category": "International Data Transfers",
        "title": "Restricted Transfers & UK International Data Transfer Agreement (IDTA)",
        "summary": "Transfer of personal data to a third country (e.g. India or USA) outside the UK/EEA is prohibited unless an adequacy decision exists, or appropriate safeguards are provided, such as the UK International Data Transfer Agreement (IDTA) or UK Addendum to EU SCCs, backed by a Transfer Risk Assessment (TRA).",
        "key_requirements": [
            "India DOES NOT have an adequacy decision from the UK Government or European Commission",
            "UK customer data accessed by developers, QA, or astrologers in India constitutes a restricted international transfer",
            "Must execute the official ICO International Data Transfer Agreement (IDTA) or UK Addendum to EU SCCs",
            "Conduct a Transfer Risk Assessment (TRA) to verify local laws in recipient country do not undermine UK protections",
            "Implement technical safeguards: zero local device storage, encrypted remote desktop / VPN tunnel"
        ],
        "penalties": "Higher maximum fine tier: Up to £17,500,000 or 4% of total worldwide turnover. Regulators can also issue a statutory Stop-Processing Order shutting down cross-border data flows.",
        "statutory_text": "Any transfer of personal data which are undergoing processing or are intended for processing after transfer to a third country or to an international organisation shall take place only if, subject to the other provisions of this Regulation, the conditions laid down in this Chapter are complied with by the controller and processor... Article 46: In the absence of an adequacy decision, a controller or processor may transfer personal data to a third country only if the controller or processor has provided appropriate safeguards, and on condition that enforceable data subject rights and effective legal remedies for data subjects are available.",
        "practical_application": "Tara UK must execute a formal IDTA with Tara Infotech (India entity) and individual Indian practitioners before giving Indian staff access to UK customer databases.",
        "keywords": ["chapter v", "article 44", "article 46", "international transfers", "idta", "sccs", "uk addendum", "transfer risk assessment", "tra", "india transfer"]
    },

    # =========================================================================
    # UK ICO STATUTORY GUIDANCE & PECR
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
        "practical_application": "Product analytics SDKs (PostHog, Google Analytics) must NOT fire on app launch until user clicks 'Accept Analytics' on the onboarding privacy banner.",
        "keywords": ["pecr", "regulation 6", "cookies", "sdk tracking", "cookie banner", "mobile telemetry", "strictly necessary", "opt-in consent", "posthog"]
    },
    {
        "id": "ICO-AI-GUIDANCE-2024",
        "jurisdiction": "UK_ICO_AI",
        "statute": "ICO Statutory Guidance on AI and Data Protection",
        "citation": "ICO Guidance on Artificial Intelligence & Generative AI (2024)",
        "category": "AI Governance",
        "title": "Statutory Data Protection Rules for Generative AI & Large Language Models",
        "summary": "The UK Information Commissioner's Office sets strict obligations for organisations deploying Generative AI and LLMs: developers and deployers are accountable for personal data ingested into prompts, model outputs, and training pipelines.",
        "key_requirements": [
            "Explicit lawful basis must be established for processing personal data in LLM prompts",
            "Zero Data Retention (ZDR): Must ensure third-party LLM providers (e.g. OpenAI) do not retain prompts for model training",
            "PII Scrubbing: Direct identifiers (names, emails, phone numbers) should be redacted before prompt dispatch",
            "Accuracy of AI outputs: Deployers must mitigate hallucinations when AI generates biographical claims about living individuals",
            "Automated Decision-Making (Art 22): Users have the right not to be subject to solely automated decisions producing legal effects; human-in-the-loop review required for significant outcomes"
        ],
        "penalties": "UK ICO regulatory audit, mandatory suspension orders on AI models, fines up to £17,500,000.",
        "statutory_text": "You must understand whether personal data is used to train, test or deploy an AI system, and whether personal data is contained in the inputs or outputs. If you use a third-party AI model via an API, you must verify the contract terms: if the provider uses your prompts to fine-tune its foundational model, you are sharing user data for secondary purposes requiring distinct lawful basis and controller-processor agreements.",
        "practical_application": "Tara must configure OpenAI API enterprise headers (zero retention), purge user consultation prompts within 30 days, and display: 'AI-assisted astrological summaries are for informational guidance and do not constitute medical, legal, or psychological advice.'",
        "keywords": ["ai guidance", "generative ai", "llm compliance", "openai zero retention", "prompt sanitization", "pii scrubbing", "hallucinations", "article 22"]
    },

    # =========================================================================
    # INDIA DIGITAL PERSONAL DATA PROTECTION ACT, 2023 (DPDPA 2023)
    # =========================================================================
    {
        "id": "IN-DPDPA-SEC-04-05",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 4 & Section 5",
        "category": "Notice & Lawful Grounds",
        "title": "Grounds for Processing & Notice Requirements",
        "summary": "A person may process the personal data of an individual only in accordance with the provisions of this Act, either for a lawful purpose for which the individual has given consent, or for certain legitimate uses. Before or at the time of requesting consent, the Data Fiduciary must give an itemised statutory notice.",
        "key_requirements": [
            "Statutory Itemised Notice must specify: (1) personal data being collected, (2) purpose of processing, (3) manner in which data principal can exercise rights, (4) grievance redressal details",
            "Multilingual accessibility: Notice must be available in English and any of the 22 languages specified in the Eighth Schedule to the Constitution of India",
            "Clear, plain, and intelligible language; cannot be hidden inside 50-page complex legal Terms of Service",
            "Notice must be served even for previously collected data upon commencement of the Act"
        ],
        "penalties": "Penalties up to ₹50 CRORE (~£5 Million) for failure to issue compliant statutory notice.",
        "statutory_text": "Sec 5(1): On or before requesting consent, the Data Fiduciary shall give to the Data Principal an itemised notice containing: (i) personal data to be processed and purpose; (ii) manner of exercising right to withdraw consent and grievance redressal; (iii) manner of making complaint to the Board. Sec 5(3): The Data Principal shall be given option to access the contents of the notice in English or any language specified in the Eighth Schedule.",
        "practical_application": "Registration screen for Indian users must provide a language selector (Hindi, Bengali, Marathi, Tamil, etc.) and a bulleted notice stating exact consultation data collected and grievance officer email.",
        "keywords": ["dpdpa 2023", "section 4", "section 5", "itemised notice", "scheduled languages", "bilingual notice", "consent notice", "data fiduciary"]
    },
    {
        "id": "IN-DPDPA-SEC-06",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 6",
        "category": "Consent Architecture",
        "title": "Conditions for Free, Specific, Informed & Unconditional Consent",
        "summary": "Consent given by the Data Principal must be free, specific, informed, unconditional, and unambiguous with a clear affirmative action. Any part of consent which infringes upon the provisions of this Act shall be invalid to that extent.",
        "key_requirements": [
            "Consent must be UNCONDITIONAL: Cannot deny service to a user for refusing consent to non-essential secondary data collection",
            "Consent Manager: Individual can give, manage, review, or withdraw consent through an interoperable Consent Manager registered with DPBI",
            "Right to Withdraw Consent: Withdrawal takes effect immediately; Data Fiduciary must cease processing unless required by statutory law",
            "Burden of proof lies on Data Fiduciary to prove compliant consent was obtained"
        ],
        "penalties": "Penalties up to ₹100 CRORE (~£10 Million) for unlawful processing without valid consent.",
        "statutory_text": "Sec 6(1): The consent given by the Data Principal shall be free, specific, informed, unconditional and unambiguous with a clear affirmative action, and shall signify an agreement to the processing of her personal data for the specified purpose and be limited to such personal data as is necessary for such specified purpose.",
        "practical_application": "Do not block users from booking a consultation if they untick marketing promotions. Implement webhook: when user toggles consent OFF, immediately halt promotional SMS/WhatsApp notifications.",
        "keywords": ["section 6", "unconditional consent", "clear affirmative action", "consent withdrawal", "consent manager", "affirmative consent"]
    },
    {
        "id": "IN-DPDPA-SEC-08",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 8(5), 8(6) & 8(7)",
        "category": "Fiduciary Security & Erasure",
        "title": "Reasonable Security Safeguards, Breach Reporting & Mandatory Erasure",
        "summary": "A Data Fiduciary must implement reasonable security safeguards to prevent personal data breaches under Section 8(5). In case of a breach, it must notify the Data Protection Board of India (DPBI) and affected users under Section 8(6). Under Section 8(7), data must be erased as soon as the user withdraws consent or the purpose is fulfilled.",
        "key_requirements": [
            "Reasonable security safeguards: end-to-end encryption, strict role-based data isolation, audit logging",
            "Mandatory breach reporting: MUST notify DPBI and affected individuals for ANY personal data breach, regardless of scale",
            "Automated purpose fulfillment erasure: Cannot retain consultation notes or chat queries indefinitely after session completion",
            "Subprocessor oversight: Data Fiduciary remains fully liable for violations caused by its Data Processors"
        ],
        "penalties": "MAXIMUM STATUTORY PENALTY: Up to ₹250 CRORE (~£25 Million) per failure to take reasonable security safeguards to prevent personal data breach! Up to ₹200 Crore for failure to report breaches to DPBI.",
        "statutory_text": "Sec 8(5): A Data Fiduciary shall protect personal data in its possession or under its control by taking reasonable security safeguards to prevent personal data breach. Sec 8(6): In the event of a personal data breach, the Data Fiduciary shall give the Board and each affected Data Principal, intimation of such breach in such form and manner as may be prescribed. Sec 8(7): A Data Fiduciary shall erase personal data upon Data Principal withdrawing consent or as soon as it is reasonable to assume that specified purpose is no longer being served.",
        "practical_application": "Tara must enforce AES-256 database column encryption on astrologer notes. Implement a cron cleanup purging session chat history 30 days post-consultation.",
        "keywords": ["section 8", "reasonable security safeguards", "250 crore fine", "breach notification", "dpbi", "mandatory erasure", "purpose fulfillment"]
    },
    {
        "id": "IN-DPDPA-SEC-09",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 9",
        "category": "Children's Protection",
        "title": "Verifiable Parental Consent & Prohibition of Behavioral Tracking of Children",
        "summary": "The Data Fiduciary shall, before processing any personal data of a child (individual below 18 years), obtain verifiable consent of the parent or lawful guardian. A Data Fiduciary shall not undertake tracking or behavioral monitoring of children or targeted advertising directed at children.",
        "key_requirements": [
            "Strict definition: Child is defined as any person under 18 years of age",
            "Verifiable parental consent mechanism required before allowing minors to register or seek consultations",
            "Absolute statutory prohibition on behavioural tracking, profiling, or targeted ads directed at children",
            "Prohibition on processing personal data that is likely to cause detrimental effect on the well-being of a child"
        ],
        "penalties": "Severe penalty tier: Up to ₹200 CRORE (~£20 Million) for breach in observance of duties in relation to children.",
        "statutory_text": "Sec 9(1): The Data Fiduciary shall, before processing any personal data of a child or a person with disability who has a lawful guardian, obtain verifiable consent of the parent... Sec 9(2): A Data Fiduciary shall not undertake tracking or behavioural monitoring of children or targeted advertising directed at children. Sec 9(3): A Data Fiduciary shall not undertake any processing that is likely to cause detrimental effect on the well-being of a child.",
        "practical_application": "App must enforce an age-gate date of birth picker. If user is under 18, prompt for Parent/Guardian OTP verification and disable all analytics tracking hooks.",
        "keywords": ["section 9", "children's data", "parental consent", "under 18", "behavioral tracking", "targeted advertising", "200 crore"]
    },
    {
        "id": "IN-DPDPA-SEC-10",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 10",
        "category": "Significant Data Fiduciary",
        "title": "Additional Obligations of Significant Data Fiduciary (SDF)",
        "summary": "The Central Government may notify any Data Fiduciary as a Significant Data Fiduciary based on factors like volume of data, sensitivity of personal data, risk to electoral democracy, sovereignty, or public order. SDFs have heightened statutory compliance burdens.",
        "key_requirements": [
            "Must appoint a resident Data Protection Officer (DPO) based in India representing the Fiduciary",
            "Must appoint an Independent Data Auditor to evaluate compliance audits",
            "Must conduct periodic Data Protection Impact Assessments (DPIA)",
            "Must undertake periodic cybersecurity audits"
        ],
        "penalties": "Penalties up to ₹150 CRORE (~£15 Million) for non-compliance with SDF obligations.",
        "statutory_text": "Sec 10(2): The Significant Data Fiduciary shall: (a) appoint a Data Protection Officer who shall be an individual based in India; (b) appoint an independent data auditor; (c) undertake Data Protection Impact Assessment and periodic audits.",
        "practical_application": "Because spiritual and astrological profiling involves sensitive beliefs and mass user consultations, Tara must maintain readiness for SDF classification.",
        "keywords": ["section 10", "significant data fiduciary", "sdf", "resident dpo", "independent data auditor", "dpia india", "150 crore"]
    },
    {
        "id": "IN-DPDPA-SEC-13",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023",
        "citation": "DPDP Act 2023 Section 13",
        "category": "Grievance Redressal",
        "title": "Mandatory Grievance Redressal Mechanism & Officer",
        "summary": "A Data Principal shall have the right of grievance redressal in respect of any act or omission of the Data Fiduciary regarding the performance of its obligations. The Data Fiduciary must establish an easily accessible redressal mechanism and publish contact details of a Grievance Redressal Officer.",
        "key_requirements": [
            "Must designate and prominently publish the name, official email, and contact address of Grievance Redressal Officer",
            "Must resolve grievances within the statutory timeline prescribed by the Central Government (typically within 30 days)",
            "Data Principal must exhaust internal grievance redressal before escalating complaints to the Data Protection Board of India (DPBI)"
        ],
        "penalties": "Penalties up to ₹50 CRORE (~£5 Million) for non-compliance with grievance handling duties.",
        "statutory_text": "Sec 13(1): A Data Principal shall have the right of grievance redressal... Sec 13(2): The Data Fiduciary shall establish an effective redressal mechanism... Sec 13(3): The Data Principal shall exhaust the opportunity of redressal provided by the Data Fiduciary before making a complaint to the Board.",
        "practical_application": "Add a dedicated section in Privacy Policy: 'Grievance Redressal Officer: Mr. Rajesh Sharma, Email: grievance@taraprivacy.io, Phone: +91-11-XXXXXXX, Address: New Delhi, India.'",
        "keywords": ["section 13", "grievance redressal", "grievance officer", "complaint mechanism", "dpbi escalation", "dispute resolution"]
    },
    {
        "id": "IN-DPDPA-SEC-16-RBI",
        "jurisdiction": "INDIA_DPDPA",
        "statute": "Digital Personal Data Protection Act, 2023 & RBI Directives",
        "citation": "DPDP Act 2023 Section 16 & RBI Payment System Data Localisation Circular",
        "category": "Cross-Border Transfers & Payment Localisation",
        "title": "Cross-Border Data Flows & RBI Financial Data Localisation",
        "summary": "Personal data may be transferred outside India for processing, subject to blacklisted countries restricted by Central Government notifications. However, under Reserve Bank of India (RBI) mandates, payment system data (UPI, card details, payment logs) must be stored exclusively in India.",
        "key_requirements": [
            "DPDPA uses a 'Blacklist' approach: transfers permitted unless destination country is expressly restricted",
            "Stricter sectoral laws prevail over DPDPA (e.g. RBI Payment Localisation Mandate 2018)",
            "All end-to-end payment data (card numbers, UPI IDs, bank accounts) processed via Razorpay/Stripe must reside in Indian data centres",
            "Overseas processing allowed for transaction clearing, but complete records must be brought back to India within 24 hours"
        ],
        "penalties": "Penalties up to ₹100 CRORE under DPDPA, plus severe regulatory action / suspension of payment gateway licenses by RBI.",
        "statutory_text": "Sec 16(1): The Central Government may, by notification, restrict the transfer of personal data by a Data Fiduciary for processing to such country or territory outside India as may be so notified. Sec 16(2): Nothing in this section shall restrict the application of any higher degree of protection or restriction provided under any other law in force in India.",
        "practical_application": "Payment transaction logs must be stored in AWS Mumbai (ap-south-1) and never transferred to foreign server storage without Indian mirroring.",
        "keywords": ["section 16", "cross-border transfer", "rbi localization", "payment data", "razorpay", "financial data storage", "data sovereignty"]
    },

    # =========================================================================
    # STATUTORY MODEL CLAUSES (FOR AUTOMATED AUDITING & REDLINING)
    # =========================================================================
    {
        "id": "MODEL-CLAUSE-ART9-CONSENT",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 9(2)(a) & DPDPA Sec 6",
        "citation": "Statutory Model Clause: Article 9 Explicit Consent",
        "category": "Model Clause",
        "title": "Compliant Explicit Consent Clause for Sensitive / Astrological Data",
        "summary": "Legally binding model clause satisfying UK GDPR Article 9 explicit consent and India DPDP Act Section 6 requirement for spiritual and consultation apps.",
        "key_requirements": [
            "Must be displayed with an unticked checkbox at booking",
            "Must explicitly name spiritual, health, and relationship data categories",
            "Must specify purpose, retention timeframe, and revocation instructions"
        ],
        "penalties": "Prevents catastrophic £17.5M UK ICO fine and ₹100 Crore DPBI fine.",
        "statutory_text": "EXPLICIT CONSENT FOR SENSITIVE CONSULTATION DATA (UK GDPR Art 9(2)(a) & DPA 2018):\n'By ticking this box, I expressly and unequivocally grant explicit consent to Tara Infotech Ltd to process my special category personal data, specifically including my date/time/place of birth, horoscope chart data, and any health, relationship, or philosophical concerns voluntarily disclosed during my consultation session. I understand this sensitive data will be processed solely to deliver bespoke astrological insights, will never be sold or used for automated advertising, and will be securely encrypted with AES-256. I retain the statutory right to withdraw my explicit consent at any time via my Account Privacy Settings or by emailing dpo@taraprivacy.io, upon which all raw consultation queries will be permanently erased within 30 days.'",
        "practical_application": "Use this clause to replace vague 'by clicking continue you agree to processing of your information' draft clauses.",
        "keywords": ["model clause", "explicit consent text", "statutory replacement", "article 9 clause", "redline template"]
    },
    {
        "id": "MODEL-CLAUSE-RETENTION",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 5(1)(e) & DPDPA Sec 8(7)",
        "citation": "Statutory Model Clause: Storage Limitation & Data Retention",
        "category": "Model Clause",
        "title": "Compliant Data Retention & Statutory Erasure Clause",
        "summary": "Legally binding model clause replacing illegal vague statements like 'we retain data as long as necessary'.",
        "key_requirements": [
            "Must specify distinct retention windows for each data category",
            "Must define ephemeral purge window for AI prompts and session transcripts",
            "Must cite statutory basis for retaining tax/billing data (6 years)"
        ],
        "penalties": "Protects against ICO Article 5(1)(e) enforcement actions.",
        "statutory_text": "STATUTORY DATA RETENTION SCHEDULE (UK GDPR Art 5(1)(e) & India DPDPA Sec 8(7)):\n'We enforce strict data minimisation and retention schedules tailored to each processing purpose:\n1. User Account Profile: Retained for the active duration of your account + 30-day grace period following a verified deletion request.\n2. Consultation Notes & Transcripts: Retained for 60 calendar days post-session to facilitate client follow-up, after which all freeform notes are cryptographically erased.\n3. AI/LLM Prompts & Summaries: Cached ephemerally for the duration of the active consultation session only; zero permanent storage is maintained on third-party AI provider servers.\n4. Billing & Invoicing Records: Retained for 6 statutory years from the end of the financial year pursuant to UK HMRC and Indian Goods and Services Tax (GST) accounting obligations.\nUpon expiry of the designated retention period, data is either permanently deleted from our active clusters or irreversibly anonymised.'",
        "practical_application": "Use to auto-replace any clause stating 'we store your information for as long as needed to fulfill our business goals'.",
        "keywords": ["model clause", "retention schedule", "storage limitation", "erasure timeline", "hmrc 6 years", "ephemeral cache"]
    },
    {
        "id": "MODEL-CLAUSE-IDTA-CROSSBORDER",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Article 46 & DPA 2018 Section 119A",
        "citation": "Statutory Model Clause: UK International Data Transfer Agreement (IDTA)",
        "category": "Model Clause",
        "title": "Compliant UK-to-India Cross-Border Data Transfer Disclosure",
        "summary": "Authoritative clause disclosing transfer of customer data to overseas developers and practitioners in India under ICO-approved IDTA safeguards.",
        "key_requirements": [
            "Must explicitly name the destination country (India)",
            "Must identify the transfer mechanism: UK ICO International Data Transfer Agreement (IDTA)",
            "Must detail technical and contractual safeguards (no local downloading, TLS 1.3 transit)"
        ],
        "penalties": "Protects against cross-border data export injunctions by the UK Information Commissioner.",
        "statutory_text": "INTERNATIONAL DATA TRANSFERS & OVERSEAS PROCESSING (UK GDPR Chapter V):\n'When you schedule a consultation or receive customer support, your personal data may be accessed by our vetted practitioners, technical support, and development engineers situated in the Republic of India. Because India has not received a formal adequacy finding from the UK Secretary of State, all overseas data access is strictly governed by the official UK Information Commissioner's Office International Data Transfer Agreement (IDTA) pursuant to Section 119A of the Data Protection Act 2018.\nUnder our IDTA and supplementary technical safeguards: (i) all data access occurs via encrypted remote sessions with zero local device download permissions; (ii) customer direct telephone numbers and email addresses are cryptographically masked; (iii) overseas personnel are bound by statutory confidentiality and DPA obligations; and (iv) UK customers retain fully enforceable third-party beneficiary rights.'",
        "practical_application": "Auto-replace vague clauses stating 'we may share data with international affiliates from time to time'.",
        "keywords": ["model clause", "idta clause", "international transfer clause", "uk to india transfer", "chapter v disclosure"]
    },
    {
        "id": "MODEL-CLAUSE-OPENAI-GOVERNANCE",
        "jurisdiction": "STATUTORY_MODEL",
        "statute": "UK GDPR Art 28 & ICO AI Guidance 2024",
        "citation": "Statutory Model Clause: Artificial Intelligence & Subprocessor Safeguards",
        "category": "Model Clause",
        "title": "Compliant AI / LLM Data Processing Disclosure Clause",
        "summary": "Statutory disclosure explaining how user consultation queries are processed by OpenAI / Azure OpenAI with zero model training and ephemeral retention.",
        "key_requirements": [
            "Disclose use of Large Language Model subprocessors",
            "Guarantee zero training on user personal consultation prompts",
            "Confirm automated PII scrubbing before API transit"
        ],
        "penalties": "Mitigates AI transparency and processor DPA violations under Articles 13, 14, and 28.",
        "statutory_text": "ARTIFICIAL INTELLIGENCE & THIRD-PARTY LLM PROCESSING:\n'To provide accelerated consultation summaries and astrological chart interpretations, our platform integrates enterprise AI Large Language Model APIs (specifically OpenAI LLC and Microsoft Azure OpenAI). We enforce strict technical and contractual guardrails under our Data Processing Addendum:\n1. Zero Model Training: Your consultation queries, birth details, and chat prompts are never used to train, retrain, or improve public foundational AI models.\n2. Prompt Redaction: Direct personal identifiers (full name, phone number, physical address) are scrubbed prior to dispatching prompts to AI endpoints.\n3. Ephemeral Processing: Prompts are processed in memory and not retained on external AI servers beyond technical response generation.\n4. Human Oversight: AI outputs provide automated interpretations and do not replace personalized professional human counseling.'",
        "practical_application": "Auto-inject into any draft privacy policy or SaaS Terms where OpenAI or Anthropic SDKs are detected.",
        "keywords": ["model clause", "ai disclosure", "openai zero retention", "subprocessor dpa", "human oversight", "ai governance"]
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
        except Exception as e:
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
            "UK Data (Use and Access) Act 2025 (DUAA 2025 - Official Legislation)",
            "GDPR EPSU Statutory Briefing",
            "UK GDPR & ICO Statutory Guidance (2024)",
            "PECR (Cookies & SDK Telemetry)",
            "India Digital Personal Data Protection Act 2023",
            "RBI Payment Data Localisation",
            "Statutory Model Clauses"
        ]
    }

