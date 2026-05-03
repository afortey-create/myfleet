"""
MyFleet v3 — Family Vehicle Fleet Manager
Deloitte light theme | vehicles.csv backend
"""

import streamlit as st
import pandas as pd
from datetime import date
import os

# ──────────────────────────────────────────────
# CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="MyFleet",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSV_PATH = "vehicles.csv"
DATE_FMT = "%d/%m/%Y"
AMBER_DAYS = 30
RED_DAYS = 7

# ──────────────────────────────────────────────
# DELOITTE PALETTE + CSS
# Primaries: Green #86BC25 | Black #000000 | Dark Gray #222222
# Surfaces:  White #FFFFFF | Light Gray #E6E6E6 | Pale Green #F1F6E4
# Status:    Red #C0392B | Amber #E67E22 | OK #3C8F2A
# ──────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --white:        #FFFFFF;
    --black:        #000000;
    --dark-gray:    #222222;
    --mid-gray:     #53565A;
    --light-gray:   #E6E6E6;
    --pale-gray:    #F5F5F5;
    --green:        #86BC25;
    --dark-green:   #3C8F2A;
    --pale-green:   #F1F6E4;
    --border:       #D0D0CE;
    --red:          #C0392B;
    --amber:        #D4750A;
    --ok:           #3C8F2A;
    --blue:         #005587;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background-color: var(--pale-gray);
    color: var(--dark-gray);
}
.stApp { background: var(--pale-gray); }
[data-testid="stSidebar"] { background: var(--white); border-right: 2px solid var(--light-gray); }
#MainMenu, footer, header { visibility: hidden; }

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.9rem 1.5rem;
    margin: -1rem -1rem 0 -1rem;
    background: var(--black);
    border-bottom: 4px solid var(--green);
}
.topbar-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--white);
    letter-spacing: -0.02em;
    line-height: 1;
}
.topbar-sub {
    font-size: 0.65rem;
    color: var(--green);
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.2rem;
}
.topbar-date {
    font-size: 0.75rem;
    color: #BBBCBC;
    letter-spacing: 0.02em;
}

/* ── Metric strip ── */
.metric-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.75rem;
    margin: 1.2rem 0 1.4rem;
}
.metric-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: 4px solid var(--border);
    border-radius: 4px;
    padding: 1rem 1.2rem 0.85rem;
    text-align: left;
}
.mc-total  { border-top-color: var(--green); }
.mc-urgent { border-top-color: var(--red); }
.mc-soon   { border-top-color: var(--amber); }
.mc-ok     { border-top-color: var(--ok); }
.metric-num {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1;
    color: var(--dark-gray);
}
.metric-lbl {
    font-size: 0.7rem;
    color: var(--mid-gray);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.3rem;
    font-weight: 600;
}

/* ── Status badge ── */
.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.22rem 0.6rem;
    border-radius: 3px;
    font-size: 0.67rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-red   { background: #FDECEA; color: var(--red);   border: 1px solid #E8B4B0; }
.badge-amber { background: #FEF3E7; color: var(--amber); border: 1px solid #F5CFA0; }
.badge-green { background: var(--pale-green); color: var(--dark-green); border: 1px solid #BDD98A; }
.badge-grey  { background: var(--light-gray); color: var(--mid-gray);   border: 1px solid var(--border); }

/* ── Days pill ── */
.dpill {
    display: inline-block;
    padding: 0.14rem 0.55rem;
    border-radius: 3px;
    font-size: 0.73rem;
    font-weight: 700;
    letter-spacing: 0.02em;
}
.dpill-green { background: var(--pale-green); color: var(--dark-green); }
.dpill-amber { background: #FEF3E7;           color: var(--amber); }
.dpill-red   { background: #FDECEA;           color: var(--red); }
.dpill-grey  { background: var(--light-gray); color: var(--mid-gray); }

/* ── Vehicle card expander ── */
.streamlit-expanderHeader {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-weight: 600 !important;
    color: var(--dark-gray) !important;
    font-size: 0.9rem !important;
}
.streamlit-expanderContent {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 4px 4px !important;
    padding: 0 !important;
}

/* ── Info labels / values ── */
.vcard-nickname   { font-size: 1.05rem; font-weight: 700; color: var(--black); }
.vcard-makemodel  { font-size: 0.8rem;  color: var(--mid-gray); margin-top: 0.1rem; }
.vcard-rego       { font-size: 0.72rem; color: var(--green); letter-spacing: 0.1em; margin-top: 0.2rem; font-weight: 700; }
.vcard-img        { width: 90px; height: 60px; object-fit: cover; border-radius: 4px; border: 1px solid var(--border); flex-shrink: 0; }

.section-title {
    font-size: 0.62rem;
    color: var(--green);
    text-transform: uppercase;
    letter-spacing: 0.14em;
    font-weight: 700;
    margin-bottom: 0.6rem;
    padding-bottom: 0.3rem;
    border-bottom: 2px solid var(--green);
    display: inline-block;
}
.info-label {
    font-size: 0.62rem;
    color: var(--mid-gray);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.12rem;
    font-weight: 600;
}
.info-value       { font-size: 0.86rem; color: var(--dark-gray); font-weight: 500; line-height: 1.35; }
.info-value-mono  { font-size: 0.84rem; color: var(--dark-gray); font-weight: 600; }
.info-value-phone { font-size: 0.84rem; color: var(--blue);      font-weight: 600; }

.odo-chip {
    display: inline-block;
    background: var(--pale-gray);
    border: 1px solid var(--border);
    border-radius: 3px;
    padding: 0.1rem 0.45rem;
    font-size: 0.7rem;
    color: var(--mid-gray);
    font-weight: 600;
}
.notes-bar {
    background: var(--pale-green);
    border-left: 3px solid var(--green);
    padding: 0.5rem 1rem;
    font-size: 0.82rem;
    color: var(--dark-gray);
    margin: 0.5rem 0 0;
}
.odlink {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    color: var(--green);
    font-size: 0.8rem;
    font-weight: 700;
    text-decoration: none;
    padding: 0.35rem 0.8rem;
    border: 1.5px solid var(--green);
    border-radius: 3px;
    background: var(--pale-green);
    margin: 0.6rem 0 0.4rem;
    letter-spacing: 0.03em;
}
.card-inner { padding: 1rem 1.2rem 0.9rem; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--white);
    border-radius: 4px;
    padding: 0;
    border: 1px solid var(--border);
    margin-bottom: 1rem;
    overflow: hidden;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0;
    color: var(--mid-gray);
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 0.55rem 1.2rem;
    border-right: 1px solid var(--border);
}
.stTabs [aria-selected="true"] {
    background: var(--green) !important;
    color: var(--white) !important;
}

/* ── Forms ── */
.stTextInput > div > input,
.stNumberInput > div > input,
.stSelectbox > div > div,
.stTextArea > div > textarea {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    color: var(--dark-gray) !important;
    border-radius: 4px !important;
    font-size: 0.88rem !important;
}
label[data-testid="stWidgetLabel"] {
    color: var(--dark-gray) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}
.stButton > button {
    border-radius: 4px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.03em !important;
}
.stButton > button[kind="primary"] {
    background: var(--green) !important;
    color: var(--white) !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--dark-green) !important;
}
.section-h {
    font-size: 0.65rem;
    color: var(--mid-gray);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    font-weight: 700;
    border-bottom: 2px solid var(--green);
    padding-bottom: 0.35rem;
    margin: 1.2rem 0 0.8rem;
    display: inline-block;
}
.form-section-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: var(--mid-gray);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    background: var(--pale-gray);
    padding: 0.3rem 0.6rem;
    border-left: 3px solid var(--green);
    margin: 1rem 0 0.5rem;
}
hr { border-color: var(--light-gray) !important; }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# DATA HELPERS
# ──────────────────────────────────────────────

COLS = [
    "Vehicle_ID","Nickname","Make","Model","Year","Rego",
    "Rego_Expiry","Insurance_Provider","Insurance_Phone",
    "Insurance_Expiry","Insurance_Excess","Named_Drivers",
    "Roadside_Provider","Roadside_Phone",
    "Last_Service_Date","Last_Service_By","Last_Service_Phone",
    "Next_Service_Due","Preferred_Centre","Preferred_Centre_Phone",
    "Odometer","Image_URL","OneDrive_Link","Notes","Status",
]
DATE_COLS = ["Rego_Expiry","Insurance_Expiry","Last_Service_Date","Next_Service_Due"]


def load_data():
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        for c in COLS:
            if c not in df.columns:
                df[c] = ""
        for col in DATE_COLS:
            df[col] = pd.to_datetime(df[col], format=DATE_FMT, errors="coerce")
        return df
    return pd.DataFrame(columns=COLS)


def save_data(df):
    out = df.copy()
    for col in DATE_COLS:
        out[col] = pd.to_datetime(out[col], errors="coerce").dt.strftime(DATE_FMT)
    out.to_csv(CSV_PATH, index=False)


def days_remaining(dt):
    if pd.isna(dt): return None
    return (pd.Timestamp(dt).date() - date.today()).days


def colour(days):
    if days is None: return "grey"
    if days <= RED_DAYS: return "red"
    if days <= AMBER_DAYS: return "amber"
    return "green"


def worst(rd, ins, svc):
    for c in ["red","amber","green","grey"]:
        if c in [colour(rd), colour(ins), colour(svc)]:
            return c
    return "grey"


def dpill(days, label=""):
    if days is None:
        return '<span class="dpill dpill-grey">—</span>'
    c = colour(days)
    t = f"{days}d" if days >= 0 else f"OVERDUE {abs(days)}d"
    return f'<span class="dpill dpill-{c}" title="{label}">{t}</span>'


def badge(status):
    icons  = {"red":"⚠","amber":"●","green":"✓","grey":"○"}
    labels = {"red":"URGENT","amber":"DUE SOON","green":"OK","grey":"UNKNOWN"}
    return f'<span class="badge badge-{status}">{icons[status]} {labels[status]}</span>'


def next_id(df):
    return 1 if df.empty else int(df["Vehicle_ID"].max()) + 1


def safe(val):
    return "" if pd.isna(val) else str(val)


def fmt(dt):
    return dt.strftime(DATE_FMT) if pd.notna(dt) else "—"


def dval(row, col):
    v = row[col]
    return v.date() if pd.notna(v) else date.today()


# ──────────────────────────────────────────────
# TOP BAR
# ──────────────────────────────────────────────

today_str = date.today().strftime("%A, %d %B %Y")
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:0.8rem">
    <span style="font-size:1.5rem">🚗</span>
    <div>
      <div class="topbar-title">MyFleet</div>
      <div class="topbar-sub">Family Vehicle Manager</div>
    </div>
  </div>
  <div class="topbar-date">{today_str}</div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LOAD + COMPUTE
# ──────────────────────────────────────────────

df = load_data()
active_df = df[df["Status"] == "Active"] if not df.empty else df

total = len(active_df)
n_urgent = n_soon = n_ok = 0
for _, r in active_df.iterrows():
    ws = worst(days_remaining(r["Rego_Expiry"]), days_remaining(r["Insurance_Expiry"]), days_remaining(r["Next_Service_Due"]))
    if ws == "red":     n_urgent += 1
    elif ws == "amber": n_soon += 1
    else:               n_ok += 1

# ──────────────────────────────────────────────
# METRIC STRIP
# ──────────────────────────────────────────────

st.markdown(f"""
<div class="metric-strip">
  <div class="metric-card mc-total">
    <div class="metric-num">{total}</div>
    <div class="metric-lbl">Active Vehicles</div>
  </div>
  <div class="metric-card mc-urgent">
    <div class="metric-num" style="color:#C0392B">{n_urgent}</div>
    <div class="metric-lbl">Urgent (&lt;7 days)</div>
  </div>
  <div class="metric-card mc-soon">
    <div class="metric-num" style="color:#D4750A">{n_soon}</div>
    <div class="metric-lbl">Due Soon (&lt;30 days)</div>
  </div>
  <div class="metric-card mc-ok">
    <div class="metric-num" style="color:#3C8F2A">{n_ok}</div>
    <div class="metric-lbl">All Clear</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# MAIN TABS
# ──────────────────────────────────────────────

tab1, tab2 = st.tabs(["📋  Fleet Dashboard", "⚙️  Admin Panel"])


# ══════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════

with tab1:
    if active_df.empty:
        st.info("No active vehicles. Add one via the Admin Panel.")
    else:
        def sort_key(row):
            ws = worst(days_remaining(row["Rego_Expiry"]), days_remaining(row["Insurance_Expiry"]), days_remaining(row["Next_Service_Due"]))
            return {"red":0,"amber":1,"green":2,"grey":3}[ws]

        sdf = active_df.copy()
        sdf["_s"] = sdf.apply(sort_key, axis=1)
        sdf = sdf.sort_values("_s").drop(columns=["_s"])

        for _, r in sdf.iterrows():
            rd   = days_remaining(r["Rego_Expiry"])
            insd = days_remaining(r["Insurance_Expiry"])
            svcd = days_remaining(r["Next_Service_Due"])
            ws   = worst(rd, insd, svcd)

            nickname  = safe(r["Nickname"]) or f"{r['Year']} {r['Make']} {r['Model']}"
            makemodel = f"{int(r['Year'])} {r['Make']} {r['Model']}"
            rego      = safe(r["Rego"])
            img_url   = safe(r["Image_URL"])
            onedrive  = safe(r["OneDrive_Link"])
            notes     = safe(r["Notes"])
            odo       = safe(r["Odometer"])

            left_border = {"red":"#C0392B","amber":"#D4750A","green":"#86BC25","grey":"#D0D0CE"}[ws]

            with st.expander(f"{nickname}  ·  {makemodel}  ·  {rego}", expanded=(ws in ["red","amber"])):

                img_tag = (
                    f'<img src="{img_url}" class="vcard-img" onerror="this.style.display=\'none\'">'
                    if img_url else
                    '<div style="width:90px;height:60px;border-radius:4px;border:1px solid #D0D0CE;background:#F5F5F5;display:flex;align-items:center;justify-content:center;font-size:1.8rem;flex-shrink:0">🚗</div>'
                )
                odo_tag = f'&nbsp;<span class="odo-chip">🔢 {int(float(odo)):,} km</span>' if odo else ""

                st.markdown(f"""
                <div class="card-inner" style="border-left:4px solid {left_border}">
                  <div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.9rem">
                    {img_tag}
                    <div style="flex:1">
                      <div class="vcard-nickname">{nickname}</div>
                      <div class="vcard-makemodel">{makemodel}</div>
                      <div class="vcard-rego">{rego}{odo_tag}</div>
                    </div>
                    <div>{badge(ws)}</div>
                  </div>
                  <hr style="margin:0 0 0.9rem">
                """, unsafe_allow_html=True)

                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown('<div class="section-title">📋 Registration</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Expires</div><div class="info-value-mono">{fmt(r["Rego_Expiry"])}</div><br>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Remaining</div>{dpill(rd,"Rego")}', unsafe_allow_html=True)
                    st.markdown('<br><div class="section-title">🛟 Roadside Assist</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Provider</div><div class="info-value">{safe(r["Roadside_Provider"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Phone</div><div class="info-value-phone">{safe(r["Roadside_Phone"]) or "—"}</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="section-title">🛡️ Insurance</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Provider</div><div class="info-value">{safe(r["Insurance_Provider"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Phone</div><div class="info-value-phone">{safe(r["Insurance_Phone"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Expires</div><div class="info-value-mono">{fmt(r["Insurance_Expiry"])}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Remaining</div>{dpill(insd,"Insurance")}', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Excess</div><div class="info-value">${safe(r["Insurance_Excess"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Named Drivers</div><div class="info-value">{safe(r["Named_Drivers"]) or "—"}</div>', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="section-title">🔧 Service</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Last Service</div><div class="info-value-mono">{fmt(r["Last_Service_Date"])}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Performed By</div><div class="info-value">{safe(r["Last_Service_By"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Phone</div><div class="info-value-phone">{safe(r["Last_Service_Phone"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Next Due</div><div class="info-value-mono">{fmt(r["Next_Service_Due"])}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Remaining</div>{dpill(svcd,"Service")}', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Preferred Centre</div><div class="info-value">{safe(r["Preferred_Centre"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Centre Phone</div><div class="info-value-phone">{safe(r["Preferred_Centre_Phone"]) or "—"}</div>', unsafe_allow_html=True)

                if notes:
                    st.markdown(f'<div class="notes-bar">📝 {notes}</div>', unsafe_allow_html=True)
                if onedrive and onedrive.startswith("http"):
                    st.markdown(f'<a href="{onedrive}" target="_blank" class="odlink">📁 Open OneDrive Documents</a>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════════════

with tab2:
    atab1, atab2, atab3 = st.tabs(["➕ Add Vehicle", "✏️ Update Vehicle", "🗑️ Retire Vehicle"])

    # ── ADD ──────────────────────────────────────
    with atab1:
        st.markdown('<div class="section-h">Add New Vehicle</div>', unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):

            st.markdown('<div class="form-section-label">Identity</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: nickname = st.text_input("Nickname", placeholder="Farm Ute")
            with c2: make     = st.text_input("Make", placeholder="Toyota")
            with c3: model    = st.text_input("Model", placeholder="Hilux")

            c4, c5, c6 = st.columns(3)
            with c4: year = st.number_input("Year", min_value=1990, max_value=date.today().year+1, value=date.today().year, step=1)
            with c5: rego = st.text_input("Rego Plate", placeholder="ABC123")
            with c6: odo  = st.number_input("Odometer (km)", min_value=0, value=0, step=100)

            st.markdown('<div class="form-section-label">Registration &amp; Insurance</div>', unsafe_allow_html=True)
            c7, c8 = st.columns(2)
            with c7: rego_exp = st.date_input("Rego Expiry", value=date.today(), format="DD/MM/YYYY")
            with c8: ins_exp  = st.date_input("Insurance Expiry", value=date.today(), format="DD/MM/YYYY")

            c9, c10, c11 = st.columns(3)
            with c9:  ins_prov  = st.text_input("Insurance Provider", placeholder="RACV")
            with c10: ins_phone = st.text_input("Insurer Phone", placeholder="13 72 28")
            with c11: ins_exc   = st.number_input("Excess ($)", min_value=0, value=0, step=50)

            named = st.text_input("Named Drivers", placeholder="John Smith / Jane Smith")

            st.markdown('<div class="form-section-label">Roadside Assistance</div>', unsafe_allow_html=True)
            c12, c13 = st.columns(2)
            with c12: road_prov  = st.text_input("Roadside Provider", placeholder="RACV")
            with c13: road_phone = st.text_input("Roadside Phone", placeholder="13 72 28")

            st.markdown('<div class="form-section-label">Service</div>', unsafe_allow_html=True)
            c14, c15 = st.columns(2)
            with c14: last_svc = st.date_input("Last Service Date", value=date.today(), format="DD/MM/YYYY")
            with c15: next_svc = st.date_input("Next Service Due", value=date.today(), format="DD/MM/YYYY")

            c16, c17 = st.columns(2)
            with c16: svc_by    = st.text_input("Performed By", placeholder="Toyota Doncaster")
            with c17: svc_phone = st.text_input("Service Centre Phone", placeholder="03 9842 1111")

            c18, c19 = st.columns(2)
            with c18: pref_centre = st.text_input("Preferred Centre", placeholder="Toyota Doncaster")
            with c19: pref_phone  = st.text_input("Preferred Centre Phone", placeholder="03 9842 1111")

            st.markdown('<div class="form-section-label">Other</div>', unsafe_allow_html=True)
            img_url = st.text_input("Vehicle Image URL (optional)", placeholder="https://...")
            od_url  = st.text_input("OneDrive Link (optional)", placeholder="https://onedrive.live.com/...")
            notes   = st.text_area("Notes", placeholder="e.g. Canopy + tow bar fitted.", height=70)

            if st.form_submit_button("✅ Add Vehicle", use_container_width=True, type="primary"):
                if not make or not model or not rego:
                    st.error("Make, Model, and Rego are required.")
                else:
                    new_row = {
                        "Vehicle_ID": next_id(df), "Nickname": nickname.strip(),
                        "Make": make.strip(), "Model": model.strip(),
                        "Year": int(year), "Rego": rego.strip().upper(),
                        "Rego_Expiry": pd.Timestamp(rego_exp),
                        "Insurance_Provider": ins_prov.strip(), "Insurance_Phone": ins_phone.strip(),
                        "Insurance_Expiry": pd.Timestamp(ins_exp),
                        "Insurance_Excess": int(ins_exc), "Named_Drivers": named.strip(),
                        "Roadside_Provider": road_prov.strip(), "Roadside_Phone": road_phone.strip(),
                        "Last_Service_Date": pd.Timestamp(last_svc),
                        "Last_Service_By": svc_by.strip(), "Last_Service_Phone": svc_phone.strip(),
                        "Next_Service_Due": pd.Timestamp(next_svc),
                        "Preferred_Centre": pref_centre.strip(), "Preferred_Centre_Phone": pref_phone.strip(),
                        "Odometer": int(odo), "Image_URL": img_url.strip(),
                        "OneDrive_Link": od_url.strip(), "Notes": notes.strip(), "Status": "Active",
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(df)
                    st.success(f"✅ {nickname or rego.upper()} added.")
                    st.rerun()

    # ── UPDATE ────────────────────────────────────
    with atab2:
        st.markdown('<div class="section-h">Update Vehicle</div>', unsafe_allow_html=True)
        if active_df.empty:
            st.info("No active vehicles.")
        else:
            opts = {f"{safe(r['Nickname']) or r['Make']}  —  {r['Rego']}": r["Vehicle_ID"] for _, r in active_df.iterrows()}
            sel_label = st.selectbox("Select Vehicle", list(opts.keys()))
            sel_id    = opts[sel_label]
            vr        = df[df["Vehicle_ID"] == sel_id].iloc[0]

            with st.form("update_form"):
                st.markdown('<div class="form-section-label">Identity</div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1: u_nick  = st.text_input("Nickname", value=safe(vr["Nickname"]))
                with c2: u_make  = st.text_input("Make", value=safe(vr["Make"]))
                with c3: u_model = st.text_input("Model", value=safe(vr["Model"]))

                c4, c5 = st.columns(2)
                with c4: u_rego = st.text_input("Rego", value=safe(vr["Rego"]))
                with c5:
                    odo_v = int(float(safe(vr["Odometer"]))) if safe(vr["Odometer"]) else 0
                    u_odo = st.number_input("Odometer (km)", min_value=0, value=odo_v, step=100)

                st.markdown('<div class="form-section-label">Registration &amp; Insurance</div>', unsafe_allow_html=True)
                c6, c7 = st.columns(2)
                with c6: u_rego_exp = st.date_input("Rego Expiry", value=dval(vr,"Rego_Expiry"), format="DD/MM/YYYY")
                with c7: u_ins_exp  = st.date_input("Insurance Expiry", value=dval(vr,"Insurance_Expiry"), format="DD/MM/YYYY")

                c8, c9, c10 = st.columns(3)
                with c8:  u_ins_prov  = st.text_input("Insurance Provider", value=safe(vr["Insurance_Provider"]))
                with c9:  u_ins_phone = st.text_input("Insurer Phone", value=safe(vr["Insurance_Phone"]))
                with c10:
                    exc_v = int(float(safe(vr["Insurance_Excess"]))) if safe(vr["Insurance_Excess"]) else 0
                    u_exc = st.number_input("Excess ($)", min_value=0, value=exc_v, step=50)

                u_named = st.text_input("Named Drivers", value=safe(vr["Named_Drivers"]))

                st.markdown('<div class="form-section-label">Roadside Assistance</div>', unsafe_allow_html=True)
                c11, c12 = st.columns(2)
                with c11: u_road_prov  = st.text_input("Roadside Provider", value=safe(vr["Roadside_Provider"]))
                with c12: u_road_phone = st.text_input("Roadside Phone", value=safe(vr["Roadside_Phone"]))

                st.markdown('<div class="form-section-label">Service</div>', unsafe_allow_html=True)
                c13, c14 = st.columns(2)
                with c13: u_last = st.date_input("Last Service Date", value=dval(vr,"Last_Service_Date"), format="DD/MM/YYYY")
                with c14: u_next = st.date_input("Next Service Due", value=dval(vr,"Next_Service_Due"), format="DD/MM/YYYY")

                c15, c16 = st.columns(2)
                with c15: u_svc_by    = st.text_input("Performed By", value=safe(vr["Last_Service_By"]))
                with c16: u_svc_phone = st.text_input("Service Phone", value=safe(vr["Last_Service_Phone"]))

                c17, c18 = st.columns(2)
                with c17: u_pref       = st.text_input("Preferred Centre", value=safe(vr["Preferred_Centre"]))
                with c18: u_pref_phone = st.text_input("Centre Phone", value=safe(vr["Preferred_Centre_Phone"]))

                st.markdown('<div class="form-section-label">Other</div>', unsafe_allow_html=True)
                u_img  = st.text_input("Vehicle Image URL", value=safe(vr["Image_URL"]))
                u_od   = st.text_input("OneDrive Link", value=safe(vr["OneDrive_Link"]))
                u_note = st.text_area("Notes", value=safe(vr["Notes"]), height=70)

                if st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary"):
                    updates = {
                        "Nickname": u_nick, "Make": u_make, "Model": u_model,
                        "Rego": u_rego.upper(), "Odometer": int(u_odo),
                        "Rego_Expiry": pd.Timestamp(u_rego_exp),
                        "Insurance_Provider": u_ins_prov, "Insurance_Phone": u_ins_phone,
                        "Insurance_Expiry": pd.Timestamp(u_ins_exp),
                        "Insurance_Excess": int(u_exc), "Named_Drivers": u_named,
                        "Roadside_Provider": u_road_prov, "Roadside_Phone": u_road_phone,
                        "Last_Service_Date": pd.Timestamp(u_last),
                        "Last_Service_By": u_svc_by, "Last_Service_Phone": u_svc_phone,
                        "Next_Service_Due": pd.Timestamp(u_next),
                        "Preferred_Centre": u_pref, "Preferred_Centre_Phone": u_pref_phone,
                        "Image_URL": u_img, "OneDrive_Link": u_od, "Notes": u_note,
                    }
                    for k, v in updates.items():
                        df.loc[df["Vehicle_ID"] == sel_id, k] = v
                    save_data(df)
                    st.success("✅ Saved.")
                    st.rerun()

    # ── RETIRE ────────────────────────────────────
    with atab3:
        st.markdown('<div class="section-h">Retire or Delete Vehicle</div>', unsafe_allow_html=True)
        if active_df.empty:
            st.info("No active vehicles.")
        else:
            r_opts  = {f"{safe(r['Nickname']) or r['Make']}  —  {r['Rego']}": r["Vehicle_ID"] for _, r in active_df.iterrows()}
            r_label = st.selectbox("Select Vehicle", list(r_opts.keys()), key="retire_sel")
            r_id    = r_opts[r_label]

            col1, col2 = st.columns(2)
            with col1:
                if st.button("🚫 Mark as Retired", use_container_width=True):
                    df.loc[df["Vehicle_ID"] == r_id, "Status"] = "Retired"
                    save_data(df)
                    st.success("Marked as Retired.")
                    st.rerun()
            with col2:
                if st.button("🗑️ Permanently Delete", use_container_width=True):
                    df = df[df["Vehicle_ID"] != r_id]
                    save_data(df)
                    st.success("Vehicle deleted.")
                    st.rerun()

        retired = df[df["Status"] == "Retired"] if not df.empty else pd.DataFrame()
        if not retired.empty:
            st.markdown('<div class="section-h" style="margin-top:1.5rem">Retired Vehicles</div>', unsafe_allow_html=True)
            for _, r in retired.iterrows():
                nick = safe(r["Nickname"]) or f"{r['Make']} {r['Model']}"
                st.markdown(
                    f'<span style="color:#53565A;font-size:0.82rem">▸ {nick} &nbsp;·&nbsp; {r["Rego"]}</span>',
                    unsafe_allow_html=True
                )
