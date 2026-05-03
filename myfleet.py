"""
MyFleet v4 — Family Vehicle Fleet Manager
Mobile-first | Deloitte light theme | vehicles.csv backend
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
# CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --white:      #FFFFFF;
    --black:      #000000;
    --dark:       #222222;
    --mid:        #53565A;
    --light:      #E6E6E6;
    --pale:       #F5F5F5;
    --green:      #86BC25;
    --dkgreen:    #3C8F2A;
    --palegreen:  #F1F6E4;
    --border:     #D0D0CE;
    --red:        #C0392B;
    --palered:    #FDECEA;
    --amber:      #D4750A;
    --paleamber:  #FEF3E7;
    --blue:       #005587;
}

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--pale);
    color: var(--dark);
}
.stApp { background: var(--pale); }
#MainMenu, footer, header { visibility: hidden; }

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.8rem 1.2rem;
    margin: -1rem -1rem 0 -1rem;
    background: var(--black);
    border-bottom: 4px solid var(--green);
}
.topbar-title { font-size: 1.3rem; font-weight: 700; color: var(--white); letter-spacing: -0.02em; }
.topbar-sub   { font-size: 0.6rem; color: var(--green); font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.15rem; }
.topbar-date  { font-size: 0.7rem; color: #BBBCBC; }

/* ── Metric strip ── */
.metric-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.6rem;
    margin: 1rem 0 1.1rem;
}
@media (max-width: 480px) {
    .metric-strip { grid-template-columns: repeat(2, 1fr); }
}
.metric-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-top: 3px solid var(--border);
    border-radius: 4px;
    padding: 0.75rem 0.9rem 0.65rem;
}
.mc-total  { border-top-color: var(--green); }
.mc-urgent { border-top-color: var(--red); }
.mc-soon   { border-top-color: var(--amber); }
.mc-ok     { border-top-color: var(--dkgreen); }
.metric-num { font-size: 2rem; font-weight: 700; line-height: 1; color: var(--dark); }
.metric-lbl { font-size: 0.62rem; color: var(--mid); text-transform: uppercase; letter-spacing: 0.07em; margin-top: 0.2rem; font-weight: 600; }

/* ── Vehicle card ── */
.vcard {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: 6px;
    margin-bottom: 0.8rem;
    overflow: hidden;
}

/* Card header */
.vcard-header {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.85rem 1rem;
    border-bottom: 1px solid var(--light);
    cursor: pointer;
}
.vcard-img {
    width: 72px; height: 50px;
    object-fit: cover;
    border-radius: 4px;
    border: 1px solid var(--border);
    flex-shrink: 0;
    background: var(--pale);
}
.vcard-img-ph {
    width: 72px; height: 50px;
    border-radius: 4px;
    border: 1px solid var(--border);
    background: var(--pale);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem; flex-shrink: 0;
}
.vcard-nick { font-size: 0.95rem; font-weight: 700; color: var(--black); }
.vcard-sub  { font-size: 0.75rem; color: var(--mid); margin-top: 0.1rem; }
.vcard-rego { font-size: 0.7rem; color: var(--green); font-weight: 700; letter-spacing: 0.08em; margin-top: 0.15rem; }

/* Status badge */
.badge {
    display: inline-flex; align-items: center; gap: 0.25rem;
    padding: 0.18rem 0.5rem; border-radius: 3px;
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 0.07em; text-transform: uppercase;
    white-space: nowrap;
}
.badge-red   { background: var(--palered);   color: var(--red);    border: 1px solid #E8B4B0; }
.badge-amber { background: var(--paleamber); color: var(--amber);  border: 1px solid #F5CFA0; }
.badge-green { background: var(--palegreen); color: var(--dkgreen);border: 1px solid #BDD98A; }
.badge-grey  { background: var(--light);     color: var(--mid);    border: 1px solid var(--border); }

/* Days pill */
.dpill {
    display: inline-block; padding: 0.1rem 0.45rem;
    border-radius: 3px; font-size: 0.7rem; font-weight: 700;
}
.dpill-green { background: var(--palegreen); color: var(--dkgreen); }
.dpill-amber { background: var(--paleamber); color: var(--amber); }
.dpill-red   { background: var(--palered);   color: var(--red); }
.dpill-grey  { background: var(--light);     color: var(--mid); }

/* Odo chip */
.odo { display: inline-block; background: var(--pale); border: 1px solid var(--border); border-radius: 3px; padding: 0.08rem 0.4rem; font-size: 0.68rem; color: var(--mid); font-weight: 600; white-space: nowrap; margin-top: 0.15rem; }

/* Info grid — 3 cols desktop, hidden on mobile (replaced by summary strip) */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0;
}
.info-section {
    padding: 0.85rem 1rem;
    border-right: 1px solid var(--light);
    border-bottom: 1px solid var(--light);
}
.info-section:last-child { border-right: none; }

/* Mobile summary strip — 3 status pills in a row */
.mobile-summary {
    display: none;
    padding: 0.6rem 0.9rem;
    gap: 0.5rem;
    border-top: 1px solid var(--light);
    flex-wrap: wrap;
}
.ms-item { display: flex; flex-direction: column; flex: 1; min-width: 80px; }
.ms-label { font-size: 0.56rem; color: var(--mid); text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; margin-bottom: 0.2rem; }

/* CSS-only expand toggle */
.detail-toggle { display: none; }
.detail-label {
    display: none;
    width: 100%;
    text-align: center;
    padding: 0.45rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: var(--green);
    border-top: 1px solid var(--light);
    cursor: pointer;
    letter-spacing: 0.04em;
    background: var(--pale);
    user-select: none;
}
.detail-label:hover { background: var(--palegreen); }
.detail-content { display: block; }

@media (max-width: 600px) {
    .info-grid { grid-template-columns: 1fr; display: none; }
    .info-section { border-right: none; }
    .mobile-summary { display: flex; }
    .detail-label { display: block; }
    .detail-toggle:checked ~ .detail-label { color: var(--mid); }
    .detail-toggle:checked ~ .detail-label::before { content: "▲ Hide detail"; }
    .detail-label::before { content: "▼ Show full detail"; }
    .detail-toggle:checked ~ .detail-content .info-grid { display: grid; grid-template-columns: 1fr; }
    .detail-content { display: none; }
    .detail-toggle:checked ~ .detail-content { display: block; }
}

.sec-title {
    font-size: 0.58rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.13em; color: var(--green);
    border-bottom: 2px solid var(--green);
    padding-bottom: 0.25rem; margin-bottom: 0.6rem;
    display: inline-block;
}
.f-label { font-size: 0.6rem; color: var(--mid); text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600; margin-top: 0.45rem; margin-bottom: 0.08rem; }
.f-label:first-child { margin-top: 0; }
.f-val   { font-size: 0.84rem; color: var(--dark); font-weight: 500; }
.f-mono  { font-size: 0.84rem; color: var(--dark); font-weight: 600; }
.f-phone { font-size: 0.84rem; color: var(--blue); font-weight: 600; }

/* Notes + link */
.notes-bar {
    background: var(--palegreen); border-left: 3px solid var(--green);
    padding: 0.5rem 1rem; font-size: 0.8rem; color: var(--dark);
    border-top: 1px solid var(--light);
}
.od-link {
    display: inline-flex; align-items: center; gap: 0.35rem;
    color: var(--green); font-size: 0.78rem; font-weight: 700;
    text-decoration: none; padding: 0.35rem 0.8rem;
    border: 1.5px solid var(--green); border-radius: 3px;
    background: var(--palegreen); margin: 0.7rem 1rem;
    letter-spacing: 0.02em;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: var(--white); border-radius: 4px;
    padding: 0; border: 1px solid var(--border); margin-bottom: 1rem; overflow: hidden;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 0; color: var(--mid); font-size: 0.82rem; font-weight: 600;
    letter-spacing: 0.03em; padding: 0.55rem 1.1rem;
    border-right: 1px solid var(--border);
}
.stTabs [aria-selected="true"] { background: var(--green) !important; color: var(--white) !important; }

/* ── Forms ── */
.stTextInput>div>input,
.stNumberInput>div>input,
.stSelectbox>div>div,
.stTextArea>div>textarea {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    color: var(--dark) !important;
    border-radius: 4px !important;
    font-size: 0.88rem !important;
}
label[data-testid="stWidgetLabel"] { color: var(--dark) !important; font-weight: 600 !important; font-size: 0.82rem !important; }
.stButton>button { border-radius: 4px !important; font-weight: 600 !important; font-size: 0.85rem !important; }
.stButton>button[kind="primary"] { background: var(--green) !important; color: var(--white) !important; border: none !important; }
.stButton>button[kind="primary"]:hover { background: var(--dkgreen) !important; }

.section-h {
    font-size: 0.62rem; color: var(--mid); text-transform: uppercase;
    letter-spacing: 0.12em; font-weight: 700;
    border-bottom: 2px solid var(--green); padding-bottom: 0.3rem;
    margin: 1.2rem 0 0.8rem; display: inline-block;
}
.form-sec {
    font-size: 0.68rem; font-weight: 700; color: var(--mid);
    text-transform: uppercase; letter-spacing: 0.1em;
    background: var(--pale); padding: 0.28rem 0.6rem;
    border-left: 3px solid var(--green); margin: 1rem 0 0.5rem;
}
hr { border-color: var(--light) !important; }

.streamlit-expanderHeader { display: none !important; }
.streamlit-expanderContent {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
}
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


def dpill_html(days, label=""):
    if days is None: return '<span class="dpill dpill-grey">—</span>'
    c = colour(days)
    t = f"{days}d" if days >= 0 else f"OVERDUE {abs(days)}d"
    return f'<span class="dpill dpill-{c}">{t}</span>'


def badge_html(ws):
    icons  = {"red":"⚠","amber":"●","green":"✓","grey":"○"}
    labels = {"red":"URGENT","amber":"DUE SOON","green":"OK","grey":"UNKNOWN"}
    return f'<span class="badge badge-{ws}">{icons[ws]} {labels[ws]}</span>'


def next_id(df):
    return 1 if df.empty else int(df["Vehicle_ID"].max()) + 1


def s(val):
    return "" if pd.isna(val) else str(val)


def fmt(dt):
    return dt.strftime(DATE_FMT) if pd.notna(dt) else "—"


def dval(row, col):
    v = row[col]
    return v.date() if pd.notna(v) else date.today()


def row(label, value, cls="f-val"):
    return f'<div class="f-label">{label}</div><div class="{cls}">{value or "—"}</div>'


# ──────────────────────────────────────────────
# TOP BAR
# ──────────────────────────────────────────────

today_str = date.today().strftime("%d %b %Y")
st.markdown(f"""
<div class="topbar">
  <div style="display:flex;align-items:center;gap:0.7rem">
    <span style="font-size:1.4rem">🚗</span>
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
    <div class="metric-lbl">Urgent &lt;7d</div>
  </div>
  <div class="metric-card mc-soon">
    <div class="metric-num" style="color:#D4750A">{n_soon}</div>
    <div class="metric-lbl">Due Soon &lt;30d</div>
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
# DASHBOARD — pure HTML cards, no st.columns
# ══════════════════════════════════════════════

with tab1:
    if active_df.empty:
        st.info("No active vehicles. Add one via the Admin Panel.")
    else:
        def sort_key(r):
            ws = worst(days_remaining(r["Rego_Expiry"]), days_remaining(r["Insurance_Expiry"]), days_remaining(r["Next_Service_Due"]))
            return {"red":0,"amber":1,"green":2,"grey":3}[ws]

        sdf = active_df.copy()
        sdf["_s"] = sdf.apply(sort_key, axis=1)
        sdf = sdf.sort_values("_s").drop(columns=["_s"])

        for _, r in sdf.iterrows():
            rd   = days_remaining(r["Rego_Expiry"])
            insd = days_remaining(r["Insurance_Expiry"])
            svcd = days_remaining(r["Next_Service_Due"])
            ws   = worst(rd, insd, svcd)

            nickname  = s(r["Nickname"]) or f"{r['Year']} {r['Make']} {r['Model']}"
            makemodel = f"{int(r['Year'])} {r['Make']} {r['Model']}"
            rego      = s(r["Rego"])
            img_url   = s(r["Image_URL"])
            onedrive  = s(r["OneDrive_Link"])
            notes     = s(r["Notes"])
            odo       = s(r["Odometer"])

            left_col = {"red":"#C0392B","amber":"#D4750A","green":"#86BC25","grey":"#D0D0CE"}[ws]

            # Image tag — use a reliable placeholder if no URL
            if img_url:
                img_tag = f'<img src="{img_url}" class="vcard-img" onerror="this.outerHTML=\'<div class=vcard-img-ph>🚗</div>\'">'
            else:
                img_tag = '<div class="vcard-img-ph">🚗</div>'

            odo_tag = f'<div><span class="odo">🔢 {int(float(odo)):,} km</span></div>' if odo else ""

            notes_html = f'<div class="notes-bar">📝 {notes}</div>' if notes else ""
            link_html  = f'<div><a href="{onedrive}" target="_blank" class="od-link">📁 Open OneDrive Documents</a></div>' if onedrive and onedrive.startswith("http") else ""

            uid = s(r["Vehicle_ID"])
            card_html = f"""
<div class="vcard" style="border-left: 4px solid {left_col}">

  <div class="vcard-header">
    {img_tag}
    <div style="flex:1;min-width:0">
      <div class="vcard-nick">{nickname}</div>
      <div class="vcard-sub">{makemodel}</div>
      <div class="vcard-rego">{rego}</div>
      {odo_tag}
    </div>
    <div style="flex-shrink:0">{badge_html(ws)}</div>
  </div>

  <div class="mobile-summary">
    <div class="ms-item">
      <div class="ms-label">Rego</div>
      {dpill_html(rd)}
      <div style="font-size:0.72rem;color:var(--mid);margin-top:0.15rem">{fmt(r["Rego_Expiry"])}</div>
    </div>
    <div class="ms-item">
      <div class="ms-label">Insurance</div>
      {dpill_html(insd)}
      <div style="font-size:0.72rem;color:var(--mid);margin-top:0.15rem">{fmt(r["Insurance_Expiry"])}</div>
    </div>
    <div class="ms-item">
      <div class="ms-label">Service</div>
      {dpill_html(svcd)}
      <div style="font-size:0.72rem;color:var(--mid);margin-top:0.15rem">{fmt(r["Next_Service_Due"])}</div>
    </div>
  </div>

  <input type="checkbox" class="detail-toggle" id="tog_{uid}">
  <label class="detail-label" for="tog_{uid}"></label>
  <div class="detail-content">
    <div class="info-grid">
      <div class="info-section">
        <div class="sec-title">Registration</div>
        {row("Expires", fmt(r["Rego_Expiry"]), "f-mono")}
        <div class="f-label">Remaining</div>{dpill_html(rd)}
        <div style="margin-top:0.9rem"></div>
        <div class="sec-title">Roadside Assist</div>
        {row("Provider", s(r["Roadside_Provider"]))}
        {row("Phone", s(r["Roadside_Phone"]), "f-phone")}
      </div>
      <div class="info-section">
        <div class="sec-title">Insurance</div>
        {row("Provider", s(r["Insurance_Provider"]))}
        {row("Phone", s(r["Insurance_Phone"]), "f-phone")}
        {row("Expires", fmt(r["Insurance_Expiry"]), "f-mono")}
        <div class="f-label">Remaining</div>{dpill_html(insd)}
        {row("Excess", "$" + s(r["Insurance_Excess"]) if s(r["Insurance_Excess"]) else "—")}
        {row("Named Drivers", s(r["Named_Drivers"]))}
      </div>
      <div class="info-section">
        <div class="sec-title">Service</div>
        {row("Last Service", fmt(r["Last_Service_Date"]), "f-mono")}
        {row("Performed By", s(r["Last_Service_By"]))}
        {row("Phone", s(r["Last_Service_Phone"]), "f-phone")}
        {row("Next Due", fmt(r["Next_Service_Due"]), "f-mono")}
        <div class="f-label">Remaining</div>{dpill_html(svcd)}
        {row("Preferred Centre", s(r["Preferred_Centre"]))}
        {row("Centre Phone", s(r["Preferred_Centre_Phone"]), "f-phone")}
      </div>
    </div>
    {notes_html}
    {link_html}
  </div>

</div>
"""
            st.markdown(card_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════════════

with tab2:
    atab1, atab2, atab3 = st.tabs(["➕ Add Vehicle", "✏️ Update Vehicle", "🗑️ Retire Vehicle"])

    # ── ADD ──────────────────────────────────────
    with atab1:
        st.markdown('<div class="section-h">Add New Vehicle</div>', unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):

            st.markdown('<div class="form-sec">Identity</div>', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            with c1: nickname = st.text_input("Nickname", placeholder="Farm Ute")
            with c2: make     = st.text_input("Make", placeholder="Toyota")
            with c3: model    = st.text_input("Model", placeholder="Hilux")

            c4, c5, c6 = st.columns(3)
            with c4: year = st.number_input("Year", min_value=1990, max_value=date.today().year+1, value=date.today().year, step=1)
            with c5: rego = st.text_input("Rego Plate", placeholder="ABC123")
            with c6: odo  = st.number_input("Odometer (km)", min_value=0, value=0, step=100)

            st.markdown('<div class="form-sec">Registration &amp; Insurance</div>', unsafe_allow_html=True)
            c7, c8 = st.columns(2)
            with c7: rego_exp = st.date_input("Rego Expiry", value=date.today(), format="DD/MM/YYYY")
            with c8: ins_exp  = st.date_input("Insurance Expiry", value=date.today(), format="DD/MM/YYYY")

            c9, c10, c11 = st.columns(3)
            with c9:  ins_prov  = st.text_input("Insurance Provider", placeholder="RACV")
            with c10: ins_phone = st.text_input("Insurer Phone", placeholder="13 72 28")
            with c11: ins_exc   = st.number_input("Excess ($)", min_value=0, value=0, step=50)

            named = st.text_input("Named Drivers", placeholder="John Smith / Jane Smith")

            st.markdown('<div class="form-sec">Roadside Assistance</div>', unsafe_allow_html=True)
            c12, c13 = st.columns(2)
            with c12: road_prov  = st.text_input("Roadside Provider", placeholder="RACV")
            with c13: road_phone = st.text_input("Roadside Phone", placeholder="13 72 28")

            st.markdown('<div class="form-sec">Service</div>', unsafe_allow_html=True)
            c14, c15 = st.columns(2)
            with c14: last_svc = st.date_input("Last Service Date", value=date.today(), format="DD/MM/YYYY")
            with c15: next_svc = st.date_input("Next Service Due", value=date.today(), format="DD/MM/YYYY")

            c16, c17 = st.columns(2)
            with c16: svc_by    = st.text_input("Performed By", placeholder="Toyota Doncaster")
            with c17: svc_phone = st.text_input("Service Centre Phone", placeholder="03 9842 1111")

            c18, c19 = st.columns(2)
            with c18: pref_centre = st.text_input("Preferred Centre", placeholder="Toyota Doncaster")
            with c19: pref_phone  = st.text_input("Preferred Centre Phone", placeholder="03 9842 1111")

            st.markdown('<div class="form-sec">Other</div>', unsafe_allow_html=True)
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
            opts = {f"{s(r['Nickname']) or r['Make']}  —  {r['Rego']}": r["Vehicle_ID"] for _, r in active_df.iterrows()}
            sel_label = st.selectbox("Select Vehicle", list(opts.keys()))
            sel_id    = opts[sel_label]
            vr        = df[df["Vehicle_ID"] == sel_id].iloc[0]

            with st.form("update_form"):
                st.markdown('<div class="form-sec">Identity</div>', unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                with c1: u_nick  = st.text_input("Nickname", value=s(vr["Nickname"]))
                with c2: u_make  = st.text_input("Make", value=s(vr["Make"]))
                with c3: u_model = st.text_input("Model", value=s(vr["Model"]))

                c4, c5 = st.columns(2)
                with c4: u_rego = st.text_input("Rego", value=s(vr["Rego"]))
                with c5:
                    odo_v = int(float(s(vr["Odometer"]))) if s(vr["Odometer"]) else 0
                    u_odo = st.number_input("Odometer (km)", min_value=0, value=odo_v, step=100)

                st.markdown('<div class="form-sec">Registration &amp; Insurance</div>', unsafe_allow_html=True)
                c6, c7 = st.columns(2)
                with c6: u_rego_exp = st.date_input("Rego Expiry", value=dval(vr,"Rego_Expiry"), format="DD/MM/YYYY")
                with c7: u_ins_exp  = st.date_input("Insurance Expiry", value=dval(vr,"Insurance_Expiry"), format="DD/MM/YYYY")

                c8, c9, c10 = st.columns(3)
                with c8:  u_ins_prov  = st.text_input("Insurance Provider", value=s(vr["Insurance_Provider"]))
                with c9:  u_ins_phone = st.text_input("Insurer Phone", value=s(vr["Insurance_Phone"]))
                with c10:
                    exc_v = int(float(s(vr["Insurance_Excess"]))) if s(vr["Insurance_Excess"]) else 0
                    u_exc = st.number_input("Excess ($)", min_value=0, value=exc_v, step=50)

                u_named = st.text_input("Named Drivers", value=s(vr["Named_Drivers"]))

                st.markdown('<div class="form-sec">Roadside Assistance</div>', unsafe_allow_html=True)
                c11, c12 = st.columns(2)
                with c11: u_road_prov  = st.text_input("Roadside Provider", value=s(vr["Roadside_Provider"]))
                with c12: u_road_phone = st.text_input("Roadside Phone", value=s(vr["Roadside_Phone"]))

                st.markdown('<div class="form-sec">Service</div>', unsafe_allow_html=True)
                c13, c14 = st.columns(2)
                with c13: u_last = st.date_input("Last Service Date", value=dval(vr,"Last_Service_Date"), format="DD/MM/YYYY")
                with c14: u_next = st.date_input("Next Service Due", value=dval(vr,"Next_Service_Due"), format="DD/MM/YYYY")

                c15, c16 = st.columns(2)
                with c15: u_svc_by    = st.text_input("Performed By", value=s(vr["Last_Service_By"]))
                with c16: u_svc_phone = st.text_input("Service Phone", value=s(vr["Last_Service_Phone"]))

                c17, c18 = st.columns(2)
                with c17: u_pref       = st.text_input("Preferred Centre", value=s(vr["Preferred_Centre"]))
                with c18: u_pref_phone = st.text_input("Centre Phone", value=s(vr["Preferred_Centre_Phone"]))

                st.markdown('<div class="form-sec">Other</div>', unsafe_allow_html=True)
                u_img  = st.text_input("Vehicle Image URL", value=s(vr["Image_URL"]))
                u_od   = st.text_input("OneDrive Link", value=s(vr["OneDrive_Link"]))
                u_note = st.text_area("Notes", value=s(vr["Notes"]), height=70)

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
            r_opts  = {f"{s(r['Nickname']) or r['Make']}  —  {r['Rego']}": r["Vehicle_ID"] for _, r in active_df.iterrows()}
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
                nick = s(r["Nickname"]) or f"{r['Make']} {r['Model']}"
                st.markdown(f'<span style="color:#53565A;font-size:0.82rem">▸ {nick} &nbsp;·&nbsp; {r["Rego"]}</span>', unsafe_allow_html=True)
