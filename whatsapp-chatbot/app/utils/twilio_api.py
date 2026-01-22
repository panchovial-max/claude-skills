"""
Twilio WhatsApp API integration
Alternative to Meta Cloud API - works without Meta Business verification
"""

import os
from typing import Optional, Dict, List
from twilio.rest import Client
from twilio.request_validator import RequestValidator


class TwilioWhatsAppAPI:
    """
    Twilio WhatsApp API client.
    Compatible interface with MetaWhatsAppAPI for easy switching.
    """

    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

        self.client = None
        self.validator = None

        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.validator = RequestValidator(self.auth_token)

    def is_configured(self) -> bool:
        """Check if Twilio is properly configured"""
        return bool(self.account_sid and self.auth_token and self.client)

    def verify_webhook(self, url: str, params: dict, signature: str) -> bool:
        """Verify webhook signature from Twilio"""
        if not self.validator:
            return False
        return self.validator.validate(url, params, signature)

    def send_text_message(self, phone_number: str, message: str) -> Dict:
        """Send a simple text message via WhatsApp"""
        if not self.client:
            return {'error': 'Twilio not configured'}

        # Ensure WhatsApp format
        to_number = self._format_whatsapp_number(phone_number)

        try:
            msg = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_number
            )

            return {
                'success': True,
                'message_sid': msg.sid,
                'status': msg.status,
                'to': msg.to
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def send_interactive_message(self, phone_number: str, message_text: str,
                                 buttons: List[str], message_id: Optional[str] = None) -> Dict:
        """
        Send message with button options.
        Note: Twilio doesn't support native WhatsApp buttons in sandbox mode.
        We simulate with numbered options in the message text.
        """
        if not self.client:
            return {'error': 'Twilio not configured'}

        # Build message with numbered options
        full_message = message_text
        if buttons:
            full_message += "\n\n"
            for idx, button in enumerate(buttons[:10], 1):
                full_message += f"{idx}️⃣ {button}\n"

        return self.send_text_message(phone_number, full_message)

    def send_template_message(self, phone_number: str, template_name: str,
                             parameters: Optional[List[str]] = None) -> Dict:
        """
        Send template message.
        Note: Twilio uses Content Templates which need to be created in Twilio Console.
        For sandbox, we just send a regular message.
        """
        if not self.client:
            return {'error': 'Twilio not configured'}

        # For sandbox, send as regular message
        # In production, you'd use Twilio Content API
        message = f"[Template: {template_name}]"
        if parameters:
            message += f"\n{', '.join(parameters)}"

        return self.send_text_message(phone_number, message)

    def mark_message_as_read(self, message_id: str) -> Dict:
        """
        Mark message as read.
        Note: Twilio doesn't have this feature - WhatsApp shows read receipts automatically.
        """
        return {'success': True, 'note': 'Twilio handles read receipts automatically'}

    def send_media_message(self, phone_number: str, media_url: str,
                          caption: Optional[str] = None) -> Dict:
        """Send image/video/document via WhatsApp"""
        if not self.client:
            return {'error': 'Twilio not configured'}

        to_number = self._format_whatsapp_number(phone_number)

        try:
            msg = self.client.messages.create(
                body=caption or '',
                from_=self.whatsapp_number,
                to=to_number,
                media_url=[media_url]
            )

            return {
                'success': True,
                'message_sid': msg.sid,
                'status': msg.status
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def _format_whatsapp_number(self, phone_number: str) -> str:
        """Format phone number for WhatsApp"""
        # Remove any existing whatsapp: prefix
        number = phone_number.replace('whatsapp:', '')

        # Ensure + prefix
        if not number.startswith('+'):
            number = '+' + number

        # Add whatsapp: prefix
        return f'whatsapp:{number}'

    @staticmethod
    def parse_incoming_message(request_form: dict) -> dict:
        """
        Parse incoming webhook data from Twilio.
        Returns standardized format compatible with Meta API parser.
        """
        return {
            'from': request_form.get('From', '').replace('whatsapp:', ''),
            'to': request_form.get('To', '').replace('whatsapp:', ''),
            'body': request_form.get('Body', ''),
            'message_sid': request_form.get('MessageSid', ''),
            'num_media': int(request_form.get('NumMedia', 0)),
            'profile_name': request_form.get('ProfileName', ''),
            'wa_id': request_form.get('WaId', ''),
            # Media attachments
            'media_url': request_form.get('MediaUrl0'),
            'media_type': request_form.get('MediaContentType0'),
        }


# Factory function to get the appropriate API based on config
def get_whatsapp_api():
    """
    Returns the configured WhatsApp API client.
    Prefers Twilio if configured, falls back to Meta.
    """
    twilio_sid = os.getenv('TWILIO_ACCOUNT_SID')

    if twilio_sid:
        return TwilioWhatsAppAPI()
    else:
        from app.utils.meta_api import MetaWhatsAppAPI
        return MetaWhatsAppAPI()
