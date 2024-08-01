import smtplib
import subprocess

#Author: Amrit Thakur
#Email: info@mail.spu.com.np
#Purpose: Startup script that check ipv6 public ip and send it over mail

# Execute the curl command to get the public IP address
ip_address = subprocess.check_output('curl -s6 ifconfig.me', shell=True).decode('utf-8').strip()

# Define sender and receiver
sender = "Notification <noreply@example.com>"
receiver = "Amrit Thakur <receiver@example.com>"

# Create the email message
message = f"""\
Subject: IPv6 Notification
To: {receiver}
From: {sender}

Your public IP address is: {ip_address}
"""

# Send the email
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("username", "password")
    server.sendmail(sender, receiver, message)

