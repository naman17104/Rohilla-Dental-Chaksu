import os
import resend

class ResendSender:
    def __init__(self):
        resend.api_key = os.getenv("RESEND_API_KEY", "")

    async def send(self, to: str, subject: str, html: str, text: str = ""):
        if not resend.api_key:
            print("RESEND_API_KEY missing, skipping email")
            return
        params = {
            "from": os.getenv("EMAIL_FROM", "Rohilla Dental <noreply@rohilla.com>"),
            "to": [to],
            "subject": subject,
            "html": html,
            "text": text or html,
        }
        try:
            resend.Emails.send(params)
            print(f"Email sent to {to}")
        except Exception as e:
            print(f"Email failed: {e}")

    def send_sync(self, to: str, subject: str, html: str):
        import asyncio
        try:
            asyncio.run(self.send(to, subject, html))
        except:
            pass