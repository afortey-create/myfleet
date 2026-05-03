"""
MyFleet — Family Vehicle Fleet Manager
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
# CUSTOM CSS — clean utilitarian dark theme
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* App background */
    .stApp {
        background-color: #0f1117;
        color: #e8eaf0;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #171b26;
        border-right: 1px solid #2a2f3e;
    }

    /* Top header strip */
    .fleet-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #0f1117 100%);
        border-bottom: 2px solid #86BC25;
        padding: 1.2rem 1.5rem 1rem;
        margin: -1rem -1rem 1.5rem -1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .fleet-header h1 {
        font-family: 'DM Mono', monospace;
        font-size: 1.6rem;
        font-weight: 500;
        color: #ffffff;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .fleet-header .tagline {
        font-size: 0.78rem;
        color: #86BC25;
        font-family: 'DM Mono', monospace;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin: 0;
    }

    /* Vehicle card */
    .vehicle-card {
        background: #171b26;
        border: 1px solid #2a2f3e;
        border-radius: 10px;
        padding: 1.1rem 1.2rem;
        margin-bottom: 1rem;
        position: relative;
        transition: border-color 0.2s;
    }
    .vehicle-card:hover {
        border-color: #86BC25;
    }

    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.18rem 0.6rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'DM Mono', monospace;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .badge-green  { background: #1a3a1f; color: #4caf50; border: 1px solid #4caf50; }
    .badge-amber  { background: #3a2c00; color: #ffb300; border: 1px solid #ffb300; }
    .badge-red    { background: #3a0a0a; color: #ef5350; border: 1px solid #ef5350; }
    .badge-grey   { background: #2a2f3e; color: #9e9e9e; border: 1px solid #9e9e9e; }

    /* Field label/value pairs */
    .field-label {
        font-size: 0.68rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-family: 'DM Mono', monospace;
        margin-bottom: 0.1rem;
    }
    .field-value {
        font-size: 0.92rem;
        color: #e8eaf0;
        font-weight: 500;
    }
    .field-value-mono {
        font-size: 0.88rem;
        color: #e8eaf0;
        font-family: 'DM Mono', monospace;
    }

    /* Days remaining pill */
    .days-pill {
        font-family: 'DM Mono', monospace;
        font-size: 0.75rem;
        padding: 0.1rem 0.45rem;
        border-radius: 4px;
        display: inline-block;
    }
    .days-green { background: #1a3a1f; color: #4caf50; }
    .days-amber { background: #3a2c00; color: #ffb300; }
    .days-red   { background: #3a0a0a; color: #ef5350; }
    .days-grey  { background: #2a2f3e; color: #9e9e9e; }

    /* Vehicle name */
    .vehicle-name {
        font-size: 1.05rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }
    .vehicle-rego {
        font-family: 'DM Mono', monospace;
        font-size: 0.78rem;
        color: #86BC25;
        letter-spacing: 0.1em;
    }

    /* Section headings */
    .section-heading {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        color: #86BC25;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        border-bottom: 1px solid #2a2f3e;
        padding-bottom: 0.4rem;
        margin: 1.2rem 0 0.8rem;
    }

    /* Summary metric boxes */
    .metric-box {
        background: #171b26;
        border: 1px solid #2a2f3e;
        border-radius: 8px;
        padding: 0.9rem 1rem;
        text-align: center;
    }
    .metric-value {
        font-family: 'DM Mono', monospace;
        font-size: 2rem;
        font-weight: 500;
        line-height: 1;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }

    /* Input overrides */
    .stTextInput input, .stDateInput input, .stSelectbox select {
        background: #1e2333 !important;
        border: 1px solid #2a2f3e !important;
        color: #e8eaf0 !important;
        border-radius: 6px !important;
    }
    .stButton > button {
        border-radius: 6px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
    }

    /* Divider */
    hr { border-color: #2a2f3e !important; }

    /* Expander */
    .streamlit-expanderHeader {
        background: #171b26 !important;
        border: 1px solid #2a2f3e !important;
        border-radius: 8px !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: #171b26;
        border-radius: 8px;
        padding: 4px;
        border: 1px solid #2a2f3e;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        color: #9e9e9e;
        font-family: 'DM Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.04em;
    }
    .stTabs [aria-selected="true"] {
        background: #86BC25 !important;
        color: #000 !important;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────
# DATA HELPERS
# ──────────────────────────────────────────────

def load_data() -> pd.DataFrame:
    if os.path.exists(CSV_PATH):
        df = pd.read_csv(CSV_PATH)
        for col in ["Rego_Expiry", "Insurance_Expiry", "Last_Service_Date", "Next_Service_Due"]:
            df[col] = pd.to_datetime(df[col], format=DATE_FMT, errors="coerce")
        return df
    else:
        return pd.DataFrame(columns=[
            "Vehicle_ID", "Make", "Model", "Year", "Rego", "Rego_Expiry",
            "Insurance_Provider", "Insurance_Expiry", "Last_Service_Date",
            "Next_Service_Due", "OneDrive_Link", "Status",
        ])


def save_data(df: pd.DataFrame):
    out = df.copy()
    for col in ["Rego_Expiry", "Insurance_Expiry", "Last_Service_Date", "Next_Service_Due"]:
        out[col] = pd.to_datetime(out[col], errors="coerce").dt.strftime(DATE_FMT)
    out.to_csv(CSV_PATH, index=False)


def days_remaining(dt) -> int | None:
    if pd.isna(dt):
        return None
    delta = (pd.Timestamp(dt).date() - date.today()).days
    return delta


def status_colour(days: int | None) -> str:
    if days is None:
        return "grey"
    if days <= RED_DAYS:
        return "red"
    if days <= AMBER_DAYS:
        return "amber"
    return "green"


def worst_status(rego_days, ins_days, svc_days) -> str:
    colours = [status_colour(d) for d in [rego_days, ins_days, svc_days]]
    priority = ["red", "amber", "green", "grey"]
    for p in priority:
        if p in colours:
            return p
    return "grey"


def days_pill_html(days: int | None, label: str) -> str:
    if days is None:
        return f'<span class="days-pill days-grey">—</span>'
    colour = status_colour(days)
    cls = f"days-{colour}"
    text = f"{days}d" if days >= 0 else f"OVERDUE {abs(days)}d"
    return f'<span class="days-pill {cls}" title="{label}">{text}</span>'


def badge_html(status: str) -> str:
    labels = {"green": "OK", "amber": "SOON", "red": "URGENT", "grey": "UNKNOWN"}
    return f'<span class="status-badge badge-{status}">{labels.get(status, status.upper())}</span>'


def next_id(df: pd.DataFrame) -> int:
    if df.empty:
        return 1
    return int(df["Vehicle_ID"].max()) + 1


# ──────────────────────────────────────────────
# PAGE HEADER
# ──────────────────────────────────────────────

st.markdown(
    """
    <div class="fleet-header">
        <div>
            <h1>🚗 MyFleet</h1>
            <p class="tagline">Family Vehicle Manager</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Load data
df = load_data()
active_df = df[df["Status"] == "Active"] if not df.empty else df


# ──────────────────────────────────────────────
# SUMMARY METRICS
# ──────────────────────────────────────────────

total = len(active_df)
urgent = 0
soon = 0

for _, row in active_df.iterrows():
    rd = days_remaining(row["Rego_Expiry"])
    ins_d = days_remaining(row["Insurance_Expiry"])
    svc_d = days_remaining(row["Next_Service_Due"])
    ws = worst_status(rd, ins_d, svc_d)
    if ws == "red":
        urgent += 1
    elif ws == "amber":
        soon += 1

ok = total - urgent - soon

col1, col2, col3, col4 = st.columns(4)
metrics = [
    (str(total), "Active Vehicles", "#86BC25"),
    (str(urgent), "Urgent (< 7 days)", "#ef5350"),
    (str(soon), "Due Soon (< 30 days)", "#ffb300"),
    (str(ok), "All Clear", "#4caf50"),
]
for col, (val, label, colour) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-value" style="color:{colour}">{val}</div>
                <div class="metric-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<br>", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# TABS
# ──────────────────────────────────────────────

tab1, tab2 = st.tabs(["📋  Fleet Dashboard", "⚙️  Admin Panel"])


# ══════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ══════════════════════════════════════════════

with tab1:
    if active_df.empty:
        st.info("No active vehicles. Add one in the Admin Panel.")
    else:
        # Sort by worst status first
        def sort_key(row):
            rd = days_remaining(row["Rego_Expiry"])
            ins_d = days_remaining(row["Insurance_Expiry"])
            svc_d = days_remaining(row["Next_Service_Due"])
            ws = worst_status(rd, ins_d, svc_d)
            return {"red": 0, "amber": 1, "green": 2, "grey": 3}[ws]

        sorted_df = active_df.copy()
        sorted_df["_sort"] = sorted_df.apply(sort_key, axis=1)
        sorted_df = sorted_df.sort_values("_sort").drop(columns=["_sort"])

        for _, row in sorted_df.iterrows():
            rd = days_remaining(row["Rego_Expiry"])
            ins_d = days_remaining(row["Insurance_Expiry"])
            svc_d = days_remaining(row["Next_Service_Due"])
            ws = worst_status(rd, ins_d, svc_d)

            rego_exp = row["Rego_Expiry"].strftime(DATE_FMT) if pd.notna(row["Rego_Expiry"]) else "—"
            ins_exp = row["Insurance_Expiry"].strftime(DATE_FMT) if pd.notna(row["Insurance_Expiry"]) else "—"
            last_svc = row["Last_Service_Date"].strftime(DATE_FMT) if pd.notna(row["Last_Service_Date"]) else "—"
            next_svc = row["Next_Service_Due"].strftime(DATE_FMT) if pd.notna(row["Next_Service_Due"]) else "—"
            link = row["OneDrive_Link"] if pd.notna(row["OneDrive_Link"]) and str(row["OneDrive_Link"]).startswith("http") else None

            border_colours = {"red": "#ef5350", "amber": "#ffb300", "green": "#4caf50", "grey": "#2a2f3e"}
            border = border_colours[ws]

            with st.expander(
                f"{row['Year']} {row['Make']} {row['Model']}  —  {row['Rego']}",
                expanded=(ws in ["red", "amber"]),
            ):
                # Header row
                c_name, c_badge = st.columns([3, 1])
                with c_name:
                    st.markdown(
                        f"""
                        <div class="vehicle-name">{row['Year']} {row['Make']} {row['Model']}</div>
                        <div class="vehicle-rego">{row['Rego']}</div>
                        """,
                        unsafe_allow_html=True,
                    )
                with c_badge:
                    st.markdown(badge_html(ws), unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)

                # Three columns: Rego | Insurance | Service
                c1, c2, c3 = st.columns(3)

                with c1:
                    st.markdown('<div class="section-heading">Registration</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Expires</div><div class="field-value-mono">{rego_exp}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Remaining</div>{days_pill_html(rd, "Rego")}', unsafe_allow_html=True)

                with c2:
                    st.markdown('<div class="section-heading">Insurance</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Provider</div><div class="field-value">{row["Insurance_Provider"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Expires</div><div class="field-value-mono">{ins_exp}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Remaining</div>{days_pill_html(ins_d, "Insurance")}', unsafe_allow_html=True)

                with c3:
                    st.markdown('<div class="section-heading">Service</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Last Service</div><div class="field-value-mono">{last_svc}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Next Due</div><div class="field-value-mono">{next_svc}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="field-label">Remaining</div>{days_pill_html(svc_d, "Service")}', unsafe_allow_html=True)

                if link:
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f'📁 &nbsp;<a href="{link}" target="_blank" style="color:#86BC25;font-family:\'DM Mono\',monospace;font-size:0.82rem;">Open OneDrive Documents</a>', unsafe_allow_html=True)

            st.markdown(f"<style>.streamlit-expanderHeader{{border-left: 3px solid {border} !important;}}</style>", unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 2 — ADMIN PANEL
# ══════════════════════════════════════════════

with tab2:
    admin_tab1, admin_tab2, admin_tab3 = st.tabs(["➕ Add Vehicle", "✏️ Update Service", "🗑️ Retire Vehicle"])


    # ── ADD VEHICLE ──────────────────────────────
    with admin_tab1:
        st.markdown('<div class="section-heading">Add New Vehicle</div>', unsafe_allow_html=True)

        with st.form("add_vehicle_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                make = st.text_input("Make", placeholder="Toyota")
                model = st.text_input("Model", placeholder="Hilux")
                year = st.number_input("Year", min_value=1990, max_value=date.today().year + 1, value=date.today().year, step=1)
                rego = st.text_input("Rego Plate", placeholder="ABC123")
            with c2:
                rego_expiry = st.date_input("Rego Expiry", value=date.today(), format="DD/MM/YYYY")
                insurance_provider = st.text_input("Insurance Provider", placeholder="RACV")
                insurance_expiry = st.date_input("Insurance Expiry", value=date.today(), format="DD/MM/YYYY")

            c3, c4 = st.columns(2)
            with c3:
                last_service = st.date_input("Last Service Date", value=date.today(), format="DD/MM/YYYY")
            with c4:
                next_service = st.date_input("Next Service Due", value=date.today(), format="DD/MM/YYYY")

            onedrive_link = st.text_input("OneDrive Link (optional)", placeholder="https://onedrive.live.com/...")

            submitted = st.form_submit_button("✅ Add Vehicle", use_container_width=True, type="primary")

            if submitted:
                if not make or not model or not rego:
                    st.error("Make, Model, and Rego are required.")
                else:
                    new_row = {
                        "Vehicle_ID": next_id(df),
                        "Make": make.strip(),
                        "Model": model.strip(),
                        "Year": int(year),
                        "Rego": rego.strip().upper(),
                        "Rego_Expiry": pd.Timestamp(rego_expiry),
                        "Insurance_Provider": insurance_provider.strip(),
                        "Insurance_Expiry": pd.Timestamp(insurance_expiry),
                        "Last_Service_Date": pd.Timestamp(last_service),
                        "Next_Service_Due": pd.Timestamp(next_service),
                        "OneDrive_Link": onedrive_link.strip() if onedrive_link else "",
                        "Status": "Active",
                    }
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    save_data(df)
                    st.success(f"✅ {year} {make} {model} ({rego.upper()}) added.")
                    st.rerun()


    # ── UPDATE SERVICE ───────────────────────────
    with admin_tab2:
        st.markdown('<div class="section-heading">Update Service History</div>', unsafe_allow_html=True)

        if active_df.empty:
            st.info("No active vehicles to update.")
        else:
            vehicle_options = {
                f"{int(row['Year'])} {row['Make']} {row['Model']} ({row['Rego']})": row["Vehicle_ID"]
                for _, row in active_df.iterrows()
            }
            selected_label = st.selectbox("Select Vehicle", list(vehicle_options.keys()))
            selected_id = vehicle_options[selected_label]

            vehicle_row = df[df["Vehicle_ID"] == selected_id].iloc[0]

            with st.form("update_service_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_last_service = st.date_input(
                        "Last Service Date",
                        value=vehicle_row["Last_Service_Date"].date() if pd.notna(vehicle_row["Last_Service_Date"]) else date.today(),
                        format="DD/MM/YYYY",
                    )
                with c2:
                    new_next_service = st.date_input(
                        "Next Service Due",
                        value=vehicle_row["Next_Service_Due"].date() if pd.notna(vehicle_row["Next_Service_Due"]) else date.today(),
                        format="DD/MM/YYYY",
                    )

                new_rego_expiry = st.date_input(
                    "Rego Expiry",
                    value=vehicle_row["Rego_Expiry"].date() if pd.notna(vehicle_row["Rego_Expiry"]) else date.today(),
                    format="DD/MM/YYYY",
                )
                new_ins_expiry = st.date_input(
                    "Insurance Expiry",
                    value=vehicle_row["Insurance_Expiry"].date() if pd.notna(vehicle_row["Insurance_Expiry"]) else date.today(),
                    format="DD/MM/YYYY",
                )
                new_ins_provider = st.text_input("Insurance Provider", value=str(vehicle_row["Insurance_Provider"]))
                new_onedrive = st.text_input("OneDrive Link", value=str(vehicle_row["OneDrive_Link"]) if pd.notna(vehicle_row["OneDrive_Link"]) else "")

                update_submitted = st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary")

                if update_submitted:
                    df.loc[df["Vehicle_ID"] == selected_id, "Last_Service_Date"] = pd.Timestamp(new_last_service)
                    df.loc[df["Vehicle_ID"] == selected_id, "Next_Service_Due"] = pd.Timestamp(new_next_service)
                    df.loc[df["Vehicle_ID"] == selected_id, "Rego_Expiry"] = pd.Timestamp(new_rego_expiry)
                    df.loc[df["Vehicle_ID"] == selected_id, "Insurance_Expiry"] = pd.Timestamp(new_ins_expiry)
                    df.loc[df["Vehicle_ID"] == selected_id, "Insurance_Provider"] = new_ins_provider.strip()
                    df.loc[df["Vehicle_ID"] == selected_id, "OneDrive_Link"] = new_onedrive.strip()
                    save_data(df)
                    st.success("✅ Vehicle updated.")
                    st.rerun()


    # ── RETIRE VEHICLE ───────────────────────────
    with admin_tab3:
        st.markdown('<div class="section-heading">Retire or Delete Vehicle</div>', unsafe_allow_html=True)

        if active_df.empty:
            st.info("No active vehicles.")
        else:
            retire_options = {
                f"{int(row['Year'])} {row['Make']} {row['Model']} ({row['Rego']})": row["Vehicle_ID"]
                for _, row in active_df.iterrows()
            }
            retire_label = st.selectbox("Select Vehicle to Retire", list(retire_options.keys()), key="retire_select")
            retire_id = retire_options[retire_label]

            col_r, col_d = st.columns(2)

            with col_r:
                if st.button("🚫 Mark as Retired", use_container_width=True):
                    df.loc[df["Vehicle_ID"] == retire_id, "Status"] = "Retired"
                    save_data(df)
                    st.success(f"Vehicle marked as Retired.")
                    st.rerun()

            with col_d:
                if st.button("🗑️ Permanently Delete", use_container_width=True, type="secondary"):
                    df = df[df["Vehicle_ID"] != retire_id]
                    save_data(df)
                    st.success("Vehicle permanently deleted.")
                    st.rerun()

            # Show retired vehicles
            retired_df = df[df["Status"] == "Retired"]
            if not retired_df.empty:
                st.markdown('<div class="section-heading">Retired Vehicles</div>', unsafe_allow_html=True)
                for _, row in retired_df.iterrows():
                    st.markdown(
                        f'<span style="color:#6b7280;font-family:\'DM Mono\',monospace;font-size:0.82rem;">▸ {int(row["Year"])} {row["Make"]} {row["Model"]} — {row["Rego"]}</span>',
                        unsafe_allow_html=True,
                    )
