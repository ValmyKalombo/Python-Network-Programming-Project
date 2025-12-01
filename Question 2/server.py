from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime

# === EMAIL RECEIPT FUNCTION ===
def send_order_receipt(customer_name, customer_email, item_name):
    EMAIL_ADDRESS = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg["Subject"] = "🧾 Order Confirmation - Tech Store"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = customer_email

    html_content = f"""
    <html>
    <body style="font-family: Arial; background-color:#f7f7f7; padding:20px;">
      <div style="background:#fff; border-radius:10px; padding:20px; max-width:600px; margin:auto;">
        <h2 style="color:#333;">✅ Order Confirmed!</h2>
        <p>Hello <b>{customer_name}</b>,</p>
        <p>Thank you for ordering from <b>Tech Store</b>.</p>
        <p>We have received your order for: <b>{item_name}</b>.</p>
        <hr>
        <p>📅 Order Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>We’ll prepare your order shortly.</p>
      </div>
    </body>
    </html>
    """

    msg.set_content("Your order has been confirmed.")
    msg.add_alternative(html_content, subtype='html')

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
            print(f"📨 Email sent successfully to {customer_email}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# File to store orders
ORDERS_FILE = "orders.json"

# ✅ FIX 1: Properly load or initialize orders and move save_orders() outside condition
orders = []
if os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "r") as f:
        orders = json.load(f)

def save_orders():
    """Save the current list of orders to a JSON file."""
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=4)


class OrderHandler(BaseHTTPRequestHandler):

    def show_homepage(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>💻 Tech Store - Order Portal</title>
            <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: radial-gradient(circle at top left, #0f2027, #203a43, #2c5364);
        color: #fff;
        text-align: center;
        padding: 40px;
        margin: 0;
    }
    h1 {
        color: #ffcc00;
        font-size: 2.5em;
        margin-bottom: 10px;
        text-shadow: 0 0 15px #ffcc00, 0 0 30px #ffcc00;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #ffcc00, 0 0 20px #ffcc00; }
        to { text-shadow: 0 0 25px #ffd633, 0 0 50px #ffd633; }
    }
    .container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 30px;
        max-width: 500px;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
    }
    form {
        margin-top: 20px;
    }
    input[type="text"] {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ffcc00;
    width: 80%;
    margin: 8px 0;
    background-color: rgba(255,255,255,0.1);
    color: #fff;
    box-shadow: 0 0 10px #ffcc00;
}

select {
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #ffcc00;
    width: 84%;
    margin: 8px 0;
    background-color: rgba(255,255,255,0.1);
    color: #fff;
    box-shadow: none;
    text-shadow: none;
    outline: none;
    appearance: none;
}

select:focus {
    border-color: #ffd633;
    background-color: rgba(255,255,255,0.15);
    box-shadow: none;
}

option {
    background-color: #2c5364;
    color: white;
    text-shadow: none;
}

    }
    button {
        background-color: #ffcc00;
        color: #333;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 0 15px #ffcc00;
    }
    button:hover {
        background-color: #ffd633;
        transform: scale(1.05);
        box-shadow: 0 0 25px #ffd633, 0 0 40px #ffd633;
    }
    a {
        display: inline-block;
        margin-top: 20px;
        color: #ffcc00;
        text-decoration: none;
        font-weight: bold;
        text-shadow: 0 0 10px #ffcc00;
    }
    a:hover {
        color: #fff;
        text-shadow: 0 0 20px #fff;
    }
</style>
        </head>
        <body>
            <div class="container">
                <h1>🛒 Tech Store Online Ordering</h1>
                <p>Welcome! Please fill in your details to order a computer part below.</p>

                <form action="/create" method="POST">
    <input type="text" name="name" placeholder="Your Name" required><br>
    <input type="email" name="email" placeholder="Your Email" required><br>
                    <select name="item" required>
                        <option value="">Select a Computer Part</option>
                        <option>Headsets</option>
                        <option>Camera</option>
                        <option>Tablets</option>
                        <option>Batteries</option>
                    </select><br>
                    <button type="submit">Place Order</button>
                </form>
                <a href="/orders">📦 View All Orders</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def show_orders(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>All Orders</title>
            <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #141E30, #243B55);
        color: #fff;
        text-align: center;
        padding: 40px;
    }
    h1 {
        color: #ffcc00;
        font-size: 2.2em;
        text-shadow: 0 0 15px #ffcc00, 0 0 25px #ffd633;
        animation: pulse 1.8s infinite alternate;
    }
    @keyframes pulse {
        from { text-shadow: 0 0 15px #ffcc00; }
        to { text-shadow: 0 0 35px #ffd633; }
    }
    table {
        width: 80%;
        margin: 30px auto;
        border-collapse: collapse;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        box-shadow: 0 0 25px rgba(255,255,255,0.2);
    }
    th, td {
        border-bottom: 1px solid #ffcc00;
        padding: 12px;
        text-align: center;
        font-size: 1.1em;
    }
    tr:hover {
        background-color: rgba(255,255,255,0.1);
        box-shadow: 0 0 15px #ffd633;
    }
    a {
        color: #ffcc00;
        text-decoration: none;
        font-weight: bold;
        text-shadow: 0 0 10px #ffcc00;
    }
    a:hover {
        color: #fff;
        text-shadow: 0 0 20px #fff;
    }
</style>
        </head>
        <body>
            <h1>📋 Order Records</h1>
            <table>
                <tr><th>Customer Name</th><th>Item Ordered</th></tr>
        """

        for i, order in enumerate(orders):
            if isinstance(order, dict) and 'name' in order and 'item' in order:
                html += f"<tr><td>{order['name']}</td><td>{order['item']}</td>"
                html += f"<td><a href='/update?id={i}'>✏️ Edit</a> | <a href='/delete?id={i}'>❌ Delete</a></td></tr>"

        html += """
            </table>
            <a href="/">⬅️ Back to Order Page</a>
        </body>
        </html>
        """
        self.wfile.write(html.encode())

    def show_update_form(self, order_id):
        order = orders[int(order_id)]
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")  # ✅ Fix encoding
        self.end_headers()

        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>✏️ Update Order</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: radial-gradient(circle at top right, #0f2027, #203a43, #2c5364);
                    color: #fff;
                    text-align: center;
                    padding: 50px;
                    margin: 0;
                }}
                .container {{
                    background: rgba(255, 255, 255, 0.08);
                    border-radius: 12px;
                    padding: 40px;
                    max-width: 500px;
                    margin: 0 auto;
                    box-shadow: 0 0 25px rgba(255,255,255,0.15);
                }}
                h1 {{
                    color: #ffcc00;
                    font-size: 2em;
                    margin-bottom: 15px;
                    text-shadow: 0 0 15px #ffcc00, 0 0 30px #ffd633;
                    animation: glow 1.8s infinite alternate;
                }}
                @keyframes glow {{
                    from {{ text-shadow: 0 0 10px #ffcc00; }}
                    to {{ text-shadow: 0 0 25px #ffd633, 0 0 50px #ffd633; }}
                }}
                input[type="text"] {{
                    padding: 12px;
                    border-radius: 5px;
                    border: 1px solid #ffcc00;
                    width: 80%;
                    margin: 10px 0;
                    background-color: rgba(255,255,255,0.1);
                    color: #fff;
                    font-size: 1em;
                    box-shadow: 0 0 10px #ffcc00; /* glow only for input box */
                }}
                select {{
                    padding: 12px;
                    border-radius: 5px;
                    border: 1px solid #ffcc00;
                    width: 84%;
                    margin: 10px 0;
                    background-color: rgba(255,255,255,0.1);
                    color: #fff;
                    box-shadow: none; /* ✅ no glow */
                    text-shadow: none; /* ✅ remove glow on text */
                    outline: none;
                    appearance: none; /* modern dropdown arrow */
                }}
                select:focus {{
                    border-color: #ffd633;
                    background-color: rgba(255,255,255,0.15);
                    box-shadow: none; /* ✅ no glow on focus */
                }}
                option {{
                    background-color: #2c5364;
                    color: white;
                    text-shadow: none; /* ✅ no text glow */
                }}
                button {{
                    background-color: #ffcc00;
                    color: #333;
                    padding: 10px 25px;
                    border: none;
                    border-radius: 8px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: 0.3s;
                    box-shadow: 0 0 15px #ffcc00;
                }}
                button:hover {{
                    background-color: #ffd633;
                    transform: scale(1.05);
                    box-shadow: 0 0 25px #ffd633, 0 0 40px #ffd633;
                }}
                a {{
                    display: inline-block;
                    margin-top: 20px;
                    color: #ffcc00;
                    text-decoration: none;
                    font-weight: bold;
                    text-shadow: 0 0 10px #ffcc00;
                }}
                a:hover {{
                    color: #fff;
                    text-shadow: 0 0 20px #fff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>✏️ Update Order</h1>
                <form action="/update?id={order_id}" method="POST">
                    <input type="text" name="name" value="{order['name']}" required><br>
                    <select name="item" required>
                        <option {'selected' if order['item'] == 'Headsets' else ''}>Headsets</option>
                        <option {'selected' if order['item'] == 'Camera' else ''}>Camera</option>
                        <option {'selected' if order['item'] == 'Tablets' else ''}>Tablets</option>
                        <option {'selected' if order['item'] == 'Batteries' else ''}>Batteries</option>
                    </select><br><br>
                    <button type="submit">Update Order</button>
                </form>
                <a href="/orders">⬅️ Back to Orders</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def delete_order(self, order_id):
        if 0 <= int(order_id) < len(orders):
            del orders[int(order_id)]
            save_orders()

        self.send_response(302)
        self.send_header("Location", "/orders")
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/favicon.ico":
            self.send_response(200)
            self.end_headers()
        elif path == "/":
            self.show_homepage()
        elif path == "/orders":
            self.show_orders()
        elif path == "/update" and "id" in query:
            self.show_update_form(query["id"][0])
        elif path == "/delete" and "id" in query:
            self.delete_order(query["id"][0])
        else:
            self.send_error(404, "Page Not Found")

    def do_POST(self):
        # ✅ FIX 2 + 3: Correct indentation and add save_orders()
        if self.path == "/create":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode())

            name = data.get('name', [''])[0]
            item = data.get('item', [''])[0]
            email = data.get('email', [''])[0]

            orders.append({'name': name, 'email': email, 'item': item})

            # Send the email receipt
            send_order_receipt(name, email, item)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            confirmation_html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Order Confirmed</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background: radial-gradient(circle at top right, #0f2027, #203a43, #2c5364);
                        color: #fff;
                        text-align: center;
                        margin: 0;
                        padding: 50px;
                    }}
                    .container {{
                        background: rgba(255, 255, 255, 0.08);
                        border-radius: 12px;
                        padding: 40px;
                        max-width: 600px;
                        margin: 0 auto;
                        box-shadow: 0 0 20px rgba(0,0,0,0.2);
                        backdrop-filter: blur(8px);
                    }}
                    h1 {{
                        color: #ffcc00;
                        font-size: 2em;
                        margin-bottom: 15px;
                        text-shadow: 0 0 15px #ffcc00, 0 0 30px #ffd633;
                        animation: glow 1.8s infinite alternate;
                    }}
                    @keyframes glow {{
                        from {{ text-shadow: 0 0 10px #ffcc00; }}
                        to {{ text-shadow: 0 0 25px #ffd633, 0 0 50px #ffd633; }}
                    }}
                    p {{
                        font-size: 1.1em;
                        color: #e0e0e0;
                    }}
                    .button {{
                        display: inline-block;
                        background-color: #ffcc00;
                        color: #333;
                        padding: 12px 25px;
                        border-radius: 8px;
                        font-weight: bold;
                        text-decoration: none;
                        margin: 15px;
                        transition: all 0.3s ease;
                        box-shadow: 0 0 15px #ffcc00;
                    }}
                    .button:hover {{
                        background-color: #ffd633;
                        transform: scale(1.05);
                        box-shadow: 0 0 25px #ffd633, 0 0 40px #ffd633;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>✅ Order Confirmed!</h1>
                    <p>Thank you, <b>{name}</b>. You have successfully ordered <b>{item}</b>.</p>
                    <a href="/" class="button">⬅️ Back to Homepage</a>
                    <a href="/orders" class="button">📦 View All Orders</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(confirmation_html.encode("utf-8"))

        elif self.path.startswith("/update"):
            parsed = urllib.parse.urlparse(self.path)
            query = urllib.parse.parse_qs(parsed.query)
            order_id = int(query["id"][0])
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = urllib.parse.parse_qs(post_data.decode())

            orders[order_id]['name'] = data.get('name', [''])[0]
            orders[order_id]['item'] = data.get('item', [''])[0]
            save_orders()

            self.send_response(302)
            self.send_header("Location", "/orders")
            self.end_headers()


def run():
    host = "localhost"
    port = 8080
    server = HTTPServer((host, port), OrderHandler)
    print(f" Server started at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
