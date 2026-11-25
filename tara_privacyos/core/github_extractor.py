"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: GitHub Repository Extractor & Use-Case Classifier
Clones and analyzes any GitHub repository or local codebase, extracts
data models, API routes, third-party dependencies, and infers the application's
real-world business use case to drive tailored statutory GDPR generation.
"""

import os
import re
import ast
import json
import shutil
import tempfile
import subprocess
import urllib.request
from pathlib import Path
from typing import Dict, List, Any, Optional

from tara_privacyos.core.pii_schema_detector import PIISchemaDetector
from tara_privacyos.core.subprocessor_detector import SubprocessorDetector

class GitHubRepoExtractor:
    """
    Extracts architectural metadata, data models, routes, dependencies,
    and business use case from any GitHub repository.
    """

    DOMAIN_KEYWORDS = {
        "Astrology & Spiritual Consultation": [
            "kundli", "horoscope", "astrology", "spiritual", "zodiac", "tarot",
            "birth_chart", "consultation", "practitioner", "vedic"
        ],
        "Telehealth & Medical Diagnostics": [
            "patient", "doctor", "health", "medical", "clinic", "symptom",
            "prescription", "treatment", "diagnosis", "telehealth", "ehr"
        ],
        "E-Commerce & Retail Marketplace": [
            "product", "order", "cart", "checkout", "shipping", "inventory",
            "merchant", "catalog", "store", "stripe", "payment"
        ],
        "FinTech & Payment Services": [
            "wallet", "ledger", "transaction", "invoice", "bank", "credit",
            "payout", "transfer", "kyc", "crypto", "exchange"
        ],
        "AI Platform & LLM Copilot": [
            "openai", "llm", "chat", "prompt", "completion", "agent",
            "embedding", "rag", "vector", "langchain", "anthropic"
        ],
        "HR & Recruitment Management": [
            "employee", "candidate", "resume", "applicant", "job", "payroll",
            "interview", "attendance", "recruitment", "cv"
        ],
        "EdTech & Student Learning": [
            "student", "course", "lesson", "quiz", "instructor", "grade",
            "school", "curriculum", "assignment", "education"
        ],
        "Maritime, Shipping & Port Operations": [
            "port", "vessel", "berth", "ship", "cargo", "container", "terminal",
            "marine", "logistics", "voyage", "quay", "anchorage", "portops", "stevedoring", "dock"
        ],
        "Logistics, Supply Chain & Freight": [
            "fleet", "truck", "warehouse", "freight", "delivery", "dispatch",
            "route", "consignment", "tracking", "driver", "transport", "shipment"
        ],
        "Developer Tools, DevOps & Cloud Infrastructure": [
            "cli", "sdk", "api", "cloud", "docker", "kubernetes", "infra",
            "deploy", "pipeline", "ci", "cd", "monitoring", "git", "cluster", "observability"
        ],
        "Cybersecurity, IAM & Identity Governance": [
            "auth", "token", "iam", "saml", "sso", "security", "vulnerability",
            "audit", "vault", "encrypt", "firewall", "identity", "zero_trust"
        ],
        "SaaS & Enterprise Collaboration": [
            "tenant", "workspace", "organization", "project", "task",
            "team", "role", "subscription", "member", "collaboration"
        ]
    }

    def __init__(self):
        self.pii_detector = PIISchemaDetector()
        self.subproc_detector = SubprocessorDetector()

    def normalize_repo_url(self, repo_url_or_path: str) -> Dict[str, Any]:
        """Normalizes GitHub URL or detects local file system path."""
        s = repo_url_or_path.strip()
        
        # Local path check
        if os.path.exists(s):
            return {
                "type": "local",
                "path": os.path.abspath(s),
                "repo_name": os.path.basename(os.path.abspath(s)),
                "clone_url": s
            }

        # Handle 'owner/repo' shorthand
        if re.match(r"^[\w\-]+/[\w\-]+$", s):
            s = f"https://github.com/{s}"

        # Standard GitHub URL
        match = re.match(r"https?://github\.com/([\w\-]+)/([\w\-]+)(?:\.git)?", s)
        if match:
            owner, repo = match.group(1), match.group(2)
            clean_repo = repo.removesuffix(".git")
            return {
                "type": "github",
                "owner": owner,
                "repo": clean_repo,
                "repo_name": f"{owner}/{clean_repo}",
                "clone_url": f"https://github.com/{owner}/{clean_repo}.git",
                "api_url": f"https://api.github.com/repos/{owner}/{clean_repo}",
                "zip_url": f"https://github.com/{owner}/{clean_repo}/archive/refs/heads/main.zip"
            }

        return {
            "type": "unknown",
            "path": s,
            "repo_name": os.path.basename(s),
            "clone_url": s
        }

    def extract_from_repo(self, repo_url_or_path: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Clones or fetches the repository, parses files, detects schemas,
        routes, dependencies, and infers use case.
        """
        info = self.normalize_repo_url(repo_url_or_path)
        temp_dir = None
        target_dir = None
        clone_success = False

        if info["type"] == "local":
            target_dir = info["path"]
        else:
            temp_dir = tempfile.mkdtemp(prefix="tara_gh_")
            clone_cmd = ["git", "clone", "--depth", "1"]
            if branch:
                clone_cmd.extend(["-b", branch])
            clone_cmd.extend([info["clone_url"], temp_dir])

            try:
                proc = subprocess.run(
                    clone_cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=45
                )
                target_dir = temp_dir
                clone_success = True
            except Exception as clone_err:
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
                raise RuntimeError(
                    f"Could not clone repository '{repo_url_or_path}'. "
                    f"Please verify that the repository URL is public and valid, or that the specified branch exists. Error details: {str(clone_err)}"
                )

        try:
            extraction_result = self._scan_directory(target_dir, info)
            return extraction_result
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def _scan_directory(self, root_dir: str, repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """Scans code files, schemas, dependencies, and README in the cloned directory."""
        readme_content = ""
        package_files = []
        raw_models = []
        raw_routes = []
        imports_and_sdks = []
        total_files = 0
        file_tree = []

        ignore_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".next", ".cache", "target"}

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            for fname in filenames:
                total_files += 1
                fpath = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(fpath, root_dir).replace("\\", "/")

                if len(file_tree) < 50:
                    file_tree.append(rel_path)

                fname_lower = fname.lower()
                ext = os.path.splitext(fname)[1].lower()

                # README extraction
                if fname_lower in ["readme.md", "readme.txt", "readme"]:
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as rf:
                            readme_content = rf.read(8000)
                    except Exception:
                        pass

                # Python AST Scan
                if ext == ".py":
                    py_data = self._parse_python(fpath, rel_path)
                    raw_models.extend(py_data.get("models", []))
                    raw_routes.extend(py_data.get("routes", []))
                    imports_and_sdks.extend(py_data.get("imports", []))

                # JS/TS Scan
                elif ext in [".js", ".ts", ".jsx", ".tsx"]:
                    js_data = self._parse_javascript(fpath, rel_path)
                    raw_models.extend(js_data.get("models", []))
                    raw_routes.extend(js_data.get("routes", []))
                    imports_and_sdks.extend(js_data.get("imports", []))

                # Database & Schema files
                elif ext in [".prisma", ".sql"]:
                    schema_data = self._parse_schema(fpath, rel_path)
                    raw_models.extend(schema_data.get("models", []))

                # Dependency declarations
                elif fname in ["requirements.txt", "package.json", "Pipfile", "pyproject.toml"]:
                    dep_items = self._parse_dependency_file(fpath, rel_path)
                    imports_and_sdks.extend(dep_items)

        # Step 2: Classify PII & Article 9 data fields
        pii_summary = self.pii_detector.inspect_models(raw_models)

        # Step 3: Classify Subprocessors & International Transfers
        subproc_summary = self.subproc_detector.detect_subprocessors(imports_and_sdks)

        # Step 4: Infer Business Domain & Primary Use-Case
        use_case_profile = self._infer_use_case(
            repo_info=repo_info,
            readme_text=readme_content,
            models=raw_models,
            routes=raw_routes,
            subprocessors=subproc_summary.get("subprocessor_register", [])
        )

        return {
            "repository_metadata": {
                "name": repo_info.get("repo_name", "Unknown Repository"),
                "source_url": repo_info.get("clone_url", ""),
                "type": repo_info.get("type", "github"),
                "total_files_scanned": total_files,
                "file_samples": file_tree[:25],
                "has_readme": bool(readme_content),
                "readme_snippet": readme_content[:400] if readme_content else "No README file detected."
            },
            "use_case_profile": use_case_profile,
            "extracted_models": raw_models,
            "pii_and_special_category": pii_summary,
            "extracted_routes": raw_routes,
            "subprocessors_and_transfers": subproc_summary
        }

    def _infer_use_case(
        self,
        repo_info: Dict[str, Any],
        readme_text: str,
        models: List[Dict[str, Any]],
        routes: List[Dict[str, Any]],
        subprocessors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyzes the combined text signals (README, model names, fields, route paths)
        to identify the specific business domain, data subjects, and processing purposes.
        """
        combined_text = (
            readme_text.lower() + " " +
            " ".join(m.get("model_name", "").lower() for m in models) + " " +
            " ".join(
                f.get("field_name", "").lower()
                for m in models
                for f in m.get("fields", [])
            ) + " " +
            " ".join(r.get("endpoint", r.get("endpoint_name", "")).lower() for r in routes)
        )

        domain_scores = {}
        for domain, kw_list in self.DOMAIN_KEYWORDS.items():
            score = 0
            for kw in kw_list:
                score += len(re.findall(r"\b" + re.escape(kw) + r"\b", combined_text))
            domain_scores[domain] = score

        # Determine primary domain
        sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
        top_domain, top_score = sorted_domains[0] if sorted_domains else ("General Web Application", 0)
        if top_score == 0:
            top_domain = "B2C / B2B Web & Mobile Application"

        # Determine Data Subjects
        data_subjects = ["Platform Users / Registered Customers"]
        if "practitioner" in combined_text or "doctor" in combined_text or "expert" in combined_text:
            data_subjects.append("External Practitioners / Professional Consultants")
        if "employee" in combined_text or "staff" in combined_text:
            data_subjects.append("Employees / Internal Contractors")
        if "patient" in combined_text:
            data_subjects.append("Patients / Healthcare Clients")
        if "child" in combined_text or "age" in combined_text or "birth" in combined_text:
            data_subjects.append("Minors / Family Members (Parental Consent Required)")

        # Determine Primary Processing Purposes
        processing_purposes = [
            "User Identity Authentication & Account Management",
            "Core Application Service Delivery & User Experience"
        ]
        if any("payment" in r.get("endpoint", "").lower() or "stripe" in combined_text for r in routes):
            processing_purposes.append("Payment Card Processing, Invoicing & Financial Accounting")
        if any("consult" in r.get("endpoint", "").lower() or "booking" in r.get("endpoint", "").lower() for r in routes):
            processing_purposes.append("1-on-1 Consultation Booking, Scheduling & Session Fulfillment")
        if any("openai" in s.get("name", "").lower() for s in subprocessors) or "ai" in combined_text:
            processing_purposes.append("Automated AI Question Summarization & Context Analysis (OpenAI / LLM)")
        if "health" in combined_text or "kundli" in combined_text:
            processing_purposes.append("Processing of Sensitive Profile Context (Explicit Consent Art 9)")

        # Target jurisdictions
        jurisdictions = ["United Kingdom (UK GDPR & DPA 2018)", "Republic of India (DPDP Act 2023)"]

        return {
            "primary_domain": top_domain,
            "confidence_score": min(100, max(60, top_score * 12)),
            "application_description": (
                f"Production software service operating in the {top_domain} space, "
                f"handling {len(models)} primary data models and {len(routes)} API endpoints."
            ),
            "data_subjects": data_subjects,
            "processing_purposes": processing_purposes,
            "applicable_jurisdictions": jurisdictions,
            "inferred_special_category": any(
                k in combined_text for k in ["health", "kundli", "spiritual", "medical", "biometric"]
            )
        }

    def _parse_python(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models, routes, and imports from a Python file using AST."""
        res = {"models": [], "routes": [], "imports": []}
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            tree = ast.parse(content, filename=rel_path)
        except Exception:
            return res

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    res["imports"].append({"source_file": rel_path, "package": alias.name, "type": "import"})
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    res["imports"].append({"source_file": rel_path, "package": node.module, "type": "from_import"})

            elif isinstance(node, ast.ClassDef):
                fields = []
                for item in node.body:
                    if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                        fields.append({"field_name": item.target.id, "line_number": item.lineno})
                    elif isinstance(item, ast.Assign):
                        for target in item.targets:
                            if isinstance(target, ast.Name):
                                fields.append({"field_name": target.id, "line_number": target.lineno})
                if fields:
                    res["models"].append({
                        "model_name": node.name,
                        "source_file": rel_path,
                        "line_number": node.lineno,
                        "fields": fields
                    })

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                decorators = []
                for dec in node.decorator_list:
                    if isinstance(dec, ast.Call):
                        if isinstance(dec.func, ast.Attribute):
                            decorators.append(f"{getattr(dec.func.value, 'id', '')}.{dec.func.attr}")
                        elif isinstance(dec.func, ast.Name):
                            decorators.append(dec.func.id)
                    elif isinstance(dec, ast.Attribute):
                        decorators.append(f"{getattr(dec.func.value, 'id', '')}.{dec.attr}")
                    elif isinstance(dec, ast.Name):
                        decorators.append(dec.id)

                route_decs = [d for d in decorators if any(r in d.lower() for r in ["get", "post", "put", "delete", "patch", "route", "api"])]
                if route_decs or "endpoint" in node.name.lower() or "api" in node.name.lower():
                    res["routes"].append({
                        "endpoint": node.name,
                        "path": f"/{node.name.replace('_', '/')}",
                        "source_file": rel_path,
                        "line_number": node.lineno,
                        "decorators": route_decs
                    })

        return res

    def _parse_javascript(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models, routes, and imports from JS/TS using regex."""
        res = {"models": [], "routes": [], "imports": []}
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return res

        # Imports
        imports = re.findall(r'''(?:import\s+.*?from\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\s*\))''', content)
        for imp in imports:
            pkg = imp[0] or imp[1]
            if pkg and not pkg.startswith("."):
                res["imports"].append({"source_file": rel_path, "package": pkg, "type": "npm_package"})

        # Routes
        route_matches = re.finditer(r'''(?:app|router|api)\.(get|post|put|delete|patch)\s*\(\s*['"]([^'"]+)['"]''', content, re.IGNORECASE)
        for m in route_matches:
            method, path = m.group(1).upper(), m.group(2)
            res["routes"].append({
                "endpoint": f"{method} {path}",
                "path": path,
                "source_file": rel_path,
                "line_number": content[:m.start()].count("\n") + 1,
                "decorators": [method]
            })

        # Mongoose / Prisma models
        schema_matches = re.finditer(r'''(?:const|let|var)\s+(\w+Schema|\w+Model)\s*=\s*new\s+Schema\(\s*\{([^}]+)\}''', content, re.DOTALL)
        for sm in schema_matches:
            name, body = sm.group(1), sm.group(2)
            fields = []
            for f_match in re.finditer(r'''(\w+)\s*:\s*\{''', body):
                fields.append({"field_name": f_match.group(1), "line_number": content[:f_match.start()].count("\n") + 1})
            if fields:
                res["models"].append({
                    "model_name": name,
                    "source_file": rel_path,
                    "line_number": content[:sm.start()].count("\n") + 1,
                    "fields": fields
                })

        return res

    def _parse_schema(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        """Parses Prisma or SQL schema definitions."""
        res = {"models": []}
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return res

        # Prisma models
        prisma_matches = re.finditer(r'''model\s+(\w+)\s*\{([^}]+)\}''', content)
        for pm in prisma_matches:
            model_name, body = pm.group(1), pm.group(2)
            fields = []
            for line in body.splitlines():
                parts = line.strip().split()
                if parts and not parts[0].startswith("//") and not parts[0].startswith("@@"):
                    fields.append({"field_name": parts[0], "line_number": 1})
            if fields:
                res["models"].append({
                    "model_name": model_name,
                    "source_file": rel_path,
                    "line_number": 1,
                    "fields": fields
                })

        # SQL CREATE TABLE
        sql_matches = re.finditer(r'''CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\(([^;]+)\)''', content, re.IGNORECASE)
        for sm in sql_matches:
            table_name, body = sm.group(1), sm.group(2)
            fields = []
            for line in body.splitlines():
                parts = line.strip().replace(",", "").split()
                if parts and parts[0].upper() not in ["PRIMARY", "FOREIGN", "KEY", "CONSTRAINT", "UNIQUE"]:
                    fields.append({"field_name": parts[0], "line_number": 1})
            if fields:
                res["models"].append({
                    "model_name": table_name,
                    "source_file": rel_path,
                    "line_number": 1,
                    "fields": fields
                })

        return res

    def _parse_dependency_file(self, fpath: str, rel_path: str) -> List[Dict[str, Any]]:
        """Parses dependency lists (package.json, requirements.txt)."""
        deps = []
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return deps

        if fpath.endswith("package.json"):
            try:
                pkg_data = json.loads(content)
                all_deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                for pkg in all_deps.keys():
                    deps.append({"source_file": rel_path, "package": pkg, "type": "npm_dependency"})
            except Exception:
                pass
        else: # requirements.txt / Pipfile
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg_name = re.split(r"[=<>]", line)[0].strip()
                    if pkg_name:
                        deps.append({"source_file": rel_path, "package": pkg_name, "type": "python_dependency"})

        return deps
