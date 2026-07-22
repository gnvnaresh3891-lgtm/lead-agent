class ContextBuilder:
    def build_context(self, lead_data: dict, signals: list) -> dict:
        return {
            "lead": lead_data,
            "recent_signals": signals,
            "company_info": lead_data.get("company_info", {}),
            "generated_at": "2024-05-24T10:00:00Z"
        }
