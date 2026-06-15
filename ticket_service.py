"""
Ticket Service — in-memory ticket store (swap for DB in production)
"""

import random
import string
from datetime import datetime


class TicketService:
    def __init__(self):
        self.tickets = []

    def create(self, data: dict) -> str:
        ticket_id = "TKT-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.tickets.append({
            "id": ticket_id,
            "created_at": datetime.utcnow().isoformat(),
            "status": "open",
            **data
        })
        return ticket_id

    def get_stats(self) -> dict:
        return {
            "total_tickets": len(self.tickets),
            "open": sum(1 for t in self.tickets if t["status"] == "open"),
            "closed": sum(1 for t in self.tickets if t["status"] == "closed"),
        }
