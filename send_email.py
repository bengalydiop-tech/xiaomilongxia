#!/usr/bin/env python3
"""小艾邮件发送脚本 - 企业邮箱版"""

import smtplib
import sys
import os
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

ENV_FILE = os.path.join(os.path.dirname(__file__), '.env.email')

def load_config():
    config = {}
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                config[k.strip()] = v.strip()
    return config

def send_email(to, subject, body, html=False):
    cfg = load_config()
    
    msg = MIMEMultipart()
    msg['From'] = cfg['EMAIL_ADDRESS']
    msg['To'] = to
    msg['Subject'] = Header(subject, 'utf-8')
    
    content_type = 'html' if html else 'plain'
    msg.attach(MIMEText(body, content_type, 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL(cfg['EMAIL_SMTP_HOST'], int(cfg['EMAIL_SMTP_PORT']))
        server.login(cfg['EMAIL_ADDRESS'], cfg['EMAIL_PASSWORD'])
        server.sendmail(cfg['EMAIL_ADDRESS'], [to], msg.as_string())
        server.quit()
        print(json.dumps({"status": "ok", "to": to, "subject": subject}, ensure_ascii=False))
        return True
    except Exception as e:
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False))
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: send_email.py <to> <subject> <body> [--html]')
        sys.exit(1)
    
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    html = '--html' in sys.argv
    
    success = send_email(to, subject, body, html)
    sys.exit(0 if success else 1)
