import pandas as pd

scored = pd.read_csv("car_showroom_leads_scored.csv")
phones = pd.read_csv("car_showroom_leads_with_phone.csv")[["name", "extracted_phone"]]

final = scored.merge(phones, on="name", how="left")
final.to_csv("car_showroom_leads_scored.csv", index=False)
print("Done! Phones merged into scored file.")
print(final[["name", "lead_category", "extracted_phone"]].head(10))