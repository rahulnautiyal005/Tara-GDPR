"""
Tara PrivacyOS — Code-to-GDPR Engine
Module: CODE-101 Repo AST Parser
Parses repositories (Python, JS/TS, Prisma, SQL) to extract data models,
API routes, and dependencies for automated privacy audits.
"""

import ast
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Any, Optional

class RepoASTParser:
    def __init__(self, target_path_or_url: str):
        self.source = target_path_or_url
        self.is_remote = target_path_or_url.startswith("http://") or target_path_or_url.startswith("https://") or target_path_or_url.startswith("git@")
        self.working_dir: Optional[str] = None
        self.parsed_files: List[Dict[str, Any]] = []

    def prepare_workspace(self) -> str:
        """Clones repo if remote, or resolves absolute path if local directory."""
        if self.is_remote:
            temp_dir = tempfile.mkdtemp(prefix="tara_repo_")
            self.working_dir = temp_dir
            try:
                subprocess.run(
                    ["git", "clone", "--depth", "1", self.source, temp_dir],
                    check=True,
                    capture_output=True,
                    text=True
                )
            except Exception as e:
                shutil.rmtree(temp_dir, ignore_errors=True)
                raise RuntimeError(f"Failed to clone remote repository {self.source}: {str(e)}")
        else:
            if not os.path.exists(self.source):
                raise FileNotFoundError(f"Local path does not exist: {self.source}")
            self.working_dir = os.path.abspath(self.source)
        
        return self.working_dir

    def cleanup(self):
        """Clean up cloned temporary folder if it was cloned."""
        if self.is_remote and self.working_dir and os.path.exists(self.working_dir):
            shutil.rmtree(self.working_dir, ignore_errors=True)

    def scan_repository(self) -> Dict[str, Any]:
        """Walks the directory and parses AST for code and config files."""
        root = self.prepare_workspace()
        results = {
            "source": self.source,
            "root_path": root,
            "models": [],
            "routes": [],
            "imports_and_sdks": [],
            "raw_schemas": [],
            "total_files_scanned": 0
        }

        # Ignored dirs
        ignore_dirs = {".git", "node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".next", ".cache"}

        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
            
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(fpath, root)
                ext = os.path.splitext(fname)[1].lower()

                if ext == ".py":
                    results["total_files_scanned"] += 1
                    py_data = self._parse_python_file(fpath, rel_path)
                    results["models"].extend(py_data.get("models", []))
                    results["routes"].extend(py_data.get("routes", []))
                    results["imports_and_sdks"].extend(py_data.get("imports", []))

                elif ext in [".js", ".ts", ".jsx", ".tsx"]:
                    results["total_files_scanned"] += 1
                    js_data = self._parse_javascript_file(fpath, rel_path)
                    results["models"].extend(js_data.get("models", []))
                    results["routes"].extend(js_data.get("routes", []))
                    results["imports_and_sdks"].extend(js_data.get("imports", []))

                elif ext in [".prisma", ".sql"]:
                    results["total_files_scanned"] += 1
                    schema_data = self._parse_schema_file(fpath, rel_path)
                    results["models"].extend(schema_data.get("models", []))

                elif fname in ["package.json", "requirements.txt", "Pipfile", "pyproject.toml"]:
                    results["total_files_scanned"] += 1
                    dep_data = self._parse_dependency_file(fpath, rel_path)
                    results["imports_and_sdks"].extend(dep_data)

        return results

    def _parse_python_file(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        res = {"models": [], "routes": [], "imports": []}
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                code_content = f.read()
            tree = ast.parse(code_content, filename=rel_path)
        except Exception:
            return res

        for node in ast.walk(tree):
            # Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    res["imports"].append({"source_file": rel_path, "package": alias.name, "type": "import"})
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    res["imports"].append({"source_file": rel_path, "package": node.module, "type": "from_import"})

            # Classes (Models / Schemas)
            elif isinstance(node, ast.ClassDef):
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        base_names.append(base.attr)

                # Check if it looks like an ORM / Pydantic model
                is_model = any(b in ["Base", "Model", "BaseModel", "DeclarativeBase", "Document"] for b in base_names)
                if is_model or True: # Capture all structured classes for potential field inspection
                    fields = []
                    for item in node.body:
                        # Type annotated fields: field_name: str
                        if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                            fields.append({
                                "field_name": item.target.id,
                                "line_number": item.lineno
                            })
                        # Normal assignments: field_name = Column(...)
                        elif isinstance(item, ast.Assign):
                            for target in item.targets:
                                if isinstance(target, ast.Name):
                                    fields.append({
                                        "field_name": target.id,
                                        "line_number": target.lineno
                                    })
                    if fields:
                        res["models"].append({
                            "model_name": node.name,
                            "source_file": rel_path,
                            "line_number": node.lineno,
                            "bases": base_names,
                            "fields": fields
                        })

            # Function / Route definitions
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

                # Check for FastAPI / Flask routes
                route_decorators = [d for d in decorators if any(r in d.lower() for r in ["get", "post", "put", "delete", "patch", "route", "api"])]
                if route_decorators:
                    args = [arg.arg for arg in node.args.args if arg.arg not in ["self", "cls"]]
                    res["routes"].append({
                        "endpoint_name": node.name,
                        "source_file": rel_path,
                        "line_number": node.lineno,
                        "decorators": route_decorators,
                        "parameters": args
                    })

        return res

    def _parse_javascript_file(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        res = {"models": [], "routes": [], "imports": []}
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return res

        # Regex for imports: import ... from 'package' or require('package')
        import_matches = re.findall(r'''(?:import\s+.*?from\s+['"]([^'"]+)['"]|require\s*\(\s*['"]([^'"]+)['"]\s*\))''', content)
        for m in import_matches:
            pkg = m[0] or m[1]
            if pkg and not pkg.startswith("."):
                res["imports"].append({"source_file": rel_path, "package": pkg, "type": "npm_package"})

        # Regex for Express / Next.js API routes: router.post('/path', ...), app.get('/path', ...)
        route_matches = re.finditer(r'''(?:app|router|api)\.(get|post|put|delete|patch)\s*\(\s*['"]([^'"]+)['"]''', content, re.IGNORECASE)
        for m in route_matches:
            method = m.group(1).upper()
            path = m.group(2)
            res["routes"].append({
                "endpoint_name": f"{method} {path}",
                "path": path,
                "method": method,
                "source_file": rel_path,
                "line_number": content[:m.start()].count("\n") + 1
            })

        # Regex for Mongoose or Prisma JS Schemas: new Schema({ ... })
        schema_blocks = re.finditer(r'''(?:const|let|var)\s+(\w+)\s*=\s*new\s+(?:mongoose\.)?Schema\s*\(\s*\{([^}]+)\}''', content, re.DOTALL)
        for m in schema_blocks:
            schema_name = m.group(1)
            raw_fields = m.group(2)
            field_lines = [line.strip().split(":")[0].strip() for line in raw_fields.split(",") if ":" in line]
            res["models"].append({
                "model_name": schema_name,
                "source_file": rel_path,
                "line_number": content[:m.start()].count("\n") + 1,
                "fields": [{"field_name": fl} for fl in field_lines if fl and not fl.startswith("//")]
            })

        return res

    def _parse_schema_file(self, fpath: str, rel_path: str) -> Dict[str, Any]:
        res = {"models": []}
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            return res

        # Prisma models: model User { ... }
        prisma_matches = re.finditer(r'''model\s+(\w+)\s*\{([^}]+)\}''', content)
        for m in prisma_matches:
            model_name = m.group(1)
            body = m.group(2)
            fields = []
            for line in body.strip().split("\n"):
                line = line.strip()
                if line and not line.startswith("//"):
                    parts = line.split()
                    if parts:
                        fields.append({"field_name": parts[0]})
            res["models"].append({
                "model_name": model_name,
                "source_file": rel_path,
                "line_number": content[:m.start()].count("\n") + 1,
                "fields": fields
            })

        # SQL CREATE TABLE table_name ( ... )
        sql_matches = re.finditer(r'''CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:["'`]?(\w+)["'`]?)\s*\(([^;]+)\)''', content, re.IGNORECASE)
        for m in sql_matches:
            tbl_name = m.group(1)
            body = m.group(2)
            fields = []
            for line in body.split(","):
                line = line.strip()
                if line and not any(line.upper().startswith(kw) for kw in ["PRIMARY KEY", "FOREIGN KEY", "CONSTRAINT", "INDEX"]):
                    fname = line.split()[0].replace('"', '').replace("'", '').replace("`", "")
                    fields.append({"field_name": fname})
            res["models"].append({
                "model_name": tbl_name,
                "source_file": rel_path,
                "line_number": content[:m.start()].count("\n") + 1,
                "fields": fields
            })

        return res

    def _parse_dependency_file(self, fpath: str, rel_path: str) -> List[Dict[str, Any]]:
        imports = []
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#"):
                    pkg = re.split(r'[=><~]', line)[0].strip()
                    if pkg:
                        imports.append({"source_file": rel_path, "package": pkg, "type": "manifest_dependency"})
        except Exception:
            pass
        return imports
