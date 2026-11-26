"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-104 Third-Party SDK & Subprocessor Detector
Detects third-party APIs, SDKs, and cloud dependencies across any programming language
and maps them to statutory Article 28 DPA obligations and international transfer mechanisms.
"""

from typing import Dict, List, Any

class SubprocessorDetector:
    # 80+ Known Global Third-Party Subprocessors & Cloud Infrastructure Providers
    SUBPROCESSOR_DATABASE = {
        # --- AI & LARGE LANGUAGE MODELS ---
        "openai": {
            "name": "OpenAI LLC",
            "aliases": ["openai", "azure_openai", "azure-openai", "gpt-4", "gpt-3.5", "text-embedding"],
            "category": "AI / Large Language Model API",
            "jurisdiction": "United States (Third Country)",
            "data_types_processed": ["User Prompts", "Question Transcripts", "Context Summaries"],
            "transfer_mechanism_required": "UK IDTA / EU SCCs + Enterprise Zero-Data Retention Agreement",
            "article_28_dpa_status": "Mandatory DPA (Ensure API opt-out of model training is active)",
            "risk_level": "CRITICAL",
            "recommendation": "Verify OpenAI API Data Processing Addendum is executed. Ensure organization account disables training on API inputs."
        },
        "anthropic": {
            "name": "Anthropic PBC",
            "aliases": ["anthropic", "claude"],
            "category": "AI / LLM API",
            "jurisdiction": "United States (Third Country)",
            "data_types_processed": ["User Queries", "Conversation Context"],
            "transfer_mechanism_required": "UK IDTA / Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA Required",
            "risk_level": "CRITICAL",
            "recommendation": "Execute Anthropic Commercial DPA. Confirm data retention schedule."
        },
        "cohere": {
            "name": "Cohere Inc.",
            "aliases": ["cohere", "cohere-ai"],
            "category": "Enterprise NLP & Embeddings",
            "jurisdiction": "Canada (Adequacy Decision) / US",
            "data_types_processed": ["Text Embeddings", "Reranking Queries"],
            "transfer_mechanism_required": "Commercial DPA + EU Adequacy Safeguards",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Cohere Enterprise Data Processing Addendum."
        },
        "huggingface": {
            "name": "Hugging Face Inc.",
            "aliases": ["huggingface", "transformers", "hf_hub", "diffusers"],
            "category": "Machine Learning Model Hosting",
            "jurisdiction": "United States / France",
            "data_types_processed": ["Model Inferences", "Fine-Tuning Datasets"],
            "transfer_mechanism_required": "Hugging Face DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Processor Agreement",
            "risk_level": "MEDIUM",
            "recommendation": "Confirm private endpoints with zero model telemetry retention."
        },
        "groq": {
            "name": "Groq Inc.",
            "aliases": ["groq"],
            "category": "Ultra-Fast LPU AI Inference",
            "jurisdiction": "United States",
            "data_types_processed": ["Application Prompts", "Real-Time AI Inferences"],
            "transfer_mechanism_required": "Standard Contractual Clauses / US Data Bridge",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Groq Data Processing Agreement with zero-retention confirmation."
        },
        "replicate": {
            "name": "Replicate Inc.",
            "aliases": ["replicate"],
            "category": "Cloud Model Inference Platform",
            "jurisdiction": "United States",
            "data_types_processed": ["Image Prompts", "Model Weights", "Inference Inputs"],
            "transfer_mechanism_required": "Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Replicate Commercial DPA."
        },
        "mistral": {
            "name": "Mistral AI",
            "aliases": ["mistral", "mistralai"],
            "category": "European Open Weights AI Platform",
            "jurisdiction": "France (EU)",
            "data_types_processed": ["AI Prompts", "Generated Completions"],
            "transfer_mechanism_required": "Direct EU GDPR Jurisdiction (GDPR Adequacy Native)",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "LOW",
            "recommendation": "Leverage native EU data residency for low transfer regulatory friction."
        },

        # --- CLOUD INFRASTRUCTURE & HOSTING ---
        "aws": {
            "name": "Amazon Web Services (AWS)",
            "aliases": ["aws", "boto3", "aws-sdk", "amplify", "s3", "dynamodb", "sqs", "sns", "lambda"],
            "category": "Cloud Infrastructure & Database Hosting",
            "jurisdiction": "United States / Ireland / UK",
            "data_types_processed": ["Primary Database", "User Files", "App Compute", "Access Logs"],
            "transfer_mechanism_required": "AWS GDPR Data Processing Addendum",
            "article_28_dpa_status": "Mandatory Cloud DPA",
            "risk_level": "HIGH",
            "recommendation": "Pin primary S3 and RDS storage to AWS London (eu-west-2) or Mumbai (ap-south-1)."
        },
        "gcp": {
            "name": "Google Cloud Platform (GCP)",
            "aliases": ["google-cloud", "google_cloud", "gcs", "bigquery", "google.golang.org"],
            "category": "Cloud Compute, Analytics & Storage",
            "jurisdiction": "United States / EU / Global",
            "data_types_processed": ["Application Hosting", "Database Backups", "Analytics Logs"],
            "transfer_mechanism_required": "Google Cloud CDPA + UK Addendum",
            "article_28_dpa_status": "Mandatory Cloud DPA",
            "risk_level": "HIGH",
            "recommendation": "Ensure GCP region is pinned to Europe (europe-west2) or India (asia-south1)."
        },
        "azure": {
            "name": "Microsoft Azure",
            "aliases": ["azure", "azure-storage", "azure-cosmos", "azure-core", "microsoft.azure"],
            "category": "Enterprise Cloud & AI Services",
            "jurisdiction": "United States / UK / Ireland",
            "data_types_processed": ["Enterprise Data", "App Services", "Database Clusters"],
            "transfer_mechanism_required": "Microsoft Products and Services DPA (Data Boundary)",
            "article_28_dpa_status": "Mandatory Cloud DPA",
            "risk_level": "HIGH",
            "recommendation": "Configure EU / UK Data Boundary in Azure tenant configuration."
        },
        "vercel": {
            "name": "Vercel Inc.",
            "aliases": ["vercel", "@vercel/"],
            "category": "Serverless Edge Hosting & Next.js Deployment",
            "jurisdiction": "United States / Global Edge",
            "data_types_processed": ["HTTP Headers", "Edge Functions", "Client IP Addresses"],
            "transfer_mechanism_required": "Vercel DPA + EU Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Hosting DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Vercel Data Processing Agreement and configure GDPR compliant edge log drains."
        },
        "netlify": {
            "name": "Netlify Inc.",
            "aliases": ["netlify"],
            "category": "Static & Serverless Web Hosting",
            "jurisdiction": "United States",
            "data_types_processed": ["Edge Functions", "Deploy Logs", "Form Submissions"],
            "transfer_mechanism_required": "Netlify DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Hosting DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Sign Netlify DPA and audit Netlify Forms privacy compliance."
        },
        "render": {
            "name": "Render Services Inc.",
            "aliases": ["render"],
            "category": "Cloud Compute & Web Hosting",
            "jurisdiction": "United States / Germany (Frankfurt)",
            "data_types_processed": ["Application Compute Logs", "HTTP Headers", "IP Telemetry"],
            "transfer_mechanism_required": "Render DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Hosting DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Render Data Processing Agreement and configure encrypted environment secrets."
        },
        "railway": {
            "name": "Railway Corp",
            "aliases": ["railway"],
            "category": "Cloud Infrastructure & Container Deployment",
            "jurisdiction": "United States",
            "data_types_processed": ["Application Logs", "Database Containers"],
            "transfer_mechanism_required": "Railway DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Hosting DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Railway DPA and deploy services to EU / UK regions."
        },
        "flyio": {
            "name": "Fly.io Inc.",
            "aliases": ["fly.io", "flyctl"],
            "category": "Edge Micro-VM Cloud Hosting",
            "jurisdiction": "United States / Global",
            "data_types_processed": ["Edge Inbound IP", "Container Compute Logs"],
            "transfer_mechanism_required": "Fly.io DPA + SCCs",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Deploy Fly apps to lhr (London) or fra (Frankfurt) regions."
        },
        "digitalocean": {
            "name": "DigitalOcean LLC",
            "aliases": ["digitalocean"],
            "category": "Cloud Droplets & Managed Databases",
            "jurisdiction": "United States / UK (LON1)",
            "data_types_processed": ["Server Logs", "Database Storage", "App Compute"],
            "transfer_mechanism_required": "DigitalOcean DPA",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Pin Droplets to London (LON1) datacenter."
        },
        "cloudflare": {
            "name": "Cloudflare Inc.",
            "aliases": ["cloudflare", "workers", "wrangler"],
            "category": "Edge CDN, DDoS Defense & DNS",
            "jurisdiction": "United States / Global Anycast",
            "data_types_processed": ["Client IP Addresses", "TLS Handshakes", "WAF Security Logs"],
            "transfer_mechanism_required": "Cloudflare Global DPA + Customer SCCs",
            "article_28_dpa_status": "Mandatory Security Processor DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Enable Cloudflare Data Localization Suite to keep UK/EU logs within statutory borders."
        },

        # --- DATABASES, VECTOR ENGINES & CACHE ---
        "mongo": {
            "name": "MongoDB Inc. (MongoDB Atlas)",
            "aliases": ["mongo", "mongoose", "mongodb", "connect-mongo"],
            "category": "Cloud Database Infrastructure",
            "jurisdiction": "United States / Ireland / AWS Cloud",
            "data_types_processed": ["User Profiles", "Application Records", "Authentication Credentials"],
            "transfer_mechanism_required": "MongoDB Atlas GDPR Data Processing Agreement",
            "article_28_dpa_status": "Mandatory Cloud Database DPA",
            "risk_level": "HIGH",
            "recommendation": "Pin MongoDB Atlas cluster to AWS London (eu-west-2) or Mumbai (ap-south-1) for statutory data residency."
        },
        "supabase": {
            "name": "Supabase Inc.",
            "aliases": ["supabase", "@supabase/"],
            "category": "Managed Postgres & Auth Infrastructure",
            "jurisdiction": "United States / AWS EU",
            "data_types_processed": ["Customer Database", "Auth Sessions", "Storage Files"],
            "transfer_mechanism_required": "Supabase DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Database DPA",
            "risk_level": "HIGH",
            "recommendation": "Select eu-west-2 (London) as primary Supabase database region."
        },
        "neon": {
            "name": "Neon Tech Inc.",
            "aliases": ["neon", "@neondatabase/"],
            "category": "Serverless Server-Branching Postgres",
            "jurisdiction": "United States / EU AWS",
            "data_types_processed": ["Relational Schemas", "Customer Profiles", "Transactional Data"],
            "transfer_mechanism_required": "Neon DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Database DPA",
            "risk_level": "HIGH",
            "recommendation": "Pin Neon compute and storage branches to eu-central-1 or eu-west-2."
        },
        "planetscale": {
            "name": "PlanetScale Inc.",
            "aliases": ["planetscale", "@planetscale/"],
            "category": "Serverless MySQL Database",
            "jurisdiction": "United States",
            "data_types_processed": ["Application DB", "User Records"],
            "transfer_mechanism_required": "PlanetScale DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Database DPA",
            "risk_level": "HIGH",
            "recommendation": "Deploy cluster to AWS eu-west-2."
        },
        "redis": {
            "name": "Redis Labs / Upstash",
            "aliases": ["redis", "ioredis", "upstash", "@upstash/"],
            "category": "In-Memory Session Store & Serverless Cache",
            "jurisdiction": "United States / EU",
            "data_types_processed": ["User Session Tokens", "Rate Limiting Counters", "Temporary Cache"],
            "transfer_mechanism_required": "Redis / Upstash DPA",
            "article_28_dpa_status": "Mandatory Session Cache DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Ensure short TTLs on PII stored in cache."
        },
        "pinecone": {
            "name": "Pinecone Systems Inc.",
            "aliases": ["pinecone", "@pinecone-database/"],
            "category": "Vector Database for AI Search",
            "jurisdiction": "United States (Third Country)",
            "data_types_processed": ["Vector Embeddings", "Document Metadata", "Prompt Search Keys"],
            "transfer_mechanism_required": "Pinecone DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Vector Database DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Pinecone DPA; do not store unencrypted PII in vector metadata attributes."
        },
        "weaviate": {
            "name": "Weaviate B.V.",
            "aliases": ["weaviate"],
            "category": "Open-Source AI Vector Engine",
            "jurisdiction": "Netherlands (EU Native)",
            "data_types_processed": ["Semantic Embeddings", "Knowledge Vectors"],
            "transfer_mechanism_required": "Direct EU GDPR Law (Native Adequacy)",
            "article_28_dpa_status": "Standard EU Processor Agreement",
            "risk_level": "LOW",
            "recommendation": "Native EU jurisdiction eliminates UK/EU cross-border transfer overhead."
        },
        "qdrant": {
            "name": "Qdrant Solutions GmbH",
            "aliases": ["qdrant"],
            "category": "Vector Search Engine",
            "jurisdiction": "Germany (EU Native)",
            "data_types_processed": ["Semantic Vectors", "Vector Payloads"],
            "transfer_mechanism_required": "Native EU GDPR Law",
            "article_28_dpa_status": "Standard EU Processor Agreement",
            "risk_level": "LOW",
            "recommendation": "Native German GDPR jurisdiction; configure payload encryption at rest."
        },

        # --- PAYMENTS & FINTECH GATEWAYS ---
        "stripe": {
            "name": "Stripe Payments UK, Ltd.",
            "aliases": ["stripe", "stripe-go", "stripe-java", "stripe-python", "stripe-node"],
            "category": "Payment Processing (PCI-DSS Level 1)",
            "jurisdiction": "United Kingdom / United States",
            "data_types_processed": ["Payment Card Tokens", "Customer Billing Address", "Transaction History"],
            "transfer_mechanism_required": "Stripe Data Processing Agreement",
            "article_28_dpa_status": "Independent Controller / Joint Controller in card data handling",
            "risk_level": "HIGH",
            "recommendation": "Use Stripe Elements to prevent raw payment card numbers from touching backend servers."
        },
        "razorpay": {
            "name": "Razorpay Software Pvt. Ltd.",
            "aliases": ["razorpay"],
            "category": "Payment Processing (India UPI, Cards, NetBanking)",
            "jurisdiction": "India",
            "data_types_processed": ["UPI ID", "Indian Bank Credentials", "Billing Details", "Transaction Records"],
            "transfer_mechanism_required": "DPDPA 2023 Compliant Merchant Agreement & RBI Tokenisation Mandate",
            "article_28_dpa_status": "Payment Processor Agreement",
            "risk_level": "HIGH",
            "recommendation": "Execute Merchant Service Agreement complying with RBI storage guidelines and DPDP Act 2023."
        },
        "paypal": {
            "name": "PayPal Holdings Inc.",
            "aliases": ["paypal", "@paypal/"],
            "category": "Global Digital Wallet & Checkout",
            "jurisdiction": "United States / Luxembourg (EU)",
            "data_types_processed": ["PayPal Account ID", "Billing Address", "Order Totals"],
            "transfer_mechanism_required": "PayPal Binding Corporate Rules (BCRs)",
            "article_28_dpa_status": "Independent Data Controller",
            "risk_level": "MEDIUM",
            "recommendation": "Audit PayPal BCR adherence for international settlement."
        },
        "square": {
            "name": "Block Inc. (Square)",
            "aliases": ["square", "squareup"],
            "category": "Point of Sale & Online Payments",
            "jurisdiction": "United States",
            "data_types_processed": ["Payment Tokens", "Customer Names"],
            "transfer_mechanism_required": "Square Global DPA",
            "article_28_dpa_status": "Payment Processor DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Square Merchant DPA."
        },
        "paddle": {
            "name": "Paddle.com Market Ltd.",
            "aliases": ["paddle"],
            "category": "Merchant of Record (Global Tax Compliance)",
            "jurisdiction": "United Kingdom",
            "data_types_processed": ["VAT Identifiers", "Customer Email", "Billing Country"],
            "transfer_mechanism_required": "UK GDPR Native Controller Agreement",
            "article_28_dpa_status": "Merchant of Record (MoR) Controller",
            "risk_level": "LOW",
            "recommendation": "Paddle acts as Merchant of Record, absorbing global VAT liabilities."
        },
        "lemonsqueezy": {
            "name": "Lemon Squeezy (Stripe Inc.)",
            "aliases": ["lemonsqueezy", "lemon-squeezy"],
            "category": "Software Merchant of Record & Licensing",
            "jurisdiction": "United States",
            "data_types_processed": ["Customer Invoices", "License Keys", "Tax Records"],
            "transfer_mechanism_required": "Stripe Global DPA",
            "article_28_dpa_status": "Merchant of Record Agreement",
            "risk_level": "MEDIUM",
            "recommendation": "Confirm customer tax data isolation."
        },

        # --- AUTHENTICATION & IDENTITY ---
        "auth0": {
            "name": "Auth0 (Okta Inc.)",
            "aliases": ["auth0", "@auth0/"],
            "category": "Identity Access Management (IAM)",
            "jurisdiction": "United States / EU Cloud",
            "data_types_processed": ["User Emails", "Password Hashes", "MFA Phone Numbers", "Login IP Telemetry"],
            "transfer_mechanism_required": "Okta / Auth0 BCRs & Data Processing Addendum",
            "article_28_dpa_status": "Mandatory IAM Processor DPA",
            "risk_level": "HIGH",
            "recommendation": "Provision Auth0 tenant in EU region (Europe-1) and enforce strict session timeout."
        },
        "clerk": {
            "name": "Clerk Inc.",
            "aliases": ["clerk", "@clerk/"],
            "category": "Modern User Authentication & Session Management",
            "jurisdiction": "United States",
            "data_types_processed": ["User Email", "Phone Number", "Social Profile Claims", "Device Fingerprints"],
            "transfer_mechanism_required": "Clerk DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Authentication DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Clerk DPA and configure encrypted webhook signing secrets."
        },
        "firebase": {
            "name": "Google Firebase",
            "aliases": ["firebase", "firebase-admin", "@firebase/"],
            "category": "Authentication, Firestore & Push Telemetry",
            "jurisdiction": "United States",
            "data_types_processed": ["Device IDs", "Push Tokens", "Authentication Metadata", "Firestore Documents"],
            "transfer_mechanism_required": "Google Cloud DPA + UK International Transfer Safeguards",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "HIGH",
            "recommendation": "Audit Firebase Analytics tracking to ensure non-essential SDK telemetry requires PECR opt-in consent."
        },
        "supertokens": {
            "name": "SuperTokens Inc.",
            "aliases": ["supertokens", "supertokens-node"],
            "category": "Open-Source / Managed User Authentication",
            "jurisdiction": "United States / Self-Hosted",
            "data_types_processed": ["Session Tokens", "User Credentials"],
            "transfer_mechanism_required": "SuperTokens DPA (if cloud) / N/A (if self-hosted)",
            "article_28_dpa_status": "Authentication Processor Agreement",
            "risk_level": "MEDIUM",
            "recommendation": "Self-host core to retain 100% on-premises data residency."
        },

        # --- COMMUNICATIONS, EMAIL & SMS ---
        "twilio": {
            "name": "Twilio Inc.",
            "aliases": ["twilio"],
            "category": "SMS, Voice & Video Communications",
            "jurisdiction": "United States",
            "data_types_processed": ["Customer Phone Numbers", "SMS Logs", "Call Audio Transcripts"],
            "transfer_mechanism_required": "Twilio Binding Corporate Rules (BCR) / DPA",
            "article_28_dpa_status": "Mandatory Communications DPA",
            "risk_level": "HIGH",
            "recommendation": "Sign Twilio Data Protection Addendum utilizing Twilio approved BCRs for UK transfers."
        },
        "sendgrid": {
            "name": "Twilio SendGrid",
            "aliases": ["sendgrid", "@sendgrid/"],
            "category": "Transactional & Marketing Email",
            "jurisdiction": "United States",
            "data_types_processed": ["Customer Email Addresses", "Email Delivery Logs", "Click Tracking"],
            "transfer_mechanism_required": "Twilio BCR / DPA",
            "article_28_dpa_status": "Mandatory Email Processor DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Disable non-essential click-tracking to prevent PECR tracker flags without user consent."
        },
        "mailgun": {
            "name": "Mailgun Technologies (Sinch)",
            "aliases": ["mailgun"],
            "category": "Transactional Email API",
            "jurisdiction": "United States / EU (Germany)",
            "data_types_processed": ["Recipient Emails", "Email Headers", "Delivery Status"],
            "transfer_mechanism_required": "Mailgun EU DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Configure Mailgun EU endpoint (api.eu.mailgun.net) to enforce EU data residency."
        },
        "postmark": {
            "name": "Postmark (ActiveCampaign)",
            "aliases": ["postmark"],
            "category": "High-Deliverability Transactional Email",
            "jurisdiction": "United States",
            "data_types_processed": ["Customer Email Addresses", "Password Reset Tokens"],
            "transfer_mechanism_required": "Postmark DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Postmark DPA and enforce 7-day message purge."
        },
        "resend": {
            "name": "Resend Inc.",
            "aliases": ["resend"],
            "category": "Modern Developer Email API",
            "jurisdiction": "United States",
            "data_types_processed": ["User Emails", "Broadcast Lists", "Message Content"],
            "transfer_mechanism_required": "Resend DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Resend Data Processing Addendum."
        },
        "pusher": {
            "name": "Pusher Ltd.",
            "aliases": ["pusher", "pusher-js"],
            "category": "Real-Time WebSocket Messaging",
            "jurisdiction": "United Kingdom (UK GDPR Native)",
            "data_types_processed": ["WebSocket Channel Data", "User Presence", "IP Telemetry"],
            "transfer_mechanism_required": "UK GDPR Native Processor Agreement",
            "article_28_dpa_status": "Mandatory WebSocket DPA",
            "risk_level": "LOW",
            "recommendation": "Execute Pusher UK DPA."
        },

        # --- MEDIA, CDN & STORAGE ---
        "cloudinary": {
            "name": "Cloudinary Ltd.",
            "aliases": ["cloudinary", "multer-storage-cloudinary"],
            "category": "Media Storage, Optimization & Image CDN",
            "jurisdiction": "United States / Israel (Adequacy Decision)",
            "data_types_processed": ["Listing Photos", "Profile Avatars", "User Media Uploads"],
            "transfer_mechanism_required": "UK Addendum / EU Standard Contractual Clauses (SCCs)",
            "article_28_dpa_status": "Mandatory Media DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Cloudinary Data Processing Addendum and enforce secure signed upload URLs."
        },
        "uploadthing": {
            "name": "Uploadthing Inc.",
            "aliases": ["uploadthing", "@uploadthing/"],
            "category": "Developer File Upload & Storage",
            "jurisdiction": "United States",
            "data_types_processed": ["Uploaded Attachments", "File Metadata", "MIME Types"],
            "transfer_mechanism_required": "Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Uploadthing DPA and enforce virus scanning."
        },

        # --- MAPS & GEOLOCATION ---
        "mapbox": {
            "name": "Mapbox Inc.",
            "aliases": ["mapbox", "@mapbox/"],
            "category": "Interactive Maps & Geolocation Telemetry",
            "jurisdiction": "United States",
            "data_types_processed": ["User IP Addresses", "Geocoordinates", "Map Telemetry"],
            "transfer_mechanism_required": "UK-US Data Bridge / EU Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Geolocation DPA",
            "risk_level": "HIGH",
            "recommendation": "Execute Mapbox Data Processing Addendum and configure privacy-preserving coordinate fuzzing."
        },
        "googlemaps": {
            "name": "Google Maps Platform",
            "aliases": ["googlemaps", "@googlemaps/", "google-maps"],
            "category": "Places, Geocoding & Routing Services",
            "jurisdiction": "United States / Global",
            "data_types_processed": ["Latitude / Longitude", "User Search Addresses", "IP Location"],
            "transfer_mechanism_required": "Google Maps Controller-to-Controller DPA",
            "article_28_dpa_status": "Controller Terms of Service",
            "risk_level": "HIGH",
            "recommendation": "Audit geocoding query retention to ensure address inputs are ephemeral."
        },

        # --- ANALYTICS, OBSERVABILITY & ERROR TRACKING ---
        "sentry": {
            "name": "Sentry (Functional Software Inc.)",
            "aliases": ["sentry", "@sentry/"],
            "category": "Application Error & Crash Telemetry",
            "jurisdiction": "United States / EU",
            "data_types_processed": ["Stack Traces", "Client Device Telemetry", "HTTP Request Headers", "User IP"],
            "transfer_mechanism_required": "Sentry DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Observability DPA",
            "risk_level": "HIGH",
            "recommendation": "Configure Sentry Data Scrubbing to redact email addresses, passwords, and tokens from error breadcrumbs."
        },
        "posthog": {
            "name": "PostHog Inc.",
            "aliases": ["posthog", "posthog-js"],
            "category": "Product Analytics & Session Recording",
            "jurisdiction": "EU Cloud / US Cloud",
            "data_types_processed": ["User Clickstreams", "Session Replays", "IP Addresses"],
            "transfer_mechanism_required": "PostHog DPA + PECR Cookie Banner Consent",
            "article_28_dpa_status": "Mandatory Processor DPA",
            "risk_level": "HIGH",
            "recommendation": "Configure PostHog EU cloud instance; enable strict input masking on session recording to mask sensitive user queries."
        },
        "datadog": {
            "name": "Datadog Inc.",
            "aliases": ["datadog", "dd-trace"],
            "category": "Infrastructure Monitoring & APM Logs",
            "jurisdiction": "United States / EU (Dublin)",
            "data_types_processed": ["Server Logs", "Network Traces", "IP Addresses"],
            "transfer_mechanism_required": "Datadog DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory APM DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Route telemetry to Datadog EU region (app.datadoghq.eu)."
        },
        "mixpanel": {
            "name": "Mixpanel Inc.",
            "aliases": ["mixpanel"],
            "category": "User Event Behavioral Analytics",
            "jurisdiction": "United States / EU Cloud",
            "data_types_processed": ["User Unique IDs", "Event Timestamps", "Feature Funnel Steps"],
            "transfer_mechanism_required": "Mixpanel DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Analytics DPA",
            "risk_level": "HIGH",
            "recommendation": "Configure Mixpanel EU residency and require user consent prior to tracker initialization."
        },
        "algolia": {
            "name": "Algolia Inc.",
            "aliases": ["algolia", "@algolia/", "algoliasearch"],
            "category": "Search-as-a-Service & Discovery",
            "jurisdiction": "United States / France (EU)",
            "data_types_processed": ["Search Query Strings", "Indexed Catalog Records", "User IP Telemetry"],
            "transfer_mechanism_required": "Algolia DPA + Standard Contractual Clauses",
            "article_28_dpa_status": "Mandatory Search DPA",
            "risk_level": "MEDIUM",
            "recommendation": "Execute Algolia DPA and disable logging on confidential user search inputs."
        }
    }

    def __init__(self):
        pass

    def detect_subprocessors(self, imports_and_sdks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Scans all imported packages, SDKs, and manifest dependencies across any programming language
        to construct a statutory Article 28 Subprocessor Register.
        """
        detected_vendors = {}

        for item in imports_and_sdks:
            pkg_name = item.get("package", "").lower().strip()
            source_file = item.get("source_file", "")
            if not pkg_name:
                continue

            for db_key, vendor_info in self.SUBPROCESSOR_DATABASE.items():
                aliases = vendor_info.get("aliases", [db_key])
                matched = False
                for alias in aliases:
                    if alias in pkg_name or (alias.startswith("@") and pkg_name.startswith(alias)):
                        matched = True
                        break

                if matched:
                    if db_key not in detected_vendors:
                        detected_vendors[db_key] = {
                            **vendor_info,
                            "detected_packages": [pkg_name],
                            "referencing_files": [source_file] if source_file else []
                        }
                    else:
                        if pkg_name not in detected_vendors[db_key]["detected_packages"]:
                            detected_vendors[db_key]["detected_packages"].append(pkg_name)
                        if source_file and source_file not in detected_vendors[db_key]["referencing_files"]:
                            detected_vendors[db_key]["referencing_files"].append(source_file)

        # International Transfer & Risk Summary
        us_transfers = [v["name"] for v in detected_vendors.values() if "United States" in v["jurisdiction"]]
        critical_vendors = [v["name"] for v in detected_vendors.values() if v["risk_level"] == "CRITICAL"]

        return {
            "total_subprocessors_detected": len(detected_vendors),
            "critical_risk_subprocessors": len(critical_vendors),
            "international_transfers_count": len(us_transfers),
            "us_transfers_detected": us_transfers,
            "subprocessor_register": list(detected_vendors.values())
        }
