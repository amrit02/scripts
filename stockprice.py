#Author: Amrit Thakur
#Email: info@mail.spu.com.np
#Purpose: Script that check LTP stock price againest given target price and if price is low or equals, send it over mail

import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import re

# Configuration
stocks = {
    "NABIL": 605,
    "NRIC": 1700,
    "NLIC": 800,
    "NICA": 400
}
base_url = "https://www.sharesansar.com/company/"

# Mailtrap SMTP settings
smtp_server = "live.smtp.mailtrap.io"
smtp_port = 587
smtp_username = "api"
smtp_password = "****************************************"  # Replace with your Mailtrap API token

# Email addresses
sender = "Share Price <no-reply@netronicstech.com.np>"
receiver = "<amritn.thakur@gmail.com>"

# Function to get LTP
def get_ltp(symbol):
    url = f"{base_url}{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    match = re.search(r"Ltp:\s*([\d,.]+)", text)
    if match:
        try:
            return float(match.group(1).replace(",", ""))
        except ValueError:
            return None
    return None

# Check all stocks
alerts = []
for symbol, target in stocks.items():
    ltp = get_ltp(symbol)
    if ltp is not None:
        print(f"{symbol}: LTP = NPR {ltp}")
        if ltp <= target:
            alerts.append(f"{symbol}: LTP = NPR {ltp} (Target: NPR {target})")
    else:
        print(f"{symbol}: Failed to retrieve LTP.")

# Send email if any alerts
if alerts:
    subject = "📉 Stock Price Alert"
    body = "The following stocks have met or dropped below their target prices:\n\n" + "\n".join(alerts)
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender, receiver, msg.as_string())
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
else:
    print("No stocks met the target price. No email sent.")
