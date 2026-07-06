import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Vehicle Lead Intelligence — Indore",
    page_icon="🚘",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="metric-container"] {
        background: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 16px;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }
    .hot-lead        { background: #ff4b4b22; color: #ff4b4b; border: 1px solid #ff4b4b; }
    .high-priority   { background: #ff914d22; color: #ff914d; border: 1px solid #ff914d; }
    .medium-priority { background: #ffd60022; color: #ffd600; border: 1px solid #ffd600; }
    .low-priority    { background: #00c85322; color: #00c853; border: 1px solid #00c853; }
    .strong-online   { background: #2979ff22; color: #2979ff; border: 1px solid #2979ff; }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #ffffff;
        margin: 28px 0 14px 0;
        padding: 10px 16px;
        border-radius: 8px;
    }
    .car-section    { background: #1a2340; border-left: 4px solid #2979ff; }
    .bike-section   { background: #1a2d1a; border-left: 4px solid #00c853; }

    .lead-card {
        background: #1e2130;
        border: 1px solid #2d3250;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
    }
    .lead-card:hover { border-color: #4a5580; }
    .lead-name   { font-size: 16px; font-weight: 700; color: #ffffff; }
    .lead-detail { font-size: 13px; color: #9aa0b8; margin-top: 4px; }
    .lead-phone  { font-size: 14px; color: #a0e4ff; margin-top: 6px; }
    .lead-url    { font-size: 13px; color: #7b8ab8; margin-top: 4px; }
    .count-pill  {
        display: inline-block;
        background: #2d3250;
        color: #9aa0b8;
        font-size: 13px;
        padding: 2px 10px;
        border-radius: 20px;
        margin-left: 10px;
    }
</style>
""", unsafe_allow_html=True)



@st.cache_data(ttl=0)
def load_data():
    files_to_try = [
        "vehicle_showroom_leads_with_phone.csv",
        "vehicle_showroom_leads_scored.csv",
        "leads_small.csv",
        "final_leads.csv",
        "car_showroom_leads_with_phone.csv",
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


def badge(category):
    mapping = {
        "Hot Lead":               ("hot-lead",        "🔥 Hot Lead"),
        "High Priority":          ("high-priority",   "⚡ High Priority"),
        "Medium Priority":        ("medium-priority", "📊 Medium Priority"),
        "Low Priority":           ("low-priority",    "✅ Low Priority"),
        "Strong Online Presence": ("strong-online",   "🌐 Strong Online"),
    }
    cls, label = mapping.get(category, ("low-priority", category))
    return f'<span class="badge {cls}">{label}</span>'


def get_col(df, *candidates, default=""):
    for c in candidates:
        if c in df.columns:
            return df[c].fillna(default).astype(str)
    return pd.Series([default] * len(df))


# ── Two Wheeler Brand Keywords ─────────────────────────────────────────────────
TWO_WHEELER_KEYWORDS = [
    "hero", "honda 2", "bajaj", "tvs", "royal enfield", "yamaha",
    "suzuki 2", "ktm", "husqvarna", "jawa", "yezdi", "ola electric",
    "ather", "revolt", "simple energy", "bounce", "two wheel", "2wheel",
    "bike", "motorcycle", "scooter", "motocorp"
]

def is_two_wheeler(name):
    name_lower = str(name).lower()
    return any(kw in name_lower for kw in TWO_WHEELER_KEYWORDS)


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## 🚘 Vehicle Dealership Lead Intelligence — Indore")
st.markdown(f"<span style='color:#666;font-size:13px'>Data source: {source_file}</span>",
            unsafe_allow_html=True)
st.markdown("---")

if df_raw.empty:
    st.error("No data files found. Run the pipeline first.")
    st.stop()

df = df_raw.copy()

names       = get_col(df, "name")
categories  = get_col(df, "lead_category", default="Unknown")
scores      = get_col(df, "lead_score",    default="0")
websites    = get_col(df, "official_url",  "website", default="")
phones      = get_col(df, "extracted_phone", "phone", default="")
has_website = get_col(df, "has_website",   "has_official_website", default="False")
reasons     = get_col(df, "lead_reason",   "official_check_reason", default="")
addresses   = get_col(df, "address",       "location", default="Indore")

# Split into car vs two-wheeler
car_mask  = ~names.apply(is_two_wheeler)
bike_mask = names.apply(is_two_wheeler)

# ── KPI Metrics ────────────────────────────────────────────────────────────────
total        = len(df)
hot          = (categories == "Hot Lead").sum()
high         = (categories == "High Priority").sum()
no_web       = (has_website.str.lower().isin(["false", "0", "no", ""])).sum()
phones_found = (phones.str.strip() != "").sum()
total_cars   = car_mask.sum()
total_bikes  = bike_mask.sum()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Businesses", total)
c2.metric("Hot Leads 🔥",      hot)
c3.metric("High Priority ⚡",  high)
c4.metric("No Website",        no_web)
c5.metric("Phones Found 📞",   phones_found)

st.markdown("---")

# ── Sidebar Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filters")

    search = st.text_input("Search by name", placeholder="e.g. Hero, Maruti, BMW...")

    vehicle_type = st.radio(
        "Vehicle Type",
        options=["All", "🚗 Cars Only", "🏍️ Two Wheelers Only"],
        index=0
    )

    all_cats = sorted(categories.unique().tolist())
    selected_cats = st.multiselect(
        "Lead Category",
        options=all_cats,
        default=all_cats
    )

    show_no_website   = st.checkbox("Only businesses WITHOUT a website", value=False)
    show_with_phone   = st.checkbox("Only businesses WITH phone number", value=False)

    st.markdown("---")
    st.markdown("### 📊 Breakdown")
    st.markdown(f"🚗 Car Showrooms: **{total_cars}**")
    st.markdown(f"🏍️ Two Wheelers: **{total_bikes}**")
    st.markdown("---")
    st.markdown("### ℹ️ Score Logic")
    st.markdown("""
- No website = High opportunity
- Few referral links = More potential
- Hot Lead = Score 80+
    """)


# ── Apply Filters ──────────────────────────────────────────────────────────────
mask = pd.Series([True] * total)

if search:
    mask &= names.str.contains(search, case=False, na=False)
if selected_cats:
    mask &= categories.isin(selected_cats)
if show_no_website:
    mask &= has_website.str.lower().isin(["false", "0", "no", ""])
if show_with_phone:
    mask &= phones.str.strip() != ""
if vehicle_type == "🚗 Cars Only":
    mask &= car_mask
elif vehicle_type == "🏍️ Two Wheelers Only":
    mask &= bike_mask


# ── Card Renderer ──────────────────────────────────────────────────────────────
def render_cards(indices):
    if not indices:
        st.info("No results match your filters.")
        return
    for i in indices:
        name     = names[i]
        cat      = categories[i]
        score    = scores[i]
        phone    = phones[i].strip()
        website  = websites[i].strip()
        reason   = reasons[i].strip()
        address  = addresses[i].strip()

        has_web_bool    = has_website[i].lower() not in ["false", "0", "no", ""]
        web_icon        = "🌐" if has_web_bool else "❌"
        phone_display   = f"📞 {phone}" if phone else "📞 Not found"
        website_display = (
            f'<a href="{website}" target="_blank" style="color:#a0e4ff">{website[:55]}...</a>'
            if website and len(website) > 10 else "No official website"
        )

        st.markdown(f"""
        <div class="lead-card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <div>
                    <div class="lead-name">{name}</div>
                    <div class="lead-detail">📍 {address}</div>
                    <div class="lead-phone">{phone_display}</div>
                    <div class="lead-url">{web_icon} {website_display}</div>
                    <div class="lead-detail" style="margin-top:8px;color:#7b8ab8">{reason}</div>
                </div>
                <div style="text-align:right;">
                    {badge(cat)}
                    <div style="color:#666;font-size:12px;margin-top:8px;">Score: {score}/100</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── Filtered indices split by type ─────────────────────────────────────────────
filtered = df.index[mask].tolist()
car_filtered  = [i for i in filtered if car_mask[i]]
bike_filtered = [i for i in filtered if bike_mask[i]]

st.markdown(f"Showing **{len(filtered)}** of **{total}** businesses")

# ── Car Section ────────────────────────────────────────────────────────────────
if vehicle_type != "🏍️ Two Wheelers Only":
    st.markdown(
        f'<div class="section-title car-section">🚗 Car Showrooms <span class="count-pill">{len(car_filtered)}</span></div>',
        unsafe_allow_html=True
    )
    render_cards(car_filtered)

# ── Two Wheeler Section ────────────────────────────────────────────────────────
if vehicle_type != "🚗 Cars Only":
    st.markdown(
        f'<div class="section-title bike-section">🏍️ Two Wheeler Dealers <span class="count-pill">{len(bike_filtered)}</span></div>',
        unsafe_allow_html=True
    )
    render_cards(bike_filtered)

# ── Raw Data Table ─────────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("📋 View Raw Data Table"):
    st.dataframe(df_raw, use_container_width=True)

# ── Download ───────────────────────────────────────────────────────────────────
st.markdown("---")
csv_data = df_raw.to_csv(index=False).encode("utf-8")
st.download_button(
    label="⬇️ Download Full Dataset as CSV",
    data=csv_data,
    file_name="indore_vehicle_leads.csv",
    mime="text/csv"
)
