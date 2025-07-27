# 🧁 Bread by Bike – Sales Dashboard

Welcome to the full-stack **Sales Dashboard** built for the London-based bakery & café **Bread by Bike**. This platform empowers daily, weekly, and yearly sales analysis using an intuitive interface, live financial stats, and automation—serving both real-world internal use and an employer-facing public preview.

---

## 🔍 Overview

This dashboard is a custom-built, production-grade analytics tool developed with:

- ⚙️ **Backend:** Django + PostgreSQL  
- 💻 **Frontend:** React (Vite) + Tailwind CSS
- ☁️ **Hosting:** Railway (backend & cron jobs), Vercel (public preview), Render (legacy/static option)  
- 🔐 **Authentication:** Session-based login with expiration  
- 📊 **Stats Engine:** Automated data fetching, processing, and chart visualization  
- 🧠 **Automation:** Cron jobs for daily recalculations of key performance metrics  

---

## 🚀 Live Demo Links

- 🔐 [**Main App (Private)**](https://breadbybike-dashboard-production.up.railway.app) — Internal app with login, background jobs & real sales data.  
- 👁️ [**Public Preview**](https://sales-dashboard-preview.vercel.app) — Static, dummy-data version for employers and the public.  

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 📦 Multi-Page Dashboard | Home, Items, and Orders pages, each with distinct KPIs |
| 🔄 Scheduled Automation | Daily and weekly cron jobs automatically run calculations |
| 🧾 Historical Order Tracking | Full itemized order data with daily snapshots |
| 📈 Responsive Visuals | D3/Chart.js-powered graphs with real-time React updates |
| 🔐 Secure Auth | Custom login with session expiration and environment variable protection |
| ⚙️ Admin Backend | Django admin panel to manually adjust or view underlying models |
| 🌐 Dual Deploy | Production and preview versions hosted on separate platforms |

---

## 🛠️ Tech Stack

**Frontend:**
- React (Vite)
- Tailwind CSS  
- Chart.js  

**Backend:**
- Django & Django REST Framework  
- PostgreSQL (via Railway)  
- Cron Jobs (via Railway Scheduled Jobs)  
- Custom calculation scripts for daily/weekly/yearly metrics  

**DevOps:**
- Railway (backend, database, cron)  
- Vercel (frontend preview)  
- GitHub Actions (optional for CI/CD)  
- Environment variables securely managed via hosting platforms  


---

## 📅 Scheduled Tasks

| Task                | Schedule (UTC) | Command                             |
|---------------------|----------------|--------------------------------------|
| Update Square Data  | 02:00 AM       | `python manage.py update_daily_stats` |
| Precalculate Values | 02:15 AM       | `python manage.py precalc_stats` |

These are handled via **Railway Scheduled Jobs**.

---

## 🧠 Developer Highlights

- ✅ Converted live SQLite3 system to PostgreSQL for production
- ✅ Built dynamic chart components with responsive breakpoints
- ✅ Resolved memory limit issues on Render by moving backend to Railway
- ✅ Designed public dummy data generator for employer-facing preview
- ✅ Diagnosed and eliminated model inflation bugs from duplicate records
- ✅ Designed fallback logic and error-handling for production stability

---

## 🧑‍💼 For Employers

If you're reviewing this project as a potential employer, here’s what you should know:

- This was built to be **practical**, **scalable**, and **visually professional**
- The real version runs **secure cron jobs**, **authentication**, and **true analytics**
- The public version lets you explore the **UX, layout, and functionality** safely

🧭 If you're interested in the source, code reviews, or a walkthrough — feel free to reach out.

---

## 📫 Contact

Built by **Matthew Rayner**  
📧 [matthew.j.rayner@gmail.com](mailto:raynerjmatthew@gmail.com)  
🌐 [sales-dashboard-preview.vercel.app](https://matthewjrayner.github.io)

---

> _"A fully deployed, full-stack app that combines frontend polish with backend power — built from the ground up with real-world impact in mind."_
