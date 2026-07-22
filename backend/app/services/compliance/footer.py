def generate_footer(jurisdiction: str, company_name: str, opt_out_link: str) -> str:
    base = f"\n\n---\n{company_name} | You are receiving this because you're a good fit for our product. "
    if jurisdiction == "GDPR":
        base += f"We process your data under legitimate interest. [Unsubscribe]({opt_out_link})"
    elif jurisdiction == "CCPA":
        base += f"[Do Not Sell My Info]({opt_out_link}) | [Unsubscribe]({opt_out_link})"
    else:
        base += f"[Unsubscribe]({opt_out_link})"
    return base
