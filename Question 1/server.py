import socket

def main():
    # Store available parts
    parts = {
        "1": "Headsets",
        "2": "Camera",
        "3": "Tablets",
        "4": "Batteries"
    }

    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 5000
    server_socket.bind((host, port))
    server_socket.listen(2)  # up to two customers

    print(f"🖥️ Tech Store Server running on {host}:{port}")
    print("Waiting for customers to connect...")

    while True:
            conn, addr = server_socket.accept()
            print(f" Connection from: {addr}")

            # Send available parts
            menu = "\nAvailable parts:\n"
            for key, value in parts.items():
                menu += f"{key}. {value}\n"
            conn.send(menu.encode())

            # Receive order
            order = conn.recv(1024).decode()
            if order in parts:
                message = f"Order confirmed for: {parts[order]}. Your item will be prepared for delivery!"
            else:
                message = "Invalid selection. Please choose a valid part number."
            conn.send(message.encode())

            conn.close()
            print(f" Connection closed with {addr}\n")

if __name__ == "__main__":
    main()