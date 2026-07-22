from fastapi import APIRouter

router = APIRouter()

@router.get("/icp")
def get_icp_config():
    return {
        "industries": ["Software", "SaaS", "Information Technology"],
        "min_employees": 50,
        "max_employees": 5000,
        "target_titles": ["VP Sales", "CRO", "Head of RevOps"]
    }

@router.put("/icp")
def update_icp_config(config: dict):
    return {"status": "updated", "config": config}

@router.get("/domains")
def get_domains():
    return [
        {"domain": "demo.com", "status": "verified"},
        {"domain": "mail.demo.com", "status": "verified"}
    ]

@router.get("/integrations")
def get_integrations():
    return [
        {"name": "Salesforce", "status": "connected"},
        {"name": "HubSpot", "status": "disconnected"}
    ]
