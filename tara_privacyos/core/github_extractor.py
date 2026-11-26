"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: Universal Polyglot GitHub Repository Extractor & Use-Case Classifier
Analyzes codebases across Python, JavaScript, TypeScript, Go, Java, C#, PHP, Rust, Ruby,
and SQL to extract data models, API endpoints, third-party cloud subprocessors,
and infers accurate business domains to generate tailored statutory GDPR & DPDPA compliance.
"""

import os
import re
import ast
import json
import shutil
import tempfile
import subprocess
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Any, Optional

from tara_privacyos.core.pii_schema_detector import PIISchemaDetector
from tara_privacyos.core.subprocessor_detector import SubprocessorDetector

class PrivateRepoError(Exception):
    """Raised when a GitHub repository is private or cannot be accessed without authentication."""
    pass

class GitHubRepoExtractor:
    """
    Extracts architectural metadata, data models, routes, dependencies,
    and business use case from any GitHub repository across all major languages.
    """

    DOMAIN_KEYWORDS = {
        "Real Estate, Property Rental & Hospitality": [
            "rental", "rent", "property", "listing", "listings", "apartment",
            "ghar", "house", "room", "accommodation", "booking", "tenant",
            "landlord", "host", "stay", "guest", "real_estate", "lease", "pg", "apnaghar", "villa", "hotel"
        ],
        "E-Commerce & Retail Marketplace": [
            "product", "order", "cart", "checkout", "shipping", "inventory",
            "merchant", "catalog", "store", "ecommerce", "sku", "basket", "vendor", "shop"
        ],
        "FinTech, Banking & Payment Services": [
            "wallet", "ledger", "transaction", "invoice", "bank", "credit", "debit",
            "payout", "transfer", "kyc", "crypto", "exchange", "fintech", "loan", "portfolio", "stock"
        ],
        "Telehealth, Medicine & Healthcare EHR": [
            "patient", "doctor", "health", "medical", "clinic", "symptom",
            "prescription", "treatment", "diagnosis", "telehealth", "ehr", "emr", "hospital", "pharma"
        ],
        "Astrology, Horoscope & Spiritual Consultation": [
            "kundli", "horoscope", "astrology", "spiritual", "zodiac", "tarot",
            "birth_chart", "consultation", "practitioner", "vedic", "numerology"
        ],
        "EdTech, Learning Management & Student Portals": [
            "student", "course", "lesson", "quiz", "instructor", "grade",
            "school", "curriculum", "assignment", "education", "edtech", "tutor", "lecture", "exam"
        ],
        "Social Media, Community & Dating Platforms": [
            "post", "feed", "like", "follow", "follower", "friend", "social", "dating",
            "match", "timeline", "comment", "community", "dm", "story"
        ],
        "Food Delivery, Restaurant & Quick Commerce": [
            "restaurant", "food", "menu", "dish", "cuisine", "delivery", "kitchen",
            "recipe", "order_food", "dining", "meal", "swiggy", "zomato", "grocery"
        ],
        "Travel, Tourism & Flight Booking": [
            "flight", "hotel", "travel", "tourism", "vacation", "trip", "itinerary",
            "airline", "ticket", "passenger", "destination", "booking_travel", "tour"
        ],
        "Fitness, Sports & Wellness Coaching": [
            "workout", "exercise", "fitness", "gym", "trainer", "calories", "nutrition",
            "diet", "steps", "cardio", "wellness", "reps", "routine"
        ],
        "Media Streaming, Audio & Video Content": [
            "stream", "video", "audio", "music", "podcast", "playlist", "track",
            "album", "channel", "playback", "broadcast", "media", "episode"
        ],
        "Automotive, Mobility & Ride Hailing": [
            "ride", "driver", "vehicle", "car", "taxi", "cab", "fare", "commute",
            "passenger", "mobility", "uber", "ola", "scooter"
        ],
        "Customer Support, CRM & Helpdesk": [
            "ticket", "agent", "support", "helpdesk", "issue", "resolution",
            "customer", "lead", "deal", "pipeline", "sla", "zendesk", "freshdesk"
        ],
        "Logistics, Supply Chain & Fleet Management": [
            "fleet", "truck", "warehouse", "freight", "consignment", "tracking", "courier"
        ],
        "Maritime, Shipping & Port Operations": [
            "port", "vessel", "berth", "ship", "cargo", "container", "terminal",
            "marine", "logistics", "voyage", "quay", "anchorage", "portops", "stevedoring", "dock"
        ],
        "HR, Payroll & Recruitment Management": [
            "employee", "candidate", "resume", "applicant", "job", "payroll",
            "interview", "attendance", "recruitment", "cv", "hr", "hiring", "timesheet"
        ],
        "Legal Tech, Privacy & Regulatory Compliance": [
            "legal", "gdpr", "dpdp", "dpdpa", "privacy", "statutory", "compliance",
            "law", "ropa", "dpia", "audit", "governance", "fiduciary", "regulatory", "dpo", "privacypolicy"
        ],
        "Gaming, Esports & Virtual Worlds": [
            "game", "player", "score", "leaderboard", "quest", "level", "guild",
            "matchmaking", "esports", "unity", "unreal"
        ],
        "IoT, Smart Hardware & Home Automation": [
            "sensor", "iot", "device", "telemetry", "hardware", "firmware",
            "mqtt", "zigbee", "actuator", "smart_home", "gateway"
        ],
        "Cybersecurity, IAM & Identity Governance": [
            "iam", "saml", "sso", "security", "vulnerability",
            "audit", "vault", "firewall", "identity", "zero_trust", "oauth"
        ],
        "AI Platform, Machine Learning & LLM Copilot": [
            "llm", "prompt", "completion", "agent", "embedding", "rag",
            "vector", "langchain", "anthropic", "gpt", "model_training", "copilot"
        ],
        "Developer Tools, DevOps & Cloud Infrastructure": [
            "devops", "kubernetes", "k8s", "terraform", "ansible", "helm",
            "ci_cd", "github_actions", "dockerfile", "cluster", "prometheus", "grafana"
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

        # GitHub URL regexes
        m1 = re.match(r"https?://github\.com/([^/]+)/([^/]+?)(?:\.git)?(?:/.*)?$", s)
        if m1:
            owner, repo = m1.group(1), m1.group(2)
            return {
                "type": "github",
                "owner": owner,
                "repo": repo,
                "repo_name": f"{owner}/{repo}",
                "clone_url": f"https://github.com/{owner}/{repo}.git",
                "api_url": f"https://api.github.com/repos/{owner}/{repo}",
                "zip_url": f"https://github.com/{owner}/{repo}/archive/refs/heads/main.zip"
            }

        m2 = re.match(r"^([^/]+)/([^/]+)$", s)
        if m2:
            owner, clean_repo = m2.group(1), m2.group(2).replace(".git", "")
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

        # For GitHub repositories: Prioritize ultra-fast GitHub API & Raw Fetch
        if info["type"] == "github":
            try:
                return self._extract_via_github_api(info, branch)
            except PrivateRepoError:
                raise
            except Exception:
                pass

        temp_dir = None
        target_dir = None

        if info["type"] == "local":
            target_dir = info["path"]
        else:
            temp_dir = tempfile.mkdtemp(prefix="tara_gh_")
            clone_cmd = [
                "git",
                "-c", "credential.helper=",
                "-c", "core.askPass=",
                "-c", "credential.interactive=false",
                "clone", "--depth", "1"
            ]
            if branch:
                clone_cmd.extend(["-b", branch])
            clone_cmd.extend([info["clone_url"], temp_dir])

            try:
                subprocess.run(
                    clone_cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=90
                )
                target_dir = temp_dir
            except Exception as clone_err:
                if temp_dir and os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir, ignore_errors=True)
                err_str = str(clone_err)
                if hasattr(clone_err, "stderr") and clone_err.stderr:
                    err_str += " " + clone_err.stderr
                if any(w in err_str.lower() for w in ["terminal prompts disabled", "could not read username", "authentication failed", "not found", "access denied", "exit status 128"]):
                    raise PrivateRepoError(
                        f"Repository '{info.get('repo_name', repo_url_or_path)}' is Private or does not exist. "
                        "Tara PrivacyOS requires the repository to be Public on GitHub to scan data models and routes."
                    )
                raise RuntimeError(
                    f"Could not clone repository '{repo_url_or_path}'. "
                    f"Please verify that the repository URL is public and valid. Error details: {err_str}"
                )

        try:
            extraction_result = self._scan_directory(target_dir, info)
            return extraction_result
        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)

    def _extract_via_github_api(self, info: Dict[str, Any], branch: Optional[str] = None) -> Dict[str, Any]:
        """Fast lightweight polyglot GitHub scanner using GitHub REST API and raw file fetching."""
        owner = info["owner"]
        repo = info["repo"]
        headers = {
            "User-Agent": "TaraPrivacyOS/3.0 (Polyglot Statutory Governance Engine)",
            "Accept": "application/vnd.github.v3+json"
        }

        # 1. Fetch default branch and verify access
        repo_api_url = f"https://api.github.com/repos/{owner}/{repo}"
        try:
            req = urllib.request.Request(repo_api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as resp:
                repo_data = json.loads(resp.read().decode("utf-8"))
                default_branch = branch or repo_data.get("default_branch", "main")
        except urllib.error.HTTPError as he:
            if he.code in (401, 403, 404):
                try:
                    resp_body = he.read().decode("utf-8", errors="ignore").lower()
                except Exception:
                    resp_body = ""
                if "rate limit" in resp_body or "api rate limit exceeded" in resp_body:
                    raise Exception("GitHub API rate limit reached, falling back to git clone.")
                raise PrivateRepoError(
                    f"Repository '{owner}/{repo}' is Private or does not exist (GitHub API HTTP {he.code}). "
                    "Tara PrivacyOS requires the repository to be Public on GitHub to scan data models and routes."
                )
            raise
        except Exception:
            default_branch = branch or "main"

        # 2. Fetch recursive git tree
        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
        try:
            t_req = urllib.request.Request(tree_url, headers=headers)
            with urllib.request.urlopen(t_req, timeout=10) as tr:
                tree_data = json.loads(tr.read().decode("utf-8"))
                tree = tree_data.get("tree", [])
        except urllib.error.HTTPError as the_err:
            if the_err.code == 404 and default_branch == "main":
                default_branch = "master"
                tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{default_branch}?recursive=1"
                with urllib.request.urlopen(urllib.request.Request(tree_url, headers=headers), timeout=10) as tr:
                    tree_data = json.loads(tr.read().decode("utf-8"))
                    tree = tree_data.get("tree", [])
            else:
                raise

        # Exclude mock, test, and benchmark fixture directories
        ignore_path_patterns = {
            "benchmark", "benchmarks", "sample_consultation_app", "test", "tests",
            "__tests__", "mock", "mocks", "fixtures", "node_modules", ".git", "dist", "build", "vendor"
        }
        blobs = [item["path"] for item in tree if item.get("type") == "blob" and not any(p in item["path"].lower().split("/") for p in ignore_path_patterns)]
        total_files = len(blobs)
        file_tree = blobs[:30]

        # Polyglot file detection
        schema_exts = (".prisma", ".sql", ".proto", ".graphql")
        code_exts = (".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".java", ".kt", ".cs", ".rs", ".php", ".rb")
        model_keywords = ["model", "schema", "entity", "entities", "types", "dto", "domain", "struct", "table", "db/"]
        route_keywords = ["route", "router", "endpoint", "controller", "api", "handler", "view", "service"]

        schema_files = [
            p for p in blobs
            if p.endswith(schema_exts) or
            (any(k in p.lower() for k in model_keywords) and p.endswith(code_exts))
        ]
        route_files = [
            p for p in blobs
            if any(k in p.lower() for k in route_keywords) and p.endswith(code_exts)
        ]
        dep_files = [
            p for p in blobs
            if os.path.basename(p).lower() in [
                "package.json", "requirements.txt", "pipfile", "pyproject.toml", "setup.py",
                "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "cargo.toml",
                "composer.json", "gemfile", "docker-compose.yml", "docker-compose.yaml", ".env.example"
            ] or p.endswith(".csproj")
        ]
        readme_files = [p for p in blobs if os.path.basename(p).lower().startswith("readme")]

        # Prioritize top 35 most relevant files for instant concurrent scan
        files_to_fetch = []
        seen = set()
        for f in (schema_files[:15] + route_files[:10] + dep_files[:8] + readme_files[:2]):
            if f not in seen:
                seen.add(f)
                files_to_fetch.append(f)

        raw_models = []
        raw_routes = []
        imports_and_sdks = []
        readme_content = ""

        def _fetch_single_file(fpath: str):
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{default_branch}/{fpath}"
            try:
                r_req = urllib.request.Request(raw_url, headers=headers)
                with urllib.request.urlopen(r_req, timeout=8) as rf:
                    return (fpath, rf.read().decode("utf-8", errors="ignore"))
            except Exception:
                return (fpath, "")

        with ThreadPoolExecutor(max_workers=8) as executor:
            fetched_results = list(executor.map(_fetch_single_file, files_to_fetch))

        for fpath, content in fetched_results:
            if not content:
                continue

            fname = os.path.basename(fpath)
            fname_lower = fname.lower()
            ext = os.path.splitext(fname)[1].lower()

            if fname_lower.startswith("readme") and not readme_content:
                readme_content = content[:8000]

            if ext in schema_exts:
                schema_data = self._parse_schema_content(content, fpath)
                raw_models.extend(schema_data.get("models", []))
            elif ext == ".py":
                py_data = self._parse_python_content(content, fpath)
                raw_models.extend(py_data.get("models", []))
                raw_routes.extend(py_data.get("routes", []))
                imports_and_sdks.extend(py_data.get("imports", []))
            elif ext in [".ts", ".js", ".tsx", ".jsx"]:
                js_data = self._parse_javascript_content(content, fpath)
                raw_models.extend(js_data.get("models", []))
                raw_routes.extend(js_data.get("routes", []))
                imports_and_sdks.extend(js_data.get("imports", []))
            elif ext == ".go":
                go_data = self._parse_go_content(content, fpath)
                raw_models.extend(go_data.get("models", []))
                raw_routes.extend(go_data.get("routes", []))
                imports_and_sdks.extend(go_data.get("imports", []))
            elif ext in [".java", ".kt"]:
                java_data = self._parse_java_content(content, fpath)
                raw_models.extend(java_data.get("models", []))
                raw_routes.extend(java_data.get("routes", []))
                imports_and_sdks.extend(java_data.get("imports", []))
            elif ext == ".cs":
                cs_data = self._parse_csharp_content(content, fpath)
                raw_models.extend(cs_data.get("models", []))
                raw_routes.extend(cs_data.get("routes", []))
                imports_and_sdks.extend(cs_data.get("imports", []))
            elif ext == ".php":
                php_data = self._parse_php_content(content, fpath)
                raw_models.extend(php_data.get("models", []))
                raw_routes.extend(php_data.get("routes", []))
                imports_and_sdks.extend(php_data.get("imports", []))
            elif ext in [".rs", ".rb"]:
                gen_data = self._parse_generic_content(content, fpath)
                raw_models.extend(gen_data.get("models", []))
                raw_routes.extend(gen_data.get("routes", []))
                imports_and_sdks.extend(gen_data.get("imports", []))

            if fname_lower in [
                "package.json", "requirements.txt", "pipfile", "pyproject.toml", "setup.py",
                "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "cargo.toml",
                "composer.json", "gemfile", "docker-compose.yml", "docker-compose.yaml", ".env.example"
            ] or ext == ".csproj":
                dep_items = self._parse_dependency_content(content, fname, fpath)
                imports_and_sdks.extend(dep_items)

        # Classify PII, subprocessors, and use-case
        pii_summary = self.pii_detector.inspect_models(raw_models)
        subproc_summary = self.subproc_detector.detect_subprocessors(imports_and_sdks)
        use_case_profile = self._infer_use_case(
            repo_info=info,
            readme_text=readme_content,
            models=raw_models,
            routes=raw_routes,
            subprocessors=subproc_summary.get("subprocessor_register", [])
        )

        return {
            "repository_metadata": {
                "name": info.get("repo_name", f"{owner}/{repo}"),
                "source_url": info.get("clone_url", f"https://github.com/{owner}/{repo}"),
                "type": "github",
                "total_files_scanned": total_files,
                "file_samples": file_tree[:25],
                "has_readme": bool(readme_content),
                "readme_snippet": readme_content[:400] if readme_content else "No README file detected."
            },
            "use_case_profile": use_case_profile,
            "extracted_models": raw_models,
            "pii_and_special_category": pii_summary,
            "extracted_routes": raw_routes,
            "routes_and_endpoints": raw_routes,
            "subprocessors_and_transfers": subproc_summary,
            "subprocessor_register": subproc_summary.get("subprocessor_register", []),
            "ast_metrics": {
                "models": raw_models,
                "routes": raw_routes,
                "dependencies": imports_and_sdks
            }
        }

    def _scan_directory(self, root_dir: str, repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """Scans code files, schemas, dependencies, and README in the cloned directory."""
        readme_content = ""
        raw_models = []
        raw_routes = []
        imports_and_sdks = []
        total_files = 0
        file_tree = []

        ignore_dirs = {
            ".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build",
            ".next", ".cache", "target", "benchmarks", "tests", "test", "fixtures", "mocks", "vendor"
        }

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
                if fname_lower.startswith("readme"):
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="ignore") as rf:
                            readme_content = rf.read(8000)
                    except Exception:
                        pass

                # Language Dispatch
                if ext == ".py":
                    py_data = self._parse_python(fpath, rel_path)
                    raw_models.extend(py_data.get("models", []))
                    raw_routes.extend(py_data.get("routes", []))
                    imports_and_sdks.extend(py_data.get("imports", []))
                elif ext in [".js", ".ts", ".jsx", ".tsx"]:
                    js_data = self._parse_javascript(fpath, rel_path)
                    raw_models.extend(js_data.get("models", []))
                    raw_routes.extend(js_data.get("routes", []))
                    imports_and_sdks.extend(js_data.get("imports", []))
                elif ext == ".go":
                    go_data = self._parse_go(fpath, rel_path)
                    raw_models.extend(go_data.get("models", []))
                    raw_routes.extend(go_data.get("routes", []))
                    imports_and_sdks.extend(go_data.get("imports", []))
                elif ext in [".java", ".kt"]:
                    java_data = self._parse_java(fpath, rel_path)
                    raw_models.extend(java_data.get("models", []))
                    raw_routes.extend(java_data.get("routes", []))
                    imports_and_sdks.extend(java_data.get("imports", []))
                elif ext == ".cs":
                    cs_data = self._parse_csharp(fpath, rel_path)
                    raw_models.extend(cs_data.get("models", []))
                    raw_routes.extend(cs_data.get("routes", []))
                    imports_and_sdks.extend(cs_data.get("imports", []))
                elif ext == ".php":
                    php_data = self._parse_php(fpath, rel_path)
                    raw_models.extend(php_data.get("models", []))
                    raw_routes.extend(php_data.get("routes", []))
                    imports_and_sdks.extend(php_data.get("imports", []))
                elif ext in [".rs", ".rb"]:
                    gen_data = self._parse_generic(fpath, rel_path)
                    raw_models.extend(gen_data.get("models", []))
                    raw_routes.extend(gen_data.get("routes", []))
                    imports_and_sdks.extend(gen_data.get("imports", []))
                elif ext in [".prisma", ".sql", ".proto", ".graphql"]:
                    schema_data = self._parse_schema(fpath, rel_path)
                    raw_models.extend(schema_data.get("models", []))

                # Dependency manifests
                if fname_lower in [
                    "requirements.txt", "package.json", "pipfile", "pyproject.toml", "setup.py",
                    "go.mod", "pom.xml", "build.gradle", "build.gradle.kts", "cargo.toml",
                    "composer.json", "gemfile", "docker-compose.yml", "docker-compose.yaml", ".env.example"
                ] or ext == ".csproj":
                    dep_items = self._parse_dependency_file(fpath, rel_path)
                    imports_and_sdks.extend(dep_items)

        # Classify PII, subprocessors, and use-case
        pii_summary = self.pii_detector.inspect_models(raw_models)
        subproc_summary = self.subproc_detector.detect_subprocessors(imports_and_sdks)
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
            "routes_and_endpoints": raw_routes,
            "subprocessors_and_transfers": subproc_summary,
            "subprocessor_register": subproc_summary.get("subprocessor_register", [])
        }

    def _infer_use_case(
        self,
        repo_info: Dict[str, Any],
        readme_text: str,
        models: List[Dict[str, Any]],
        routes: List[Dict[str, Any]],
        subprocessors: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyzes combined text signals to identify business domain, data subjects, and processing purposes."""
        repo_name_str = (repo_info.get("repo_name", "") + " " + repo_info.get("source_url", "")).lower()
        combined_text = (
            repo_name_str + " " +
            readme_text.lower() + " " +
            " ".join(m.get("model_name", "").lower() for m in models) + " " +
            " ".join(
                f.get("field_name", "").lower()
                for m in models
                for f in m.get("fields", [])
            ) + " " +
            " ".join(r.get("endpoint", r.get("path", "")).lower() for r in routes)
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

        # Determine Data Subjects with strict word boundaries
        data_subjects = ["Platform Users / Registered Customers"]
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["tenant", "renter", "student", "guest", "roommate"]):
            data_subjects.append("Tenants, Renters & Prospective Guests")
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["landlord", "host", "property_owner", "owner"]):
            data_subjects.append("Property Owners, Landlords & Hosts")
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["practitioner", "doctor", "healer", "astrologer", "consultant"]):
            data_subjects.append("External Practitioners / Professional Consultants")
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["employee", "staff", "candidate", "payroll"]):
            data_subjects.append("Employees / Internal Contractors")
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["patient", "ehr", "medical_record"]):
            data_subjects.append("Patients / Healthcare Clients")
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["child", "minor", "parental_consent", "underage"]):
            data_subjects.append("Minors / Family Members (Parental Consent Required)")

        # Determine Primary Processing Purposes
        processing_purposes = [
            "User Identity Authentication & Account Management",
            "Core Application Service Delivery & User Experience"
        ]
        if any("payment" in r.get("endpoint", "").lower() or "billing" in r.get("endpoint", "").lower() for r in routes) or any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["stripe", "razorpay", "billing"]):
            processing_purposes.append("Payment Card Processing, Invoicing & Financial Accounting")
        if any(re.search(r"\b(consult|booking|appointment)\b", r.get("endpoint", "").lower()) for r in routes) or bool(re.search(r"\b(booking|rental|listing|stay)\b", combined_text)):
            processing_purposes.append("Rental Property Listing, Booking Reservation & Stay Management")
        if bool(re.search(r"\b(review|rating|comment)\b", combined_text)):
            processing_purposes.append("User Reviews, Property Ratings & Community Feedback")
        if any("mapbox" in s.get("name", "").lower() for s in subprocessors) or bool(re.search(r"\b(map|mapbox|location|geometry)\b", combined_text)):
            processing_purposes.append("Interactive Property Mapping & Geolocation Visualization (Mapbox)")
        if any("cloudinary" in s.get("name", "").lower() for s in subprocessors) or bool(re.search(r"\b(cloudinary|photo|upload|image)\b", combined_text)):
            processing_purposes.append("Media Storage, Listing Photo Uploads & CDN Delivery (Cloudinary)")
        if any("openai" in s.get("name", "").lower() for s in subprocessors) or any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["openai", "llm", "copilot", "prompt"]):
            processing_purposes.append("Automated AI Question Summarization & Context Analysis (OpenAI / LLM)")
        if any(re.search(r"\b" + re.escape(w) + r"\b", combined_text) for w in ["health_symptoms", "diagnosis", "biometric"]):
            processing_purposes.append("Processing of Sensitive Profile Context (Explicit Consent Art 9)")

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

    # ==============================================================
    # POLYGLOT CODE & SCHEMA PARSERS
    # ==============================================================

    def _parse_python(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_python_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_python_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models, routes, and imports from Python source text (Pydantic, SQLAlchemy, Django)."""
        res = {"models": [], "routes": [], "imports": []}
        try:
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
                                # Captures SQLAlchemy Column or Django models.Field assignments
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
                        decorators.append(dec.func.id)

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
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_javascript_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_javascript_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models (Mongoose, Prisma, TypeORM, Zod, TS Interfaces), routes, and npm packages."""
        res = {"models": [], "routes": [], "imports": []}

        # Imports & requires
        imports = re.findall(r'''(?:import\s+.*?from\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\s*\))''', content)
        for imp in imports:
            pkg = imp[0] or imp[1]
            if pkg and not pkg.startswith("."):
                res["imports"].append({"source_file": rel_path, "package": pkg, "type": "npm_package"})

        # Express / Fastify / Next.js routes
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

        found_model_names = set()

        # 1. Mongoose Schemas (Balanced-brace parser)
        schema_patterns = [
            r'(?:const|let|var)\s+(\w+)\s*=\s*new\s+(?:mongoose\.)?Schema\s*\(',
            r'mongoose\.model\s*\(\s*[\'"](\w+)[\'"]\s*,\s*new\s+(?:mongoose\.)?Schema\s*\('
        ]
        for pat in schema_patterns:
            for sm in re.finditer(pat, content):
                name = sm.group(1)
                if name in found_model_names:
                    continue
                start_pos = sm.end()
                brace_start = content.find('{', start_pos)
                if brace_start == -1 or brace_start - start_pos > 25:
                    continue

                depth = 0
                end_pos = -1
                in_str = None
                i = brace_start
                n = len(content)
                while i < n:
                    c = content[i]
                    if in_str:
                        if c == in_str and content[i-1] != '\\':
                            in_str = None
                    elif c in ('"', "'", '`'):
                        in_str = c
                    elif c == '{':
                        depth += 1
                    elif c == '}':
                        depth -= 1
                        if depth == 0:
                            end_pos = i
                            break
                    i += 1

                if end_pos != -1:
                    body = content[brace_start+1:end_pos]
                    fields = []
                    d = 0
                    idx = 0
                    body_len = len(body)
                    while idx < body_len:
                        ch = body[idx]
                        if ch in ('"', "'", '`'):
                            q = ch
                            idx += 1
                            while idx < body_len and (body[idx] != q or body[idx-1] == '\\'):
                                idx += 1
                        elif ch in ('{', '['):
                            d += 1
                        elif ch in ('}', ']'):
                            d -= 1
                        elif d == 0:
                            fm = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:', body[idx:])
                            if fm:
                                fn = fm.group(1)
                                if fn not in ('type', 'required', 'default', 'enum', 'ref', 'min', 'max', 'select'):
                                    fields.append({"field_name": fn, "line_number": 1})
                                idx += fm.end() - 1
                        idx += 1

                    if "passportlocalmongoose" in content.lower().replace("-", ""):
                        if not any(f["field_name"] == "username" for f in fields):
                            fields.append({"field_name": "username", "line_number": 1})

                    if fields:
                        found_model_names.add(name)
                        res["models"].append({
                            "model_name": name,
                            "source_file": rel_path,
                            "line_number": content[:sm.start()].count("\n") + 1,
                            "fields": fields
                        })

        # 2. TypeScript Interfaces & Types
        for im in re.finditer(r'(?:export\s+)?(?:interface|type)\s+(\w+)(?:\s*=\s*|\s+extends[^{]+|\s*)\{([^}]+)\}', content):
            name = im.group(1)
            if name in found_model_names:
                continue
            body = im.group(2)
            fields = []
            for line in body.splitlines():
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                km = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\??\s*:', line)
                if km:
                    fn = km.group(1)
                    if fn not in ("type", "readonly"):
                        fields.append({"field_name": fn, "line_number": 1})
            if fields:
                found_model_names.add(name)
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        # 3. TypeORM / ES6 Classes with columns
        for cm in re.finditer(r'(?:@Entity[^{]*\s+)?(?:export\s+)?class\s+(\w+)[^{]*\{([^}]+)\}', content):
            name = cm.group(1)
            if name in found_model_names:
                continue
            body = cm.group(2)
            fields = []
            for line in body.splitlines():
                line = line.strip()
                fm = re.match(r'([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\??\s*:\s*[\w<>\[\]]+', line)
                if fm:
                    fields.append({"field_name": fm.group(1), "line_number": 1})
            if fields:
                found_model_names.add(name)
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        return res

    def _parse_go(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_go_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_go_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models (structs with json tags), routes (Gin, Fiber, Chi), and imports from Go."""
        res = {"models": [], "routes": [], "imports": []}

        # Imports
        for m in re.finditer(r'import\s*\(([^)]+)\)', content):
            for line in m.group(1).splitlines():
                line = line.strip().strip('"')
                if line and not line.startswith("//"):
                    res["imports"].append({"source_file": rel_path, "package": line, "type": "go_package"})
        for m in re.finditer(r'import\s+"([^"]+)"', content):
            res["imports"].append({"source_file": rel_path, "package": m.group(1), "type": "go_package"})

        # Routes: r.GET("/api/v1/user", ...)
        for m in re.finditer(r'\.(GET|POST|PUT|DELETE|PATCH)\s*\(\s*["\']([^"\']+)["\']', content, re.IGNORECASE):
            method, path = m.group(1).upper(), m.group(2)
            res["routes"].append({"endpoint": f"{method} {path}", "path": path, "source_file": rel_path, "line_number": 1, "decorators": [method]})

        # Structs
        for m in re.finditer(r'type\s+(\w+)\s+struct\s*\{([^}]+)\}', content):
            name = m.group(1)
            body = m.group(2)
            fields = []
            for line in body.splitlines():
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                tag_match = re.search(r'json:"([^",]+)', line)
                if tag_match:
                    fn = tag_match.group(1)
                else:
                    parts = line.split()
                    fn = parts[0] if parts else None
                if fn and fn != "-":
                    fields.append({"field_name": fn, "line_number": 1})
            if fields:
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        return res

    def _parse_java(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_java_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_java_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models (Spring JPA entities), endpoints, and imports from Java/Kotlin."""
        res = {"models": [], "routes": [], "imports": []}

        # Imports
        for m in re.finditer(r'import\s+([\w.]+);', content):
            res["imports"].append({"source_file": rel_path, "package": m.group(1), "type": "java_import"})

        # Routes (@GetMapping, @PostMapping)
        for m in re.finditer(r'@(GetMapping|PostMapping|PutMapping|DeleteMapping|PatchMapping|RequestMapping)\s*\(\s*(?:value\s*=\s*)?["\']([^"\']+)["\']', content):
            method = m.group(1).replace("Mapping", "").upper()
            path = m.group(2)
            res["routes"].append({"endpoint": f"{method} {path}", "path": path, "source_file": rel_path, "line_number": 1, "decorators": [method]})

        # Classes
        for m in re.finditer(r'(?:public\s+)?class\s+(\w+)[^{]*\{([^}]+)\}', content):
            name = m.group(1)
            body = m.group(2)
            fields = []
            for line in body.splitlines():
                fm = re.search(r'(?:private|protected|public)\s+[\w<>,.?\[\]]+\s+(\w+)\s*;', line)
                if fm:
                    fn = fm.group(1)
                    if fn not in ("serialVersionUID",):
                        fields.append({"field_name": fn, "line_number": 1})
            if fields:
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        return res

    def _parse_csharp(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_csharp_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_csharp_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models (EF Core classes), ASP.NET routes, and namespaces from C#."""
        res = {"models": [], "routes": [], "imports": []}

        for m in re.finditer(r'using\s+([\w.]+);', content):
            res["imports"].append({"source_file": rel_path, "package": m.group(1), "type": "csharp_namespace"})

        for m in re.finditer(r'\[(HttpGet|HttpPost|HttpPut|HttpDelete|Route)\s*\(\s*["\']([^"\']+)["\']\s*\)\]', content):
            method = m.group(1).replace("Http", "").upper()
            path = m.group(2)
            res["routes"].append({"endpoint": f"{method} {path}", "path": path, "source_file": rel_path, "line_number": 1, "decorators": [method]})

        for m in re.finditer(r'(?:public\s+)?class\s+(\w+)[^{]*\{([^}]+)\}', content):
            name = m.group(1)
            body = m.group(2)
            fields = []
            for line in body.splitlines():
                fm = re.search(r'public\s+[\w<>,.?\[\]]+\s+(\w+)\s*\{\s*get;', line)
                if fm:
                    fields.append({"field_name": fm.group(1), "line_number": 1})
            if fields:
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        return res

    def _parse_php(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_php_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_php_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Extracts models (Laravel Eloquent), routes, and composer packages from PHP."""
        res = {"models": [], "routes": [], "imports": []}

        for m in re.finditer(r'use\s+([\w\\]+);', content):
            res["imports"].append({"source_file": rel_path, "package": m.group(1), "type": "php_use"})

        for m in re.finditer(r'Route::(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']', content):
            method, path = m.group(1).upper(), m.group(2)
            res["routes"].append({"endpoint": f"{method} {path}", "path": path, "source_file": rel_path, "line_number": 1, "decorators": [method]})

        for m in re.finditer(r'class\s+(\w+)\s+extends\s+Model[^{]*\{([^}]+)\}', content):
            name = m.group(1)
            body = m.group(2)
            fields = []
            fillable_match = re.search(r'protected\s+\$fillable\s*=\s*\[([^\]]+)\];', body)
            if fillable_match:
                for fn in re.findall(r'["\'](\w+)["\']', fillable_match.group(1)):
                    fields.append({"field_name": fn, "line_number": 1})
            if fields:
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        return res

    def _parse_generic(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_generic_content(content, rel_path)
        except Exception:
            return {"models": [], "routes": [], "imports": []}

    def _parse_generic_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Generic fallback parser for Rust structs, Ruby models, or unknown typed languages."""
        res = {"models": [], "routes": [], "imports": []}

        # Rust pub struct Name { field: type }
        for m in re.finditer(r'(?:pub\s+)?struct\s+(\w+)[^{]*\{([^}]+)\}', content):
            name = m.group(1)
            body = m.group(2)
            fields = []
            for line in body.splitlines():
                line = line.strip()
                fm = re.match(r'(?:pub\s+)?([a-zA-Z_$][a-zA-Z0-9_$]*)\s*:\s*[\w<>\[\]]+', line)
                if fm:
                    fields.append({"field_name": fm.group(1), "line_number": 1})
            if fields:
                res["models"].append({"model_name": name, "source_file": rel_path, "line_number": 1, "fields": fields})

        # Ruby class Name < ApplicationRecord
        for m in re.finditer(r'class\s+(\w+)\s*<\s*ApplicationRecord', content):
            res["models"].append({"model_name": m.group(1), "source_file": rel_path, "line_number": 1, "fields": []})

        return res

    def _parse_schema(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            return self._parse_schema_content(content, rel_path)
        except Exception:
            return {"models": []}

    def _parse_schema_content(self, content: str, rel_path: str) -> Dict[str, Any]:
        """Parses Prisma, SQL DDL, Protobuf, or GraphQL schemas."""
        res = {"models": []}

        # Prisma models
        for pm in re.finditer(r'model\s+(\w+)\s*\{([^}]+)\}', content):
            model_name, body = pm.group(1), pm.group(2)
            fields = []
            for line in body.splitlines():
                parts = line.strip().split()
                if parts and not parts[0].startswith("//") and not parts[0].startswith("@@"):
                    fields.append({"field_name": parts[0], "line_number": 1})
            if fields:
                res["models"].append({"model_name": model_name, "source_file": rel_path, "line_number": 1, "fields": fields})

        # SQL CREATE TABLE
        for sm in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:["`]?\w+["`]?\.)?["`]?(\w+)["`]?\s*\(([^;]+)\)', content, re.IGNORECASE):
            table_name, body = sm.group(1), sm.group(2)
            fields = []
            for line in body.splitlines():
                parts = line.strip().replace(",", "").replace('"', '').replace('`', '').split()
                if parts and parts[0].upper() not in ["PRIMARY", "FOREIGN", "KEY", "CONSTRAINT", "UNIQUE", "CHECK", "INDEX"]:
                    fields.append({"field_name": parts[0], "line_number": 1})
            if fields:
                res["models"].append({"model_name": table_name, "source_file": rel_path, "line_number": 1, "fields": fields})

        # Protobuf messages
        for m in re.finditer(r'message\s+(\w+)\s*\{([^}]+)\}', content):
            msg_name, body = m.group(1), m.group(2)
            fields = []
            for line in body.splitlines():
                parts = line.strip().replace(";", "").split()
                if len(parts) >= 3 and "=" in parts:
                    eq_idx = parts.index("=")
                    fn = parts[eq_idx - 1]
                    fields.append({"field_name": fn, "line_number": 1})
            if fields:
                res["models"].append({"model_name": msg_name, "source_file": rel_path, "line_number": 1, "fields": fields})

        return res

    def _parse_dependency_file(self, fpath: str, rel_path: str) -> List[Dict[str, Any]]:
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            fname = os.path.basename(fpath)
            return self._parse_dependency_content(content, fname, rel_path)
        except Exception:
            return []

    def _parse_dependency_content(self, content: str, fname: str, rel_path: str) -> List[Dict[str, Any]]:
        """Parses dependency lists across npm, pip, go, maven, gradle, cargo, composer, gemfile, docker-compose, and .env."""
        deps = []
        fname_lower = fname.lower()

        if fname_lower == "package.json":
            try:
                pkg_data = json.loads(content)
                all_deps = {**pkg_data.get("dependencies", {}), **pkg_data.get("devDependencies", {})}
                for pkg in all_deps.keys():
                    deps.append({"source_file": rel_path, "package": pkg, "type": "npm_dependency"})
            except Exception:
                pass
        elif fname_lower in ["go.mod"]:
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("require") or (not line.startswith("module") and "/" in line):
                    parts = line.replace("require", "").replace("(", "").replace(")", "").strip().split()
                    if parts:
                        deps.append({"source_file": rel_path, "package": parts[0], "type": "go_module"})
        elif fname_lower == "pom.xml":
            for m in re.finditer(r'<artifactId>([^<]+)</artifactId>', content):
                deps.append({"source_file": rel_path, "package": m.group(1).strip(), "type": "maven_dependency"})
        elif fname_lower in ["build.gradle", "build.gradle.kts"]:
            for m in re.finditer(r'(?:implementation|api|compileOnly)\s*[\'"]([^:\'"]+):([^:\'"]+)', content):
                pkg = f"{m.group(1)}:{m.group(2)}"
                deps.append({"source_file": rel_path, "package": pkg, "type": "gradle_dependency"})
        elif fname_lower == "cargo.toml":
            in_deps = False
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("[dependencies]"):
                    in_deps = True
                elif line.startswith("["):
                    in_deps = False
                elif in_deps and "=" in line:
                    crate = line.split("=")[0].strip()
                    deps.append({"source_file": rel_path, "package": crate, "type": "cargo_crate"})
        elif fname_lower == "composer.json":
            try:
                cdata = json.loads(content)
                all_deps = {**cdata.get("require", {}), **cdata.get("require-dev", {})}
                for pkg in all_deps.keys():
                    deps.append({"source_file": rel_path, "package": pkg, "type": "composer_package"})
            except Exception:
                pass
        elif fname_lower == "gemfile":
            for m in re.finditer(r'gem\s+[\'"]([^\'"]+)[\'"]', content):
                deps.append({"source_file": rel_path, "package": m.group(1), "type": "ruby_gem"})
        elif fname_lower in [".env.example", ".env.sample", ".env.template"]:
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    eq = line.find("=")
                    key = line[:eq].strip() if eq != -1 else line
                    deps.append({"source_file": rel_path, "package": key, "type": "env_credential"})
        elif fname_lower in ["docker-compose.yml", "docker-compose.yaml"]:
            for m in re.finditer(r'image:\s*([^\s:]+)', content):
                deps.append({"source_file": rel_path, "package": m.group(1), "type": "docker_image"})
        else: # requirements.txt / Pipfile / setup.py
            for line in content.splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg_name = re.split(r"[=<>]", line)[0].strip()
                    if pkg_name:
                        deps.append({"source_file": rel_path, "package": pkg_name, "type": "python_dependency"})

        return deps
