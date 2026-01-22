"""
Example: Test conversations with the chatbot
Run this to simulate user interactions
"""

import sys
sys.path.insert(0, '/Users/franciscovialbrown/.claude-worktrees/GitHub/crazy-mcclintock/whatsapp-chatbot')

from app.flows.conversation_engine import PhotographyFlow, MarketingFlow
from app.utils.lead_router import LeadRouter

# Test Photography Flow
print("=" * 60)
print("TEST 1: Photography Lead")
print("=" * 60)

photo_flow = PhotographyFlow()

# Simulate user interaction
user_responses = {
    'project_type': 'Ecuestre',
    'gallery_or_brand': 'Galería',
    'timeline': 'Marzo 2026',
    'budget': '>50k'
}

print("\n🎨 Photography Flow Test")
print(f"Project: {user_responses['project_type']}")
print(f"Usage: {user_responses['gallery_or_brand']}")
print(f"Timeline: {user_responses['timeline']}")
print(f"Budget: {user_responses['budget']}")

lead_data = {
    'service_category': 'photography',
    'sub_category': user_responses['project_type'],
    'use_case': user_responses['gallery_or_brand'],
    'timeline': user_responses['timeline'],
    'budget_range': user_responses['budget']
}

lead_quality = LeadRouter.determine_lead_quality(lead_data)
service_rec = LeadRouter.determine_recommended_service(lead_data)

print(f"\n✅ Lead Quality: {lead_quality.upper()}")
print(f"📋 Recommended: {service_rec['service']}")

# Test Marketing Flow
print("\n" + "=" * 60)
print("TEST 2: Marketing Lead (HOT)")
print("=" * 60)

marketing_flow = MarketingFlow()

user_responses_hot = {
    'problem': 'Optimizar',
    'current_campaigns': 'Sí',
    'current_spend': '>10k',
    'service_budget': 'Premium'
}

print("\n💰 Marketing Flow Test (HOT Lead)")
print(f"Problem: {user_responses_hot['problem']}")
print(f"Current Campaigns: {user_responses_hot['current_campaigns']}")
print(f"Current Spend: {user_responses_hot['current_spend']}")

lead_data_hot = {
    'service_category': 'marketing',
    'problem': user_responses_hot['problem'],
    'current_campaigns': user_responses_hot['current_campaigns'],
    'current_spend': user_responses_hot['current_spend']
}

lead_quality_hot = LeadRouter.determine_lead_quality(lead_data_hot)
service_rec_hot = LeadRouter.determine_recommended_service(lead_data_hot)

print(f"\n✅ Lead Quality: {lead_quality_hot.upper()}")
print(f"💡 Recommended: {service_rec_hot['service']}")
print(f"💰 Price: {service_rec_hot['price_range']}")

# Test Marketing Flow - Cold
print("\n" + "=" * 60)
print("TEST 3: Marketing Lead (COLD)")
print("=" * 60)

user_responses_cold = {
    'problem': 'Presencia',
    'current_campaigns': 'No',
    'current_spend': '<500',
    'service_budget': '600'
}

lead_data_cold = {
    'service_category': 'marketing',
    'problem': user_responses_cold['problem'],
    'current_campaigns': user_responses_cold['current_campaigns'],
    'current_spend': user_responses_cold['current_spend']
}

lead_quality_cold = LeadRouter.determine_lead_quality(lead_data_cold)
service_rec_cold = LeadRouter.determine_recommended_service(lead_data_cold)

print("\n💤 Marketing Flow Test (COLD Lead)")
print(f"Problem: {user_responses_cold['problem']}")
print(f"Current Spend: {user_responses_cold['current_spend']}")
print(f"\n✅ Lead Quality: {lead_quality_cold.upper()}")
print(f"💡 Recommended: {service_rec_cold['service']}")
print(f"💰 Price: {service_rec_cold['price_range']}")

# Test brief formatting
print("\n" + "=" * 60)
print("TEST 4: Lead Brief Format")
print("=" * 60)

test_lead = {
    'name': 'María García',
    'phone_number': '+56912345678',
    'email': 'maria@ejemplo.com',
    'company': 'Equestrian Gallery CH',
    'service_category': 'photography',
    'sub_category': 'Ecuestre',
    'budget_range': '>50k',
    'project_description': 'Sesión de fotografía ecuestre para galería de arte en Santiago'
}

brief = LeadRouter.format_lead_brief(test_lead)
print(brief)

print("\n✅ All tests completed!")
