"""
Benchmark Target App: API Routes
Simulates API endpoints of a consultation marketplace.
"""

from fastapi import FastAPI, Depends, HTTPException

app = FastAPI(title="Consultation API")

@app.post("/api/auth/register")
def register_user(full_name: str, email: str, phone: str, dob: str):
    return {"message": "User registered successfully"}

@app.post("/api/consultations/create")
def book_consultation(user_id: int, practitioner_id: int, spiritual_goals: str, health_symptoms: str):
    # Missing explicit Art 9 consent parameter
    return {"session_id": 101, "status": "booked"}

@app.post("/api/chat/llm-insight")
def generate_ai_insight(prompt: str, user_birth_details: str):
    # Invokes OpenAI workflow
    return {"ai_reading": "Your planetary alignment indicates a period of transformation."}

@app.get("/api/practitioner/client-details")
def get_client_details(practitioner_id: int, user_id: int):
    # VULNERABILITY: Directly returns raw customer phone and email to practitioner
    return {
        "client_name": "Pooja Sharma",
        "phone_number": "+447911123456",
        "email": "pooja.sharma@example.co.uk",
        "health_symptoms": "Chronic anxiety and career blockage"
    }

@app.post("/api/payments/checkout")
def create_payment_intent(user_id: int, amount: float):
    return {"client_secret": "pi_12345_secret"}
