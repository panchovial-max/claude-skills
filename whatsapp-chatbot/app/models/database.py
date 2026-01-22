from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    company = db.Column(db.String(255))
    service_category = db.Column(db.String(50))  # photography, video, marketing
    sub_category = db.Column(db.String(100))  # ecuestre, automotriz, etc
    budget_range = db.Column(db.String(50))
    project_description = db.Column(db.Text)
    lead_quality = db.Column(db.String(20))  # hot, warm, cold
    status = db.Column(db.String(50), default='new')  # new, qualified, contacted, converted, lost
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    conversation_id = db.Column(db.String(255))

    # Campaign Attribution
    campaign_source = db.Column(db.String(100))  # instagram_post, instagram_story, referral, google, direct
    campaign_name = db.Column(db.String(255))    # "Jan2026_Portfolio_Week1"
    utm_source = db.Column(db.String(100))
    utm_medium = db.Column(db.String(100))
    utm_campaign = db.Column(db.String(100))
    first_message = db.Column(db.Text)           # Original message for attribution analysis

    # Notion Sync
    notion_page_id = db.Column(db.String(100))   # Reference to Notion page
    
    conversations = db.relationship('Conversation', back_populates='lead', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'phone_number': self.phone_number,
            'name': self.name,
            'email': self.email,
            'company': self.company,
            'service_category': self.service_category,
            'sub_category': self.sub_category,
            'budget_range': self.budget_range,
            'lead_quality': self.lead_quality,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'campaign_source': self.campaign_source,
            'campaign_name': self.campaign_name,
            'utm_source': self.utm_source,
            'utm_medium': self.utm_medium,
            'utm_campaign': self.utm_campaign,
            'notion_page_id': self.notion_page_id
        }

class Conversation(db.Model):
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)
    message_text = db.Column(db.Text)
    sender = db.Column(db.String(20))  # 'bot' or 'user'
    flow_state = db.Column(db.String(100))  # tracking conversation step
    metadata = db.Column(db.JSON)  # store answers to qualification questions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    lead = db.relationship('Lead', back_populates='conversations')

class CampaignMetric(db.Model):
    __tablename__ = 'campaign_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'))
    metric_type = db.Column(db.String(50))  # impression, click, message, qualification, conversion
    value = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
