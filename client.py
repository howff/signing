#!/usr/bin/env python3

import smtplib
import ssl
from email.mime.text import MIMEText

# Configuration
port = 8587
smtp_server = "localhost"
login = "user@example.com"
password = "secret123"

sender_email = "fake@example.com"
receiver_email = "billgates@microsoft.com"

# Plain text content
text = """\
Hi,
How's it going?
Bye.
"""

# Create MIMEText object
message = MIMEText(text, "plain")
message["Subject"] = "Plain text email"
message["From"] = sender_email
message["To"] = receiver_email

# Send the email
with smtplib.SMTP(smtp_server, port) as server:
    server.starttls(context = ssl.create_default_context())  # use None to disable cert checks
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

print('Sent')
