import streamlit as st
import plotly.graph_objects as go
import joblib
import pandas as pd
import textwrap

model = joblib.load("bnpl_model.pkl")

st.set_page_config(page_title="BNPL Risk", page_icon="🛡️", layout="wide")



# ---------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500&display=swap');

    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }

    .stApp {
        background: #060E1D;
        color: #e6e9ef;
    }

    #MainMenu, footer, header {visibility: hidden;}

    .block-container {
        padding-top: 5.5rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* ---------- NAVBAR ---------- */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 16px 40px;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        width: 100%;
        z-index: 999999;
        background: #060E1D;
        box-shadow: 0 4px 20px rgba(0,0,0,0.35);
    }
    .navbar-logo {
        font-size: 22px;
        font-weight: 800;
        color: #ffffff;
    }
    .navbar-logo span { color: #3b82f6; }
    .navbar-links a {
        color: #9aa4b2;
        text-decoration: none;
        margin: 0 18px;
        font-weight: 500;
        font-size: 15px;
    }
    .icon-badge {
        width: 34px; height: 34px; border-radius: 9px;
        background: linear-gradient(135deg,#3b82f6,#1d4ed8);
        display:flex; align-items:center; justify-content:center;
        font-size:16px; margin-right:8px; box-shadow: 0 0 20px rgba(59,130,246,.4);
    }

    /* ---------- HERO ---------- */
    .pill {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(59,130,246,0.08);
        border: 1px solid rgba(59,130,246,0.35);
        color: #60a5fa;
        padding: 6px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 1px;
        font-family: 'JetBrains Mono', monospace;
        margin-bottom: 22px;
    }
    .hero-title {
        font-size: 52px;
        font-weight: 800;
        line-height: 1.12;
        color: #ffffff;
        margin-bottom: 20px;
    }
    .hero-title .blue { color: #3b82f6; }
    .hero-sub {
        color: #9aa4b2;
        font-size: 17px;
        line-height: 1.6;
        max-width: 520px;
        margin-bottom: 28px;
    }

    /* ---------- CARD ---------- */
    .card {
        background: linear-gradient(180deg, rgba(20,26,38,0.9), rgba(15,20,30,0.9));
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 22px 24px;
    }
    .card-label {
        font-family: 'JetBrains Mono', monospace;
        color: #3b82f6;
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 600;
    }
    .card-title { color: #fff; font-size: 19px; font-weight: 700; margin-top: 4px;}
    .live-badge {
        background: rgba(34,197,94,0.12); color:#22c55e; border:1px solid rgba(34,197,94,.35);
        padding: 4px 12px; border-radius: 20px; font-size:12px; font-weight:600;
    }

    .mini-stat {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 12px;
        padding: 14px 16px;
        text-align:center;
    }
    .mini-stat .lab { color:#7c8797; font-size:11px; letter-spacing:1px; font-family:'JetBrains Mono',monospace;}
    .mini-stat .val { color:#fff; font-size:22px; font-weight:700; margin-top:4px;}

    .bar-row { display:flex; align-items:center; margin: 10px 0; gap: 12px;}
    .bar-name { width: 90px; color:#c7ccd6; font-size:13px;}
    .bar-track { flex:1; height:8px; background:rgba(255,255,255,0.06); border-radius:6px; overflow:hidden;}
    .bar-fill { height:100%; border-radius:6px; }
    .bar-pct { width:40px; text-align:right; color:#c7ccd6; font-size:13px;}

    /* ---------- STAT ROW under hero ---------- */
    .stat-big { font-size: 34px; font-weight: 800; color:#fff; }
    .stat-lab { color:#7c8797; font-size:14px; margin-top:2px;}

    /* ---------- METRIC TILES ---------- */
    .metric-tile {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 20px;
    }
    .metric-icon {
        width:38px; height:38px; border-radius:10px;
        display:flex; align-items:center; justify-content:center;
        font-size:18px; margin-bottom: 14px;
    }
    .metric-lab { color:#7c8797; font-size:11px; letter-spacing:1px; font-family:'JetBrains Mono',monospace;}
    .metric-val { color:#fff; font-size:26px; font-weight:800; margin-top:4px;}
    .metric-sub { color:#8b93a3; font-size:12.5px; margin-top: 4px;}

    /* ---------- SECTION HEADERS ---------- */
    .eyebrow { color:#3b82f6; font-family:'JetBrains Mono',monospace; font-size:12px; letter-spacing:2px; font-weight:700;}
    .sec-title { color:#fff; font-size:34px; font-weight:800; margin: 6px 0 10px 0;}
    .sec-sub { color:#9aa4b2; font-size:15.5px; max-width: 700px; line-height:1.6; margin-bottom: 20px;}

    .insight-box {
        background: rgba(59,130,246,0.06);
        border: 1px solid rgba(59,130,246,0.25);
        border-radius: 14px;
        padding: 18px 20px;
        display:flex; gap:14px; align-items:flex-start;
        margin-top: 20px;
    }
    .insight-title { color:#fff; font-weight:700; margin-bottom:4px;}
    .insight-text { color:#aab2c0; font-size:14.5px; line-height:1.6;}
    .insight-text b { color:#e6e9ef; }

    /* ---------- FORM ---------- */
    .form-label {
        color:#7c8797; font-size:11.5px; letter-spacing:1px; font-family:'JetBrains Mono',monospace;
        margin-bottom: 4px; text-transform:uppercase;
    }
    div[data-testid="stNumberInput"] input, div[data-testid="stTextInput"] input {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: #fff !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        color: #fff !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg,#3b82f6,#2563eb);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 0;
        font-weight: 700;
        font-size: 16px;
        width: 100%;
        box-shadow: 0 8px 24px rgba(37,99,235,0.35);
    }

    .risk-badge-low { background: rgba(34,197,94,0.12); color:#22c55e; border:1px solid rgba(34,197,94,.4); padding:6px 16px; border-radius:20px; font-weight:700; font-size:13px; display:inline-block;}
    .risk-badge-med { background: rgba(245,158,11,0.12); color:#f59e0b; border:1px solid rgba(245,158,11,.4); padding:6px 16px; border-radius:20px; font-weight:700; font-size:13px; display:inline-block;}
    .risk-badge-high { background: rgba(239,68,68,0.12); color:#ef4444; border:1px solid rgba(239,68,68,.4); padding:6px 16px; border-radius:20px; font-weight:700; font-size:13px; display:inline-block;}

    .factor-dot { width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:10px;}

    hr { border-color: rgba(255,255,255,0.07); }

    .footer-title { text-align:center; color:#fff; font-size:20px; font-weight:800; margin-top: 10px;}
    .footer-sub { text-align:center; color:#8b93a3; margin: 10px 0 20px 0; }
    .footer-links { text-align:center; color:#9aa4b2; }
    .footer-copy { text-align:center; color:#5c6474; font-size:12.5px; margin-top:16px; font-family:'JetBrains Mono',monospace;}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# NAVBAR
# ---------------------------------------------------------------------------
st.markdown("""
<div class="navbar">
    <div style="display:flex; align-items:center;">
        <div class="icon-badge">🛡️</div>
        <div class="navbar-logo">BNPL <span>Risk</span></div>
    </div>
    <div class="navbar-links">
        <a href="#about">About</a>
        <a href="#analysis">Analysis</a>
        <a href="#prediction">Prediction</a>
    </div>
    <div></div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# HERO
# ---------------------------------------------------------------------------
st.markdown('<a name="about"></a>', unsafe_allow_html=True)
col_l, col_r = st.columns([1.05, 1], gap="large")

with col_l:
    st.markdown("""
    <div class="pill">⚡ AI-POWERED CREDIT INTELLIGENCE</div>
    <div class="hero-title">Predict BNPL<br><span class="blue">Credit Risk</span><br>with AI</div>
    <div class="hero-sub">
        Analyze customer financial behavior and predict the probability of default
        using machine learning. Make smarter lending decisions in seconds.
    </div>
    """, unsafe_allow_html=True)
    b1, b2 = st.columns([1, 1])
    with b1:
        st.link_button("Predict Risk →", "#prediction", use_container_width=True)
    with b2:
        st.link_button("View Analysis 📊", "#analysis", use_container_width=True)

with col_r:
    st.markdown("""
    <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div class="card-label">RISK INTELLIGENCE</div>
                <div class="card-title">Portfolio Dashboard</div>
            </div>
            <div class="live-badge">● Live</div>
        </div>
        <div style="display:flex; gap:12px; margin-top:18px;">
            <div class="mini-stat" style="flex:1;"><div class="lab">CUSTOMERS</div><div class="val">11,200</div></div>
            <div class="mini-stat" style="flex:1;"><div class="lab">DEFAULT RATE</div><div class="val">12.4%</div></div>
            <div class="mini-stat" style="flex:1;"><div class="lab">HIGH RISK</div><div class="val">576</div></div>
        </div>
        <div style="margin-top:20px; color:#7c8797; font-size:11px; letter-spacing:1px; font-family:'JetBrains Mono',monospace;">RISK DISTRIBUTION</div>
        <div class="bar-row">
            <div class="bar-name">Low Risk</div>
            <div class="bar-track"><div class="bar-fill" style="width:73.17%; background:#22c55e;"></div></div>
            <div class="bar-pct">73.17%</div>
        </div>
        <div class="bar-row">
            <div class="bar-name">Medium Risk</div>
            <div class="bar-track"><div class="bar-fill" style="width21.27%; background:#f59e0b;"></div></div>
            <div class="bar-pct">21.27%</div>
        </div>
        <div class="bar-row">
            <div class="bar-name">High Risk</div>
            <div class="bar-track"><div class="bar-fill" style="width:5.57%; background:#ef4444;"></div></div>
            <div class="bar-pct">5.57%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul"]
    vals = [9.5, 9.8, 10.6, 11.4, 11.9, 12.6, 12.4]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=vals, mode="lines", line=dict(color="#3b82f6", width=3),
                              fill="tozeroy", fillcolor="rgba(59,130,246,0.12)"))
    fig.update_layout(
        height=170, margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#7c8797", tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, visible=False),
        title=dict(text="DEFAULT RATE TREND    ↓ 2.1% this month", font=dict(size=11, color="#7c8797"), x=0),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("<br>", unsafe_allow_html=True)

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown('<div class="stat-big">74%</div><div class="stat-lab">Model Accuracy</div>', unsafe_allow_html=True)
with s2:
    st.markdown('<div class="stat-big">820+</div><div class="stat-lab">Customers Assessed</div>', unsafe_allow_html=True)
with s3:
    st.markdown('<div class="stat-big">&lt;2s</div><div class="stat-lab">Avg Prediction Time</div>', unsafe_allow_html=True)

st.markdown("<br><hr><br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# METRIC TILES
# ---------------------------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
tiles = [
    ("👥", "rgba(59,130,246,0.15)", "TOTAL CUSTOMERS", "10.345", "+480 this month"),
    ("⚠️", "rgba(239,68,68,0.15)", "DEFAULT RATE", "39.05%", "↓ 2.1% vs last month"),
    ("📈", "rgba(34,197,94,0.15)", "AVERAGE INCOME", "35.05K", "Per month"),
    ("💳", "rgba(245,158,11,0.15)", "AVG CREDIT SCORE", "448", "Fair — improving"),
]
for col, (icon, bg, lab, val, sub) in zip([m1, m2, m3, m4], tiles):
    with col:
        st.markdown(textwrap.dedent(f"""
        <div class="metric-tile">
            <div class="metric-icon" style="background:{bg};">{icon}</div>
            <div class="metric-lab">{lab}</div>
            <div class="metric-val">{val}</div>
            <div class="metric-sub">{sub}</div>
        </div>
        """), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------------------------
st.markdown('<a name="analysis"></a>', unsafe_allow_html=True)
st.markdown("""
<div class="eyebrow">ANALYTICS</div>
<div class="sec-title">Customer Insights</div>
<div class="sec-sub">Distribution analysis across key credit risk indicators to identify vulnerable customer segments.</div>
""", unsafe_allow_html=True)

a1, a2, a3 = st.columns(3)

def bar_chart(x, y, color, title, icon, icon_bg):
    fig = go.Figure(go.Bar(x=x, y=y, marker_color=color, marker_line_width=0))
    fig.update_layout(
        height=260, margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, color="#7c8797", tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#7c8797", tickfont=dict(size=11)),
    )
    return fig

with a1:
    st.markdown("""<div class="card"><div class="card-label">DISTRIBUTION</div><div class="card-title">Age Groups</div>""", unsafe_allow_html=True)
    fig = bar_chart(["18-24","25-34","35-44","45-54","55-64","65+"], [1350,3850,2650,1550,900,450], "#3b82f6", "", "", "")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with a2:
    st.markdown("""<div class="card"><div class="card-label">DISTRIBUTION</div><div class="card-title">Monthly Income</div>""", unsafe_allow_html=True)
    fig = bar_chart(["<$2k","$2-4k","$4-6k","$6-8k","$8-10k",">$10k"], [1080,2280,2820,2020,1230,430], "#22c55e", "", "", "")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with a3:
    st.markdown("""<div class="card"><div class="card-label">DISTRIBUTION</div><div class="card-title">Credit Score</div>""", unsafe_allow_html=True)
    fig = bar_chart(["300-499","500-579","580-669","670-739","740-799","800+"], [750,1750,2550,3050,2350,1400], "#a855f7", "", "", "")
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box">
    <div style="font-size:20px;">💡</div>
    <div>
        <div class="insight-title">Key Insight</div>
        <div class="insight-text">
            Customers aged 25–34 represent the largest segment, while those under 25 show disproportionately
            higher default rates. The 580–670 credit score band contains the highest-risk concentration —
            customers here are <b>3.2× more likely</b> to default than those scoring above 740. Understand which
            customer groups are more likely to default.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br><hr><br>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------------------------

st.markdown('<a name="prediction"></a>', unsafe_allow_html=True)

st.markdown("""
<div class="eyebrow">ML MODEL</div>
<div class="sec-title">Check Customer Risk</div>
<div class="sec-sub">
    Enter customer details below to get an instant AI-powered default probability assessment.
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# INPUT FORM
# ---------------------------------------------------------------------------
# Wrapped in st.form so editing a field does NOT trigger an immediate rerun.
# All current field values are only captured/submitted together when the
# user presses the submit button below - this avoids the classic Streamlit
# bug where changing an input after a previous prediction leaves the old
# result on screen until you happen to click twice.

with st.form("bnpl_risk_form"):

    f1, f2, f3 = st.columns(3)

    # =========================
    # COLUMN 1 - NUMERICAL
    # =========================

    with f1:

        st.markdown('<div class="form-label">AGE</div>', unsafe_allow_html=True)
        age = st.number_input("age", min_value=18, max_value=100, value=28, label_visibility="collapsed")

        st.markdown('<div class="form-label">MONTHLY INCOME ($)</div>', unsafe_allow_html=True)
        monthly_income = st.number_input("monthly_income", min_value=0.0, value=4500.0, step=100.0, label_visibility="collapsed")

        st.markdown('<div class="form-label">CREDIT SCORE</div>', unsafe_allow_html=True)
        credit_score = st.number_input("credit_score", min_value=300, max_value=850, value=650, label_visibility="collapsed")

        st.markdown('<div class="form-label">PURCHASE AMOUNT ($)</div>', unsafe_allow_html=True)
        purchase_amount = st.number_input("purchase_amount", min_value=0.0, value=850.0, step=10.0, label_visibility="collapsed")

        st.markdown('<div class="form-label">BNPL INSTALLMENTS</div>', unsafe_allow_html=True)
        bnpl_installments = st.number_input("bnpl_installments", min_value=1, max_value=24, value=6, label_visibility="collapsed")

    # =========================
    # COLUMN 2 - NUMERICAL
    # =========================

    with f2:

        st.markdown('<div class="form-label">REPAYMENT DELAY (DAYS)</div>', unsafe_allow_html=True)
        repayment_delay_days = st.number_input("repayment_delay_days", min_value=0, max_value=365, value=0, step=1, label_visibility="collapsed")

        st.markdown('<div class="form-label">MISSED PAYMENTS</div>', unsafe_allow_html=True)
        missed_payments = st.number_input("missed_payments", min_value=0, max_value=20, value=0, step=1, label_visibility="collapsed")

        st.markdown('<div class="form-label">APP USAGE FREQUENCY</div>', unsafe_allow_html=True)
        app_usage_frequency = st.number_input("app_usage_frequency", min_value=0, value=10, step=1, label_visibility="collapsed")

        st.markdown('<div class="form-label">DEBT-TO-INCOME RATIO</div>', unsafe_allow_html=True)
        debt_to_income_ratio = st.number_input("debt_to_income_ratio", min_value=0.0, max_value=2.0, value=0.35, step=0.01, format="%.2f", label_visibility="collapsed")

    # =========================
    # COLUMN 3 - CATEGORICAL
    # =========================

    with f3:

        st.markdown('<div class="form-label">EMPLOYMENT TYPE</div>', unsafe_allow_html=True)
        employment_type = st.selectbox(
            "employment_type",
            ["Salaried (Full-time)", "Salaried (Part-time)", "Self-employed", "Unemployed", "Student"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="form-label">PRODUCT CATEGORY</div>', unsafe_allow_html=True)
        product_category = st.selectbox(
            "product_category",
            ["Electronics", "Fashion", "Home", "Beauty", "Travel", "Other"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="form-label">LOCATION</div>', unsafe_allow_html=True)
        location = st.selectbox(
            "location",
            ["Cairo", "Giza", "Alexandria", "Other"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="form-label">CUSTOMER SEGMENT</div>', unsafe_allow_html=True)
        customer_segment = st.selectbox(
            "customer_segment",
            ["New", "Regular", "Premium", "High Value"],
            label_visibility="collapsed"
        )

    # ---------------------------------------------------------------------------
    # PREDICT BUTTON (form submit)
    # ---------------------------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)
    predict_clicked = st.form_submit_button("🛡️  Predict Risk", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# PREDICTION
# ---------------------------------------------------------------------------

if predict_clicked:

    # -------------------------------------------------------
    # INPUT VALIDATION
    # -------------------------------------------------------
    # Catch logically impossible combinations before sending them to the
    # model. The model was trained only on realistic data, so out-of-
    # distribution inputs (e.g. more missed payments than total
    # installments) can produce unreliable / misleading probabilities.

    validation_errors = []

    if missed_payments > bnpl_installments:
        validation_errors.append(
            f"Missed Payments ({missed_payments}) can't exceed BNPL Installments ({bnpl_installments})."
        )

    if validation_errors:
        for err in validation_errors:
            st.warning(f"⚠️ {err}")
        st.session_state["ran_prediction"] = False
        st.stop()

    # Create dataframe with EXACT feature names used during training
    input_data = pd.DataFrame([{
        # Numerical features
        "age": age,
        "monthly_income": monthly_income,
        "credit_score": credit_score,
        "purchase_amount": purchase_amount,
        "bnpl_installments": bnpl_installments,
        "repayment_delay_days": repayment_delay_days,
        "missed_payments": missed_payments,
        "app_usage_frequency": app_usage_frequency,
        "debt_to_income_ratio": debt_to_income_ratio,
        # Categorical features
        "employment_type": employment_type,
        "product_category": product_category,
        "location": location,
        "customer_segment": customer_segment
    }])

    try:
        probability = model.predict_proba(input_data)[0][1] * 100
        probability = round(float(probability), 1)

        st.session_state["ran_prediction"] = True
        st.session_state["prob"] = probability

    except Exception as e:
        st.error(f"Prediction error: {e}")
        st.stop()


# ---------------------------------------------------------------------------
# DISPLAY RESULT
# ---------------------------------------------------------------------------

if st.session_state.get("ran_prediction", False):

    prob = st.session_state["prob"]

    # -------------------------------------------------------
    # RISK LEVEL
    # -------------------------------------------------------

    if prob < 30:
        badge_html = '<span class="risk-badge-low">✓ LOW RISK</span>'
        color = "#22c55e"
        verdict = "Unlikely to Default"

    elif prob < 60:
        badge_html = '<span class="risk-badge-med">⚠ MEDIUM RISK</span>'
        color = "#f59e0b"
        verdict = "Moderate Default Risk"

    else:
        badge_html = '<span class="risk-badge-high">⛔ HIGH RISK</span>'
        color = "#ef4444"
        verdict = "Likely to Default"

    # -------------------------------------------------------
    # GAUGE
    # -------------------------------------------------------

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=prob,
            number={"suffix": "%", "font": {"size": 40, "color": "#ffffff"}},
            gauge={
                "axis": {"range": [0, 100], "visible": False},
                "bar": {"color": color, "thickness": 0.25},
                "bgcolor": "rgba(255,255,255,0.05)",
                "borderwidth": 0
            },
            domain={"x": [0, 1], "y": [0, 1]}
        )
    )

    gauge.update_layout(
        height=280,
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#fff"}
    )

    # -------------------------------------------------------
    # RESULT LAYOUT
    # -------------------------------------------------------

    result_col1, result_col2 = st.columns([1, 1.3])

    # =========================
    # LEFT RESULT
    # =========================

    with result_col1:

        st.markdown(
            textwrap.dedent(f"""
            <div style="display:flex; justify-content:space-between; align-items:center;">
                {badge_html}
                <span style="color:#7c8797; font-size:11px; font-family:'JetBrains Mono',monospace;">AI MODEL</span>
            </div>
            """),
            unsafe_allow_html=True
        )

        st.plotly_chart(gauge, use_container_width=True, config={"displayModeBar": False})

        st.markdown(
            textwrap.dedent(f"""
            <div style="text-align:center; margin-top:-20px;">
                <div style="color:#7c8797; font-size:11px; letter-spacing:1px; font-family:'JetBrains Mono',monospace;">
                    DEFAULT PROBABILITY
                </div>
                <div style="color:{color}; font-size:36px; font-weight:800;">
                    {prob}%
                </div>
                <div style="color:#c7ccd6; font-size:15px;">
                    {verdict}
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )

    # =========================
    # RIGHT RESULT
    # =========================

    with result_col2:

        st.markdown(
            '<div class="card-label" style="margin-top:20px;">INPUT SUMMARY</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            textwrap.dedent(f"""
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:18px; margin-top:12px;">
                <div style="color:#c7ccd6; font-size:14px; line-height:2;">
                    <b>Age:</b> {age}<br>
                    <b>Monthly Income:</b> ${monthly_income:,.0f}<br>
                    <b>Credit Score:</b> {credit_score}<br>
                    <b>Purchase Amount:</b> ${purchase_amount:,.0f}<br>
                    <b>BNPL Installments:</b> {bnpl_installments}<br>
                    <b>Repayment Delay:</b> {repayment_delay_days} days<br>
                    <b>Missed Payments:</b> {missed_payments}<br>
                    <b>App Usage:</b> {app_usage_frequency}<br>
                    <b>DTI:</b> {debt_to_income_ratio:.2f}<br>
                    <b>Employment:</b> {employment_type}<br>
                    <b>Product:</b> {product_category}<br>
                    <b>Location:</b> {location}<br>
                    <b>Segment:</b> {customer_segment}
                </div>
            </div>
            """),
            unsafe_allow_html=True
        )
