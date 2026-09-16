from typing import Any
from receptionist.email_service.templates import build_info_packet_email
from receptionist.email_service.smtp import SMTPSender

class EmailChannel:
    def __init__(self, config: Any):
        self.config = config
        self.sender_type = getattr(config, 'sender_type', 'smtp')
        # init sender based on type
        if self.sender_type == 'smtp':
            self.sender = SMTPSender(config)
        else:
            raise ValueError(f"Unknown email sender type: {self.sender_type}")

    def send(self, to: str, subject: str, body: str, **kwargs):
        # if file is unreadable, the email must still send.
        try:
            return self.sender.send(to=to, subject=subject, body=body, **kwargs)
        except Exception as e:
            print(f"Email send failed: {e}")
            # fallback - do not crash the app
            return False

    def send_info_packet(self, to: str, packet: dict):
        email_data = build_info_packet_email(packet)
        return self.send(
            to=to,
            subject=email_data.get('subject', 'Info Packet'),
            body=email_data.get('body', '')
        )
