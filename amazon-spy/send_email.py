"""
Send the daily Amazon Spy report by email.
Reads MAIL_FROM, MAIL_PASSWORD, MAIL_TO from environment variables (GitHub Secrets).
Supports Gmail (smtp.gmail.com) and Outlook/Hotmail (smtp.office365.com).
"""

import os
import smtplib
import sys
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path


def _smtp_settings(from_addr: str) -> tuple[str, int]:
    domain = from_addr.split("@")[-1].lower()
    if "gmail" in domain:
        return "smtp.gmail.com", 587
    if domain in ("hotmail.com", "outlook.com", "live.com", "msn.com"):
        return "smtp.office365.com", 587
    return "smtp.gmail.com", 587


def send(html_report_path: Path, email_body_path: Path) -> None:
    mail_from = os.environ.get("MAIL_FROM", "").strip()
    mail_password = os.environ.get("MAIL_PASSWORD", "").strip()
    mail_to = os.environ.get("MAIL_TO", "").strip()

    if not all([mail_from, mail_password, mail_to]):
        print("⚠️  Email skipped — MAIL_FROM / MAIL_PASSWORD / MAIL_TO not set in secrets.")
        return

    date_str = datetime.utcnow().strftime("%a %d %b %Y")
    subject = f"📦 Amazon Spy 🇵🇦 — {date_str}"

    msg = MIMEMultipart("mixed")
    msg["Subject"] = subject
    msg["From"] = f"Amazon Spy Bot <{mail_from}>"
    msg["To"] = mail_to

    # Email body (simplified HTML)
    body_html = email_body_path.read_text(encoding="utf-8")
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    # Attachment — full interactive report
    report_bytes = html_report_path.read_bytes()
    attachment = MIMEApplication(report_bytes, Name="reporte-completo.html")
    attachment["Content-Disposition"] = 'attachment; filename="reporte-completo.html"'
    msg.attach(attachment)

    server, port = _smtp_settings(mail_from)
    print(f"📧 Sending email to {mail_to} via {server}:{port}...")

    with smtplib.SMTP(server, port, timeout=30) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(mail_from, mail_password)
        smtp.send_message(msg)

    print(f"✅ Email sent → {mail_to}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_email.py <report.html> <email_body.html>")
        sys.exit(1)
    send(Path(sys.argv[1]), Path(sys.argv[2]))
