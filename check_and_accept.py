#!/usr/bin/env python3
"""Check mailbox, auto-accept matching assignments, forward content."""
import imaplib
import smtplib
import email
import email.utils
from email.header import decode_header
from email.mime.text import MIMEText
import os
import sys

IMAP_SERVER = os.environ.get('IMAP_HOST', 'imap.infomaniak.com')
IMAP_PORT = int(os.environ.get('IMAP_PORT', 993))
IMAP_USER = os.environ.get('IMAP_USER', 'musicom@wiertz.tech')
IMAP_PASS = os.environ.get('IMAP_PASS', '')
SMTP_SERVER = 'smtp.infomaniak.com'
SMTP_PORT = 587

SENDER = 'ax.wi@ik.me'
KEYWORDS = ['[Musicom]', '[Composition]', '[Pattern]', '[Matrix]', '[Loop]']


def decode_str(s):
    if s is None:
        return ''
    parts = decode_header(s)
    out = []
    for part, charset in parts:
        if isinstance(part, bytes):
            out.append(part.decode(charset or 'utf-8', errors='replace'))
        else:
            out.append(str(part))
    return ''.join(out)


def get_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='replace')
        for part in msg.walk():
            ct = part.get_content_type()
            if ct == 'text/html':
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode('utf-8', errors='replace')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode('utf-8', errors='replace')
    return ''


def send_reply(to_addr, subject):
    try:
        reply = MIMEText('Accepted')
        reply['From'] = IMAP_USER
        reply['To'] = to_addr
        reply['Subject'] = f'Re: {subject}'
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as s:
            s.starttls()
            s.login(IMAP_USER, IMAP_PASS)
            s.send_message(reply)
        return True
    except Exception as e:
        print(f'ERROR: Failed to send reply: {e}', file=sys.stderr)
        return False


def main():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(IMAP_USER, IMAP_PASS)
        mail.select('INBOX')
        status, data = mail.search(None, 'UNSEEN', f'(FROM "{SENDER}")')
    except Exception as e:
        print(f'ERROR: {e}', file=sys.stderr)
        print('[SILENT]', flush=True)
        sys.exit(0)

    ids = data[0].split() if data[0] else []
    if not ids:
        mail.logout()
        print('[SILENT]', flush=True)
        sys.exit(0)

    matched = False
    for mid in ids:
        status, msg_data = mail.fetch(mid, '(RFC822)')
        if status != 'OK':
            continue
        msg = email.message_from_bytes(msg_data[0][1])
        subject = decode_str(msg.get('Subject', ''))
        from_addr = decode_str(msg.get('From', ''))
        date = decode_str(msg.get('Date', ''))
        body = get_body(msg)

        if not any(kw.lower() in subject.lower() for kw in KEYWORDS):
            continue

        matched = True
        to_addr = email.utils.parseaddr(from_addr)[1] if from_addr else SENDER
        reply_ok = send_reply(to_addr, subject)

        print(f'From: {from_addr}')
        print(f'Subject: {subject}')
        print(f'Date: {date}')
        print(f'Accepted: {"OK" if reply_ok else "FAILED"}')
        print('Content:')
        print(body)
        print('---')

    mail.logout()
    if not matched:
        print('[SILENT]', flush=True)


if __name__ == '__main__':
    main()
