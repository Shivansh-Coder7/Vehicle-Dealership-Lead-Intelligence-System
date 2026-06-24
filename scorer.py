import pandas as pd
import ast

print("Loading online presence data...")
data = pd.read_csv("car_showroom_online_presence.csv")


REFERRAL_DOMAINS = [
    "justdial.com",
    "indiamart.com",
    "cardekho.com",
    "carwale.com",
    "cars24.com",
    "olx.in",
    "sulekha.com",
    "yellowpages.in",
]


for domain in REFERRAL_DOMAINS:
    col = domain.replace(".", "_").replace("-", "_")
    data[col] = 0

data["total_referral_links"] = 0


for idx, row in data.iterrows():
    try:
        links = ast.literal_eval(row["relevant_links"])
    except:
        links = []

    count = 0
    for link in links:
        domain = str(link.get("domain", "")).lower()
        if domain in REFERRAL_DOMAINS:
            col = domain.replace(".", "_").replace("-", "_")
            data.at[idx, col] += 1
            count += 1
    data.at[idx, "total_referral_links"] = count


def calculate_score(row):
    """
    Higher score = bigger lead opportunity for us.
    No website = high score (they need digital help).
    Few referral platforms = less visible = more opportunity.
    """
    
    score = 10 if row["has_website"] else 70

    
    unique_platforms = sum([
        row.get("justdial_com", 0) > 0,
        row.get("indiamart_com", 0) > 0,
        row.get("cardekho_com", 0) > 0,
        row.get("carwale_com", 0) > 0,
    ])
    score += max(0, (3 - unique_platforms) * 5)

    return min(score, 100)


def lead_category(score):
    if score <= 20:
        return "Strong Online Presence"
    elif score <= 40:
        return "Low Priority"
    elif score <= 60:
        return "Medium Priority"
    elif score <= 80:
        return "High Priority"
    else:
        return "Hot Lead"


def lead_reason(row):
    """Generate a human-readable reason for the score."""
    if row["has_website"]:
        return "Business has an official website - lower digital opportunity"
    else:
        if row["total_referral_links"] == 0:
            return "No website and no referral presence - maximum digital opportunity"
        else:
            return f"No official website but listed on {row['total_referral_links']} referral platform(s)"


data["lead_score"] = data.apply(calculate_score, axis=1)
data["lead_category"] = data["lead_score"].apply(lead_category)
data["lead_reason"] = data.apply(lead_reason, axis=1)


data.to_csv("car_showroom_leads_scored.csv", index=False)


final_df = data[["name", "official_url", "has_website", "lead_score", "lead_category", "lead_reason"]]
final_df.to_csv("final_leads.csv", index=False)

print("Scoring complete!")
print("=" * 50)
print(final_df.to_string())
print("\nSaved to car_showroom_leads_scored.csv and final_leads.csv")
print(f"\nLead breakdown:")
print(data["lead_category"].value_counts().to_string())