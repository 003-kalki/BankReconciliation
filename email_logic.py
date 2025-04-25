
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachments():
    from_email = "add your email"
    from_password = " "
    to_email = "add recepients email"

    subject = "Mismatched Transactions Report"
    body = "Hi,\n\nPlease find attached the mismatched transactions report and summary.\n\nThanks,\nShyam"

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachments = ["mismatched_transactions.csv", "summary_report.txt"]

    for file_path in attachments:
        try:
            with open(file_path, "rb") as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={file_path}')
                msg.attach(part)
        except Exception as e:
            print(f"⚠️ Could not attach file {file_path}: {e}")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, from_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f" Failed to send email: {e}")

