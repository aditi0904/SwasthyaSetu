# main.py
import os
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, String, Integer, Boolean, Column, ForeignKey, text
from sqlalchemy.orm import declarative_base, Session, relationship
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# --- boot ---
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./swasthyasetu.db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
Base = declarative_base()

# --- ORM models (must match Neon tables) ---
class HBP(Base):
    __tablename__ = "hbp_packages"
    package_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    icd_code = Column(String, nullable=False)
    base_tariff_inr = Column(Integer, nullable=False)
    preauth_required = Column(Boolean, default=False)
    length_of_stay_days = Column(Integer)
    notes = Column(String)

class Plan(Base):
    __tablename__ = "plans"
    plan_id = Column(String, primary_key=True)
    plan_name = Column(String, nullable=False, unique=True)
    tier = Column(String)
    base_copay_percent = Column(Integer, nullable=False)

class Coverage(Base):
    __tablename__ = "plan_coverage"
    plan_id = Column(String, ForeignKey("plans.plan_id"), primary_key=True)
    package_id = Column(String, ForeignKey("hbp_packages.package_id"), primary_key=True)
    covered = Column(Boolean, nullable=False)
    copay_percent = Column(Integer)
    sublimit_inr = Column(Integer)
    waiting_months = Column(Integer, default=0)
    preauth_override = Column(Boolean, default=False)
    room_cap = Column(String)
    notes = Column(String)
    plan = relationship("Plan")
    pkg = relationship("HBP")

# --- Initialize database ---
def init_database():
    """Create tables and seed data if they don't exist"""
    Base.metadata.create_all(engine)
    
    with Session(engine) as db:
        # Check if data exists
        existing = db.query(Plan).count()
        if existing > 0:
            return  # Already initialized
        
        # Seed data
        packages = [
            HBP(package_id="PKG001", name="Fracture of Lower End of Radius Treatment",
                icd_code="S52.5", base_tariff_inr=25000, preauth_required=False,
                length_of_stay_days=3, notes="Standard orthopedic care"),
            HBP(package_id="PKG002", name="Type 2 Diabetes Management",
                icd_code="E11", base_tariff_inr=15000, preauth_required=True,
                length_of_stay_days=5, notes="Includes medication and monitoring"),
            HBP(package_id="PKG003", name="Hypertension Treatment",
                icd_code="I10", base_tariff_inr=12000, preauth_required=False,
                length_of_stay_days=2, notes="Basic cardiovascular care"),
        ]
        
        plans = [
            Plan(plan_id="PLAN_BASIC", plan_name="Basic Plan", tier="Bronze", base_copay_percent=20),
            Plan(plan_id="PLAN_STANDARD", plan_name="Standard Plan", tier="Silver", base_copay_percent=15),
            Plan(plan_id="PLAN_PREMIUM", plan_name="Premium Plan", tier="Gold", base_copay_percent=10),
        ]
        
        coverages = [
            Coverage(plan_id="PLAN_BASIC", package_id="PKG001", covered=True, copay_percent=20,
                    sublimit_inr=20000, waiting_months=3, room_cap="Shared"),
            Coverage(plan_id="PLAN_BASIC", package_id="PKG002", covered=False),
            Coverage(plan_id="PLAN_STANDARD", package_id="PKG001", covered=True, copay_percent=15,
                    sublimit_inr=25000, waiting_months=1, room_cap="Semi-private"),
            Coverage(plan_id="PLAN_STANDARD", package_id="PKG002", covered=True, copay_percent=15,
                    waiting_months=6, preauth_override=True, room_cap="Semi-private"),
            Coverage(plan_id="PLAN_PREMIUM", package_id="PKG001", covered=True, copay_percent=10,
                    waiting_months=0, room_cap="Private"),
            Coverage(plan_id="PLAN_PREMIUM", package_id="PKG002", covered=True, copay_percent=10,
                    waiting_months=0, room_cap="Private"),
            Coverage(plan_id="PLAN_PREMIUM", package_id="PKG003", covered=True, copay_percent=10,
                    waiting_months=0, room_cap="Private"),
        ]
        
        db.add_all(packages + plans + coverages)
        db.commit()

# Initialize on module import
init_database()

# --- API models ---
class ClaimIn(BaseModel):
    member_id: str
    plan_name: str
    icd_code: str
    package_id: str
    admission_type: str
    length_days: Optional[int] = None
    estimated_cost_inr: Optional[int] = None
    months_enrolled: int = 12

class Finding(BaseModel):
    check: str
    result: str
    note: Optional[str] = None

class DecisionOut(BaseModel):
    claim_status: str
    claim_score: float
    explanation: str
    findings: List[Finding]
    approved_amount_inr: Optional[int] = None
    next_actions: List[str] = []

# --- app ---
app = FastAPI(title="Claim Validator (Neon + HBP + Synthetic Plans)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- utilities ----------
def score(findings: List[Finding]) -> float:
    scored = [f for f in findings if f.result in ("PASS", "FAIL", "REQUIRED")]
    if not scored:
        return 100.0
    passed = sum(1 for f in scored if f.result == "PASS")
    base = round(100.0 * passed / len(scored), 2)
    has_sublimit = any(f.check == "sublimit" and f.result == "APPLIED" for f in findings)
    has_copay = any(f.check == "copay" for f in findings)
    penalty = (5 if has_copay else 0) + (10 if has_sublimit else 0)
    return max(0.0, round(base - penalty, 2))

def resolve_plan(db: Session, plan_name_input: str) -> Optional[Plan]:
    s = plan_name_input.strip()
    plan = db.query(Plan).filter(Plan.plan_id == s).one_or_none()
    if plan:
        return plan
    plan = db.query(Plan).filter(Plan.plan_name.ilike(s)).one_or_none()
    return plan

# ---------- basic meta/health ----------
@app.get("/health")
def health():
    with Session(engine) as db:
        db.execute(text("SELECT 1"))
    return {"ok": True}

@app.get("/meta/plans")
def list_plans():
    with Session(engine) as db:
        rows = db.query(Plan.plan_id, Plan.plan_name, Plan.tier, Plan.base_copay_percent).all()
        return [
            {"plan_id": r[0], "plan_name": r[1], "tier": r[2], "base_copay_percent": r[3]}
            for r in rows
        ]

@app.get("/meta/packages")
def list_packages(icd_code: Optional[str] = None, limit: int = 100):
    with Session(engine) as db:
        q = db.query(HBP.package_id, HBP.name, HBP.icd_code, HBP.base_tariff_inr)
        if icd_code:
            q = q.filter(HBP.icd_code == icd_code)
        rows = q.order_by(HBP.package_id).limit(limit).all()
        return [
            {"package_id": r[0], "name": r[1], "icd_code": r[2], "tariff": r[3]}
            for r in rows
        ]

# ---------- main endpoint ----------
@app.post("/validate_claim", response_model=DecisionOut)
def validate_claim(claim: ClaimIn):
    findings: List[Finding] = []

    with Session(engine) as db:
        pkg = db.get(HBP, claim.package_id)
        if not pkg:
            raise HTTPException(
                status_code=404,
                detail={"error": "Unknown package_id", "package_id": claim.package_id,
                        "hint": "Check /meta/packages or verify your HBP seed"}
            )

        if pkg.icd_code != claim.icd_code:
            findings.append(Finding(check="pkg_icd_match", result="FAIL",
                                     note=f"Package maps to ICD {pkg.icd_code}, not {claim.icd_code}"))
            return DecisionOut(
                claim_status="❌ Denied",
                claim_score=score(findings),
                explanation=f"Package {claim.package_id} is linked to ICD {pkg.icd_code}, not {claim.icd_code}.",
                findings=findings,
                next_actions=["Pick the correct HBP package for this ICD"]
            )
        findings.append(Finding(check="icd_valid", result="PASS"))
        findings.append(Finding(check="pkg_icd_match", result="PASS"))

        plan = resolve_plan(db, claim.plan_name)
        if not plan:
            all_plans = db.query(Plan.plan_name, Plan.plan_id).all()
            suggestions = [{"plan_name": p[0], "plan_id": p[1]} for p in all_plans]
            raise HTTPException(
                status_code=404,
                detail={"error": "Unknown plan", "input": claim.plan_name, "try_one_of": suggestions}
            )
        findings.append(Finding(check="plan_exists", result="PASS"))

        cov = db.query(Coverage).filter(
            Coverage.plan_id == plan.plan_id,
            Coverage.package_id == claim.package_id
        ).one_or_none()

        if not cov or not cov.covered:
            findings.append(Finding(check="coverage", result="FAIL", note="Excluded under this plan"))
            return DecisionOut(
                claim_status="❌ Denied",
                claim_score=score(findings),
                explanation="This ICD/package is excluded under the selected plan.",
                findings=findings
            )
        findings.append(Finding(check="coverage", result="PASS"))

        waiting = cov.waiting_months or 0
        if claim.months_enrolled < waiting:
            left = waiting - claim.months_enrolled
            findings.append(Finding(check="waiting", result="FAIL", note=f"{left} months remaining"))
            return DecisionOut(
                claim_status="❌ Denied",
                claim_score=score(findings),
                explanation=f"Waiting period not completed ({waiting} months).",
                findings=findings,
                next_actions=[f"Complete {left} more month(s) of enrollment"]
            )
        findings.append(Finding(check="waiting", result="PASS"))

        preauth_needed = bool(cov.preauth_override or pkg.preauth_required)
        if preauth_needed and claim.admission_type.lower() == "elective":
            findings.append(Finding(check="preauth", result="REQUIRED"))
            return DecisionOut(
                claim_status="🟡 Needs Pre-Authorization",
                claim_score=score(findings),
                explanation="Pre-authorization required for this package (elective admission).",
                findings=findings,
                next_actions=["Submit pre-authorization form", "Upload doctor's notes"]
            )
        findings.append(Finding(check="preauth", result="PASS" if preauth_needed else "N/A"))

        findings.append(Finding(check="admission", result="PASS"))

        est = claim.estimated_cost_inr or pkg.base_tariff_inr
        sublimit = cov.sublimit_inr
        copay = cov.copay_percent if cov.copay_percent is not None else plan.base_copay_percent

        approved_base = min(est, sublimit) if sublimit else est
        insurer_pay = approved_base - int(approved_base * (copay / 100))

        findings.append(Finding(check="sublimit", result="APPLIED" if sublimit else "N/A",
                                 note=f"₹{sublimit}" if sublimit else None))
        findings.append(Finding(check="copay", result="APPLIED", note=f"{copay}%"))

        status = "✅ Valid" if approved_base == est else "⚠️ Partial"

        return DecisionOut(
            claim_status=status,
            claim_score=score(findings),
            explanation=(
                f"Covered under {plan.plan_name}. "
                + ("Pre-auth not required. " if not preauth_needed else "")
                + (f"Sub-limit ₹{sublimit}. " if sublimit else "")
                + f"Subject to {copay}% co-pay."
            ).strip(),
            findings=findings,
            approved_amount_inr=insurer_pay
        )