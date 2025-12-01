import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# 🧠 Step 1: Load email credentials from environment variables
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# 🧾 Step 2: Define a function to send the order confirmation email
def send_order_receipt(customer_name, customer_email, item_name):
    # Create the email message
    msg = EmailMessage()
    msg["Subject"] = "🧾 Order Confirmation - Tech Store"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = customer_email

    # Email body (HTML styled for a nice look)
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f2f2f2; padding: 20px;">
        <div style="background-color: white; border-radius: 10px; padding: 20px; max-width: 600px; margin: auto;">
            <h2 style="color: #333;">✅ Order Confirmed!</h2>
            <p>Hello <strong>{customer_name}</strong>,</p>
            <p>Thank you for shopping with <b>Tech Store</b>.</p>
            <p>We have successfully received your order for:</p>
            <p style="font-size: 1.2em; color: #008080;"><strong>{item_name}</strong></p>
            <hr>
            <p>📅 Order Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>We will process your order shortly and send you another email once it’s ready for delivery.</p>
            <p>Kind regards,<br><strong>The Tech Store Team</strong></p>
        </div>
    </body>
    </html>
    """

    # Set email content
    msg.set_content("Your order has been confirmed.")
    msg.add_alternative(html_content, subtype='html')

    # Step 3: Connect to Gmail’s secure SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()  # Encrypt connection
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"📨 Receipt sent successfully to {customer_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# 🧩 Step 4: Example usage
if __name__ == "__main__":
    print("=== Tech Store Email System ===")
    name = input("Enter customer name: ")
    email = input("Enter customer email: ")
    item = input("Enter ordered item: ")

    send_order_receipt(name, email, item)