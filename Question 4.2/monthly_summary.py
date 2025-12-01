import os
import smtplib
import json
from datetime import datetime
from email.message import EmailMessage

# === 1. Load credentials securely from environment variables ===
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# === 2. Load all orders from orders.json ===
ORDERS_FILE = r"C:\Users\valmy\OneDrive - Eduvos\Year 2 Courses\Python Network Programming\Project 2\Question 2\orders.json"


def load_orders():
    if not os.path.exists(ORDERS_FILE):
        print("❌ No orders file found.")
        return []
    with open(ORDERS_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


# === 3. Format a summary report ===
def generate_summary(orders):
    if not orders:
        return "<p>No orders were placed this month.</p>"

    html = """
    <h3>📅 Monthly Purchase Summary</h3>
    <table border='1' cellspacing='0' cellpadding='6' style='border-collapse:collapse;'>
      <tr style='background-color:#f2f2f2;'>
        <th>Customer Name</th>
        <th>Item Ordered</th>
      </tr>
    """
    for order in orders:
        name = order.get("name", "Unknown")
        item = order.get("item", "N/A")
        html += f"<tr><td>{name}</td><td>{item}</td></tr>"
    html += "</table>"
    return html


# === 4. Send the summary email ===
def send_monthly_summary():
    orders = load_orders()
    html_summary = generate_summary(orders)
    current_month = datetime.now().strftime("%B %Y")

    msg = EmailMessage()
    msg["Subject"] = f"🧾 Tech Store Monthly Summary – {current_month}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS  # send to yourself or manager

    body = f"""
    <html>
    <body style="font-family:Arial, sans-serif;">
      <h2>Tech Store Monthly Sales Report</h2>
      <p>Dear Manager,</p>
      <p>Here is the summary of all orders for <b>{current_month}</b>.</p>
      {html_summary}
      <p style="margin-top:20px;">Kind regards,<br><b>Tech Store System</b></p>
    </body>
    </html>
    """
    msg.set_content("Monthly sales summary attached.")
    msg.add_alternative(body, subtype='html')

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"📨 Monthly summary sent successfully to {EMAIL_ADDRESS}")
    except Exception as e:
        print(f"❌ Failed to send summary: {e}")


# === 5. Run the function manually or via scheduler ===
if __name__ == "__main__":
    send_monthly_summary()
