import socket, ssl, json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

HOST = '127.0.0.1'
PORT = 8443

# Application symmetric key (32 bytes for AES-256).
# In real systems you'd derive per-session keys (e.g., from a KDF or handshake).
# For this educational demo we generate a static key and print it so client can use it.
APP_KEY = b'\xb5\x08\x80\x8e3\x88\xa1\x11>\xffQ\n\xf3\x80\x9d32*\xc4h\x03\t$tr\x05\xa5\xf3\xf3h\x809'
print("Application AES key (base16) — give this to client for demo:", APP_KEY.hex())

def build_ssl_context():
    ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ctx.load_cert_chain(certfile='certs/server.crt', keyfile='certs/server.key')
    ctx.load_verify_locations(cafile='certs/ca.crt')
    ctx.verify_mode = ssl.CERT_REQUIRED  # require client certificate
    return ctx

def decrypt_and_process(encrypted_blob: bytes):
    """
    Encrypted blob format (JSON bytes encoded):
    {
      "nonce": "<hex>",
      "ciphertext": "<hex>",
      "aad": "<optional hex or empty>"
    }
    """
    payload = json.loads(encrypted_blob.decode('utf-8'))
    nonce = bytes.fromhex(payload['nonce'])
    ct = bytes.fromhex(payload['ciphertext'])
    aad = bytes.fromhex(payload.get('aad', '')) if payload.get('aad') else None

    aesgcm = AESGCM(APP_KEY)
    if aad:
        plaintext = aesgcm.decrypt(nonce, ct, aad)
    else:
        plaintext = aesgcm.decrypt(nonce, ct, None)
    return plaintext.decode('utf-8')

def main():
    context = build_ssl_context()
    bindsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    bindsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    bindsock.bind((HOST, PORT))
    bindsock.listen(5)
    print(f"[SERVER] Listening on {HOST}:{PORT} (TLS, mTLS required)")

    while True:
        newsock, addr = bindsock.accept()
        try:
            with context.wrap_socket(newsock, server_side=True) as ssock:
                print(f"[SERVER] TLS connection from {addr}")
                # read size first (4 bytes network order)
                size_bytes = ssock.recv(4)
                if len(size_bytes) < 4:
                    print("[SERVER] invalid size header")
                    continue
                size = int.from_bytes(size_bytes, 'big')
                data = b''
                while len(data) < size:
                    chunk = ssock.recv(min(4096, size - len(data)))
                    if not chunk:
                        break
                    data += chunk
                if not data:
                    print("[SERVER] no payload")
                    continue

                # decrypt application payload
                try:
                    text = decrypt_and_process(data)
                    print("[SERVER] Received (decrypted):", text)
                    # example response (echo)
                    response_plain = f"Server received: {text}"
                    # encrypt response
                    aesgcm = AESGCM(APP_KEY)
                    resp_nonce = os.urandom(12)
                    resp_ct = aesgcm.encrypt(resp_nonce, response_plain.encode('utf-8'), None)
                    resp_payload = json.dumps({
                        "nonce": resp_nonce.hex(),
                        "ciphertext": resp_ct.hex()
                    }).encode('utf-8')
                    # send size + payload
                    ssock.sendall(len(resp_payload).to_bytes(4, 'big') + resp_payload)
                except Exception as e:
                    print("[SERVER] Decrypt/Process error:", e)
                    ssock.sendall(b'ERR')
        except ssl.SSLError as e:
            print("[SERVER] SSL error:", e)
        except Exception as e:
            print("[SERVER] Connection error:", e)
        finally:
            try:
                newsock.close()
            except:
                pass

if __name__ == '__main__':
    main()
