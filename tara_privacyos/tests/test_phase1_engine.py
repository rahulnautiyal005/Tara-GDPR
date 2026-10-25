"""
Tara PrivacyOS — Phase 1 Test Suite
Verifies AST parser, PII classifier, Route tracer, Subprocessor detector,
and statutory legal generators.
"""

import os
import unittest
from tara_privacyos.core.repo_ast_parser import RepoASTParser
from tara_privacyos.core.pii_schema_detector import PIISchemaDetector
from tara_privacyos.core.api_route_tracer import APIRouteTracer
from tara_privacyos.core.subprocessor_detector import SubprocessorDetector
from tara_privacyos.legal_engines.uk_gdpr_mandates_gen import UKGDPRMandatesGenerator
from tara_privacyos.legal_engines.india_dpdpa_mandates_gen import IndiaDPDPAMandatesGenerator
from tara_privacyos.privacyos_engine import PrivacyOSEngine

class TestPhase1Engine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.benchmark_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "benchmarks", "sample_consultation_app"))

    def test_repo_ast_parser(self):
        parser = RepoASTParser(self.benchmark_dir)
        results = parser.scan_repository()
        self.assertGreater(results["total_files_scanned"], 0)
        self.assertGreater(len(results["models"]), 0, "Should detect at least 1 model")
        self.assertGreater(len(results["routes"]), 0, "Should detect at least 1 route")
        self.assertGreater(len(results["imports_and_sdks"]), 0, "Should detect imports")

    def test_pii_schema_detector(self):
        parser = RepoASTParser(self.benchmark_dir)
        results = parser.scan_repository()
        detector = PIISchemaDetector()
        pii_res = detector.inspect_models(results["models"])
        
        self.assertGreater(pii_res["special_category_fields_detected"], 0, "Should detect Article 9 health/spiritual fields")
        self.assertIn("KundliConsultationModel", pii_res["high_risk_art9_models"])
        self.assertGreater(pii_res["standard_pii_fields_detected"], 0, "Should detect email/phone PII")

    def test_api_route_tracer(self):
        parser = RepoASTParser(self.benchmark_dir)
        results = parser.scan_repository()
        detector = PIISchemaDetector()
        pii_res = detector.inspect_models(results["models"])
        tracer = APIRouteTracer()
        route_res = tracer.trace_routes(results["routes"], pii_res)

        self.assertFalse(route_res["dsar_erasure_implemented"], "Sample app does not implement erasure endpoint")
        self.assertGreater(len(route_res["compliance_gaps"]), 0, "Should flag missing erasure endpoint")
        self.assertGreater(route_res["practitioner_routes_count"], 0, "Should identify practitioner routes")

    def test_subprocessor_detector(self):
        parser = RepoASTParser(self.benchmark_dir)
        results = parser.scan_repository()
        detector = SubprocessorDetector()
        sub_res = detector.detect_subprocessors(results["imports_and_sdks"])

        detected_names = [v["name"] for v in sub_res["subprocessor_register"]]
        self.assertIn("OpenAI LLC", detected_names, "Should detect OpenAI")
        self.assertIn("Stripe Payments UK, Ltd.", detected_names, "Should detect Stripe")
        self.assertIn("Amazon Web Services (AWS)", detected_names, "Should detect AWS")

    def test_full_pipeline_scan(self):
        engine = PrivacyOSEngine()
        report = engine.scan(self.benchmark_dir)

        self.assertIn("scan_metadata", report)
        self.assertIn("uk_gdpr_compliance_package", report)
        self.assertIn("india_dpdpa_compliance_package", report)
        self.assertTrue(report["uk_gdpr_compliance_package"]["dpia_required"], "DPIA should be required for Art 9 data")
        self.assertGreater(len(report["uk_gdpr_compliance_package"]["article_30_ropa"]), 0, "RoPA should be generated")

if __name__ == "__main__":
    unittest.main()
