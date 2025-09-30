import os
import requests
import streamlit as st

# ================== CONFIG ==================
API_BASE = os.getenv("CLAIM_API_BASE", "http://127.0.0.1:8000")

# ===== Your palette =====
BG_GRAD_1   = "#1b003a"   # deep purple-black
BG_GRAD_2   = "#0a001a"   # near-black navy
CARD_BG     = "#1e003a"   # dark violet
INPUT_BG    = "#2a004a"   # slightly lighter purple
BORDER_VIO  = "#4a007a"   # muted violet border

ACCENT_PRIMARY = "#8c52ff"                     # vivid electric violet
ACCENT_HOVER   = "#5a2aff"                     # deep neon purple
ACCENT_GLOW    = "rgba(140, 82, 255, 0.5)"     # glow

TEXT_PRIMARY   = "#ffffff"   # white
TEXT_SECONDARY = "#e0e0e0"   # light gray
TEXT_MUTED     = "#b0b0b0"   # soft gray

ERR  = "#ff4d4d"
OK   = "#00e676"
WARN = "#ffc107"
INFO = "#29b6f6"

st.set_page_config(page_title="Claim Validator", page_icon="💳", layout="wide")

# ================== THEME & CLEAN UI ==================
st.markdown(f"""
<style>
/* Hide Streamlit chrome (dots, header, footer) */
#MainMenu {{visibility: hidden;}}
header {{visibility: hidden;}}
footer {{visibility: hidden;}}
[data-testid="stToolbar"], [data-testid="stStatusWidget"], [data-testid="stDecoration"] {{display:none !important;}}

/* Page gradient */
html, body, [class^="css"] {{
  background: radial-gradient(1200px 800px at 20% -10%, {BG_GRAD_1} 0%, transparent 60%),
              radial-gradient(1200px 800px at 100% 0%, {BG_GRAD_1} 0%, transparent 60%),
              linear-gradient(180deg, {BG_GRAD_1} 0%, {BG_GRAD_2} 60%);
  color: {TEXT_PRIMARY};
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
}}
h1, h2, h3, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {{
  color: {TEXT_PRIMARY};
  letter-spacing: 0.2px;
}}

/* Cards */
.card {{
  background: {CARD_BG};
  border-radius: 18px;
  padding: 16px 18px;
  border: 1px solid {BORDER_VIO};
  box-shadow: 0 10px 30px rgba(0,0,0,.35);
}}

/* Pills / badges */
.badge {{
  display:inline-block; padding:6px 10px; border-radius:999px; font-weight:600; font-size:0.8rem;
  background: rgba(140,82,255,0.12); color:{ACCENT_PRIMARY}; border:1px solid {BORDER_VIO};
}}
.pill-success {{ background: rgba(0,230,118,0.12); color:{OK};   border:1px solid rgba(0,230,118,0.45);}}
.pill-warn    {{ background: rgba(255,193,7,0.12); color:{WARN}; border:1px solid rgba(255,193,7,0.45);}}
.pill-danger  {{ background: rgba(255,77,77,0.12); color:{ERR};  border:1px solid rgba(255,77,77,0.45);}}
.pill-neutral {{ background: rgba(140,82,255,0.12); color:{ACCENT_PRIMARY}; border:1px solid {BORDER_VIO};}}

/* Inputs (select, text, number) */
.stSelectbox > div > div, .stTextInput > div > div, .stNumberInput > div > div {{
  background:{INPUT_BG}; border:1px solid {BORDER_VIO}; border-radius:12px;
}}
.stSelectbox:hover > div > div, .stTextInput:hover > div > div, .stNumberInput:hover > div > div {{
  border-color:{ACCENT_PRIMARY};
}}
.stSelectbox:focus-within > div > div, .stTextInput:focus-within > div > div, .stNumberInput:focus-within > div > div {{
  box-shadow: 0 0 0 3px {ACCENT_GLOW};
  border-color:{ACCENT_PRIMARY};
}}
label, .small {{ color:{TEXT_MUTED}; }}
span, p, li {{ color:{TEXT_SECONDARY}; }}

/* Radio + Checkboxes – remove purple box */
.stRadio > div {{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 4px 0 !important;
}}
.stRadio label {{ color: {TEXT_SECONDARY} !important; font-weight:500; }}
.stRadio div[role="radiogroup"] {{ gap: 18px; }}
.stRadio input[type="radio"] {{ accent-color: {ACCENT_PRIMARY} !important; }}

.stCheckbox > div {{
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}}
.stCheckbox input[type="checkbox"] {{ accent-color: {ACCENT_PRIMARY} !important; }}

/* Buttons */
div.stButton > button:first-child {{
  background:{ACCENT_PRIMARY};
  color: {TEXT_PRIMARY};
  border: 1px solid {BORDER_VIO};
  border-radius: 14px;
  padding: 10px 18px;
  font-weight: 700;
}}
div.stButton > button:first-child:hover {{
  background:{ACCENT_HOVER};
  box-shadow: 0 0 0 4px {ACCENT_GLOW};
}}

/* Tables */
thead tr th {{ color:{TEXT_SECONDARY}; border-bottom:1px solid {BORDER_VIO}; }}
tbody tr td {{ color:{TEXT_PRIMARY}; border-bottom:1px solid rgba(255,255,255,0.06); }}
</style>
""", unsafe_allow_html=True)

# ================== API HELPERS ==================
def api_get(path, **params):
    r = requests.get(f"{API_BASE}{path}", params=params, timeout=15)
    if r.status_code >= 400:
        try: raise RuntimeError(r.json())
        except Exception: raise RuntimeError(r.text)
    return r.json()

def api_post(path, payload):
    r = requests.post(f"{API_BASE}{path}", json=payload, timeout=20)
    if r.status_code >= 400:
        try: raise RuntimeError(r.json())
        except Exception: raise RuntimeError(r.text)
    return r.json()

@st.cache_data(ttl=60)
def fetch_plans(): return api_get("/meta/plans")

@st.cache_data(ttl=60)
def fetch_packages_filtered(icd_code: str): return api_get("/meta/packages", icd_code=icd_code)

@st.cache_data(ttl=60)
def fetch_packages_all(): return api_get("/meta/packages")

# ================== HEADER ==================
st.markdown(f"""
<div class="card" style="margin-bottom: 12px; display:flex; align-items:center; justify-content:space-between;">
  <div>
    <h1 style="margin-bottom:6px;">💳 Claim Validator Dashboard</h1>
    <div class="small">Government-authorized HBP packages + synthetic plan rules</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ================== LAYOUT (logic unchanged) ==================
left, right = st.columns([0.52, 0.48])

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Claim Input")

    try:
        plans = fetch_plans()
        plan_display = [f'{p["plan_name"]} ({p["plan_id"]})' for p in plans]
        plan_names = [p["plan_name"] for p in plans]
        plan_choice = st.selectbox("Insurance Plan", plan_display, index=0 if plan_display else None, key="plan_sel")
        chosen_idx = plan_display.index(plan_choice) if plan_display else 0
        chosen_plan_name = plan_names[chosen_idx]
    except Exception as e:
        st.error(f"Failed to load plans: {e}")
        chosen_plan_name = ""

    member_id = st.text_input("Member ID", value="P001")
    icd_code  = st.text_input("ICD-10 Code", value="S52.5")

    mode = st.radio("HBP Package input mode",
                    ["Pick from list (filtered by ICD)", "Enter package_id manually"],
                    index=0, horizontal=True)

    pkg_id = None
    if mode.startswith("Pick"):
        packages, used_fallback = [], False
        try:
            icd = icd_code.strip()
            packages = fetch_packages_filtered(icd) if icd else fetch_packages_all()
        except Exception:
            used_fallback = True
            try: packages = fetch_packages_all()
            except Exception: packages = []

        options = ["— Select HBP package —"] + [
            f'{p["package_id"]} — {p["name"]}  (ICD {p["icd_code"]}, ₹{p["tariff"]})'
            for p in packages
        ]
        choice = st.selectbox("HBP Package", options=options, index=0, key="pkg_sel")
        if choice != "— Select HBP package —":
            pkg_id = packages[options.index(choice) - 1]["package_id"]

        if used_fallback: st.info("Filtered lookup failed; showing full package list instead.", icon="ℹ️")
        if not packages:  st.warning("No packages available. Check your HBP seed or try manual entry.", icon="⚠️")

    else:
        pkg_id = st.text_input("Enter HBP package_id (e.g., HBP006)", placeholder="HBP006").strip() or None

    admission_type = st.selectbox("Admission Type", ["inpatient", "elective", "emergency", "daycare"], index=0)
    length_days    = st.number_input("Length of Stay (days)", min_value=0, max_value=60, value=3)
    est_cost       = st.number_input("Estimated Cost (₹)", min_value=0, max_value=1000000, value=35000, step=5000)
    months_enrolled= st.number_input("Months Enrolled in Plan", min_value=0, max_value=120, value=12)

    run = st.button("Validate Claim")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Decision")

    if run and chosen_plan_name and pkg_id:
        payload = {
            "member_id": member_id.strip(),
            "plan_name": chosen_plan_name,
            "icd_code": icd_code.strip(),
            "package_id": pkg_id,
            "admission_type": admission_type,
            "length_days": int(length_days) if length_days else None,
            "estimated_cost_inr": int(est_cost) if est_cost else None,
            "months_enrolled": int(months_enrolled),
        }
        try:
            res = api_post("/validate_claim", payload)
            status = res["claim_status"]; score = res["claim_score"]
            expl   = res["explanation"];   amt   = res.get("approved_amount_inr")
            findings = res.get("findings", []); next_actions = res.get("next_actions", [])

            if status.startswith("✅"): pill = "pill-success"
            elif status.startswith("❌"): pill = "pill-danger"
            elif status.startswith("🟡"): pill = "pill-warn"
            else: pill = "pill-neutral"

            st.markdown(f"""
            <div class="card" style="background:{CARD_BG}; border:1px solid {BORDER_VIO}; margin-bottom:12px;">
              <div style="display:flex; align-items:center; gap:12px; justify-content:space-between;">
                <div class="badge {pill}" style="font-size:1rem;">{status}</div>
                <div class="badge">Score: {score}%</div>
              </div>
              <div style="margin-top:10px; color:{TEXT_PRIMARY}; font-size:1.05rem;">{expl}</div>
              <div class="small" style="margin-top:6px;">Plan: <b>{chosen_plan_name}</b> • Package: <b>{pkg_id}</b> • ICD: <b>{icd_code}</b></div>
            </div>
            """, unsafe_allow_html=True)

            if amt is not None:
                st.metric(label="Approved Amount (₹)", value=f"{amt:,}")

            if findings:
                st.markdown("#### Checks & Findings")
                st.table([{"Check": f["check"], "Result": f["result"], "Note": f.get("note")} for f in findings])

            if next_actions:
                st.markdown("#### Next Actions")
                for a in next_actions:
                    st.markdown(f"- {a}")

        except Exception:
            st.error("Validation failed. Please verify inputs and try again.", icon="❌")

    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    f"""<div class="small" style="opacity:0.8; margin-top:8px;">
      Uses HBP packages + synthetic plan rules (demo).
    </div>""",
    unsafe_allow_html=True
)
