# 🔐 SecureChat – End-to-End Encrypted Chat Application

SecureChat is a secure real-time messaging application developed using **Python, Flask, Flask-SocketIO, and MySQL**. The application implements **End-to-End Encryption (E2EE)** to ensure that only the sender and intended recipient can read exchanged messages.

In addition to secure messaging, the application includes a comprehensive **Security Testing Lab**, an **Admin Dashboard**, real-time **Security Monitoring**, and various cybersecurity simulations such as **Message Tampering**, **Replay Attack**, and **Man-in-the-Middle (MITM)** simulations. This project demonstrates secure communication, applied cryptography, and defensive cybersecurity techniques.

---

# 📌 Features

## 👤 User Authentication
- User Registration
- Secure Login
- Password Hashing
- Session Management
- Logout Functionality

## 💬 Real-Time Secure Chat
- One-to-One Messaging
- Instant Message Delivery
- Chat History
- Message Timestamps
- Typing Indicator
- Modern Chat Interface
- Dark Mode Support

## 🔐 End-to-End Encryption
- AES Message Encryption
- Encrypted Message Storage
- Secure Encryption Keys
- Confidential Communication

## 🛡️ Message Integrity Protection
- HMAC Verification
- Integrity Validation
- Tamper Detection
- Secure Message Verification

## 🧪 Security Testing Lab

The integrated Security Testing Lab allows users to perform various cybersecurity experiments and verify the security of the communication system.

### 🔐 Encryption Integrity Test
- Verify successful encryption and decryption
- Validate encrypted message integrity
- Ensure message confidentiality

### ✏️ Message Tampering Test
- Simulate message modification
- Detect altered encrypted messages
- Demonstrate integrity verification

### 🔑 Encryption Key Strength Test
- Analyze encryption key strength
- Demonstrate strong vs weak encryption
- Security recommendations

### 🔄 Replay Attack Simulation
- Simulate replaying captured messages
- Demonstrate replay attack concepts
- Validate replay protection

### 🕵️ Man-in-the-Middle (MITM) Simulation
- Simulate intercepted communication
- Demonstrate secure encrypted transmission
- Show protection provided by End-to-End Encryption

### 📊 Test Result Dashboard
- Real-time PASS / FAIL status
- Security explanations
- Learning-oriented attack demonstrations

---

# 📊 Admin Dashboard

The application includes a dedicated administrator panel for monitoring security events.

### Dashboard Features

- Registered User Statistics
- Login Monitoring
- Failed Login Attempts
- Brute Force Attack Detection
- Security Event Logs
- Security Alerts
- User Management
- Activity Monitoring
- Interactive Charts
- Security Analytics

---

# 🚨 Security Monitoring

The application continuously monitors user activities and logs important security events.

Examples include:

- Successful Login
- Failed Login
- Admin Login
- Admin Login Failure
- Brute Force Detection
- Suspicious Activity
- Security Alerts

---

# 📄 Reports

- PDF Report Generation
- CSV Export
- Security Logs
- Investigation Reports

---

# 🛠️ Technologies Used

## Backend
- Python
- Flask
- Flask-SocketIO
- Flask-Login
- PyCryptodome
- Werkzeug Security

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap
- Chart.js

## Database
- MySQL

## Cryptography
- AES Encryption
- HMAC
- SHA-512
- Password Hashing

---

# 🔒 Security Features

- End-to-End Encryption (E2EE)
- AES Encryption
- HMAC Integrity Verification
- SHA-512 Hashing
- Secure Password Hashing
- Content Security Policy (CSP)
- Secure Session Management
- Security Logging
- Brute Force Detection
- Message Tampering Detection
- Replay Attack Simulation
- MITM Attack Simulation
- Encryption Testing
- Security Dashboard

---

# 📂 Project Structure

```
SecureChat/
│
├── app.py
├── config.py
├── crypto_utils.py
├── database/
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│   ├── login.html
│   ├── register.html
│   ├── chat.html
│   ├── admin_dashboard.html
│   ├── testing_lab.html
│
├── uploads/
├── reports/
├── security_logs/
├── requirements.txt
└── README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/mca25sakpalsoham-afk/SecureChat.git
```

---

## Navigate to Project

```bash
cd SecureChat
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

---

## Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure MySQL

Create a MySQL database and import the SQL schema.

Update your database credentials inside `config.py`.

---

## Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

# 📸 Screenshots

Include screenshots of:

- Login Page
- Registration Page
- Chat Interface
- Dark Mode
- Admin Dashboard
- Security Log Viewer
- Testing Lab
- Encryption Integrity Test
- Message Tampering Test
- Replay Attack Simulation
- MITM Simulation
- Brute Force Detection Graph
- Encrypted Database Messages

---

# 🎯 Learning Outcomes

This project demonstrates practical implementation of:

- End-to-End Encryption
- Secure Web Application Development
- Cryptography Fundamentals
- AES Encryption
- HMAC Integrity Verification
- SHA-512 Hashing
- Secure Authentication
- Password Hashing
- Session Management
- Real-Time Communication
- Security Monitoring
- Brute Force Detection
- Message Tampering Detection
- Replay Attack Simulation
- Man-in-the-Middle Attack Simulation
- Secure Database Design
- Security Logging
- Cybersecurity Best Practices

---

# 🚀 Future Enhancements

- Group Chat Support
- Encrypted File Sharing
- Voice and Video Calls
- Two-Factor Authentication (2FA)
- Push Notifications
- Digital Signatures
- AI-Based Threat Detection
- Secure Key Exchange using RSA
- Mobile Application
- Cloud Deployment
- SIEM Integration
- Threat Intelligence Dashboard

---

# 👨‍💻 Author

**Soham Sakpal**

Master of Computer Applications (MCA)

Cybersecurity Enthusiast | Secure Software Development | Cryptography

GitHub:
https://github.com/mca25sakpalsoham-afk

---

# 📜 License

This project is developed for educational purposes and cybersecurity learning.

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
