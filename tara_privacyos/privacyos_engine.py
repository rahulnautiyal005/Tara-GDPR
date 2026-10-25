"""
Tara PrivacyOS — Code-to-GDPR Engine
Master Pipeline Orchestrator
Coordinates AST parsing, PII schema detection, API route tracing,
subprocessor auditing, and UK GDPR + India DPDPA statutory generation.
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

from tara_privacyos.core.repo_ast_parser import RepoASTParser
from tara_privacyos.core.pii_schema_detector import PIISchemaDetector
from tara_privacyos.core.api_route_tracer import APIRouteTracer
from tara_privacyos.core.subprocessor_detector import SubprocessorDetector
from tara_privacyos.legal_engines.uk_gdpr_mandates_gen import UKGDPRMandatesGenerator
from tara_privacyos.legal_engines.india_dpdpa_mandates_gen import IndiaDPDPAMandatesGenerator

class PrivacyOSEngine:
    def __init__(self):
        self.pii_detector = PIISchemaDetector()
        self.route_tracer = APIRouteTracer()
        self.subproc_detector = SubprocessorDetector()
        self.uk_generator = UKGDPRMandatesGenerator()
        self.india_generator = IndiaDPDPAMandatesGenerator()

    def scan(self, target_path_or_url: str) -> Dict[str, Any]:
        """Runs the complete Phase 1 Code-to-GDPR audit pipeline."""
        start_time = datetime.now()
        parser = RepoASTParser(target_path_or_url)

        try:
            # Step 1: AST Repository Scan (CODE-101)
            ast_results = parser.scan_repository()

            # Step 2: PII & Article 9 Schema Detection (CODE-102)
            pii_summary = self.pii_detector.inspect_models(ast_results["models"])

            # Step 3: API Route & Data-Flow Tracing (CODE-103)
            route_summary = self.route_tracer.trace_routes(ast_results["routes"], pii_summary)

            # Step 4: Subprocessor & International Transfer Scan (CODE-104)
            subproc_summary = self.subproc_detector.detect_subprocessors(ast_results["imports_and_sdks"])

            # Step 5: UK GDPR Statutory Mandates & RoPA (CODE-105)
            uk_gdpr_package = self.uk_generator.generate_mandates(pii_summary, route_summary, subproc_summary)

            # Step 6: India DPDP Act 2023 Statutory Obligations (CODE-106)
            india_dpdpa_package = self.india_generator.generate_mandates(pii_summary, route_summary, subproc_summary)

            duration_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # Risk Scoring & Health Grade
            risk_score, health_grade = self._compute_compliance_grade(pii_summary, route_summary, subproc_summary)

            audit_report = {
                "scan_metadata": {
                    "source": target_path_or_url,
                    "scan_timestamp": datetime.now().isoformat(),
                    "duration_ms": duration_ms,
                    "total_files_scanned": ast_results["total_files_scanned"],
                    "privacyos_version": "1.0.0-phase1",
                    "overall_risk_score": risk_score,
                    "health_grade": health_grade
                },
                "ast_overview": {
                    "models_count": len(ast_results["models"]),
                    "routes_count": len(ast_results["routes"]),
                    "dependencies_count": len(ast_results["imports_and_sdks"])
                },
                "pii_and_special_category": pii_summary,
                "api_data_flows": route_summary,
                "subprocessors_and_transfers": subproc_summary,
                "uk_gdpr_compliance_package": uk_gdpr_package,
                "india_dpdpa_compliance_package": india_dpdpa_package
            }

            return audit_report

        finally:
            parser.cleanup()

    def _compute_compliance_grade(self, pii_summary: Dict[str, Any], route_summary: Dict[str, Any], subproc_summary: Dict[str, Any]) -> tuple:
        """Calculates 0-100 compliance risk score and letter grade."""
        score = 100

        # Special category data without explicit consent
        if pii_summary.get("special_category_fields_detected", 0) > 0:
            score -= 20
        
        # Missing DSAR erasure endpoint
        if not route_summary.get("dsar_erasure_implemented", False):
            score -= 15

        # Missing DSAR portability endpoint
        if not route_summary.get("dsar_portability_implemented", False):
            score -= 10

        # Critical subprocessors
        if subproc_summary.get("critical_risk_subprocessors", 0) > 0:
            score -= 15

        # International transfers without documented IDTA
        if subproc_summary.get("international_transfers_count", 0) > 0:
            score -= 15

        # Practitioner routes with potential data leakage
        if route_summary.get("practitioner_routes_count", 0) > 0:
            score -= 10

        score = max(0, min(100, score))

        if score >= 90:
            grade = "A (Compliant)"
        elif score >= 75:
            grade = "B (Minor Gaps)"
        elif score >= 55:
            grade = "C (High Risk — Rectify Before Launch)"
        else:
            grade = "F (Critical Regulatory Vulnerability)"

        return score, grade
