# Setup Workflow: Image Generation with Weavy + Notion + Google Drive

## Overview
Este workflow automatiza la generación de 5 variaciones de imágenes basadas en un brief creativo capturado en Notion, usando Weavy como motor de diseño, y almacena las imágenes en Google Drive con actualización automática del enlace en la página de Notion.

---

## 📋 Flujo del Workflow

```
[1] Notion Trigger
    ↓
[2] Extrae detalles del brief (cliente, descripción, estilo, colores, público)
    ↓
[3] Construye prompt creativo
    ↓
[4] Envía a Weavy API para generar 5 variaciones
    ↓
[5] Crea carpeta en Google Drive con nombre del cliente
    ↓
[6] Carga todas las imágenes generadas en Google Drive
    ↓
[7] Actualiza página de Notion con enlace de Google Drive
    ↓
[8] Envía notificación por email a Pancho
```

---

## 🔧 Requisitos Previos

### 1. **Notion Setup**
Necesitas una base de datos en Notion con los siguientes campos:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| **Cliente** | Text | Nombre del cliente |
| **Descripción del proyecto** | Rich Text | Detalles del proyecto |
| **Estilo visual** | Select | Opciones: minimalista, colorido, elegante, moderno, vintage |
| **Paleta de colores** | Rich Text | Ej: "Azul marino, blanco, dorado" |
| **Público objetivo** | Rich Text | Descripción del público |
| **Notas específicas PVB** | Rich Text | Contexto adicional |
| **Listo para generar imágenes** | Checkbox | TRUE cuando el brief esté completo |
| **Google Drive Link** | URL | Se actualiza automáticamente con el enlace |

### 2. **APIs y Credenciales Necesarias**

#### Weavy API
- Regístrate en [Weavy.ai](https://app.weavy.ai/)
- Obtén tu API Key
- En n8n: Crear credencial `weavy_api_key`

#### Google Drive OAuth
- En n8n: Conectar con tu cuenta de Google
- Credencial: `google_drive_oauth`
- Permisos necesarios: crear carpetas, subir archivos, compartir

#### Notion API
- En Notion: Settings → Integrations → Create new integration
- Copiar Integration Token
- En n8n: Crear credencial `notion_api`

---

## 📌 Configuración en n8n

### Paso 1: Importar el Workflow
1. En n8n: **Workflows** → **Import**
2. Cargar archivo: `image-generation-weavy.json`

### Paso 2: Configurar Credenciales
1. Abrir cada nodo que requiera credenciales
2. Asignar las API keys correspondientes:
   - **Notion Trigger**: `notion_api`
   - **Fetch Latest Brief**: `notion_api`
   - **Google Drive - Create Folder**: `google_drive_oauth`
   - **Google Drive - Upload**: `google_drive_oauth`
   - **Notion - Update Link**: `notion_api`

### Paso 3: Ajustar Variables
En cada nodo, reemplazar placeholders:
- `{{ $notionDatabase }}`: ID de la base de datos Notion
- `pancho@pvbestudio.com`: Email del destinatario

---

## 🚀 Cómo Usar

### Para Generar Imágenes:
1. **En Notion**: Crear nueva página con los detalles del brief
2. **Completar campos**:
   - Cliente
   - Descripción del proyecto
   - Estilo visual (seleccionar de opciones)
   - Paleta de colores
   - Público objetivo
   - Notas adicionales
3. **Marcar checkbox**: "Listo para generar imágenes" ✅
4. **Esperar** (5-10 minutos típicamente)
5. **Resultado**: 
   - Google Drive Link aparece en Notion automáticamente
   - Email de confirmación a Pancho con enlace

---

## 🎨 Ejemplo de Brief

```
Cliente: Collagen Fans Premium
Descripción: Línea de suplementos de colágeno premium para mujeres 25-45 años
Estilo visual: Elegante y minimalista
Paleta de colores: Rosa pálido, blanco, oro rosa
Público objetivo: Mujeres profesionales, interesadas en wellness y belleza
Notas PVB: Deben reflejar lujo, cuidado personal, feminidad
```

---

## 📊 Variables de Salida

El workflow genera:
- **5 imágenes PNG**: Una por cada variación
- **Carpeta en Google Drive**: Nombrada como `[Cliente] - [Fecha]`
- **Email de notificación**: Con resumen y enlaces
- **Enlace en Notion**: Actualizado automáticamente

---

## ⚠️ Troubleshooting

### "Error de autenticación con Weavy"
- Verificar API Key en credenciales
- Confirmar que la cuenta Weavy está activa

### "No se crea carpeta en Google Drive"
- Verificar que OAuth está correctamente configurado
- Asegurar que la carpeta raíz `/PVB Creative Briefs` existe

### "No se actualiza Notion"
- Verificar que el campo `Google Drive Link` es de tipo URL
- Confirmar que Integration Token de Notion es válido

---

## 🔄 Integraciones Futuras

- ✅ Enviar imágenes directamente al cliente por WhatsApp
- ✅ Agregar historial de briefs en Notion
- ✅ Integrar feedback del cliente en ciclo de iteración
- ✅ Guardar imágenes en servidor local como backup

---

## 📝 Notas

- Cada variación tarda ~2-3 minutos en generarse
- Las imágenes se guardan con nombrado automático
- El workflow se ejecuta cada vez que se marca el checkbox (evitar clics accidentales)

---

**Creado para:** PVB Estudio Creativo  
**Última actualización:** 20 Enero 2026  
**Versión:** 1.0
