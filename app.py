import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Car Showroom Lead Intelligence",
    page_icon="🚗",
    layout="wide"
)

st.markdown("""
""", unsafe_allow_html=True)

@st.cache_data(ttl=0)
def load_data():
    files_to_try = [
        "car_showroom_leads_scored.csv",
        "car_showroom_leads_with_phone.csv",
        "final_leads.csv",
        "car_showroom_online_presence.csv",
        "businesses.csv",
    ]

    for fname in files_to_try:
        if os.path.exists(fname):
            df = pd.read_csv(fname)
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
            return df, fname

    return pd.DataFrame(), "none"

df_raw, source_file = load_data()

def badge(category: str) -> str:
    mapping = {
        "Hot Lead": ("hot-lead", "🔥 Hot Lead"),
        "High Priority": ("high-priority", "⚡ High Priority"),
        "Medium Priority": ("medium-priority", "📊 Medium Priority"),
        "Low Priority": ("low-priority", "✅ Low Priority"),
        "Strong Online Presence": ("strong-online", "🌐 Strong Online"),
    }
    cls, label = mapping.get(category, ("low-priority", category))
    return f'{label}'

def get_col(df, *candidates, default=""):
    for c in candidates:
        if c in df.columns:
            return df[c].fillna(default).astype(str)
    return pd.Series([default] * len(df))

st.markdown("## 🚗 Car Showroom Lead Intelligence — Indore")
st.markdown(
    f"Data source: {source_file}",
    unsafe_allow_html=True
)
st.markdown("---")

if df_raw.empty:
    st.error("No data files found. Run the pipeline first: osm_scraper.py → online_presence_checker.py → scorer.py → google_phone_scraper.py")
    st.stop()

df = df_raw.copy()

names = get_col(df, "name")
categories = get_col(df, "lead_category", default="Unknown")
scores = get_col(df, "lead_score", default="0")
websites = get_col(df, "official_url", "website", default="")
phones = get_col(df, "extracted_phone", "phone", default="")
has_website = get_col(df, "has_website", "has_official_website", default="False")
reasons = get_col(df, "lead_reason", "official_check_reason", default="")
addresses = get_col(df, "address", "location", default="Indore")

total = len(df)
hot = (categories == "Hot Lead").sum()
high = (categories == "High Priority").sum()
no_website = (has_website.str.lower().isin(["false", "0", "no", ""])).sum()
phones_found = (phones.str.strip() != "").sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Businesses", total)
c2.metric("Hot Leads 🔥", hot)
c3.metric("High Priority ⚡", high)
c4.metric("No Website", no_website)
c5.metric("Phones Found 📞", phones_found)

st.markdown("---")

with st.sidebar:
    st.markdown("### 🔍 Filters")

    search = st.text_input("Search by name", placeholder="e.g. Maruti, BMW...")

    all_cats = sorted(categories.unique().tolist())
    selected_cats = st.multiselect(
        "Lead Category",
        options=all_cats,
        default=all_cats
    )

    show_no_website_only = st.checkbox(
        "Show only businesses WITHOUT a website",
        value=False
    )
    show_with_phone_only = st.checkbox(
        "Show only businesses WITH phone number",
        value=False
    )

    st.markdown("---")
    st.markdown("### 📊 About")
    st.markdown("""
    This dashboard shows AI-scored car showroom leads in Indore.

    **Score Logic:**
    - No website = High opportunity
    - Few referral links = More potential
    - Hot Lead = Score 80+
    """)

mask = pd.Series([True] * total)

if search:
    mask &= names.str.contains(search, case=False, na=False)

if selected_cats:
    mask &= categories.isin(selected_cats)

if show_no_website_only:
    mask &= has_website.str.lower().isin(["false", "0", "no", ""])

if show_with_phone_only:
    mask &= phones.str.strip() != ""

filtered_indices = df.index[mask].tolist()

st.markdown(
    f"Showing {len(filtered_indices)} of {total} businesses",
    unsafe_allow_html=True
)

if not filtered_indices:
    st.info("No results match your filters.")
else:
    for i in filtered_indices:
        name = names[i]
        cat = categories[i]
        score = scores[i]
        phone = phones[i].strip()
        website = websites[i].strip()
        reason = reasons[i].strip()
        address = addresses[i].strip()

        has_web_bool = has_website[i].lower() not in ["false", "0", "no", ""]
        web_icon = "🌐" if has_web_bool else "❌"

        phone_display = f"📞 {phone}" if phone else "📞 Not found"

        website_display = (
            f'<a href="{website}" target="_blank" style="color:#a0e4ff">{website[:60]}...</a>'
            if website and len(website) > 10
            else "No official website"
        )

        st.markdown(
            f"""
            <div class="lead-card">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="lead-name">{name}</div>
                        <div class="lead-detail">📍 {address}</div>
                        <div class="lead-phone">{phone_display}</div>
                        <div class="lead-url">{web_icon} {website_display}</div>
                        <div class="lead-detail" style="margin-top:8px; color:#7b8ab8">{reason}</div>
                    </div>
                    <div style="text-align:right;">
                        {badge(cat)}
                        <div style="color:#666; font-size:13px; margin-top:8px;">Score: {score}/100</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

with st.expander("📋 View Raw Data Table"):
    st.dataframe(df_raw, use_container_width=True)

st.markdown("---")

csv_data = df_raw.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Full Dataset as CSV",
    data=csv_data,
    file_name="indore_car_showroom_leads.csv",
    mime="text/csv"
)
