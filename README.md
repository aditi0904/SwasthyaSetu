# SwasthyaSetu – India’s Integrated Digital Health Ecosystem

SwasthyaSetu is a **digital bridge between traditional medicine (AYUSH) and modern healthcare**. It ensures **interoperability, safety, and scalability** in India’s health ecosystem by integrating **dual coding systems, AI-driven semantic mapping, and universal health records**.

The platform is **modular, regulatory-compliant, and globally interoperable**, designed to empower patients, clinicians, insurers, and policymakers alike.

---

## 🚀 Key Features

* **Dual Coding Integration**: Syncs AYUSH terminologies with **WHO ICD-11** and India’s **NAMASTE standards**.
* **AI Semantic Mapping**: Maps herbal, traditional, and modern treatments for hybrid care plans.
* **Allergy & Safety Alerts**: Detects **herb-drug interactions** and prevents unsafe prescriptions.
* **Universal Health Records**: Patient-centric records linked to **ABHA ID** (Ayushman Bharat Health Account).
* **Health Passport**: QR-enabled, portable patient record for cross-system access.
* **Insurance Claim Validation**: Simplifies claims with transparent coding and interoperability.
* **Scalable & Modular Design**: Works across **mobile, web, and offline-first setups** for rural access.

---

## 🏗️ System Architecture

1. **Frontend** – React + TailwindCSS (patient and clinician dashboards).
2. **Backend** – Node.js / FastAPI with FHIR R4-compliant APIs.
3. **Data Layer** – PostgreSQL + NoSQL for structured & unstructured health data.
4. **Standards & Interoperability**

   * FHIR R4 (core data exchange standard).
   * WHO ICD-11 API (global terminology sync).
   * NAMASTE & TM2 integration (AYUSH coding).
   * ABDM APIs (NDHM-compliant health stack).
5. **Security & Access Control**

   * OAuth2 / OpenID Connect.
   * Role-based access for clinicians, patients, insurers.

---

## 🛠️ Tech Stack

**Frontend**: React, TailwindCSS
**Dashboard**: Streamlit (analytics & admin panel)
**Backend**: Node.js / FastAPI
**Database**: PostgreSQL, MongoDB
**APIs & Standards**: FHIR R4, WHO ICD-11, NAMASTE (TM2), ABDM APIs
**Security**: OAuth2, JWT
**Cloud & Deployment**: Docker, Kubernetes, AWS / NIC Cloud

---

## 📦 Setup Instructions

### Prerequisites

* Node.js v18+
* Python 3.10+ (for FastAPI modules)
* PostgreSQL 14+
* Docker (for containerized deployment)

### Installation

```bash
# Clone repository
git clone https://github.com/<your-org>/swasthyasetu.git
cd swasthyasetu

# Install frontend
cd frontend
npm install
npm start

# Install backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 📊 Example Use Case

1. **Patient Visit** – AYUSH practitioner records diagnosis in NAMASTE coding.
2. **Interoperability** – System automatically maps diagnosis to ICD-11 for insurance and clinical records.
3. **Safety Layer** – AI alerts if prescribed herbal medicine conflicts with patient’s ongoing allopathic drugs.
4. **Universal Record** – Updated data stored in **FHIR R4-compliant EHR**, accessible via ABHA ID.
5. **Claim Processing** – Insurer validates treatment with standardized coding, reducing fraud & delays.

---

## 🔒 Compliance & Security

* **HIPAA, NDHM & CDSCO aligned**
* **Data Encryption** at rest & transit
* **Consent-based access** with ABDM protocols

---

## 🌍 Impact

* **Patients**: Safer, portable, and accessible health records.
* **Clinicians**: Evidence-based hybrid treatment planning.
* **Insurers**: Fraud-free claim validation.
* **Policy Makers**: Unified dataset for public health decisions.

---

## 🤝 Contributing

We welcome contributions! Please fork this repo, create a feature branch, and submit a pull request.

---

## 📜 License

MIT License – free to use, modify, and distribute.

---

## ✨ Acknowledgments

* Ministry of AYUSH, Government of India
* WHO ICD-11 Team
* ABDM / NDHM for India’s health stack
* Open-source FHIR & HL7 community

---
