import smtplib
from email.mime.text import MIMEText


def send_invite_email(to_email, invite_link):

    sender = "jagh2292@gmail.com"
    password = "dcfo tcro ergq hrfm"

    msg = MIMEText(
        f"You were invited to join a league.\n\nClick here:\n{invite_link}"
    )

    msg["Subject"] = "League Invitation"
    msg["From"] = sender
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.sendmail(sender, to_email, msg.as_string())