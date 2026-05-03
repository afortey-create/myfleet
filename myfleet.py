"""
MyFleet v2 — Family Vehicle Fleet Manager
Streamlit application | vehicles.csv backend
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
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
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --bg:       #0c0f1a;
    --surface:  #131729;
    --surface2: #1a2038;
    --border:   #232b45;
    --border2:  #2d3a5c;
    --text:     #e4e8f5;
    --muted:    #6b7599;
    --accent:   #86BC25;
    --accent2:  #5a8a12;
    --red:      #ff4d4d;
    --amber:    #ffaa00;
    --green:    #3ddc84;
    --blue:     #4d9fff;
}

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    background-color: var(--bg);
    color: var(--text);
}

.stApp { background: var(--bg); }
[data-testid="stSidebar"] { background: var(--surface); border-right: 1px solid var(--border); }
#MainMenu, footer, header { visibility: hidden; }

/* TOP BAR */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 1.5rem 0.9rem;
    margin: -1rem -1rem 0 -1rem;
    background: linear-gradient(90deg,#0c0f1a 0%,#131729 60%,#0c0f1a 100%);
    border-bottom: 1px solid var(--border);
    position: relative;
    overflow: hidden;
}
.topbar::before {
    content:'';
    position:absolute;top:0;left:0;right:0;height:2px;
    background:linear-gradient(90deg,transparent,var(--accent),transparent);
}
.topbar-title {
    font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:800;
    color:#fff;letter-spacing:-0.03em;line-height:1;
}
.topbar-sub {
    font-size:0.65rem;color:var(--accent);font-weight:600;
    letter-spacing:0.14em;text-transform:uppercase;
}
.topbar-date { font-size:0.72rem;color:var(--muted);letter-spacing:0.04em; }

/* METRIC STRIP */
.metric-strip {
    display:grid;grid-template-columns:repeat(4,1fr);
    gap:0.75rem;margin:1.2rem 0 1.4rem;
}
.metric-card {
    background:var(--surface);border:1px solid var(--border);
    border-radius:10px;padding:0.9rem 1rem 0.8rem;text-align:center;
    position:relative;overflow:hidden;
}
.metric-card::after {
    content:'';position:absolute;bottom:0;left:0;right:0;height:2px;
}
.mc-total::after  { background:var(--accent); }
.mc-urgent::after { background:var(--red); }
.mc-soon::after   { background:var(--amber); }
.mc-ok::after     { background:var(--green); }
.metric-num {
    font-family:'Syne',sans-serif;font-size:2.2rem;
    font-weight:700;line-height:1;
}
.metric-lbl {
    font-size:0.65rem;color:var(--muted);text-transform:uppercase;
    letter-spacing:0.1em;margin-top:0.25rem;font-weight:500;
}

/* BADGE */
.badge {
    display:inline-flex;align-items:center;gap:0.25rem;
    padding:0.2rem 0.55rem;border-radius:20px;font-size:0.65rem;
    font-weight:700;letter-spacing:0.08em;text-transform:uppercase;
}
.badge-red   { background:rgba(255,77,77,0.12);   color:var(--red);   border:1px solid rgba(255,77,77,0.3); }
.badge-amber { background:rgba(255,170,0,0.12);   color:var(--amber); border:1px solid rgba(255,170,0,0.3); }
.badge-green { background:rgba(61,220,132,0.1);   color:var(--green); border:1px solid rgba(61,220,132,0.3); }
.badge-grey  { background:rgba(107,117,153,0.15); color:var(--muted); border:1px solid rgba(107,117,153,0.3); }

/* DAY PILL */
.dpill {
    display:inline-block;padding:0.12rem 0.5rem;border-radius:5px;
    font-size:0.72rem;font-weight:600;letter-spacing:0.03em;
}
.dpill-green { background:rgba(61,220,132,0.1);   color:var(--green); }
.dpill-amber { background:rgba(255,170,0,0.12);   color:var(--amber); }
.dpill-red   { background:rgba(255,77,77,0.12);   color:var(--red); }
.dpill-grey  { background:rgba(107,117,153,0.15); color:var(--muted); }

/* INFO GRID */
.info-section-title {
    font-size:0.62rem;color:var(--accent);text-transform:uppercase;
    letter-spacing:0.14em;font-weight:700;margin-bottom:0.65rem;
    font-family:'Syne',sans-serif;
}
.info-label {
    font-size:0.6rem;color:var(--muted);text-transform:uppercase;
    letter-spacing:0.09em;margin-bottom:0.15rem;font-weight:500;
}
.info-value      { font-size:0.85rem;color:var(--text);font-weight:500;line-height:1.3; }
.info-value-mono { font-size:0.82rem;color:var(--text);font-weight:500;letter-spacing:0.02em; }
.info-value-phone{ font-size:0.82rem;color:var(--blue);font-weight:500; }

/* MISC */
.vcard-nickname   { font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:#fff; }
.vcard-makemodel  { font-size:0.8rem;color:var(--muted);margin-top:0.1rem; }
.vcard-rego       { font-size:0.72rem;color:var(--accent);letter-spacing:0.1em;margin-top:0.2rem;font-weight:600; }
.vcard-img        { width:90px;height:60px;object-fit:cover;border-radius:8px;border:1px solid var(--border2);flex-shrink:0;background:var(--surface2); }
.odo-chip         { display:inline-block;background:var(--surface2);border:1px solid var(--border2);border-radius:6px;padding:0.12rem 0.5rem;font-size:0.72rem;color:var(--muted); }
.notes-bar        { background:rgba(134,188,37,0.07);border-left:3px solid var(--accent);padding:0.5rem 1rem;font-size:0.8rem;color:var(--muted);font-style:italic; }
.odlink           { display:inline-flex;align-items:center;gap:0.4rem;color:var(--accent);font-size:0.78rem;font-weight:600;text-decoration:none;padding:0.4rem 0.85rem;border:1px solid var(--accent2);border-radius:6px;background:rgba(134,188,37,0.07);margin:0.7rem 0 0.5rem; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap:3px;background:var(--surface);border-radius:10px;
    padding:4px;border:1px solid var(--border);margin-bottom:1rem;
}
.stTabs [data-baseweb="tab"] {
    border-radius:7px;color:var(--muted);font-family:'Syne',sans-serif;
    font-size:0.78rem;font-weight:600;letter-spacing:0.04em;padding:0.4rem 1rem;
}
.stTabs [aria-selected="true"] { background:var(--accent) !important;color:#000 !important; }

/* FORMS */
.stTextInput>div>input,
.stNumberInput>div>input,
.stSelectbox>div>div,
.stTextArea>div>textarea {
    background:var(--surface2) !important;
    border:1px solid var(--border2) !important;
    color:var(--text) !important;border-radius:8px !important;
}
.stButton>button { font-family:'Syne',sans-serif !important;font-weight:600 !important;border-radius:8px !important; }
.stButton>button[kind="primary"] { background:var(--accent) !important;color:#000 !important;border:none !important; }
.section-h {
    font-family:'Syne',sans-serif;font-size:0.65rem;color:var(--accent);
    text-transform:uppercase;letter-spacing:0.14em;font-weight:700;
    border-bottom:1px solid var(--border);padding-bottom:0.4rem;margin:1rem 0 0.7rem;
}
hr { border-color:var(--border) !important; }
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
    if pd.isna(dt):
        return None
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
    t = f"{days}d" if days >= 0 else f"⚠ OVERDUE {abs(days)}d"
    return f'<span class="dpill dpill-{c}" title="{label}">{t}</span>'


def badge(status):
    icons  = {"red":"●","amber":"●","green":"●","grey":"○"}
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
# LOAD DATA + COMPUTE
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
    <div class="metric-num" style="color:#86BC25">{total}</div>
    <div class="metric-lbl">Active Vehicles</div>
  </div>
  <div class="metric-card mc-urgent">
    <div class="metric-num" style="color:#ff4d4d">{n_urgent}</div>
    <div class="metric-lbl">Urgent (&lt;7 days)</div>
  </div>
  <div class="metric-card mc-soon">
    <div class="metric-num" style="color:#ffaa00">{n_soon}</div>
    <div class="metric-lbl">Due Soon (&lt;30 days)</div>
  </div>
  <div class="metric-card mc-ok">
    <div class="metric-num" style="color:#3ddc84">{n_ok}</div>
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

            border_col = {"red":"#ff4d4d","amber":"#ffaa00","green":"#3ddc84","grey":"#232b45"}[ws]

            with st.expander(f"{nickname}  ·  {makemodel}  ·  {rego}", expanded=(ws in ["red","amber"])):

                # Header
                img_tag = f'<img src="{img_url}" class="vcard-img" onerror="this.style.display=\'none\'">' if img_url else '<div style="width:90px;height:60px;border-radius:8px;border:1px solid #2d3a5c;background:#1a2038;display:flex;align-items:center;justify-content:center;font-size:1.6rem;flex-shrink:0">🚗</div>'
                odo_tag = f'&nbsp;<span class="odo-chip">🔢 {int(float(odo)):,} km</span>' if odo else ""

                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:1rem;padding:0.4rem 0 0.9rem">
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

                # Three columns
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown('<div class="info-section-title">📋 Registration</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Expires</div><div class="info-value-mono">{fmt(r["Rego_Expiry"])}</div><br>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Remaining</div>{dpill(rd,"Rego")}', unsafe_allow_html=True)

                    st.markdown('<br><div class="info-section-title">🛟 Roadside Assist</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Provider</div><div class="info-value">{safe(r["Roadside_Provider"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Phone</div><div class="info-value-phone">{safe(r["Roadside_Phone"]) or "—"}</div>', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="info-section-title">🛡️ Insurance</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Provider</div><div class="info-value">{safe(r["Insurance_Provider"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Phone</div><div class="info-value-phone">{safe(r["Insurance_Phone"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Expires</div><div class="info-value-mono">{fmt(r["Insurance_Expiry"])}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Remaining</div>{dpill(insd,"Insurance")}', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Excess</div><div class="info-value">${safe(r["Insurance_Excess"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Named Drivers</div><div class="info-value">{safe(r["Named_Drivers"]) or "—"}</div>', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="info-section-title">🔧 Service</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Last Service</div><div class="info-value-mono">{fmt(r["Last_Service_Date"])}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Performed By</div><div class="info-value">{safe(r["Last_Service_By"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Phone</div><div class="info-value-phone">{safe(r["Last_Service_Phone"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Next Due</div><div class="info-value-mono">{fmt(r["Next_Service_Due"])}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Remaining</div>{dpill(svcd,"Service")}', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Preferred Centre</div><div class="info-value">{safe(r["Preferred_Centre"]) or "—"}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="info-label">Centre Phone</div><div class="info-value-phone">{safe(r["Preferred_Centre_Phone"]) or "—"}</div>', unsafe_allow_html=True)

                # Notes + link
                if notes:
                    st.markdown(f'<div class="notes-bar">📝 {notes}</div>', unsafe_allow_html=True)
                if onedrive and onedrive.startswith("http"):
                    st.markdown(f'<a href="{onedrive}" target="_blank" class="odlink">📁 Open OneDrive Documents</a>', unsafe_allow_html=True)

            st.markdown(f"<style>.streamlit-expanderHeader{{border-left:3px solid {border_col} !important}}</style>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════════════

with tab2:
    atab1, atab2, atab3 = st.tabs(["➕ Add Vehicle", "✏️ Update Vehicle", "🗑️ Retire Vehicle"])

    # ── ADD ──────────────────────────────────────
    with atab1:
        st.markdown('<div class="section-h">Add New Vehicle</div>', unsafe_allow_html=True)
        with st.form("add_form", clear_on_submit=True):

            st.markdown("**Identity**")
            c1, c2, c3 = st.columns(3)
            with c1: nickname = st.text_input("Nickname", placeholder="Farm Ute")
            with c2: make     = st.text_input("Make", placeholder="Toyota")
            with c3: model    = st.text_input("Model", placeholder="Hilux")

            c4, c5, c6 = st.columns(3)
            with c4: year = st.number_input("Year", min_value=1990, max_value=date.today().year+1, value=date.today().year, step=1)
            with c5: rego = st.text_input("Rego Plate", placeholder="ABC123")
            with c6: odo  = st.number_input("Odometer (km)", min_value=0, value=0, step=100)

            st.markdown("**Registration & Insurance**")
            c7, c8 = st.columns(2)
            with c7: rego_exp = st.date_input("Rego Expiry", value=date.today(), format="DD/MM/YYYY")
            with c8: ins_exp  = st.date_input("Insurance Expiry", value=date.today(), format="DD/MM/YYYY")

            c9, c10, c11 = st.columns(3)
            with c9:  ins_prov  = st.text_input("Insurance Provider", placeholder="RACV")
            with c10: ins_phone = st.text_input("Insurer Phone", placeholder="13 72 28")
            with c11: ins_exc   = st.number_input("Excess ($)", min_value=0, value=0, step=50)

            named = st.text_input("Named Drivers", placeholder="John Smith / Jane Smith")

            st.markdown("**Roadside Assistance**")
            c12, c13 = st.columns(2)
            with c12: road_prov  = st.text_input("Roadside Provider", placeholder="RACV")
            with c13: road_phone = st.text_input("Roadside Phone", placeholder="13 72 28")

            st.markdown("**Service**")
            c14, c15 = st.columns(2)
            with c14: last_svc = st.date_input("Last Service Date", value=date.today(), format="DD/MM/YYYY")
            with c15: next_svc = st.date_input("Next Service Due", value=date.today(), format="DD/MM/YYYY")

            c16, c17 = st.columns(2)
            with c16: svc_by    = st.text_input("Performed By", placeholder="Toyota Doncaster")
            with c17: svc_phone = st.text_input("Service Centre Phone", placeholder="03 9842 1111")

            c18, c19 = st.columns(2)
            with c18: pref_centre = st.text_input("Preferred Centre", placeholder="Toyota Doncaster")
            with c19: pref_phone  = st.text_input("Preferred Centre Phone", placeholder="03 9842 1111")

            st.markdown("**Other**")
            img_url  = st.text_input("Vehicle Image URL (optional)", placeholder="https://...")
            od_url   = st.text_input("OneDrive Link (optional)", placeholder="https://onedrive.live.com/...")
            notes    = st.text_area("Notes", placeholder="e.g. Canopy + tow bar fitted.", height=70)

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
                st.markdown("**Identity**")
                c1, c2, c3 = st.columns(3)
                with c1: u_nick  = st.text_input("Nickname", value=safe(vr["Nickname"]))
                with c2: u_make  = st.text_input("Make", value=safe(vr["Make"]))
                with c3: u_model = st.text_input("Model", value=safe(vr["Model"]))

                c4, c5 = st.columns(2)
                with c4: u_rego = st.text_input("Rego", value=safe(vr["Rego"]))
                with c5:
                    odo_v = int(float(safe(vr["Odometer"]))) if safe(vr["Odometer"]) else 0
                    u_odo = st.number_input("Odometer (km)", min_value=0, value=odo_v, step=100)

                st.markdown("**Registration & Insurance**")
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

                st.markdown("**Roadside Assistance**")
                c11, c12 = st.columns(2)
                with c11: u_road_prov  = st.text_input("Roadside Provider", value=safe(vr["Roadside_Provider"]))
                with c12: u_road_phone = st.text_input("Roadside Phone", value=safe(vr["Roadside_Phone"]))

                st.markdown("**Service**")
                c13, c14 = st.columns(2)
                with c13: u_last = st.date_input("Last Service Date", value=dval(vr,"Last_Service_Date"), format="DD/MM/YYYY")
                with c14: u_next = st.date_input("Next Service Due", value=dval(vr,"Next_Service_Due"), format="DD/MM/YYYY")

                c15, c16 = st.columns(2)
                with c15: u_svc_by    = st.text_input("Performed By", value=safe(vr["Last_Service_By"]))
                with c16: u_svc_phone = st.text_input("Service Phone", value=safe(vr["Last_Service_Phone"]))

                c17, c18 = st.columns(2)
                with c17: u_pref       = st.text_input("Preferred Centre", value=safe(vr["Preferred_Centre"]))
                with c18: u_pref_phone = st.text_input("Centre Phone", value=safe(vr["Preferred_Centre_Phone"]))

                st.markdown("**Other**")
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
                st.markdown(f'<span style="color:#6b7599;font-size:0.82rem">▸ {nick} &nbsp;·&nbsp; {r["Rego"]}</span>', unsafe_allow_html=True)
