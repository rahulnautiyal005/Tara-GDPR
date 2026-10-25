"""
Benchmark Target App: Models
Simulates a real-world consultation & marketplace application.
"""

from typing import Optional, List
from datetime import datetime

class UserModel:
    id: int
    full_name: str
    email: str
    phone_number: str
    password_hash: str
    date_of_birth: str
    birth_time: str
    birth_place: str
    ip_address: str
    created_at: datetime

class KundliConsultationModel:
    id: int
    user_id: int
    practitioner_id: int
    health_symptoms: Optional[str]
    relationship_problem: Optional[str]
    spiritual_goals: str
    horoscope_chart_data: str
    consultation_notes: str
    session_status: str

class PractitionerModel:
    id: int
    practitioner_name: str
    specialisation: str
    country: str  # e.g., India
    pan_number: str
    bank_account: str
    is_active: bool

class PaymentTransactionModel:
    id: int
    user_id: int
    stripe_customer_id: str
    amount_gbp: float
    billing_postal_code: str
    card_last4: str
    payment_status: str
