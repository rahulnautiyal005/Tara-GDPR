"""
Entrypoint to run Tara PrivacyOS & GDPR AI Copilot Web Application
"""
import os
import uvicorn

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    reload_mode = False

    print("=" * 60)
    print("Starting Tara PrivacyOS Enterprise Server...")
    print(f"Web Application available at: http://{host}:{port}")
    print(f"API Documentation at:         http://{host}:{port}/docs")
    print("Direct URLs:")
    print(f"  • Login Page:    http://{host}:{port}/login")
    print(f"  • Dashboard:     http://{host}:{port}/dashboard")
    print(f"  • AI Copilot:    http://{host}:{port}/copilot")
    print(f"  • Scan Details:  http://{host}:{port}/scan-details")
    print(f"  • Exec Plan:     http://{host}:{port}/plan")
    print("=" * 60)
    uvicorn.run("tara_privacyos.api.server:app", host=host, port=port, reload=reload_mode)

