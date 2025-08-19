🍴 Restaurant Billing Software

A simple Restaurant Billing Software built with Streamlit that allows restaurant owners to manage menu items, generate bills, and store records in an SQLite database.

📌 Features

📝 Add & Manage Food Items (stored in SQLite database)

📊 Interactive Dashboard built using Streamlit

💰 Billing System – generate bills for selected items

🕒 Date & Time support using datetime

📄 Generate PDF Bill Receipts using FPDF

📷 QR Code Generation for quick payment reference

💾 Store and Retrieve Bills for future records

🛠️ Tech Stack

Streamlit
 – UI & Dashboard

SQLite3
 – Database

Pandas
 – Data handling

streamlit-option-menu
 – Sidebar navigation

FPDF
 – PDF generation

qrcode
 – QR Code generation

⚙️ Installation

Clone this repository

git clone https://github.com/your-username/restaurant-billing.git
cd restaurant-billing


Install dependencies using pip

pip install streamlit
pip install pandas
pip install fpdf
pip install qrcode
pip install streamlit-option-menu


Run the Streamlit App

streamlit run app.py

🚀 Usage

Start the app using streamlit run app.py.

Use the sidebar menu to:

Add / Update food items in the database.

Select food items and generate a bill.

Export bill as PDF with QR code for payment.

