# Online Milk Diary — College Project Report

## 1. Introduction

The **Online Milk Diary** is a web-based Dairy Cooperative Management System developed using **Python Django**. It digitizes the daily milk collection process, farmer record management, billing, and reporting for dairy cooperatives. Traditionally, milk collection data is maintained in paper registers which leads to errors, delays in payment, and difficulty in generating reports. This system solves these problems by providing a centralized online platform.

## 2. Problem Statement

Dairy cooperatives face challenges in:
- Manual record keeping of daily milk collection
- Calculating payments based on fat percentage and rate charts
- Tracking deductions (feed, loans) and pending payments
- Generating daily/monthly reports for management and farmers

## 3. Objectives

- Automate daily milk collection entry (morning/evening shifts)
- Maintain farmer master data and collection center information
- Auto-calculate payment based on fat % and rate chart
- Generate monthly billing with deductions
- Provide role-based access (Admin, Operator, Accountant, Farmer)
- Generate daily reports with PDF and Excel export
- Deploy as a live web application accessible via internet

## 4. Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.12, Django 5.x |
| Database | SQLite (dev), PostgreSQL (production) |
| Frontend | HTML5, Bootstrap 5, Chart.js |
| Reports | ReportLab (PDF), OpenPyXL (Excel) |
| Deployment | Render.com (Free tier) |
| Server | Gunicorn + WhiteNoise |

## 5. System Modules

### 5.1 Accounts Module
- User authentication (login/logout)
- Role-based access control
- User registration (Admin only)

### 5.2 Farmers Module
- Farmer registration with ID, contact, bank details
- Collection center management
- Farmer profile and search

### 5.3 Collection Module
- Daily milk entry (date, shift, quantity, fat %, SNF %)
- Automatic rate calculation from rate chart
- Rate chart configuration by fat percentage slabs

### 5.4 Billing Module
- Monthly billing generation from milk entries
- Deduction management (feed, loan, other)
- Payment tracking (pending/paid, cash/bank/UPI)

### 5.5 Reports Module
- Admin dashboard with KPIs and 7-day chart
- Daily collection report
- Farmer ledger (month-wise)
- PDF and Excel export

## 6. Database Design

**Main Tables:**
- `User` — username, role, phone
- `CollectionCenter` — name, location
- `Farmer` — farmer_id, name, village, center, bank details
- `RateChart` — min_fat, max_fat, price_per_liter
- `MilkEntry` — farmer, date, shift, quantity, fat, amount
- `Deduction` — farmer, type, amount, month
- `Payment` — farmer, month, gross, deductions, net, status

## 7. User Roles

| Role | Permissions |
|------|-------------|
| Admin | Full system access, rate chart, centers, users |
| Operator | Add farmers, milk entries |
| Accountant | Billing, payments, deductions, reports |
| Farmer | View own profile, ledger, payments |

## 8. Testing

| Test Case | Expected Result | Status |
|-----------|-----------------|--------|
| Admin login | Dashboard displayed | Pass |
| Add farmer | Farmer saved in database | Pass |
| Milk entry | Amount auto-calculated | Pass |
| Generate billing | Monthly payment records created | Pass |
| Export PDF | PDF file downloaded | Pass |
| Farmer login | Only own data visible | Pass |

## 9. Deployment

The application is deployed on **Render.com** (free tier):
- Public URL: `https://your-app-name.onrender.com`
- PostgreSQL database (free)
- Automatic deploy from GitHub

## 10. Conclusion

The Online Milk Diary system successfully automates dairy cooperative operations including milk collection, billing, and reporting. It reduces manual work, improves accuracy, and provides transparency for farmers. The system is scalable and can be extended with SMS notifications, mobile app, and multi-center analytics in future.

## 11. Future Enhancements

- SMS notifications to farmers
- Mobile app using Django REST Framework
- Barcode/QR based farmer identification
- Inventory and dispatch tracking
- Multi-language support

---

**Submitted by:** [Your Name]  
**Roll No:** [Your Roll No]  
**Department:** [Your Department]  
**College:** [Your College Name]  
**Guide:** [Guide Name]
