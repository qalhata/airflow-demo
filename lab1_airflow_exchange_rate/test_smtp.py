import smtplib
import ssl
import os
from dotenv import load_dotenv

EMAIL = "qalhatatechnologies@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465  # For SSL
SMTP_USER = os.getenv("EMAIL")  # Your Gmail username
SMTP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD") # Your Gmail password or App Password
SENDER_EMAIL = EMAIL
RECEIVER_EMAIL = "devops@qalhatatech.com" # An email address you can check

message = f"""\
Subject: SMTP SSL Test from Python

This is a test email sent from Python using smtplib with SSL on port {SMTP_PORT}."""

# Try with SSL (port 465)
print(f"Attempting to connect to {SMTP_HOST}:{SMTP_PORT} with SSL...")
context = ssl.create_default_context()
try:
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context) as server:
        print("Connected successfully with SSL.")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("Logged in successfully.")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
        print(f"Email sent successfully to {RECEIVER_EMAIL} via SSL!")
except Exception as e:
    print(f"Error with SSL on port {SMTP_PORT}: {e}")

print("-" * 30)

# Try with STARTTLS (port 587)
SMTP_PORT_STARTTLS = 587
message_starttls = f"""\
Subject: SMTP STARTTLS Test from Python

This is a test email sent from Python using smtplib with STARTTLS on port {SMTP_PORT_STARTTLS}."""

print(f"Attempting to connect to {SMTP_HOST}:{SMTP_PORT_STARTTLS} with STARTTLS...")
try:
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT_STARTTLS) as server:
        print(f"Connected successfully to port {SMTP_PORT_STARTTLS}.")
        server.starttls(context=context) # Secure the connection
        print("STARTTLS initiated successfully.")
        server.login(SMTP_USER, SMTP_PASSWORD)
        print("Logged in successfully.")
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message_starttls)
        print(f"Email sent successfully to {RECEIVER_EMAIL} via STARTTLS!")
except Exception as e:
    print(f"Error with STARTTLS on port {SMTP_PORT_STARTTLS}: {e}")
    