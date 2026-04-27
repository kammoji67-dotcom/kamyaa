import streamlit as st
import anthropic
import json

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="✈️ Trip Budget Planner",
    page_icon="✈️",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: #f7f3ee;
    min-height: 100vh;
}

/* ── Header ── */
.app-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 24px;
    padding: 3rem 2.5rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.app-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 250px; height: 250px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(255,165,0,0.15), transparent 70%);
}

.app-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 30%;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(100,200,255,0.1), transparent 70%);
}

.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 900;
    color: white;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 1;
}

.header-title span {
    background: linear-gradient(90deg, #ffa500, #ff6b35, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.header-sub {
    color: rgba(255,255,255,0.5);
    font-size: 1rem;
    font-weight: 300;
    position: relative;
    z-index: 1;
    letter-spacing: 0.03em;
}

/* ── Section labels ── */
.section-label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.6rem;
}

/* ── Destination chips ── */
.dest-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin: 0.5rem 0 1.5rem;
}

.dest-chip {
    padding: 0.5rem 1rem;
    border-radius: 999px;
    border: 1.5px solid #d0c8be;
    background: white;
    color: #333;
    font-size: 0.85rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-flex;
    align-items: center;
    gap: 6px;
}

.dest-chip.selected {
    background: #1a1a2e;
    border-color: #1a1a2e;
    color: white;
}

.dest-chip:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* ── Form card ── */
.form-card {
    background: white;
    border-radius: 20px;
    padding: 1.8rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div > div,
.stDateInput > div > div > input {
    border-radius: 12px !important;
    border: 1.5px solid #e0d8d0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    background: #faf8f5 !important;
    color: #1a1a2e !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #ffa500 !important;
    box-shadow: 0 0 0 3px rgba(255,165,0,0.12) !important;
}

.stTextInput label, .stNumberInput label,
.stSelectbox label, .stDateInput label,
.stSlider label, .stMultiSelect label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #888 !important;
}

.stSlider > div > div > div > div {
    background: #ffa500 !important;
}

/* ── Estimate button ── */
.stButton > button {
    background: linear-gradient(135deg, #1a1a2e, #0f3460) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.85rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    letter-spacing: 0.04em !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.25s !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(15,52,96,0.35) !important;
}

/* ── Result cards ── */
.total-card {
    background: linear-gradient(135deg, #1a1a2e, #0f3460);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    color: white;
    margin-bottom: 1.5rem;
}

.total-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 0.5rem;
}

.total-amount {
    font-family: 'Playfair Display', serif;
    font-size: 3.5rem;
    font-weight: 900;
    background: linear-gradient(90deg, #ffa500, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1;
    margin-bottom: 0.3rem;
}

.total-range {
    color: rgba(255,255,255,0.4);
    font-size: 0.85rem;
    font-weight: 300;
}

.breakdown-card {
    background: white;
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}

.breakdown-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #1a1a2e;
    margin-bottom: 1rem;
    padding-bottom: 0.7rem;
    border-bottom: 1.5px solid #f0ebe4;
}

.expense-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.55rem 0;
    border-bottom: 1px solid #f7f3ee;
}

.expense-row:last-child { border-bottom: none; }

.expense-name {
    display: flex;
    align-items: center;
    gap: 8px;
    color: #444;
    font-size: 0.9rem;
}

.expense-amount {
    font-weight: 600;
    color: #1a1a2e;
    font-size: 0.95rem;
}

.expense-bar-wrap {
    width: 100%;
    height: 5px;
    background: #f0ebe4;
    border-radius: 99px;
    margin-top: 0.25rem;
    overflow: hidden;
}

.expense-bar {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #ffa500, #ff6b35);
}

.tip-card {
    background: #fff8f0;
    border: 1.5px solid #ffddb3;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.8rem;
}

.tip-title {
    font-weight: 600;
    font-size: 0.8rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #cc7700;
    margin-bottom: 0.4rem;
}

.tip-text {
    color: #5a3a00;
    font-size: 0.88rem;
    line-height: 1.7;
    font-weight: 300;
}

.info-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}

.info-badge {
    background: #f7f3ee;
    border-radius: 10px;
    padding: 0.6rem 1rem;
    flex: 1;
    text-align: center;
}

.info-badge-label {
    font-size: 0.62rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #999;
    margin-bottom: 0.2rem;
}

.info-badge-val {
    font-weight: 600;
    color: #1a1a2e;
    font-size: 0.9rem;
}

.itinerary-card {
    background: white;
    border-radius: 18px;
    padding: 1.5rem;
    box-shadow: 0 2px 15px rgba(0,0,0,0.05);
    margin-bottom: 1rem;
}

.day-label {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    color: #ffa500;
    font-size: 1rem;
    margin-bottom: 0.3rem;
}

.day-text {
    color: #555;
    font-size: 0.88rem;
    line-height: 1.8;
    font-weight: 300;
}

/* Tab overrides */
.stTabs [data-baseweb="tab-list"] {
    background: #f0ebe4;
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    color: #888 !important;
    background: transparent !important;
}

.stTabs [aria-selected="true"] {
    background: white !important;
    color: #1a1a2e !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.08) !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 1100px; }

/* Multiselect */
.stMultiSelect > div > div {
    border-radius: 12px !important;
    border: 1.5px solid #e0d8d0 !important;
    background: #faf8f5 !important;
}
</style>
""", unsafe_allow_html=True)

# ── Destination data ───────────────────────────────────────────────────────────
DESTINATIONS = {
    "🗼 Paris, France": {"region": "Europe", "currency": "EUR", "flag": "🇫🇷"},
    "🗽 New York, USA": {"region": "North America", "currency": "USD", "flag": "🇺🇸"},
    "🗾 Tokyo, Japan": {"region": "Asia", "currency": "JPY", "flag": "🇯🇵"},
    "🏯 Bali, Indonesia": {"region": "Asia", "currency": "IDR", "flag": "🇮🇩"},
    "🏛️ Rome, Italy": {"region": "Europe", "currency": "EUR", "flag": "🇮🇹"},
    "🌴 Maldives": {"region": "Asia", "currency": "MVR", "flag": "🇲🇻"},
    "🎡 London, UK": {"region": "Europe", "currency": "GBP", "flag": "🇬🇧"},
    "🐨 Sydney, Australia": {"region": "Oceania", "currency": "AUD", "flag": "🇦🇺"},
    "🎭 Dubai, UAE": {"region": "Middle East", "currency": "AED", "flag": "🇦🇪"},
    "🌸 Singapore": {"region": "Asia", "currency": "SGD", "flag": "🇸🇬"},
    "🏔️ Manali, India": {"region": "South Asia", "currency": "INR", "flag": "🇮🇳"},
    "🌊 Goa, India": {"region": "South Asia", "currency": "INR", "flag": "🇮🇳"},
    "🕌 Istanbul, Turkey": {"region": "Europe/Asia", "currency": "TRY", "flag": "🇹🇷"},
    "🏖️ Phuket, Thailand": {"region": "Asia", "currency": "THB", "flag": "🇹🇭"},
    "🌺 Santorini, Greece": {"region": "Europe", "currency": "EUR", "flag": "🇬🇷"},
    "🦁 Nairobi, Kenya": {"region": "Africa", "currency": "KES", "flag": "🇰🇪"},
    "🎶 Barcelona, Spain": {"region": "Europe", "currency": "EUR", "flag": "🇪🇸"},
    "🏔️ Swiss Alps, Switzerland": {"region": "Europe", "currency": "CHF", "flag": "🇨🇭"},
    "🌃 Seoul, South Korea": {"region": "Asia", "currency": "KRW", "flag": "🇰🇷"},
    "🏜️ Rajasthan, India": {"region": "South Asia", "currency": "INR", "flag": "🇮🇳"},
}

# ── Claude API call ────────────────────────────────────────────────────────────
def estimate_trip(destination, days, travelers, budget_style, travel_month, from_city, activities):
    client = anthropic.Anthropic()

    prompt = f"""You are an expert travel budget consultant. Provide a detailed, accurate expense estimate for the following trip.

Trip Details:
- Destination: {destination}
- Traveling from: {from_city}
- Duration: {days} days
- Number of travelers: {travelers}
- Budget style: {budget_style} (Budget = hostels/cheap eats, Mid-range = 3-star hotels/restaurants, Luxury = 5-star/fine dining)
- Travel month: {travel_month}
- Planned activities: {', '.join(activities) if activities else 'General sightseeing'}

Respond ONLY in valid JSON (no markdown, no extra text):

{{
  "destination_overview": "2-3 sentences about the destination and what makes it great for this trip",
  "best_time_to_visit": "one sentence about travel month suitability",
  "currency": "local currency name and symbol",
  "total_min_inr": "minimum total cost in INR as integer (for all travelers)",
  "total_max_inr": "maximum total cost in INR as integer (for all travelers)",
  "total_min_usd": "minimum total cost in USD as integer (for all travelers)",
  "total_max_usd": "maximum total cost in USD as integer (for all travelers)",
  "per_person_min_inr": "per person minimum cost in INR as integer",
  "per_person_max_inr": "per person maximum cost in INR as integer",
  "breakdown": [
    {{"category": "Flights / Transport to destination", "icon": "✈️", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Accommodation", "icon": "🏨", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Local Transport", "icon": "🚌", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Food & Dining", "icon": "🍽️", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Activities & Entry Fees", "icon": "🎟️", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Shopping & Souvenirs", "icon": "🛍️", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Travel Insurance & Visa", "icon": "📋", "min_inr": 0, "max_inr": 0, "note": "brief note"}},
    {{"category": "Miscellaneous", "icon": "💡", "min_inr": 0, "max_inr": 0, "note": "brief note"}}
  ],
  "sample_itinerary": [
    {{"day": "Day 1", "plan": "detailed plan for day 1"}},
    {{"day": "Day 2", "plan": "detailed plan for day 2"}},
    {{"day": "Day 3", "plan": "detailed plan for day 3"}}
  ],
  "money_saving_tips": [
    "tip 1",
    "tip 2",
    "tip 3",
    "tip 4"
  ],
  "must_do": ["must-do activity 1", "must-do activity 2", "must-do activity 3"],
  "packing_essentials": ["item 1", "item 2", "item 3", "item 4", "item 5"],
  "visa_info": "brief visa requirements from India",
  "best_booking_platform": "recommended booking approach"
}}

Make all INR amounts realistic and accurate for {budget_style} travel. Include flights from {from_city} to {destination}. Scale costs for {travelers} travelers total."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=3000,
        messages=[{"role": "user", "content": prompt}],
    )

    text = "".join(b.text for b in response.content if hasattr(b, "text"))
    clean = text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
    <div class="header-title">Plan Your <span>Dream Trip</span> 🌍</div>
    <div class="header-sub">Get instant AI-powered expense estimates for your next adventure</div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.6], gap="large")

with col_left:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    st.markdown('<div class="section-label">🌏 Choose Your Destination</div>', unsafe_allow_html=True)
    selected_dest = st.selectbox(
        "Destination",
        options=list(DESTINATIONS.keys()),
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown('<div class="section-label">📍 Your Departure City</div>', unsafe_allow_html=True)
    from_city = st.text_input("From City", value="Mumbai", label_visibility="collapsed", placeholder="e.g. Delhi, Mumbai, Bangalore")

    col_a, col_b = st.columns(2)
    with col_a:
        days = st.number_input("🗓️ Days", min_value=1, max_value=60, value=7)
    with col_b:
        travelers = st.number_input("👥 Travelers", min_value=1, max_value=20, value=2)

    travel_month = st.selectbox(
        "📅 Travel Month",
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"],
        index=5,
    )

    budget_style = st.select_slider(
        "💰 Budget Style",
        options=["Budget / Backpacker", "Mid-range", "Luxury / Premium"],
        value="Mid-range",
    )

    activities = st.multiselect(
        "🎯 Planned Activities",
        ["Sightseeing & Heritage", "Beach & Water Sports", "Adventure & Trekking",
         "Shopping", "Food Tours", "Nightlife", "Spa & Wellness", "Wildlife Safari",
         "Photography Tours", "Cooking Classes", "Museum Hopping", "Skiing / Snow"],
        default=["Sightseeing & Heritage", "Food Tours"],
    )

    st.markdown("</div>", unsafe_allow_html=True)

    estimate_btn = st.button("✈️ Estimate My Trip Budget")

# ── Right panel ───────────────────────────────────────────────────────────────
with col_right:
    if not estimate_btn:
        dest_info = DESTINATIONS[selected_dest]
        st.markdown(f"""
        <div style="background:white; border-radius:20px; padding:2rem; box-shadow:0 2px 20px rgba(0,0,0,0.06); text-align:center;">
            <div style="font-size:5rem; margin-bottom:1rem;">{dest_info['flag']}</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.8rem; font-weight:700; color:#1a1a2e; margin-bottom:0.3rem;">{selected_dest.split(' ', 1)[1]}</div>
            <div style="color:#999; font-size:0.85rem; font-weight:500; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1.5rem;">{dest_info['region']} · {dest_info['currency']}</div>
            <div style="background:#f7f3ee; border-radius:14px; padding:1.2rem; color:#666; font-size:0.9rem; line-height:1.7; font-weight:300;">
                Fill in your trip details on the left and click <strong style="color:#1a1a2e;">"Estimate My Trip Budget"</strong> to get a detailed AI-powered breakdown of your travel expenses including flights, hotels, food, activities and more!
            </div>
            <div style="margin-top:1.5rem; display:flex; justify-content:center; gap:1rem; flex-wrap:wrap;">
                <span style="background:#fff3e0; color:#cc7700; padding:0.4rem 0.9rem; border-radius:999px; font-size:0.78rem; font-weight:600;">✈️ Flights</span>
                <span style="background:#e8f5e9; color:#2e7d32; padding:0.4rem 0.9rem; border-radius:999px; font-size:0.78rem; font-weight:600;">🏨 Hotels</span>
                <span style="background:#e3f2fd; color:#1565c0; padding:0.4rem 0.9rem; border-radius:999px; font-size:0.78rem; font-weight:600;">🍽️ Food</span>
                <span style="background:#fce4ec; color:#c62828; padding:0.4rem 0.9rem; border-radius:999px; font-size:0.78rem; font-weight:600;">🎟️ Activities</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if estimate_btn:
        with st.spinner("🌍 Calculating your dream trip expenses..."):
            try:
                data = estimate_trip(
                    destination=selected_dest.split(' ', 1)[1],
                    days=days,
                    travelers=travelers,
                    budget_style=budget_style,
                    travel_month=travel_month,
                    from_city=from_city or "Mumbai",
                    activities=activities,
                )

                # ── Total card ──────────────────────────────────────────
                st.markdown(f"""
                <div class="total-card">
                    <div class="total-label">Total Estimated Budget · {travelers} Traveler{'s' if travelers>1 else ''} · {days} Days</div>
                    <div class="total-amount">₹{int(data['total_min_inr']):,} – ₹{int(data['total_max_inr']):,}</div>
                    <div class="total-range">≈ ${int(data['total_min_usd']):,} – ${int(data['total_max_usd']):,} USD</div>
                    <div style="margin-top:1rem; color:rgba(255,255,255,0.5); font-size:0.8rem;">
                        Per person: ₹{int(data['per_person_min_inr']):,} – ₹{int(data['per_person_max_inr']):,}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Info badges ─────────────────────────────────────────
                st.markdown(f"""
                <div class="info-row">
                    <div class="info-badge">
                        <div class="info-badge-label">Travel Month</div>
                        <div class="info-badge-val">{travel_month}</div>
                    </div>
                    <div class="info-badge">
                        <div class="info-badge-label">Budget Style</div>
                        <div class="info-badge-val">{budget_style.split('/')[0].strip()}</div>
                    </div>
                    <div class="info-badge">
                        <div class="info-badge-label">Currency</div>
                        <div class="info-badge-val">{data.get('currency','—')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # ── Tabs ────────────────────────────────────────────────
                tab1, tab2, tab3, tab4 = st.tabs(["💰 Breakdown", "🗺️ Itinerary", "💡 Tips & Packing", "📋 Visa & Info"])

                with tab1:
                    breakdown = data.get("breakdown", [])
                    total_max = sum(int(b.get("max_inr", 0)) for b in breakdown) or 1

                    st.markdown('<div class="breakdown-card">', unsafe_allow_html=True)
                    st.markdown('<div class="breakdown-title">Expense Breakdown</div>', unsafe_allow_html=True)

                    for item in breakdown:
                        pct = int(item.get("max_inr", 0)) / total_max * 100
                        st.markdown(f"""
                        <div class="expense-row">
                            <div>
                                <div class="expense-name">{item.get('icon','')} {item.get('category','')}</div>
                                <div style="color:#aaa; font-size:0.75rem; margin-top:2px;">{item.get('note','')}</div>
                                <div class="expense-bar-wrap">
                                    <div class="expense-bar" style="width:{pct:.0f}%;"></div>
                                </div>
                            </div>
                            <div class="expense-amount" style="min-width:140px; text-align:right; padding-left:1rem;">
                                ₹{int(item.get('min_inr',0)):,}–{int(item.get('max_inr',0)):,}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("</div>", unsafe_allow_html=True)

                    # Must-do
                    must = data.get("must_do", [])
                    if must:
                        st.markdown(f"""
                        <div class="tip-card">
                            <div class="tip-title">⭐ Must-Do in {selected_dest.split(' ',1)[1].split(',')[0]}</div>
                            <div class="tip-text">{'  ·  '.join(must)}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with tab2:
                    itinerary = data.get("sample_itinerary", [])
                    overview = data.get("destination_overview", "")
                    best_time = data.get("best_time_to_visit", "")

                    if overview:
                        st.markdown(f"""
                        <div class="itinerary-card">
                            <div class="breakdown-title">About {selected_dest.split(' ',1)[1].split(',')[0]}</div>
                            <div class="day-text">{overview}</div>
                            <div style="margin-top:0.8rem; background:#fff8f0; border-radius:10px; padding:0.8rem; color:#cc7700; font-size:0.85rem;">
                                🗓 <strong>Best time to visit:</strong> {best_time}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                    for day in itinerary:
                        st.markdown(f"""
                        <div class="itinerary-card">
                            <div class="day-label">{day.get('day','')}</div>
                            <div class="day-text">{day.get('plan','')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    if len(itinerary) < days:
                        st.markdown(f"""
                        <div style="text-align:center; color:#aaa; font-size:0.85rem; padding:1rem; font-style:italic;">
                            + {days - len(itinerary)} more days of exploration to plan based on your interests!
                        </div>
                        """, unsafe_allow_html=True)

                with tab3:
                    tips = data.get("money_saving_tips", [])
                    if tips:
                        st.markdown('<div class="breakdown-title" style="font-family:Playfair Display,serif; font-size:1.1rem; font-weight:700; color:#1a1a2e; margin-bottom:1rem;">💡 Money-Saving Tips</div>', unsafe_allow_html=True)
                        for tip in tips:
                            st.markdown(f"""
                            <div class="tip-card" style="margin-bottom:0.7rem;">
                                <div class="tip-text">💰 {tip}</div>
                            </div>
                            """, unsafe_allow_html=True)

                    packing = data.get("packing_essentials", [])
                    if packing:
                        st.markdown("""
                        <div style="background:white; border-radius:18px; padding:1.5rem; box-shadow:0 2px 15px rgba(0,0,0,0.05); margin-top:1rem;">
                            <div style="font-family:'Playfair Display',serif; font-size:1.1rem; font-weight:700; color:#1a1a2e; margin-bottom:1rem;">🎒 Packing Essentials</div>
                        """, unsafe_allow_html=True)
                        cols = st.columns(2)
                        for i, item in enumerate(packing):
                            with cols[i % 2]:
                                st.markdown(f"""
                                <div style="background:#f7f3ee; border-radius:10px; padding:0.6rem 1rem; margin-bottom:0.5rem; font-size:0.85rem; color:#444;">
                                    ✓ {item}
                                </div>
                                """, unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                    booking = data.get("best_booking_platform", "")
                    if booking:
                        st.markdown(f"""
                        <div class="tip-card" style="margin-top:1rem;">
                            <div class="tip-title">🎫 Best Booking Approach</div>
                            <div class="tip-text">{booking}</div>
                        </div>
                        """, unsafe_allow_html=True)

                with tab4:
                    visa = data.get("visa_info", "")
                    if visa:
                        st.markdown(f"""
                        <div class="breakdown-card">
                            <div class="breakdown-title">📋 Visa Information</div>
                            <div class="day-text">{visa}</div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown(f"""
                    <div class="tip-card">
                        <div class="tip-title">⚠️ Disclaimer</div>
                        <div class="tip-text">
                            These are AI-generated estimates based on average travel costs. Actual prices may vary based on booking timing, seasonality, exchange rates, and personal preferences. Always cross-check with current travel sites like MakeMyTrip, Booking.com, or Skyscanner before finalizing your budget.
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            except json.JSONDecodeError:
                st.error("Something went wrong parsing the estimate. Please try again!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
