import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = 'localhost'
    port = 5000

    # Connect to server
    client_socket.connect((host, port))
    print("Connected to Tech Store Server!\n")

    # Receive the menu
    menu = client_socket.recv(1024).decode()
    print(menu)

    # Let user choose part
    order = input("Enter the number of the part you want to order: ")
    client_socket.send(order.encode())

    # Receive confirmation
    message = client_socket.recv(1024).decode()
    print("\n" + message)

    client_socket.close()

if __name__ == "__main__":
    main()