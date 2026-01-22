"""
Conversation flow engine for PVB Chatbot
Handles different conversation flows based on service category
Uses PVB services configuration
"""

from app.config.pvb_services import (
    WELCOME_MESSAGE_ES, WELCOME_MESSAGE_EN,
    SOURCE_QUESTION_ES, SOURCE_QUESTION_EN, CAMPAIGN_SOURCES,
    PHOTOGRAPHY_TYPE_ES, PHOTOGRAPHY_CONTEXT_ECUESTRE, PHOTOGRAPHY_CONTEXT_AUTOMOTRIZ,
    PHOTOGRAPHY_CONTEXT_ECOMMERCE, PHOTOGRAPHY_VIDEO, PHOTOGRAPHY_DATE, PHOTOGRAPHY_LOCATION,
    PHOTOGRAPHY_PRODUCTS, PHOTOGRAPHY_PRODUCT_ANGLES, PHOTOGRAPHY_ECOMMERCE_SHIPMENT, PHOTOGRAPHY_BUDGET,
    MARKETING_PROBLEM_ES, MARKETING_CAMPAIGNS, MARKETING_SPEND, MARKETING_BUDGET,
    MARKETING_RECOMMENDATION_AI, MARKETING_RECOMMENDATION_STRATEGIC, MARKETING_RECOMMENDATION_PREMIUM,
    ABOUT_PVB, ABOUT_PRICING,
    CONTACT_CAPTURE_PHOTO, CONTACT_CAPTURE_MARKETING,
    CONFIRMATION_PHOTO, CONFIRMATION_MARKETING, CLOSING_QUALIFIED,
    HANDOFF_MESSAGE, HANDOFF_CONFIRMATION,
    FAQS, LEAD_SCORING_WEIGHTS, LEAD_QUALITY_THRESHOLDS
)

class ConversationFlow:
    """Base conversation flow"""
    
    def __init__(self, language='es'):
        self.current_step = 'greeting'
        self.language = language
        self.data = {}
        self.step_counter = 0
    
    def get_greeting(self):
        """Get initial greeting - now asks source first"""
        if self.language == 'en':
            message = SOURCE_QUESTION_EN
        else:
            message = SOURCE_QUESTION_ES

        return {
            'message': message,
            'quick_replies': ['1', '2', '3', '4'],
            'next_step': 'source_question'
        }

    def handle_source_question(self, choice):
        """Handle source attribution response and move to category selection"""
        source_map = {
            '1': 'instagram_post',
            '2': 'instagram_story',
            '3': 'referral',
            '4': 'direct'
        }

        # Store source in data
        self.data['campaign_source'] = source_map.get(choice, 'direct')

        # Now show service options
        if self.language == 'en':
            message = WELCOME_MESSAGE_EN
        else:
            message = WELCOME_MESSAGE_ES

        return {
            'message': message,
            'quick_replies': ['1', '2', '3', '4'],
            'next_step': 'category_selection',
            'campaign_source': self.data['campaign_source']
        }

    def handle_category_selection(self, choice):
        """Route to appropriate service flow"""
        if choice in ['1', 'fotografía', 'foto', 'photo']:
            return {'next_flow': 'photography', 'message': PHOTOGRAPHY_TYPE_ES}
        elif choice in ['2', 'marketing', 'marketing digital']:
            return {'next_flow': 'marketing', 'message': MARKETING_PROBLEM_ES}
        elif choice in ['3', 'conocer más', 'info', 'about']:
            return {'next_flow': 'about', 'message': ABOUT_PVB}
        elif choice in ['4', 'pancho', 'hablar']:
            return {'next_flow': 'handoff', 'message': HANDOFF_MESSAGE}
        else:
            return {
                'message': "No entendí tu opción. Por favor responde con 1, 2, 3 o 4:",
                'quick_replies': ['1', '2', '3', '4']
            }


class PhotographyFlow(ConversationFlow):
    """Flow for photography & video services"""
    
    def __init__(self):
        super().__init__()
        self.current_step = 'project_type'
        self.steps = [
            'project_type',
            'context_or_type',
            'location',
            'date',
            'budget',
            'contact_capture'
        ]
    
    def get_next_message(self, current_step, user_input=None):
        """Get next message in photography flow"""
        
        if current_step == 'project_type':
            return {
                'message': PHOTOGRAPHY_TYPE_ES,
                'quick_replies': ['Ecuestre', 'Automotriz', 'Video', 'Otro'],
                'next_step': 'context_or_type'
            }
        
        elif current_step == 'context_or_type':
            if user_input and 'ecuestre' in user_input.lower():
                self.data['project_type'] = 'ecuestre'
                return {
                    'message': PHOTOGRAPHY_CONTEXT_ECUESTRE,
                    'quick_replies': ['Galería', 'Marca ecuestre', 'Uso personal', 'Evento'],
                    'next_step': 'location'
                }
            elif user_input and 'automotriz' in user_input.lower():
                self.data['project_type'] = 'automotriz'
                return {
                    'message': PHOTOGRAPHY_CONTEXT_AUTOMOTRIZ,
                    'quick_replies': ['Galería', 'Marca', 'Editorial', 'Campaña'],
                    'next_step': 'location'
                }
            elif user_input and 'ecommerce' in user_input.lower() or 'productos' in user_input.lower():
                self.data['project_type'] = 'ecommerce'
                return {
                    'message': PHOTOGRAPHY_CONTEXT_ECOMMERCE,
                    'quick_replies': ['Tienda online', 'Catálogo', 'Redes sociales', 'Lanzamiento'],
                    'next_step': 'products'
                }
            elif user_input and 'video' in user_input.lower():
                self.data['project_type'] = 'video'
                return {
                    'message': PHOTOGRAPHY_VIDEO,
                    'quick_replies': ['Comercial', 'Corporativo', 'Cinematográfico', 'Redes'],
                    'next_step': 'location'
                }
            else:
                return {
                    'message': "Por favor especifica el tipo: Ecuestre, Automotriz, E-commerce, Video, u Otro",
                    'quick_replies': ['Ecuestre', 'Automotriz', 'E-commerce', 'Video', 'Otro'],
                    'next_step': 'context_or_type'
                }
        
        elif current_step == 'products':
            self.data['context'] = user_input
            return {
                'message': PHOTOGRAPHY_PRODUCTS,
                'quick_replies': ['1-5', '6-15', '16-50', '+50'],
                'next_step': 'angles'
            }
        
        elif current_step == 'angles':
            self.data['product_count'] = user_input
            return {
                'message': PHOTOGRAPHY_PRODUCT_ANGLES,
                'quick_replies': ['Pack básico (3)', 'Pack completo (5)', 'Pack 360', 'Múltiples'],
                'next_step': 'shipment'
            }
        
        elif current_step == 'shipment':
            self.data['photo_style'] = user_input
            return {
                'message': PHOTOGRAPHY_ECOMMERCE_SHIPMENT,
                'quick_replies': ['Envío postal', 'Retiro en estudio', 'Punto de entrega', 'Otro'],
                'next_step': 'date'
            }
        
        elif current_step == 'location':
            self.data['context'] = user_input
            return {
                'message': PHOTOGRAPHY_LOCATION,
                'quick_replies': ['Por definir'],
                'next_step': 'date'
            }
        
        elif current_step == 'date':
            self.data['location'] = user_input
            return {
                'message': PHOTOGRAPHY_DATE,
                'quick_replies': [],
                'next_step': 'budget'
            }
        
        elif current_step == 'budget':
            self.data['date'] = user_input
            return {
                'message': PHOTOGRAPHY_BUDGET,
                'quick_replies': ['<1k', '1-3k', '3-10k', '>10k', 'Cotización'],
                'next_step': 'contact_capture'
            }
        
        elif current_step == 'contact_capture':
            self.data['budget'] = user_input
            return {
                'message': "Perfecto. Para poder contactarte necesitamos algunos datos:\n\n" + \
                          "\n".join([f"{k}: {v}" for k, v in CONTACT_CAPTURE_PHOTO.items()]),
                'next_step': 'confirmation'
            }
        
        elif current_step == 'confirmation':
            return {
                'message': f"✅ ¡Excelente! Hemos registrado tu proyecto de fotografía {self.data.get('project_type', '')}.\n\n" + \
                          "Pancho te contactará dentro de 24-48 horas para discutir los detalles.\n\n" + \
                          "Mientras tanto, puedes ver nuestro trabajo en: panchovial.com",
                'next_step': 'completed'
            }


class MarketingFlow(ConversationFlow):
    """Flow for marketing digital services"""
    
    def __init__(self):
        super().__init__()
        self.current_step = 'problem'
        self.steps = [
            'problem',
            'campaigns',
            'spend',
            'budget',
            'contact_capture',
            'recommendation'
        ]
    
    def get_next_message(self, current_step, user_input=None):
        """Get next message in marketing flow"""
        
        if current_step == 'problem':
            return {
                'message': MARKETING_PROBLEM_ES,
                'quick_replies': ['Más ventas', 'Anuncios no funcionan', 'Lanzar', 'Automatizar', 'No sé'],
                'next_step': 'campaigns'
            }
        
        elif current_step == 'campaigns':
            self.data['problem'] = user_input
            return {
                'message': MARKETING_CAMPAIGNS,
                'quick_replies': ['Meta Ads', 'Google Ads', 'Ambas', 'Ninguna'],
                'next_step': 'spend'
            }
        
        elif current_step == 'spend':
            self.data['campaigns'] = user_input
            return {
                'message': MARKETING_SPEND,
                'quick_replies': ['<$500', '$500-2k', '$2-5k', '>$5k'],
                'next_step': 'budget'
            }
        
        elif current_step == 'budget':
            self.data['spend'] = user_input
            
            # Determine recommendation based on budget
            if user_input and '500' in user_input or 'AI' in user_input.lower():
                self.data['recommendation'] = 'ai_ads'
                message = MARKETING_RECOMMENDATION_AI
            elif user_input and ('1' in user_input or '3' in user_input):
                self.data['recommendation'] = 'strategic'
                message = MARKETING_RECOMMENDATION_STRATEGIC
            elif user_input and ('7' in user_input or 'premium' in user_input.lower()):
                self.data['recommendation'] = 'premium'
                message = MARKETING_RECOMMENDATION_PREMIUM
            else:
                return {
                    'message': MARKETING_BUDGET,
                    'quick_replies': ['$600', '$1-3k', '$3-7k', 'Más info'],
                    'next_step': 'budget'
                }
            
            return {
                'message': message,
                'quick_replies': ['Sí', 'No', 'Más info'],
                'next_step': 'contact_capture'
            }
        
        elif current_step == 'contact_capture':
            return {
                'message': "¡Genial! Para poder ayudarte mejor, necesitamos algunos datos:\n\n" + \
                          "\n".join([f"{k}: {v}" for k, v in CONTACT_CAPTURE_MARKETING.items()]),
                'next_step': 'confirmation'
            }
        
        elif current_step == 'confirmation':
            return {
                'message': f"✅ Perfecto. Hemos registrado tu información.\n\n" + \
                          f"Pancho te contactará dentro de 24 horas para una consulta estratégica gratuita.\n\n" + \
                          "En el interim, puedes conocer más en: panchovial.com",
                'next_step': 'completed'
            }


class AboutFlow(ConversationFlow):
    """Flow for information requests"""
    
    def __init__(self):
        super().__init__()
        self.current_step = 'about_menu'
    
    def get_next_message(self, current_step, user_input=None):
        """Get next message in about flow"""
        
        if current_step == 'about_menu':
            return {
                'message': ABOUT_PVB,
                'quick_replies': ['Fotografía', 'Marketing', 'Casos', 'Precios'],
                'next_step': 'about_selection'
            }
        
        elif current_step == 'about_selection':
            if user_input and 'fotog' in user_input.lower():
                return {
                    'message': "📸 Fotografía Fine Art\n\nNos especializamos en:\n" + \
                              "🐴 Fotografía ecuestre de nivel galería\n" + \
                              "🏎️ Fotografía automotriz cinematográfica\n" + \
                              "🎬 Producción audiovisual Super Bowl\n\n" + \
                              "Ver portfolio: panchovial.com\n\n" + \
                              "¿Te gustaría saber más o comenzar un proyecto?",
                    'quick_replies': ['Sí', 'Contactar', 'Volver'],
                    'next_step': 'category_selection'
                }
            elif user_input and 'market' in user_input.lower():
                return {
                    'message': "📊 Marketing Digital con IA\n\n" + \
                              "Ofrecemos:\n" + \
                              "🤖 AI Ad Generation ($600)\n" + \
                              "📈 Paquete Estratégico ($1-3k)\n" + \
                              "🎯 Paquete Premium ($3-7k)\n\n" + \
                              "¿Te gustaría conocer más sobre alguno?",
                    'quick_replies': ['AI', 'Estratégico', 'Premium', 'Precio'],
                    'next_step': 'category_selection'
                }
            elif user_input and 'precio' in user_input.lower():
                return {
                    'message': ABOUT_PRICING,
                    'quick_replies': ['Fotografía', 'Marketing', 'Volver'],
                    'next_step': 'category_selection'
                }
            else:
                return {
                    'message': "¿Qué tipo de información buscas?",
                    'quick_replies': ['Fotografía', 'Marketing', 'Precios'],
                    'next_step': 'about_selection'
                }


class FAQFlow(ConversationFlow):
    """Flow for frequently asked questions"""
    
    def __init__(self):
        super().__init__()
    
    def get_faq_response(self, question_key):
        """Get FAQ response"""
        if question_key in FAQS:
            return FAQS[question_key]['answer']
        else:
            return "No tengo una respuesta para esa pregunta. ¿Quieres hablar directamente con Pancho?"
    
    def get_faq_options(self):
        """Get FAQ menu"""
        options = list(FAQS.keys())
        message = "¿Cuál de estas preguntas te interesa?\n\n"
        for i, key in enumerate(options, 1):
            message += f"{i}️⃣ {FAQS[key]['question']}\n"
        return {
            'message': message,
            'quick_replies': [str(i) for i in range(1, len(options) + 1)],
            'next_step': 'faq_selection'
        }


class HandoffFlow(ConversationFlow):
    """Flow for direct conversation with Pancho"""
    
    def __init__(self):
        super().__init__()
        self.current_step = 'name_capture'
    
    def get_next_message(self, current_step, user_input=None):
        """Get next message in handoff flow"""
        
        if current_step == 'name_capture':
            return {
                'message': HANDOFF_MESSAGE,
                'quick_replies': [],
                'next_step': 'handoff_confirmation'
            }
        
        elif current_step == 'handoff_confirmation':
            self.data['name'] = user_input
            return {
                'message': HANDOFF_CONFIRMATION,
                'quick_replies': ['No gracias', 'Sí, tengo una pregunta'],
                'next_step': 'completed'
            }


def route_flow(category, language='es'):
    """Route to appropriate conversation flow"""
    flows = {
        'photography': PhotographyFlow(),
        'marketing': MarketingFlow(),
        'about': AboutFlow(),
        'faq': FAQFlow(),
        'handoff': HandoffFlow()
    }
    
    flow = flows.get(category)
    if flow:
        flow.language = language
    
    return flow


def process_flow_step(flow, current_step, user_input=None):
    """Process a step in a conversation flow"""
    if isinstance(flow, PhotographyFlow):
        return flow.get_next_message(current_step, user_input)
    elif isinstance(flow, MarketingFlow):
        return flow.get_next_message(current_step, user_input)
    elif isinstance(flow, AboutFlow):
        return flow.get_next_message(current_step, user_input)
    elif isinstance(flow, FAQFlow):
        return flow.get_faq_response(user_input)
    elif isinstance(flow, HandoffFlow):
        return flow.get_next_message(current_step, user_input)
    
    return None
