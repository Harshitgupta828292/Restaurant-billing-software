🍴 Restaurant Billing Software

A complete Restaurant Billing System built with Streamlit.
This project helps restaurants manage their menu, generate bills, authenticate users, and store transaction records securely in an SQLite database.

✨ Features

🔐 User Authentication

Admin / Cashier login system

Secure access to billing and database

📝 Menu Management

Add / Update / Delete food items

Store all menu items in SQLite database

💰 Billing System

Select multiple food items with quantity

Auto calculate total price & taxes

Store transaction history

📄 PDF Bill Generation

Generate printable PDF receipts using FPDF

Customer details + order details + bill total

📷 QR Code Integration

Generate QR code for easy UPI/Payment reference

QR embedded inside bill PDF

📊 Dashboard & Reports

View daily sales

Search old bills

Filter by date

🕒 Date & Time Support

Auto timestamp on every bill

🛠️ Tech Stack

Streamlit
 – Frontend & Dashboard

SQLite3
 – Database

Pandas
 – Data management

streamlit-option-menu
 – Sidebar Navigation

FPDF
 – PDF generation

qrcode
 – QR Code generation

datetime
 – Bill timestamps

⚙️ Installation

Clone this repository

git clone https://github.com/your-username/restaurant-billing.git
cd restaurant-billing


Install dependencies using pip

<p>pip install streamlit</p>
<p>pip install pandas</p>
<p>pip install fpdf</p>
<p>pip install qrcode</p>
<p>pip install streamlit-option-menu</p>


Run the Streamlit App

streamlit run app.py

🚀 Usage

Start the app with streamlit run app.py

Login as Admin / Cashier

Use the sidebar to:

📋 Manage menu items

🧾 Generate bills

📄 Download PDF bill with QR code

📊 Check sales reports

🔮 Future Scope

🌍 Multi-branch support

💳 Integrate payment gateways (Stripe / Razorpay / Paytm / UPI)

📱 Mobile-friendly UI

📈 Export analytics (CSV/Excel)

☁️ Cloud deployment for online usage
