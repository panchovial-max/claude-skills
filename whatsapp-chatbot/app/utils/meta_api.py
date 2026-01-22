"""
Meta WhatsApp Cloud API integration
Handles sending messages and webhook verification
"""

import requests
import json
import os
import hmac
import hashlib
from typing import Optional, Dict, List

class MetaWhatsAppAPI:
    
    def __init__(self):
        self.api_version = os.getenv('META_API_VERSION', 'v18.0')
        self.access_token = os.getenv('META_ACCESS_TOKEN')
        self.phone_number_id = os.getenv('META_PHONE_NUMBER_ID')
        self.verify_token = os.getenv('META_VERIFY_TOKEN')
        self.base_url = f"https://graph.instagram.com/{self.api_version}"
    
    def verify_webhook(self, request_body: str, signature: str) -> bool:
        """Verify webhook signature from Meta"""
        hash_object = hmac.new(
            self.verify_token.encode(),
            request_body.encode(),
            hashlib.sha256
        )
        expected_signature = hash_object.hexdigest()
        return hmac.compare_digest(signature, expected_signature)
    
    def send_text_message(self, phone_number: str, message: str) -> Dict:
        """Send a simple text message"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'text',
            'text': {
                'body': message
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    def send_interactive_message(self, phone_number: str, message_text: str, 
                                 buttons: List[str], message_id: Optional[str] = None) -> Dict:
        """Send interactive message with quick reply buttons"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        # Build quick replies
        quick_replies = []
        for idx, button_text in enumerate(buttons[:3]):  # Max 3 quick replies
            quick_replies.append({
                'type': 'quick_reply',
                'quick_reply': {
                    'id': f'btn_{idx}',
                    'title': button_text
                }
            })
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'interactive',
            'interactive': {
                'type': 'button',
                'body': {
                    'text': message_text
                },
                'action': {
                    'buttons': quick_replies
                }
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    def send_template_message(self, phone_number: str, template_name: str, 
                             parameters: Optional[List[str]] = None) -> Dict:
        """Send pre-approved template message"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        body_params = [{'type': 'text', 'text': param} for param in (parameters or [])]
        
        data = {
            'messaging_product': 'whatsapp',
            'to': phone_number,
            'type': 'template',
            'template': {
                'name': template_name,
                'language': {
                    'code': 'es_ES'
                },
                'components': [
                    {
                        'type': 'body',
                        'parameters': body_params
                    }
                ] if body_params else []
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    
    def mark_message_as_read(self, message_id: str) -> Dict:
        """Mark incoming message as read"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message_id
        }
        
        response = requests.post(url, json=data, headers=headers)
        return response.json()
