"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-103 API Route & Controller Data-Flow Tracer
Analyzes API endpoints to identify data flows, catch missing DSAR hooks,
and detect practitioner data leakage or unconsented collection.
"""

from typing import Dict, List, Any

class APIRouteTracer:
    # Key compliance endpoint patterns
    DSAR_ERASURE_PATTERNS = ["delete", "remove", "erase", "account/delete", "gdpr/forget"]
    DSAR_PORTABILITY_PATTERNS = ["export", "download-data", "portability", "my-data", "gdpr/export"]
    CONSENT_ENDPOINT_PATTERNS = ["consent", "privacy-preference", "opt-in", "terms/accept"]
    
    # Sensitive consultation & AI endpoints
    SENSITIVE_CONSULTATION_PATTERNS = ["consultation", "session", "horoscope", "kundli", "chat", "counseling", "expert"]
    AI_WORKFLOW_PATTERNS = ["llm", "openai", "claude", "gemini", "ai-chat", "generate-reading", "summarize"]
    PRACTITIONER_ACCESS_PATTERNS = ["practitioner", "astrologer", "expert", "vendor", "partner"]

    def __init__(self):
        pass

    def trace_routes(self, parsed_routes: List[Dict[str, Any]], parsed_models_summary: Dict[str, Any]) -> Dict[str, Any]:
        """Audits route definitions against statutory GDPR and DPDP requirements."""
        traced_routes = []
        has_erasure_endpoint = False
        has_export_endpoint = False
        has_consent_endpoint = False
        practitioner_endpoints = []
        ai_endpoints = []
        sensitive_data_endpoints = []
        compliance_gaps = []

        for r in parsed_routes:
            name = r.get("endpoint_name", "").lower()
            path = r.get("path", "").lower()
            file_src = r.get("source_file", "")
            params = [p.lower() for p in r.get("parameters", [])]
            combined_desc = f"{name} {path} {' '.join(params)}"

            # DSAR Checks
            if any(pat in combined_desc for pat in self.DSAR_ERASURE_PATTERNS):
                has_erasure_endpoint = True
            if any(pat in combined_desc for pat in self.DSAR_PORTABILITY_PATTERNS):
                has_export_endpoint = True
            if any(pat in combined_desc for pat in self.CONSENT_ENDPOINT_PATTERNS):
                has_consent_endpoint = True

            # Route classification
            is_practitioner_route = any(pat in combined_desc for pat in self.PRACTITIONER_ACCESS_PATTERNS)
            is_ai_route = any(pat in combined_desc for pat in self.AI_WORKFLOW_PATTERNS)
            is_sensitive_route = any(pat in combined_desc for pat in self.SENSITIVE_CONSULTATION_PATTERNS)

            route_risks = []

            if is_practitioner_route:
                practitioner_endpoints.append(r)
                route_risks.append({
                    "rule": "UK GDPR Art 5(1)(c) Data Minimisation & Commercial Protection",
                    "severity": "HIGH",
                    "description": "Practitioner route detected. Ensure customer direct contact details (phone, email) are strictly masked to prevent off-platform poaching and unauthorized data copying."
                })

            if is_ai_route:
                ai_endpoints.append(r)
                route_risks.append({
                    "rule": "UK GDPR Art 22 & ICO AI Guidance / DPDPA Sec 4",
                    "severity": "HIGH",
                    "description": "Endpoint invokes AI/LLM workflow. Statutory requirement: Ensure zero-retention API flag is enabled and verify user personal data is not processed for model training."
                })

            if is_sensitive_route:
                sensitive_data_endpoints.append(r)
                # Check if consent parameter is captured
                consent_params = [p for p in params if "consent" in p or "agree" in p or "accepted" in p]
                if not consent_params:
                    route_risks.append({
                        "rule": "UK GDPR Art 9(2)(a) Explicit Consent",
                        "severity": "CRITICAL",
                        "description": "Sensitive consultation endpoint does not verify explicit Article 9 consent payload or token before processing sensitive consultation data."
                    })

            traced_routes.append({
                "endpoint": r.get("endpoint_name"),
                "path": r.get("path", r.get("endpoint_name")),
                "source_file": file_src,
                "line_number": r.get("line_number"),
                "is_sensitive": is_sensitive_route,
                "is_ai": is_ai_route,
                "is_practitioner": is_practitioner_route,
                "risk_flags": route_risks
            })

        # Overall Architectural Gap Analysis
        if not has_erasure_endpoint:
            compliance_gaps.append({
                "statute": "UK GDPR Article 17 (Right to Erasure) & DPDPA 2023 Section 12(3)",
                "severity": "CRITICAL",
                "finding": "Missing automated Account & Data Deletion endpoint (e.g. DELETE /api/user/account).",
                "remediation": "Add statutory deletion API that soft-deletes user profile and cryptographically scrubs PII within 30 days."
            })

        if not has_export_endpoint:
            compliance_gaps.append({
                "statute": "UK GDPR Article 20 (Right to Data Portability)",
                "severity": "HIGH",
                "finding": "Missing automated Personal Data Export endpoint (e.g. GET /api/user/export-data).",
                "remediation": "Provide structured JSON/CSV data export bundle for users upon request."
            })

        if not has_consent_endpoint and parsed_models_summary.get("special_category_fields_detected", 0) > 0:
            compliance_gaps.append({
                "statute": "UK GDPR Article 7 & Article 9(2)(a) Conditions for Consent",
                "severity": "CRITICAL",
                "finding": "No dedicated Consent Recording / Audit Logging API detected in routes.",
                "remediation": "Implement POST /api/consent endpoint storing immutable timestamped consent records (timestamp, user_id, purpose, IP, notice_version)."
            })

        return {
            "total_routes_traced": len(parsed_routes),
            "sensitive_routes_count": len(sensitive_data_endpoints),
            "ai_routes_count": len(ai_endpoints),
            "practitioner_routes_count": len(practitioner_endpoints),
            "dsar_erasure_implemented": has_erasure_endpoint,
            "dsar_portability_implemented": has_export_endpoint,
            "consent_endpoint_implemented": has_consent_endpoint,
            "compliance_gaps": compliance_gaps,
            "traced_routes": traced_routes
        }
