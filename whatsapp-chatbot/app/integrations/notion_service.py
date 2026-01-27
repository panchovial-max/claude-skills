"""
Notion Integration Service for PVB WhatsApp Chatbot
Handles two-way sync between leads database and Notion
"""

import os
import httpx
from datetime import datetime
from typing import Optional
from notion_client import Client


class NotionService:
    """Service for syncing leads to Notion and fetching campaign content"""

    def __init__(self):
        self.api_key = os.getenv('NOTION_API_KEY')
        self.leads_db_id = os.getenv('NOTION_LEADS_DB_ID')
        self.content_db_id = os.getenv('NOTION_CONTENT_DB_ID')
        self.client = None

        if self.api_key:
            self.client = Client(auth=self.api_key)

    def is_configured(self) -> bool:
        """Check if Notion is properly configured"""
        return bool(self.api_key and self.leads_db_id)

    # =========================================================================
    # LEADS → NOTION
    # =========================================================================

    def sync_lead(self, lead_data: dict) -> Optional[str]:
        """
        Create or update a lead in Notion.
        Returns the Notion page ID.
        """
        if not self.is_configured():
            print("Notion not configured, skipping sync")
            return None

        # Check if lead already exists in Notion
        existing_page_id = lead_data.get('notion_page_id')

        if existing_page_id:
            return self._update_lead(existing_page_id, lead_data)
        else:
            # Check by phone number
            existing = self._find_lead_by_phone(lead_data.get('phone_number'))
            if existing:
                return self._update_lead(existing, lead_data)
            else:
                return self._create_lead(lead_data)

    def _create_lead(self, lead_data: dict) -> Optional[str]:
        """Create a new lead page in Notion"""
        try:
            properties = self._build_lead_properties(lead_data)

            response = self.client.pages.create(
                parent={"database_id": self.leads_db_id},
                properties=properties
            )

            page_id = response['id']
            print(f"Created Notion lead: {page_id}")
            return page_id

        except Exception as e:
            print(f"Error creating Notion lead: {e}")
            return None

    def _update_lead(self, page_id: str, lead_data: dict) -> Optional[str]:
        """Update an existing lead page in Notion"""
        try:
            properties = self._build_lead_properties(lead_data)

            self.client.pages.update(
                page_id=page_id,
                properties=properties
            )

            print(f"Updated Notion lead: {page_id}")
            return page_id

        except Exception as e:
            print(f"Error updating Notion lead: {e}")
            return None

    def _find_lead_by_phone(self, phone_number: str) -> Optional[str]:
        """Find a lead in Notion by phone number"""
        if not phone_number:
            return None

        try:
            # Use direct HTTP request since notion-client v2.7 doesn't have databases.query
            response = httpx.post(
                f'https://api.notion.com/v1/databases/{self.leads_db_id}/query',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Notion-Version': '2022-06-28',
                    'Content-Type': 'application/json'
                },
                json={
                    "filter": {
                        "property": "Phone",
                        "phone_number": {
                            "equals": phone_number
                        }
                    }
                },
                timeout=10.0
            )

            if response.status_code == 200:
                results = response.json().get('results', [])
                if results:
                    return results[0]['id']
            return None

        except Exception as e:
            print(f"Error searching Notion: {e}")
            return None

    def _build_lead_properties(self, lead_data: dict) -> dict:
        """Build Notion properties from lead data"""
        properties = {}

        # Title (Name)
        if lead_data.get('name'):
            properties['Name'] = {
                'title': [{'text': {'content': lead_data['name']}}]
            }
        else:
            properties['Name'] = {
                'title': [{'text': {'content': lead_data.get('phone_number', 'Unknown')}}]
            }

        # Phone
        if lead_data.get('phone_number'):
            properties['Phone'] = {
                'phone_number': lead_data['phone_number']
            }

        # Email
        if lead_data.get('email'):
            properties['Email'] = {
                'email': lead_data['email']
            }

        # Company
        if lead_data.get('company'):
            properties['Company'] = {
                'rich_text': [{'text': {'content': lead_data['company']}}]
            }

        # Service Category (Select)
        if lead_data.get('service_category'):
            properties['Service'] = {
                'select': {'name': lead_data['service_category'].capitalize()}
            }

        # Sub-category (Select)
        if lead_data.get('sub_category'):
            properties['Sub-category'] = {
                'select': {'name': lead_data['sub_category'].capitalize()}
            }

        # Budget (Select)
        if lead_data.get('budget_range'):
            properties['Budget'] = {
                'select': {'name': lead_data['budget_range']}
            }

        # Lead Quality (Select)
        if lead_data.get('lead_quality'):
            quality = lead_data['lead_quality'].upper()
            properties['Quality'] = {
                'select': {'name': quality}
            }

        # Status (Select - since Status type requires special setup)
        # Skip status for now as it's not configured in the database
        # if lead_data.get('status'):
        #     properties['Status'] = {
        #         'select': {'name': lead_data['status'].capitalize()}
        #     }

        # Campaign Source (Select)
        if lead_data.get('campaign_source'):
            properties['Source'] = {
                'select': {'name': lead_data['campaign_source']}
            }

        # Campaign Name (Text)
        if lead_data.get('campaign_name'):
            properties['Campaign'] = {
                'rich_text': [{'text': {'content': lead_data['campaign_name']}}]
            }

        # Notes/Description
        if lead_data.get('project_description'):
            properties['Notes'] = {
                'rich_text': [{'text': {'content': lead_data['project_description'][:2000]}}]
            }

        # Created date
        if lead_data.get('created_at'):
            created = lead_data['created_at']
            if isinstance(created, str):
                properties['Created'] = {'date': {'start': created}}
            elif isinstance(created, datetime):
                properties['Created'] = {'date': {'start': created.isoformat()}}

        return properties

    # =========================================================================
    # NOTION → BOT (Campaign Content)
    # =========================================================================

    def get_campaign_schedule(self, days_ahead: int = 7) -> list:
        """
        Fetch upcoming scheduled posts from Notion content calendar.
        Returns list of posts scheduled for the next N days.
        """
        if not self.api_key or not self.content_db_id:
            print("Content calendar not configured")
            return []

        try:
            today = datetime.utcnow().date().isoformat()

            # Use direct HTTP request since notion-client v2.7 moved query method
            response = httpx.post(
                f'https://api.notion.com/v1/databases/{self.content_db_id}/query',
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Notion-Version': '2022-06-28',
                    'Content-Type': 'application/json'
                },
                json={
                    "filter": {
                        "and": [
                            {
                                "property": "Publish Date",
                                "date": {
                                    "on_or_after": today
                                }
                            },
                            {
                                "property": "Status",
                                "select": {
                                    "equals": "Scheduled"
                                }
                            }
                        ]
                    },
                    "sorts": [
                        {
                            "property": "Publish Date",
                            "direction": "ascending"
                        }
                    ]
                },
                timeout=10.0
            )

            posts = []
            if response.status_code == 200:
                for page in response.json().get('results', []):
                    posts.append(self._parse_content_page(page))

            return posts

        except Exception as e:
            print(f"Error fetching campaign schedule: {e}")
            return []

    def get_post_by_id(self, post_id: str) -> Optional[dict]:
        """Get a specific content post from Notion by page ID"""
        if not self.client:
            return None

        try:
            page = self.client.pages.retrieve(page_id=post_id)
            return self._parse_content_page(page)
        except Exception as e:
            print(f"Error fetching post: {e}")
            return None

    def _parse_content_page(self, page: dict) -> dict:
        """Parse a Notion content page into a dict"""
        props = page.get('properties', {})

        return {
            'id': page['id'],
            # Support both naming conventions
            'title': self._get_title(props.get('Content Title', props.get('Title', {}))),
            'date': self._get_date(props.get('Publish Date', props.get('Date', {}))),
            'type': self._get_select(props.get('Type', {})),
            'status': self._get_select(props.get('Status', {})),  # Changed from _get_status
            'platform': self._get_multi_select(props.get('Channel', props.get('Platform', {}))),
            'funnel_stage': self._get_select(props.get('Funnel Stage', {})),
            'topic_cluster': self._get_select(props.get('Topic Cluster', {})),
            'target_keyword': self._get_rich_text(props.get('Target Keyword', {})),
            'campaign': self._get_rich_text(props.get('Campaign', {})),
            'cta_link': self._get_url(props.get('CTA Link', {})),
            'caption': self._get_rich_text(props.get('Caption', {}))
        }

    # =========================================================================
    # Property Helpers
    # =========================================================================

    def _get_title(self, prop: dict) -> str:
        title = prop.get('title', [])
        if title:
            return title[0].get('text', {}).get('content', '')
        return ''

    def _get_rich_text(self, prop: dict) -> str:
        text = prop.get('rich_text', [])
        if text:
            return text[0].get('text', {}).get('content', '')
        return ''

    def _get_select(self, prop: dict) -> Optional[str]:
        select = prop.get('select')
        if select:
            return select.get('name')
        return None

    def _get_multi_select(self, prop: dict) -> list:
        multi = prop.get('multi_select', [])
        return [item.get('name') for item in multi]

    def _get_status(self, prop: dict) -> Optional[str]:
        status = prop.get('status')
        if status:
            return status.get('name')
        return None

    def _get_date(self, prop: dict) -> Optional[str]:
        date = prop.get('date')
        if date:
            return date.get('start')
        return None

    def _get_url(self, prop: dict) -> Optional[str]:
        return prop.get('url')
