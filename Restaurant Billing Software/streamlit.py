import streamlit as st
import sqlite3
import pandas as pd
from streamlit_option_menu import option_menu
import datetime
import qrcode
from io import BytesIO
from fpdf import FPDF

# ============ CACHE FOOD DATA ============
@st.cache_data(ttl=600)
def get_data():
    with sqlite3.connect("restaurant.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM food")
        return cur.fetchall()

# ============ SAVE SALE ============
def save_sale_to_db(purchase_date, cart, total_amount, payment_mode):
    with sqlite3.connect("restaurant.db") as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_date TEXT,
                item_name TEXT,
                category TEXT,
                price REAL,
                quantity INTEGER,
                payment_mode TEXT,
                total REAL
            )
        """)
        for item in cart.values():
            cur.execute(
                "INSERT INTO sales (purchase_date, item_name, category, price, quantity, payment_mode, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (purchase_date.strftime('%Y-%m-%d'), item['name'], item['category'], item['price'], item['qty'], payment_mode, total_amount)
            )
        conn.commit()

# ============ QR GENERATOR ============
def generate_qr_code(data: str):
    qr = qrcode.QRCode(version=1, box_size=8, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# ============ PDF BILL ============
def generate_pdf_bill(purchase_date, cart, total_amount, gst_amount, payment_mode):
    pdf = FPDF()
    pdf.add_page()

    # Load fonts
    pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
    pdf.add_font("DejaVu", "B", "DejaVuSans-Bold.ttf", uni=True)

    pdf.set_font("DejaVu", "", 16)
    pdf.cell(0, 10, "Restaurant Bill", ln=True, align="C")
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(0, 10, f"Purchase Date: {purchase_date.strftime('%d-%m-%Y')}", ln=True)
    pdf.cell(0, 10, f"Payment Mode: {payment_mode}", ln=True)
    pdf.ln(8)

    pdf.set_font("DejaVu", "B", 12)
    pdf.cell(80, 10, "Item", border=1)
    pdf.cell(30, 10, "Qty", border=1)
    pdf.cell(40, 10, "Price", border=1)
    pdf.cell(40, 10, "Total", border=1, ln=True)

    pdf.set_font("DejaVu", "", 12)
    for item in cart.values():
        item_total = item['price'] * item['qty']
        pdf.cell(80, 10, item['name'], border=1)
        pdf.cell(30, 10, str(item['qty']), border=1)
        pdf.cell(40, 10, f"₹{item['price']:.2f}", border=1)
        pdf.cell(40, 10, f"₹{item_total:.2f}", border=1, ln=True)

    subtotal = total_amount - gst_amount
    pdf.cell(150, 10, "Subtotal", border=1)
    pdf.cell(40, 10, f"₹{subtotal:.2f}", border=1, ln=True)

    pdf.cell(150, 10, "GST (5%)", border=1)
    pdf.cell(40, 10, f"₹{gst_amount:.2f}", border=1, ln=True)

    pdf.cell(150, 10, "Total", border=1)
    pdf.cell(40, 10, f"₹{total_amount:.2f}", border=1, ln=True)

    pdf_output = pdf.output(dest='S')  # already bytes
    buffer = BytesIO(pdf_output)
    buffer.seek(0)
    return buffer

# ============ LOGIN ============
def check_login(username, password):
    return username == st.session_state.get("username") and password == st.session_state.get("password")

if "username" not in st.session_state:
    st.session_state.username = "harshit"
if "password" not in st.session_state:
    st.session_state.password = "gupta"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Incorrect username or password.")

def logout():
    st.session_state.logged_in = False
    st.rerun()

def admin_panel():
    st.title("Admin Panel - Change Credentials")
    new_username = st.text_input("New Username", value=st.session_state.username)
    new_password = st.text_input("New Password", type="password")
    if st.button("Update Credentials"):
        if new_username and new_password:
            st.session_state.username = new_username
            st.session_state.password = new_password
            st.success("Credentials updated. Please logout and login again.")
        else:
            st.error("Please enter both username and password.")

# ============ MAIN APP ============
if not st.session_state.logged_in:
    login_page()
    st.stop()

with st.sidebar:
    st.header(f"Restaurant Billing - Admin: {st.session_state.username}")
    purchase_date = st.date_input("Select Purchase Date", value=datetime.date.today())
    menu_choice = option_menu("Menu", ["All", "Purchase", "Sales Data", "Admin"])
    st.button("Logout", on_click=logout)

# ============ ALL PRODUCTS ============
if menu_choice == "All":
    st.title("All Products")
    data = get_data()
    if data:
        df = pd.DataFrame(data, columns=["ID", "Item Name", "Category", "Price"])
        if "cart" not in st.session_state:
            st.session_state.cart = {}

        # Big square buttons
        st.markdown("""
        <style>
        div.stButton > button {
            width: 4cm; height: 4cm; font-size: 16px; margin: 5px 0; white-space: pre-wrap;
        }
        </style>
        """, unsafe_allow_html=True)

        cols_per_row = 4
        for i in range(0, len(df), cols_per_row):
            cols = st.columns(cols_per_row)
            for idx, row in enumerate(df.iloc[i:i+cols_per_row].itertuples()):
                with cols[idx]:
                    qty = st.session_state.cart.get(row.ID, {}).get("qty", 0)
                    label = f"{row._2}\n₹{row.Price}" + (f"\nQty: {qty}" if qty > 0 else "")
                    if st.button(label, key=f"btn_{row.ID}"):
                        if row.ID in st.session_state.cart:
                            st.session_state.cart[row.ID]["qty"] += 1
                        else:
                            st.session_state.cart[row.ID] = {
                                "name": row._2,
                                "category": row.Category,
                                "price": row.Price,
                                "qty": 1
                            }

        st.subheader(f"Cart ({purchase_date.strftime('%d-%m-%Y')})")
        total_amount = 0
        to_remove = []

        if st.session_state.cart:
            for item_id, info in list(st.session_state.cart.items()):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"{info['name']} ({info['category']}) - ₹{info['price']}")
                with col2:
                    new_qty = st.number_input("Qty", min_value=0, value=info["qty"], key=f"qty_{item_id}")
                    if new_qty == 0:
                        to_remove.append(item_id)
                    else:
                        st.session_state.cart[item_id]["qty"] = new_qty

                if info["qty"] > 0:
                    total_amount += info["price"] * info["qty"]

            for item_id in to_remove:
                del st.session_state.cart[item_id]
                st.rerun()

            if total_amount > 0:
                gst = round(total_amount * 0.05, 2)
                st.markdown(f"**Subtotal:** ₹{total_amount}")
                st.markdown(f"**GST (5%):** ₹{gst}")
                st.markdown(f"### Total: ₹{total_amount + gst}")
            else:
                st.write("No items selected yet.")
        else:
            st.write("No items selected yet.")

# ============ PURCHASE ============
elif menu_choice == "Purchase":
    st.title("Purchase Page")
    st.subheader("Add New Food Item")
    item_name = st.text_input("Item Name")
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0, step=1.0)

    if st.button("Add Item"):
        if item_name and category and price > 0:
            with sqlite3.connect("restaurant.db") as conn:
                cur = conn.cursor()
                cur.execute("CREATE TABLE IF NOT EXISTS food (id INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT, category TEXT, price REAL)")
                cur.execute("INSERT INTO food (item_name, category, price) VALUES (?, ?, ?)", (item_name, category, price))
                conn.commit()
            st.success(f"{item_name} added successfully!")
        else:
            st.error("Please fill all fields.")

    st.subheader("Make a Purchase")
    purchase_mode = st.radio("Purchase Mode", ["Online Purchase", "Offline Purchase"])
    upi_id = st.text_input("UPI ID", value="yourupi@bank")

    if "cart" not in st.session_state or not st.session_state.cart:
        st.info("Cart is empty.")
    else:
        current_total = sum(info["price"] * info["qty"] for info in st.session_state.cart.values())
        gst_amount = round(current_total * 0.05, 2)
        final_amount = current_total + gst_amount

        st.write(f"Subtotal: ₹{current_total}")
        st.write(f"GST: ₹{gst_amount}")
        st.write(f"Total: ₹{final_amount}")

        if purchase_mode == "Online Purchase" and upi_id.strip():
            upi_uri = f"upi://pay?pa={upi_id.strip()}&pn=Customer&am={final_amount}&cu=INR"
            qr_img_buf = generate_qr_code(upi_uri)
            st.image(qr_img_buf, caption="Scan UPI QR Code")
            st.download_button("Download QR", qr_img_buf, file_name="upi_qr.png", mime="image/png")

        pay_key = f"paid_{purchase_date.strftime('%Y%m%d')}"
        if not st.session_state.get(pay_key, False):
            if st.button("Confirm Payment"):
                save_sale_to_db(purchase_date, st.session_state.cart, final_amount, purchase_mode)
                pdf_buf = generate_pdf_bill(purchase_date, st.session_state.cart, final_amount, gst_amount, purchase_mode)
                st.session_state.cart = {}
                st.session_state[pay_key] = True
                st.success("Payment confirmed!")
                st.download_button("Download Bill PDF", pdf_buf, file_name="bill.pdf", mime="application/pdf")
        else:
            st.success("Payment already done for today.")

# ============ SALES DATA ============
elif menu_choice == "Sales Data":
    st.title("Sales Data")
    selected_date = st.date_input("Select Date", value=datetime.date.today())
    with sqlite3.connect("restaurant.db") as conn:
        df_sales = pd.read_sql(
            "SELECT item_name, quantity, price FROM sales WHERE purchase_date = ?",
            conn, params=(selected_date.strftime('%Y-%m-%d'),)
        )
    if not df_sales.empty:
        df_sales['total'] = df_sales['quantity'] * df_sales['price']
        st.bar_chart(df_sales.groupby('item_name')['total'].sum())
        st.dataframe(df_sales)
    else:
        st.write("No sales data for selected date.")

# ============ ADMIN ============
elif menu_choice == "Admin":
    admin_panel()
