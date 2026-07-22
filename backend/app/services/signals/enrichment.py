class MockEnrichmentProvider:
    def enrich_company(self, domain: str) -> dict:
        return {
            "domain": domain,
            "company_name": domain.split(".")[0].capitalize() + " Corp",
            "industry": "Software",
            "company_size": 250,
            "annual_revenue": "$50M - $100M",
            "tech_stack": ["Salesforce", "Marketo", "AWS"],
            "location": "San Francisco, CA"
        }
        
    def enrich_person(self, email: str) -> dict:
        parts = email.split("@")
        name = parts[0].split(".")
        first_name = name[0].capitalize()
        last_name = name[1].capitalize() if len(name) > 1 else ""
        
        return {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "job_title": "VP of Sales",
            "seniority": "Executive",
            "linkedin_url": f"https://linkedin.com/in/{first_name.lower()}-{last_name.lower()}",
            "phone": "+1-555-010-2938"
        }
