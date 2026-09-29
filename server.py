#!/usr/bin/env python3

import argparse
import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message
from aiosmtpd.smtp import AuthResult, LoginPassword
import datetime
from email.message import EmailMessage
import os
import ssl
import sys
import time

hostname = ""
hostport = 8587

# ========== AUTHENTICATOR ==========
class Authenticator:
    def __init__(self):
        pass
    def __call__(self, server, session, envelope, mechanism, auth_data):
        # Allow everyone!
        return AuthResult(success=True)


# ========== MESSAGE HANDLER ==========
class MailHandler():
    async def handle_DATA(self, server, session, envelope):
        # Display message on console
        print("=== Email Received ===")
        print("From:", envelope.mail_from)
        print("To:", envelope.rcpt_tos)
        print("Body:\n", envelope.content.decode('utf-8', errors='replace'))
        print("======================")
        # Respond to sender
        return "250 Message accepted"

# ========== CONTROLLER ==========
def main():
    global hostname
    global hostport

    hostname = os.environ.get('SMTPHOST', hostname)
    hostport = int(os.environ.get('SMTPPORT', str(hostport)))

    parser = argparse.ArgumentParser(description='smtpserver')
    parser.add_argument('--port', action="store", help='port on which to listen')
    parser.add_argument('--host', action="store", help='network interface on which to listen')
    args = parser.parse_args()
    if args.port:
        hostport = int(args.port)
    if args.host:
        hostname = args.host

    # SSL context for STARTTLE
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain("server.pem", "server.key")  # your cert + key

    #loop = asyncio.new_event_loop()

    controller = Controller(
        handler = MailHandler(),
        hostname=hostname,
        port=hostport,
        auth_required=True,
        authenticator=Authenticator(),
        tls_context=context,
        require_starttls=True,
        #loop=loop,
    )

    controller.start()
    print(f"{datetime.datetime.now()} SMTP server with STARTTLS running at host '{hostname}' on port {hostport}...")
    controller._thread.join()

    #try:
    #    #asyncio.get_event_loop().run_forever()
    #    #loop.run_forever()
    #    time.sleep(1)
    #except KeyboardInterrupt:
    #    print("Shutting down...")
    #    controller.stop()
    #    #loop.stop()


if __name__ == "__main__":
    main()
