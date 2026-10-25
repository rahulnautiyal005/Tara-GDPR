"""
Tara PrivacyOS — Developer CLI Scanner
Executes Code-to-GDPR scans directly from the command line.
"""

import argparse
import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from tara_privacyos.privacyos_engine import PrivacyOSEngine

def main():
    parser = argparse.ArgumentParser(description="Tara PrivacyOS — Code-to-GDPR Static Audit Scanner")
    parser.add_argument("--path", type=str, default="./tara_privacyos/benchmarks/sample_consultation_app", help="Path to local codebase or repo folder")
    parser.add_argument("--repo", type=str, help="Remote Git repository URL to clone and scan")
    parser.add_argument("--out", type=str, default="privacyos_audit_report.json", help="Path to write JSON audit report")
    args = parser.parse_args()

    target = args.repo if args.repo else args.path

    console = Console()
    console.print(Panel.fit(
        "[bold cyan]TARA PRIVACYOS[/bold cyan] — [bold white]Code-to-GDPR Static Security & Compliance Scanner[/bold white]\n"
        "[dim]Target: " + target + "[/dim]",
        border_style="cyan"
    ))

    engine = PrivacyOSEngine()
    with console.status("[bold green]Analyzing AST trees, PII schemas, routes, and subprocessors...", spinner="dots"):
        try:
            report = engine.scan(target)
        except Exception as e:
            console.print(f"[bold red]Scan Error: {str(e)}[/bold red]")
            sys.exit(1)

    meta = report["scan_metadata"]
    grade_color = "green" if "A" in meta["health_grade"] else ("yellow" if "B" in meta["health_grade"] else "red")

    # Overview Table
    overview_tbl = Table(title="Audit Executive Summary", style="bold white")
    overview_tbl.add_column("Metric", style="cyan")
    overview_tbl.add_column("Value", style="bold")
    overview_tbl.add_row("Scanned Source", meta["source"])
    overview_tbl.add_row("Total Files Scanned", str(meta["total_files_scanned"]))
    overview_tbl.add_row("Scan Duration", f"{meta['duration_ms']} ms")
    overview_tbl.add_row("Compliance Health Grade", f"[{grade_color}]{meta['health_grade']}[/{grade_color}]")
    overview_tbl.add_row("Overall Compliance Score", f"[{grade_color}]{meta['overall_risk_score']} / 100[/{grade_color}]")
    console.print(overview_tbl)

    # PII & Article 9 Table
    pii = report["pii_and_special_category"]
    pii_tbl = Table(title="Detected Database & ORM PII Schemas", style="cyan")
    pii_tbl.add_column("Model Name", style="bold white")
    pii_tbl.add_column("PII Fields", style="yellow")
    pii_tbl.add_column("Special Category (Art 9)", style="red")
    pii_tbl.add_column("Statutory Mandate", style="magenta")

    for f in pii.get("detailed_findings", []):
        special_cat = [fld["field_name"] for fld in f["fields"] if fld.get("is_art9")]
        std_pii = [fld["field_name"] for fld in f["fields"] if not fld.get("is_art9")]
        pii_tbl.add_row(
            f["model_name"],
            ", ".join(std_pii) or "None",
            ", ".join(special_cat) or "[green]None[/green]",
            "Explicit Consent (Art 9)" if special_cat else "Standard Contract (Art 6)"
        )
    console.print(pii_tbl)

    # Routes & Compliance Gaps
    routes = report["api_data_flows"]
    gap_tbl = Table(title="Statutory Architectural Gaps Detected", style="red")
    gap_tbl.add_column("Statutory Clause", style="bold white")
    gap_tbl.add_column("Severity", style="bold red")
    gap_tbl.add_column("Finding", style="yellow")
    gap_tbl.add_column("Developer Remediation", style="green")

    for g in routes.get("compliance_gaps", []):
        gap_tbl.add_row(g["statute"], g["severity"], g["finding"], g["remediation"])
    console.print(gap_tbl)

    # Subprocessors Table
    subprocs = report["subprocessors_and_transfers"].get("subprocessor_register", [])
    if subprocs:
        sub_tbl = Table(title="Third-Party Subprocessors & Cross-Border Transfers", style="yellow")
        sub_tbl.add_column("Subprocessor", style="bold white")
        sub_tbl.add_column("Jurisdiction", style="blue")
        sub_tbl.add_column("Risk Level", style="red")
        sub_tbl.add_column("Transfer Mechanism Needed", style="magenta")

        for s in subprocs:
            sub_tbl.add_row(s["name"], s["jurisdiction"], s["risk_level"], s["transfer_mechanism_required"])
        console.print(sub_tbl)

    # Save to disk
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    console.print(f"\n[bold green][OK] Full statutory audit report exported to:[/bold green] [bold white]{args.out}[/bold white]\n")

if __name__ == "__main__":
    main()
