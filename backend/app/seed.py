import random
import datetime
from sqlalchemy.orm import Session
from app.models import Organization, Lead, Signal, Campaign, Message, SuppressionEntry

def seed_database(db: Session):
    if db.query(Organization).first():
        return

    # 1. Create Demo Organization
    org = Organization(name="Demo Org")
    db.add(org)
    db.commit()
    db.refresh(org)

    # 2. Campaigns
    campaigns = []
    campaign_data = [
        {"name": "Q3 Enterprise Outreach", "status": "active", "total_leads": 12, "total_sent": 12, "total_opened": 8, "total_replied": 4},
        {"name": "SMB Growth Initiative", "status": "active", "total_leads": 20, "total_sent": 18, "total_opened": 10, "total_replied": 2},
        {"name": "Re-engagement 2026", "status": "draft", "total_leads": 0, "total_sent": 0, "total_opened": 0, "total_replied": 0},
        {"name": "Product Launch - Alpha", "status": "paused", "total_leads": 15, "total_sent": 5, "total_opened": 2, "total_replied": 0},
        {"name": "Inbound Follow-up", "status": "completed", "total_leads": 30, "total_sent": 30, "total_opened": 25, "total_replied": 10}
    ]
    for cd in campaign_data:
        camp = Campaign(
            org_id=org.id,
            name=cd["name"],
            status=cd["status"],
            total_leads=cd["total_leads"],
            total_sent=cd["total_sent"],
            total_opened=cd["total_opened"],
            total_replied=cd["total_replied"]
        )
        db.add(camp)
        campaigns.append(camp)
    db.commit()
    for camp in campaigns: db.refresh(camp)

    # 3. Leads
    companies = ["TechFlow", "DataStack", "CloudNova", "Vertex Solutions", "PulseAI", "SignalForge", "Nextera", "Quantum Labs", "ByteShift", "ClearPath", "OmniStack", "ScaleGrid", "NovaBridge", "Zenith Systems", "ApexCloud", "Meridian AI", "StackPulse", "Riviera Tech", "ForgePoint", "Elevate SaaS"]
    names = ["Sarah Chen", "Marcus Rodriguez", "Emily Watson", "James Liu", "Priya Patel", "David Kim", "Rachel Morrison", "Alex Thompson", "Maya Johansson", "Carlos Rivera", "Aisha Okafor", "Daniel Park", "Sophie Laurent", "Omar Hassan", "Lisa Nakamura"]
    titles = ["VP of Revenue Operations", "Head of Growth", "CRO", "Director of Sales", "VP of Engineering", "Head of RevOps", "VP Marketing", "Chief Revenue Officer", "Director of Business Development", "VP of Sales Operations"]
    statuses = ["new", "enriched", "sequenced", "replied", "qualified", "booked", "lost"]

    leads = []
    for _ in range(60):
        name = random.choice(names).split()
        comp = random.choice(companies)
        lead = Lead(
            org_id=org.id,
            first_name=name[0],
            last_name=name[1],
            email=f"{name[0].lower()}.{name[1].lower()}@{comp.lower().replace(' ', '')}.com",
            title=random.choice(titles),
            company_name=comp,
            status=random.choice(statuses),
            icp_fit_score=random.uniform(50, 100),
            intent_score=random.uniform(10, 100)
        )
        lead.composite_score = (lead.icp_fit_score * 0.4) + (lead.intent_score * 0.6)
        db.add(lead)
        leads.append(lead)
    db.commit()
    for lead in leads: db.refresh(lead)

    # 4. Signals
    signal_types = ["job_change", "funding", "hiring_surge", "tech_change", "new_leadership", "competitor_removal", "job_posting", "website_visit"]
    for _ in range(120):
        lead = random.choice(leads)
        stype = random.choice(signal_types)
        sdata = {"source": "LinkedIn", "details": f"Triggered {stype} event"}
        sig = Signal(
            lead_id=lead.id,
            signal_type=stype,
            signal_data=sdata,
            detected_at=datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(0, 30))
        )
        db.add(sig)
    db.commit()

    # 5. Messages
    for _ in range(250):
        lead = random.choice(leads)
        campaign = random.choice(campaigns)
        msg = Message(
            lead_id=lead.id,
            campaign_id=campaign.id,
            channel="email",
            subject=f"Quick question for {lead.company_name}",
            body=f"Hi {lead.first_name}, I noticed your recent activity. Let's chat!",
            status=random.choice(["sent", "delivered", "opened", "replied", "bounced", "draft"]),
            sent_at=datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(0, 60))
        )
        db.add(msg)
    db.commit()

    # 6. Suppression
    for _ in range(15):
        sup = SuppressionEntry(
            org_id=org.id,
            email=f"suppressed{random.randint(1,1000)}@example.com",
            reason="Unsubscribed",
            source="Email Link"
        )
        db.add(sup)
    db.commit()
    print("Database seeded successfully with richer data and correct models.")
