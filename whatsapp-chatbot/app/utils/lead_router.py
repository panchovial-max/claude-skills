"""
Lead routing and handoff logic
Determines when to hand off to Pancho and sends notifications
PVB-specific scoring and service recommendations
"""

import requests
import json
import os
from datetime import datetime
from app.config.pvb_services import LEAD_SCORING_WEIGHTS, LEAD_QUALITY_THRESHOLDS, CAMPAIGN_SOURCES

class LeadRouter:
    
    @staticmethod
    def determine_lead_quality(lead_data: dict) -> str:
        """
        Evaluate lead quality based on collected data
        Uses PVB-specific scoring weights for photography and marketing
        Returns: 'hot', 'warm', or 'cold'
        """
        score = 0
        
        # Photography/Video leads scoring
        if lead_data.get('service_category') == 'photography':
            weights = LEAD_SCORING_WEIGHTS.get('photography', {})
            
            # Budget scoring for photography
            budget = lead_data.get('budget_range')
            if budget == '>10k':
                score += weights.get('budget_>10k', 3)
            elif budget == '3-10k':
                score += weights.get('budget_3-10k', 2)
            elif budget == '1-3k':
                score += weights.get('budget_1-3k', 1)
            
            # Type scoring
            if lead_data.get('project_type') in ['ecuestre', 'automotriz']:
                score += weights.get('context_gallery', 2)
            elif lead_data.get('context') == 'Galería':
                score += weights.get('context_gallery', 2)
            elif lead_data.get('context') == 'Marca':
                score += weights.get('context_brand', 1)
            
            # Additional factors
            if lead_data.get('location'):
                score += weights.get('has_location', 1)
            if lead_data.get('date'):
                score += weights.get('has_date', 1)
        
        # Marketing leads scoring
        elif lead_data.get('service_category') == 'marketing':
            weights = LEAD_SCORING_WEIGHTS.get('marketing', {})
            
            # Current spend scoring
            spend = lead_data.get('spend')
            if spend == '>5k' or '>$5k' in str(spend):
                score += weights.get('spend_>5k', 3)
            elif spend == '$2-5k' or '2-5k' in str(spend):
                score += weights.get('spend_2-5k', 2)
            elif spend == '$500-2k' or '500-2k' in str(spend):
                score += weights.get('spend_500-2k', 1)
            
            # Campaign experience
            if lead_data.get('campaigns') == 'Sí' or lead_data.get('campaigns') == 'Meta Ads':
                score += weights.get('has_campaigns', 2)
            
            # Problem scoring
            if lead_data.get('problem') == 'Anuncios no funcionan':
                score += weights.get('problem_ads_not_working', 2)
            elif lead_data.get('problem') == 'Lanzar':
                score += weights.get('problem_launch', 1)
            
            # Service budget scoring (what they can pay)
            if lead_data.get('recommendation') == 'premium':
                score += weights.get('budget_3-7k', 3)
            elif lead_data.get('recommendation') == 'strategic':
                score += weights.get('budget_1-3k', 2)
            elif lead_data.get('recommendation') == 'ai_ads':
                score += weights.get('budget_500-1k', 1)
        
        # Campaign source bonus (referrals are more valuable)
        campaign_source = lead_data.get('campaign_source')
        if campaign_source and campaign_source in CAMPAIGN_SOURCES:
            score += CAMPAIGN_SOURCES[campaign_source].get('score_bonus', 0)

        # Classification using thresholds
        thresholds = LEAD_QUALITY_THRESHOLDS
        if score >= thresholds['hot']['min']:
            return 'hot'
        elif score >= thresholds['warm']['min']:
            return 'warm'
        else:
            return 'cold'
    
    @staticmethod
    def determine_recommended_service(lead_data: dict) -> dict:
        """
        Recommend appropriate service tier based on lead data
        PVB uses 3 tiers for marketing: $600 AI Ads, $1-3k Strategic, $3-7k Premium
        """
        if lead_data.get('service_category') == 'marketing':
            spend = lead_data.get('spend', '')
            
            # Premium if high current spend
            if '>$5k' in str(spend) or '>5k' in str(spend):
                lead_data['recommendation'] = 'premium'
                return {
                    'service': 'Premium Consulting',
                    'name': 'Paquete Premium Completo',
                    'price_range': '$3,000 - $7,000',
                    'includes': [
                        'Estrategia completa de marketing',
                        'Gestión total de Meta Ads',
                        'Copywriting de respuesta directa',
                        'Secuencias de email automatizadas',
                        'Sistema de automatización personalizado',
                        'Reportes semanales',
                        'Acceso directo a Pancho'
                    ]
                }
            
            # Strategic if medium spend or campaign experience
            elif ('$2' in str(spend) or '2-5k' in str(spend) or 
                  lead_data.get('campaigns') == 'Sí'):
                lead_data['recommendation'] = 'strategic'
                return {
                    'service': 'Strategic Marketing',
                    'name': 'Paquete Estratégico',
                    'price_range': '$1,000 - $3,000',
                    'includes': [
                        'Análisis de voz de marca',
                        'Estrategia de contenido mensual',
                        'Copywriting de respuesta directa',
                        'Automatizaciones avanzadas',
                        'Soporte y optimización continua'
                    ]
                }
            
            # AI Ads for entry-level
            else:
                lead_data['recommendation'] = 'ai_ads'
                return {
                    'service': 'AI Ad Generation',
                    'name': 'AI Ad Generation',
                    'price_range': '$600',
                    'includes': [
                        'Análisis de negocio y audiencia',
                        'Generación de creativos con IA',
                        'Configuración de campañas Meta Ads',
                        'Automatización básica',
                        'Optimización de audiencias'
                    ]
                }
        
        # Photography/Video - custom quotes
        if lead_data.get('service_category') == 'photography':
            budget = lead_data.get('budget_range', '')
            if '>10k' in str(budget) or '10k' in str(budget):
                return {
                    'service': 'Premium Photography',
                    'price_range': 'Cotización personalizada (>$10,000)',
                    'description': 'Proyecto de alto presupuesto - Llamada estratégica con Pancho'
                }
            elif '3-10k' in str(budget):
                return {
                    'service': 'Professional Photography',
                    'price_range': 'Cotización $3,000 - $10,000',
                    'description': 'Proyecto profesional - Discusión de alcance'
                }
            else:
                return {
                    'service': 'Custom Photography Quote',
                    'price_range': 'Según proyecto',
                    'description': 'Evaluar detalles del proyecto'
                }
        
        return {
            'service': 'Custom Consultation',
            'price_range': 'TBD',
            'description': 'Book call with Pancho'
        }
    
    @staticmethod
    def send_admin_notification(lead_data: dict, notification_type: str = 'new_lead'):
        """
        Send notification to admin (Pancho) about new qualified lead
        Uses n8n webhook to trigger automated workflows
        Also syncs lead to Notion if configured
        """
        n8n_webhook = os.getenv('N8N_WEBHOOK_URL')

        # Determine quality and service before sending
        lead_quality = LeadRouter.determine_lead_quality(lead_data)
        recommended_service = LeadRouter.determine_recommended_service(lead_data)

        # Sync to Notion
        notion_page_id = LeadRouter.sync_to_notion(lead_data)
        if notion_page_id:
            lead_data['notion_page_id'] = notion_page_id

        if not n8n_webhook:
            print("⚠️ N8N_WEBHOOK_URL not configured")
            return notion_page_id  # Still return Notion result

        payload = {
            'notification_type': notification_type,
            'lead': lead_data,
            'timestamp': datetime.utcnow().isoformat(),
            'recommended_service': recommended_service,
            'lead_quality': lead_quality,
            'priority': lead_quality.upper(),  # HOT, WARM, or COLD
            'notification_channels': LeadRouter.get_notification_channels(lead_quality),
            'notion_page_id': notion_page_id
        }

        try:
            response = requests.post(n8n_webhook, json=payload, timeout=10)
            print(f"✅ Notification sent to n8n: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"❌ Error sending notification: {str(e)}")
            return False

    @staticmethod
    def sync_to_notion(lead_data: dict):
        """
        Sync lead to Notion database
        Returns the Notion page ID if successful
        """
        try:
            from app.integrations.notion_service import NotionService
            notion = NotionService()

            if not notion.is_configured():
                print("ℹ️ Notion not configured, skipping sync")
                return None

            page_id = notion.sync_lead(lead_data)
            if page_id:
                print(f"✅ Lead synced to Notion: {page_id}")
            return page_id

        except Exception as e:
            print(f"❌ Error syncing to Notion: {str(e)}")
            return None
    
    @staticmethod
    def get_notification_channels(lead_quality: str) -> list:
        """
        Get notification channels based on lead quality
        """
        thresholds = LEAD_QUALITY_THRESHOLDS
        return thresholds.get(lead_quality, {}).get('notification', ['email'])
    
    @staticmethod
    def format_lead_brief(lead_data: dict) -> str:
        """Format lead data as readable brief for Pancho"""
        
        quality = LeadRouter.determine_lead_quality(lead_data)
        service = LeadRouter.determine_recommended_service(lead_data)
        
        service_category = lead_data.get('service_category', 'N/A')
        
        if service_category == 'photography':
            brief = f"""
📸 NUEVO LEAD DE FOTOGRAFÍA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Nombre: {lead_data.get('name', 'N/A')}
📱 WhatsApp: {lead_data.get('phone_number', 'N/A')}
📧 Email: {lead_data.get('email', 'N/A')}
🏢 Empresa: {lead_data.get('company', 'N/A')}

📸 PROYECTO:
   Tipo: {lead_data.get('project_type', 'N/A')}
   Contexto: {lead_data.get('context', 'N/A')}
   Ubicación: {lead_data.get('location', 'N/A')}
   Fecha: {lead_data.get('date', 'N/A')}
   Presupuesto: {lead_data.get('budget_range', 'N/A')}

🔥 Calidad: {quality.upper()}
💡 Recomendación: {service.get('service')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """
        else:  # marketing
            brief = f"""
📊 NUEVO LEAD DE MARKETING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👤 Nombre: {lead_data.get('name', 'N/A')}
📱 WhatsApp: {lead_data.get('phone_number', 'N/A')}
📧 Email: {lead_data.get('email', 'N/A')}
🏢 Empresa: {lead_data.get('company', 'N/A')}

📊 MARKETING:
   Problema: {lead_data.get('problem', 'N/A')}
   Campañas actuales: {lead_data.get('campaigns', 'N/A')}
   Gasto mensual: {lead_data.get('spend', 'N/A')}
   Website: {lead_data.get('website', 'N/A')}

🔥 Calidad: {quality.upper()}
💡 Recomendación: {service.get('name')}
💰 Rango: {service.get('price_range')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """
        
        return brief
