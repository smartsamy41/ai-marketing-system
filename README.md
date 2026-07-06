# 🌐 Free Basics – AI Affiliate & SEO Platform

## 🚀 STATUS
Live Production System on Google Cloud Run

---

## 🧠 SYSTEM OVERVIEW

Free Basics is a:
- Affiliate Marketing System
- SEO Landingpage Platform
- Tracking & Analytics Engine
- Future AI Content System

---

## 🏗 ARCHITECTURE

### Frontend (FastAPI)
- / → Home
- /energie → Check24 (Strom, Gas)
- /finanzen → Tarifcheck (Kredit, Konto)
- /tech → Amazon Products
- /telekom → Telekom Offers

---

### 💰 AFFILIATE SYSTEM
Providers:
- Check24
- Tarifcheck
- Amazon (Tracking ID: freebasics-21)
- Telekom Partner Links

All links include:
✔ "Werbung / Anzeige"

---

### 📊 TRACKING SYSTEM
- Click Tracking
- Conversion Tracking
- Revenue Stats

Endpoint:
- /stats

---

## 🚀 DEPLOYMENT

Google Cloud Run:

```bash
gcloud run deploy ai-marketing-system --source . --region europe-west1
