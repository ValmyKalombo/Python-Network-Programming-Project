import socket, ssl, json, os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

HOST = '127.0.0.1'
PORT = 8443

# Paste the application key printed by the server (hex)
APP_KEY_HEX = "b508808e3388a1113eff510af3809d33322ac468030924747205a5f3f3688039"
APP_KEY = bytes.fromhex(APP_KEY_HEX)

def build_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile='certs/ca.crt')
    ctx.load_cert_chain(certfile='certs/client.crt', keyfile='certs/client.key')
    # optional: require host verification if CN matches 'localhost'
    ctx.check_hostname = False
    return ctx

def encrypt_message(plaintext: str):
    aesgcm = AESGCM(APP_KEY)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return json.dumps({
        "nonce": nonce.hex(),
        "ciphertext": ct.hex()
    }).encode('utf-8')

def decrypt_response(data: bytes):
    payload = json.loads(data.decode('utf-8'))
    nonce = bytes.fromhex(payload['nonce'])
    ct = bytes.fromhex(payload['ciphertext'])
    aesgcm = AESGCM(APP_KEY)
    pt = aesgcm.decrypt(nonce, ct, None)
    return pt.decode('utf-8')

def main():
    context = build_ssl_context()
    raw = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    with context.wrap_socket(raw, server_hostname='localhost') as ssock:
        ssock.connect((HOST, PORT))
        print("[CLIENT] TLS connected to server (mTLS)")

        # Example application message
        msg = "Order: Camera x1 for user Alice"
        payload = encrypt_message(msg)
        # send length header + payload
        ssock.sendall(len(payload).to_bytes(4, 'big') + payload)
        # receive response length header
        size_bytes = ssock.recv(4)
        size = int.from_bytes(size_bytes, 'big')
        data = b''
        while len(data) < size:
            chunk = ssock.recv(min(4096, size - len(data)))
            if not chunk:
                break
            data += chunk
        if data:
            resp = decrypt_response(data)
            print("[CLIENT] Decrypted response:", resp)
        else:
            print("[CLIENT] No response or error")

if __name__ == '__main__':
    main()