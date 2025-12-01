# Python-Network-Programming-Project
Eduvos – ITPNA2-B34

This project demonstrates multiple networking concepts using Python, including:

📌 Question 1 – TCP Client & Server (Computer Part Ordering)

✔ Basic socket programming
✔ Multi-client handling
✔ Order processing

📌 Question 2 – HTTP CRUD Ordering System

✔ Custom HTTP server using http.server
✔ Create, Read, Update, Delete (CRUD)
✔ Styled interactive webpage (HTML + CSS)
✔ File-based JSON storage

📌 Question 3 – Secure Communication

✔ SSL/TLS certificate generation (OpenSSL)
✔ Encrypted TCP communication
✔ AES-GCM symmetric encryption
✔ Certificate-based authentication

📡 Question 4 – Email Automation System (SMTP, TLS & SSL)

This part of the project implements a complete email delivery system using Python's smtplib and Google SMTP servers.
Two major features were built:

✔ 4.1 – Automatic Email Receipt for Each Order

Every time a customer successfully orders a component, the system sends them a receipt via email.

Email Protocol Used: SMTP with TLS

The system uses:

🔹 SMTP (Simple Mail Transfer Protocol)

The standard protocol for sending emails over the internet.

Port used: 587

Server: smtp.gmail.com

🔹 TLS (Transport Layer Security)

The system upgrades the SMTP connection using:

server.starttls()


This enables encrypted communication between the Python script and Google's SMTP server.

🔐 Why TLS?

Protects the login credentials

Encrypts the email content

Prevents eavesdropping

Ensures message integrity

✔ 4.2 – Monthly Summary Email System

A scheduled script sends a summary of all purchases for the month.

Email Protocol Used: SMTP over SSL

This version uses port 465, which establishes a secure connection before sending any data.

Difference Between TLS and SSL in the Project
Feature	TLS (Used in 4.1)	SSL (Used in 4.2)
Port	587	465
Security Start	Starts unencrypted → upgrades to TLS	Encrypted from the beginning
Usage	Login-based receipts	Automated scheduled summary
Strength	More modern & secure	Legacy but still supported

By using both SMTP + TLS and SMTP + SSL, the project demonstrates two ways secure email delivery is implemented in real-world applications.

🛠 Requirements
Python 3.11+
pip install cryptography
pip install schedule


📫 Contact

Developed by Valmy Kalombo
Email: valmykalombo@gmail.com

LinkedIn: www.linkedin.com/in/valmy-kalombo-b606b7257
