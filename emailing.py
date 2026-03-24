import smtplib
import imghdr
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SENDER = os.getenv("EMAIL_SENDER")
PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER = os.getenv("EMAIL_RECEIVER")

def send_email(image_path):
    print("Sending email...")
    email_message = EmailMessage()
    email_message["Subject"] = "New customer showed up"
    email_message["From"] = SENDER 
    email_message["To"] = RECEIVER  
    email_message.set_content("Hey, A new customer just showed up")

    with open(image_path, "rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype= "image", subtype = imghdr.what(None, content))

    try:
        gmail = smtplib.SMTP("smtp.gmail.com", 587) 
        gmail.ehlo()
        gmail.starttls()
        gmail.login(SENDER, PASSWORD)
        gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
        gmail.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")