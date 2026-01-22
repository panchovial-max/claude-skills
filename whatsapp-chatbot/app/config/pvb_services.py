"""
PVB Studio Creative - Services Configuration
Complete service offerings, messaging, and workflows
"""

# ============================================================================
# SERVICES CATALOG
# ============================================================================

SERVICES = {
    'photography': {
        'name': 'Fotografía Fine Art',
        'subtypes': {
            'ecuestre': {
                'name': 'Fotografía Ecuestre',
                'description': 'Trabajo artístico de nivel museístico para galerías',
                'portfolio': 'panchovial.com',
                'contexts': ['Galería', 'Marca ecuestre', 'Uso personal', 'Evento'],
            },
            'automotriz': {
                'name': 'Fotografía Automotriz',
                'description': 'Estética cinematográfica para galerías y marcas',
                'portfolio': 'panchovial.com',
                'contexts': ['Galería', 'Marca automotriz', 'Editorial', 'Campaña publicitaria'],
            },
            'otro': {
                'name': 'Otro tipo de fotografía',
                'description': 'Trabajos especializados a medida',
                'portfolio': 'panchovial.com',
            }
        },
        'budget_ranges': {
            '<1k': 'Menos de $1,000 USD',
            '1-3k': '$1,000 - $3,000 USD',
            '3-10k': '$3,000 - $10,000 USD',
            '>10k': 'Más de $10,000 USD',
            'custom': 'Prefiero recibir una cotización primero'
        },
        'timeline_note': 'Entrega típica 2-4 semanas después de la sesión'
    },
    'audiovisual': {
        'name': 'Producción Audiovisual',
        'description': 'Capacidad de producción nivel Super Bowl',
        'types': {
            'comercial': 'Comercial de TV/digital',
            'corporativo': 'Video corporativo',
            'cinematografico': 'Contenido cinematográfico',
            'redes': 'Contenido para redes sociales'
        },
        'portfolio': 'panchovial.com',
        'timeline_note': 'Plazo según complejidad, típicamente 4-8 semanas'
    },
    'marketing': {
        'name': 'Marketing Digital con IA',
        'tiers': {
            'ai_ads': {
                'name': 'AI Ad Generation',
                'price': '$600 USD',
                'description': 'Entrada accesible para probar el enfoque',
                'includes': [
                    'Análisis de tu negocio y audiencia',
                    'Generación de creativos con IA optimizados',
                    'Configuración de campañas en Meta Ads',
                    'Automatización básica del embudo',
                    'Optimización de audiencias',
                    'Reporte de resultados'
                ],
                'ideal_for': 'Empresas que quieren probar la estrategia antes de comprometerse'
            },
            'strategic': {
                'name': 'Paquete Estratégico',
                'price': '$1,000 - $3,000 USD',
                'description': 'Estrategia más completa',
                'includes': [
                    'Todo lo del AI Ad Generation',
                    'Análisis de voz de marca',
                    'Estrategia de contenido mensual',
                    'Copywriting de respuesta directa',
                    'Automatizaciones avanzadas',
                    'Soporte y optimización continua'
                ]
            },
            'premium': {
                'name': 'Paquete Premium Completo',
                'price': '$3,000 - $7,000 USD',
                'description': 'Servicio más completo para resultados serios',
                'includes': [
                    'Estrategia completa de marketing digital',
                    'Gestión total de Meta Ads',
                    'Copywriting de respuesta directa',
                    'Secuencias de email automatizadas',
                    'Sistema de automatización personalizado',
                    'Análisis de competencia',
                    'Reportes semanales',
                    'Acceso directo a Pancho'
                ],
                'timeline': '2-4 semanas para ver primeras métricas, 4-8 semanas para resultados consistentes'
            }
        }
    }
}

# ============================================================================
# CAMPAIGN SOURCES (for attribution tracking)
# ============================================================================

CAMPAIGN_SOURCES = {
    'instagram_post': {'name': 'Post de Instagram', 'score_bonus': 1},
    'instagram_story': {'name': 'Historia/Reel de Instagram', 'score_bonus': 1},
    'referral': {'name': 'Recomendación', 'score_bonus': 2},
    'google': {'name': 'Google', 'score_bonus': 0},
    'direct': {'name': 'Directo/Otro', 'score_bonus': 0},
}

SOURCE_QUESTION_ES = """¡Gracias por escribirnos!

Antes de continuar, ¿cómo nos encontraste?

1️⃣ Vi un post en Instagram
2️⃣ Vi una historia/reel en Instagram
3️⃣ Me lo recomendaron
4️⃣ Otro"""

SOURCE_QUESTION_EN = """Thanks for reaching out!

Before we continue, how did you find us?

1️⃣ Saw a post on Instagram
2️⃣ Saw a story/reel on Instagram
3️⃣ Someone recommended you
4️⃣ Other"""

# ============================================================================
# CONVERSATION MESSAGES
# ============================================================================

WELCOME_MESSAGE_ES = """¡Hola! 👋 Soy el asistente de PVB Estudio Creativo.

Somos un estudio boutique que combina fotografía fine art con marketing digital potenciado por IA.

¿En qué puedo ayudarte hoy?

1️⃣ Fotografía o producción audiovisual
2️⃣ Marketing digital y publicidad
3️⃣ Quiero conocer más sobre ustedes
4️⃣ Hablar directamente con Pancho

Responde con el número de tu interés:"""

WELCOME_MESSAGE_EN = """Hi! 👋 I'm the assistant for PVB Estudio Creativo.

We're a boutique studio combining fine art photography with AI-powered digital marketing.

How can I help you today?

1️⃣ Photography or video production
2️⃣ Digital marketing and advertising
3️⃣ I want to learn more about you
4️⃣ Speak directly with Pancho

Reply with your choice:"""

# ============================================================================
# PHOTOGRAPHY FLOW MESSAGES
# ============================================================================

PHOTOGRAPHY_TYPE_ES = """¡Genial! Nos especializamos en producción visual de alto nivel.

¿Qué tipo de proyecto tienes en mente?

🐴 Fotografía ecuestre
🚗 Fotografía automotriz
🛍️ Fotografía de productos (e-commerce)
🎬 Producción de video/film
📸 Otro tipo de fotografía"""

PHOTOGRAPHY_CONTEXT_ECUESTRE = """La fotografía ecuestre es una de nuestras especialidades principales.

Pancho captura la elegancia y poder de los caballos con fotos de calidad y belleza cinematográfica. Perfectas para gente que ama los caballos y quiere tener esas imágenes en su oficina o casa.

Portfolio: panchovial.com

¿Para qué necesitas las fotografías?

🏠 Para tu oficina o casa (colección personal)
🏢 Para marca o empresa ecuestre
🎯 Para eventos o campañas
📸 Simplemente porque amas los caballos"""

PHOTOGRAPHY_CONTEXT_AUTOMOTRIZ = """Nuestra fotografía automotriz tiene un enfoque cinematográfico, creando imágenes hermosas y poderosas.

Pancho captura la esencia y belleza de los autos que amas. Fotos de calidad cinematográfica perfectas para tu oficina, casa, o proyecto profesional.

Portfolio: panchovial.com

¿Cuál es el contexto del proyecto?

🏠 Para tu oficina o casa (colección personal)
🚘 Para marca, concesionario o empresa
🎯 Para campaña publicitaria o proyecto
📸 Porque amas los autos"""

PHOTOGRAPHY_CONTEXT_ECOMMERCE = """La fotografía de productos para e-commerce es crucial para vender online.

Pancho crea imágenes de alta calidad que muestran tus productos de la mejor manera, aumentando conversiones y atrayendo clientes.

Portfolio: panchovial.com

¿Para qué necesitas las fotos de productos?

🛒 Para tu tienda online (Shopify, WooCommerce, etc)
📦 Para catalogo de precios/distribuidor
📱 Para Instagram y redes sociales
🎯 Para campaña de lanzamiento de productos"""

PHOTOGRAPHY_PRODUCT_ANGLES = """¿Qué estilos de fotos necesitas para cada producto?

📸 Pack básico (3 fotos)
   • Frente
   • 3/4
   • Lado

📸📸 Pack completo (5 fotos)
   • Frente
   • 3/4
   • Lado
   • Detalle (zoom)
   • Estilo/Lifestyle (en contexto)

📸📸📸 Pack 360 (Video/múltiples ángulos)
   • Rotación completa 360°
   • Ideal para e-commerce interactivo
   • Aumenta conversión significativamente"""

PHOTOGRAPHY_ECOMMERCE_SHIPMENT = """Los productos se fotografían en el Estudio PVB para garantizar calidad, iluminación y consistencia perfectas.

¿Cómo prefieres hacer llegar tus productos?

📮 Envío postal (recomendado para provincias)
🚗 Retiro en estudio PVB (si eres de Santiago)
📍 Punto de entrega acordado
🤝 Otro método"""

PHOTOGRAPHY_VIDEO = """Pancho es director y fotógrafo con experiencia en producciones audiovisuales internacionales de nivel Super Bowl.

Tenemos capacidad completa de producción:
• Dirección cinematográfica
• Producción audiovisual premium
• Experiencia en proyectos internacionales

¿Qué tipo de producción necesitas?

📺 Comercial de TV/digital
🎥 Video corporativo
🎬 Contenido cinematográfico
📱 Contenido para redes sociales (premium)"""

PHOTOGRAPHY_DATE = "📅 ¿Tienes una fecha tentativa para el proyecto?"

PHOTOGRAPHY_LOCATION = """📍 ¿Tienes una ubicación en mente para el proyecto?

(Si aún no lo sabes, no hay problema)"""

PHOTOGRAPHY_PRODUCTS = """¿Cuántos productos necesitas fotografiar?

📦 1-5 productos
📦📦 6-15 productos
📦📦📦 16-50 productos
📦📦📦📦 Más de 50 productos"""

PHOTOGRAPHY_BUDGET = """¿Tienes un presupuesto aproximado en mente?

💰 Menos de $1,000 USD
💰 $1,000 - $3,000 USD
💰 $3,000 - $10,000 USD
💰💰 Más de $10,000 USD
💰💰💰 Prefiero recibir una cotización primero"""

# ============================================================================
# MARKETING FLOW MESSAGES
# ============================================================================

MARKETING_PROBLEM_ES = """¡Perfecto! En PVB combinamos estrategia de marketing con inteligencia artificial para maximizar resultados.

¿Cuál es tu principal desafío ahora mismo?

📈 Necesito más ventas/clientes
🎯 Mis anuncios no están funcionando bien
🚀 Quiero lanzar un producto/servicio
🤖 Me interesa automatizar mi marketing
💡 No sé por dónde empezar"""

MARKETING_CAMPAIGNS = """¿Ya tienes campañas de publicidad activas?

✅ Sí, en Meta (Facebook/Instagram)
✅ Sí, en Google Ads
✅ Sí, en ambas plataformas
❌ No tengo campañas activas
🤷 Tuve antes pero las pausé"""

MARKETING_SPEND = """¿Cuánto estás invirtiendo actualmente en publicidad al mes?

💵 Menos de $500 USD
💵 $500 - $2,000 USD
💵 $2,000 - $5,000 USD
💵💵 Más de $5,000 USD"""

MARKETING_BUDGET = """¿Cuál es tu presupuesto para servicios de marketing?

🟢 $500 - $1,000 USD (Servicio AI Ad Generation)
🟡 $1,000 - $3,000 USD (Paquete Estratégico)
🔵 $3,000 - $7,000 USD (Paquete Premium)
⚪ Prefiero conocer opciones primero"""

# Service recommendations based on budget
MARKETING_RECOMMENDATION_AI = """Perfecto. Nuestro servicio de AI Ad Generation ($600 USD) es ideal para ti:

✅ Generación de anuncios optimizados con IA
✅ Configuración de campañas en Meta Ads
✅ Automatización básica con n8n
✅ Optimización inicial de audiencias
✅ Reporte de resultados

Es la forma más accesible de probar nuestro enfoque antes de escalar.

¿Te gustaría agendar una llamada para conocer más detalles?"""

MARKETING_RECOMMENDATION_STRATEGIC = """Con ese presupuesto podemos hacer un trabajo estratégico más completo:

✅ Todo lo del paquete AI Ad Generation
✅ Análisis de voz de marca
✅ Estrategia de contenido mensual
✅ Copywriting de respuesta directa
✅ Automatizaciones avanzadas
✅ Soporte y optimización continua

¿Quieres que Pancho te explique cómo funcionaría para tu caso específico?"""

MARKETING_RECOMMENDATION_PREMIUM = """Excelente. Con el paquete Premium tienes acceso a todo nuestro arsenal:

✅ Estrategia completa de marketing digital
✅ Gestión total de Meta Ads
✅ Copywriting de respuesta directa
✅ Secuencias de email automatizadas
✅ Sistema de automatización personalizado
✅ Análisis de competencia
✅ Reportes semanales
✅ Acceso directo a Pancho

Este es nuestro servicio más completo para empresas que quieren resultados serios.

¿Agendamos una llamada estratégica?"""

# ============================================================================
# ABOUT PVB MESSAGES
# ============================================================================

ABOUT_PVB = """¡Con gusto te cuento sobre nosotros!

PVB Estudio Creativo es un estudio boutique fundado por Pancho Vial.

Pancho es fotógrafo y director especializado en capturar la belleza de lo que te apasiona:
• Caballos con toda su elegancia
• Autos con toda su potencia
• Producciones audiovisuales de nivel premium

Nuestro enfoque: crear fotos y videos de calidad y bonitas que luzcan espectaculares en tu oficina, casa, o proyectos profesionales.

Además:
🤖 MARKETING ESTRATÉGICO
• Marketing digital potenciado por IA
• Automatización y resultados medibles
• Estrategia para creativos y empresas

📍 Basado en Chile

¿Qué te gustaría saber más?

1️⃣ Sobre fotografía y producciones
2️⃣ Sobre marketing digital
3️⃣ Ver portfolio
4️⃣ Conocer precios"""

ABOUT_PRICING = """Nuestros servicios tienen diferentes rangos:

📸 FOTOGRAFÍA Y VIDEO
Cotización personalizada según el proyecto.
Desde $1,000 USD para sesiones hasta proyectos de producción mayores.

🤖 MARKETING DIGITAL
- AI Ad Generation: $600 USD
- Paquete Estratégico: $1,000 - $3,000 USD
- Paquete Premium: $3,000 - $7,000 USD

Todos los precios incluyen una consulta inicial gratuita para entender tu caso.

¿Sobre cuál te gustaría más información?"""

# ============================================================================
# CONTACT CAPTURE
# ============================================================================

CONTACT_CAPTURE_PHOTO = {
    'name': "👤 Tu nombre:",
    'company': "🏢 Empresa o marca (si aplica):",
    'email': "📧 Email:",
    'whatsapp': "📱 WhatsApp (para coordinar):"
}

CONTACT_CAPTURE_MARKETING = {
    'name': "👤 Tu nombre:",
    'company': "🏢 Nombre de tu empresa/marca:",
    'website': "🌐 Website o Instagram (si tienes):",
    'email': "📧 Email:",
    'whatsapp': "📱 WhatsApp:",
    'description': "💬 Cuéntame brevemente sobre tu negocio y qué vendes:"
}

# ============================================================================
# FAQs
# ============================================================================

FAQS = {
    'ubicacion': {
        'question': '¿Dónde están ubicados?',
        'answer': """Estamos basados en Chile 🇨🇱, pero trabajamos con clientes internacionales.

Para fotografía, Pancho puede viajar según el proyecto.
Para marketing digital, trabajamos 100% remoto con clientes de cualquier parte del mundo.

¿De dónde nos escribes?"""
    },
    'empresas_pequenas': {
        'question': '¿Trabajan con empresas pequeñas?',
        'answer': """¡Absolutamente! 

Nuestro servicio de AI Ad Generation ($600 USD) está diseñado específicamente como punto de entrada accesible para empresas que quieren probar el marketing profesional sin una inversión enorme.

Es la mejor forma de ver resultados antes de escalar.

¿Te gustaría conocer más sobre este servicio?"""
    },
    'tiempo_resultados': {
        'question': '¿Cuánto tiempo toma ver resultados?',
        'answer': """Depende del servicio:

📸 Fotografía: Entrega típica de 2-4 semanas después de la sesión

📈 Marketing:
- Primeras métricas: 1-2 semanas
- Resultados consistentes: 4-8 semanas
- Optimización completa: 2-3 meses

El marketing no es magia instantánea, pero con el enfoque correcto los resultados llegan.

¿Tienes alguna urgencia específica?"""
    },
    'que_incluye_600': {
        'question': '¿Qué incluye el servicio de $600?',
        'answer': """El servicio de AI Ad Generation incluye:

✅ Análisis de tu negocio y audiencia
✅ Generación de creativos con IA optimizados
✅ Configuración de campañas en Meta Ads
✅ Automatización básica del embudo
✅ Optimización de audiencias
✅ Reporte de resultados

Es ideal para probar nuestro enfoque antes de pasar a paquetes mayores.

¿Quieres que te explique cómo funcionaría para tu negocio?"""
    },
    'formas_pago': {
        'question': '¿Qué formas de pago aceptan?',
        'answer': """Aceptamos:

💳 Transferencia bancaria (Chile)
💳 PayPal (internacional)
💳 Transferencia USD (internacional)

Para proyectos grandes, podemos acordar pagos en cuotas.

¿Tienes alguna preferencia o necesidad especial?"""
    },
    'idiomas': {
        'question': '¿Hablan inglés?',
        'answer': """¡Yes! Pancho is fully bilingual (Spanish/English).

We work with international clients and all our services are available in English.

Would you like to continue in English?"""
    }
}

# ============================================================================
# FOLLOW-UP MESSAGES
# ============================================================================

FOLLOWUP_24H = """¡Hola! 👋

Vi que estuviste interesado en [SERVICIO] pero no alcanzamos a completar la conversación.

¿Hay algo más que pueda ayudarte o alguna pregunta que tengas?

Estoy aquí para ayudarte."""

FOLLOWUP_3D = """Hola de nuevo 👋

Solo quería recordarte que Pancho está disponible para una consulta gratuita sobre [TEMA DE INTERÉS].

Sin compromiso, solo para entender tu caso y ver si podemos ayudarte.

¿Te gustaría agendar 15 minutos esta semana?"""

FOLLOWUP_7D = """¡Hola! Último mensaje, lo prometo 😊

Si en algún momento necesitas ayuda con fotografía o marketing, aquí estaremos.

Puedes escribirnos cuando quieras.

¡Éxito con tus proyectos!"""

# ============================================================================
# CONFIRMATION MESSAGES
# ============================================================================

CONFIRMATION_PHOTO = """✅ ¡Perfecto! Resumen de tu solicitud:

- Proyecto: [TIPO]
- Contexto: [CONTEXTO]
- Fecha tentativa: [FECHA]
- Ubicación: [LUGAR]
- Presupuesto: [RANGO]

Pancho te contactará dentro de las próximas 24-48 horas para discutir los detalles.

¿Hay algo más que quieras agregar sobre tu proyecto?"""

CONFIRMATION_MARKETING = """✅ ¡Perfecto! He registrado tu información:

- Nombre: [NOMBRE]
- Empresa: [EMPRESA]
- Problema: [PROBLEMA]
- Presupuesto: [RANGO]
- Servicio recomendado: [SERVICIO]

Pancho te contactará dentro de 24 horas para una llamada estratégica gratuita donde analizaremos tu caso específico.

Mientras tanto, ¿tienes alguna pregunta?"""

CLOSING_QUALIFIED = """¡Excelente! 🎉

He registrado toda tu información. Pancho te contactará pronto para discutir los detalles.

Mientras tanto:
📸 Puedes ver nuestro trabajo en panchovial.com
📱 Síguenos en Instagram

¡Gracias por tu interés en PVB Estudio Creativo!"""

CLOSING_NOT_READY = """¡Entendido! No hay presión.

Cuando estés listo para dar el siguiente paso, aquí estaremos.

Te dejo algunos recursos mientras tanto:
🌐 Portfolio: panchovial.com
📱 Instagram: @panchovial

¡Éxito con tu proyecto!"""

# ============================================================================
# HANDOFF TO PANCHO
# ============================================================================

HANDOFF_MESSAGE = """¡Claro! Pancho estará encantado de hablar contigo.

Para que pueda prepararse para la conversación:

👤 ¿Cuál es tu nombre?"""

HANDOFF_CONFIRMATION = """✅ Perfecto. Le he notificado a Pancho sobre tu interés.

Te contactará dentro de las próximas 24 horas.

Si es urgente, puedes escribirle directamente a su WhatsApp.

¿Hay algo más en lo que pueda ayudarte mientras tanto?"""

# ============================================================================
# LEAD QUALITY SCORING
# ============================================================================

LEAD_SCORING_WEIGHTS = {
    'photography': {
        'budget_>10k': 3,
        'budget_3-10k': 2,
        'budget_1-3k': 1,
        'context_gallery': 2,
        'context_brand': 1,
        'has_location': 1,
        'has_date': 1
    },
    'marketing': {
        'spend_>5k': 3,
        'spend_2-5k': 2,
        'spend_500-2k': 1,
        'has_campaigns': 2,
        'problem_ads_not_working': 2,
        'problem_launch': 1,
        'budget_3-7k': 3,
        'budget_1-3k': 2,
        'budget_500-1k': 1
    }
}

LEAD_QUALITY_THRESHOLDS = {
    'hot': {'min': 5, 'notification': ['email', 'whatsapp']},
    'warm': {'min': 3, 'notification': ['email']},
    'cold': {'min': 0, 'notification': ['email']}
}
