# Restaurant Live Table Order & Billing System

A full-stack Restaurant Management system built using **Django REST Framework** and **React**, designed to manage live table occupancy, menu orders, and billing workflow with role-based access.

This project was developed as part of a Full-Stack Django Developer take-home assessment.

---

## 📌 Features Overview

### 🍽 Table Management
- Track table status:
  - **AVAILABLE**
  - **OCCUPIED**
  - **BILL_REQUESTED**
  - **CLOSED**
- Automatic status transitions based on order and billing lifecycle

### 📋 Menu & Orders
- Manager can create / enable / disable menu items
- Waiter can:
  - Create orders for tables
  - Add / update / remove order items
  - Manage order lifecycle
- Orders are strictly tied to table status

### 💳 Billing
- Generate bill with subtotal + tax
- Cashier can:
  - View pending bills
  - Mark bill as paid
- Table automatically closes after successful payment

### 👥 Role-Based Access Control
- **Waiter**
  - Create orders
  - Add/update order items
  - Request bill
- **Cashier**
  - Generate bill
  - Accept payment
- **Manager**
  - Manage tables
  - Manage menu items
  - View all orders and bills

### 🔔 Background / Business Logic
- Automatic table state transitions based on order & billing status
- Order item modification locked after bill request

---

## 🖼 UI Screenshots

Application screenshots are available in the **`website_images/`** folder at the repository root.

---

## 🛠 Tech Stack

### Backend
- Python
- Django
- Django REST Framework
- SQLite (default for assessment)

### Frontend
- React
- Vite
- Axios
- Bootstrap

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/littlenewprogrammer123/Restaurant-Live-Table-Order-Billing-System.git
cd Restaurant-Live-Table-Order-Billing-System

Backend Setup (Django)

cd backend
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Backend will run at: http://localhost:8000


Frontend Setup (React)
cd frontend/restaurant-ui
npm install
npm run dev

Frontend will run at: http://localhost:5173


🔐 Default Roles & Access

Roles are managed via Django Groups:

WAITER

CASHIER

MANAGER

Assign roles to users from Django Admin:

http://localhost:8000/admin


📝 Notes & Assumptions

SQLite is used for simplicity (assessment purpose)

Authentication handled via session-based login

Status transitions are strictly validated server-side

UI focuses on functionality over advanced styling

Designed to be easily extensible (notifications, WebSockets, etc.)



🚀 Possible Future Improvements

Real-time updates using WebSockets

Email / notification alerts for pending bills

Payment gateway integration

Detailed sales reports for managers


👤 Author

Vibin
BCA Graduate | Java Full-Stack | Django & React Developer


📄 Assignment Context

This project fulfills the requirements outlined in the Restaurant Live Table Order & Billing System take-home assignment.
