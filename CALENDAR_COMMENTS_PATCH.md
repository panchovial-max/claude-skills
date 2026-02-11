# Calendar Comments - Modificaciones a calendar.html

## 1. Agregar estilos CSS (antes de `</style>`)

```css
/* Comments Section Styles */
.comments-section {
    margin-top: 30px;
    padding-top: 20px;
    border-top: 2px solid #e2e8f0;
}

.comments-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
}

.comments-header h4 {
    margin: 0;
    color: #2d3748;
    font-size: 18px;
}

.comment {
    background: #f7fafc;
    border-left: 4px solid #667eea;
    padding: 15px;
    margin-bottom: 15px;
    border-radius: 8px;
}

.comment.agency-comment {
    border-left-color: #48bb78;
    background: #f0fff4;
}

.comment-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}

.comment-author {
    font-weight: 600;
    color: #2d3748;
}

.comment-badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}

.comment-badge.client {
    background: #667eea;
    color: white;
}

.comment-badge.agency {
    background: #48bb78;
    color: white;
}

.comment-time {
    color: #718096;
    font-size: 13px;
    margin-left: auto;
}

.comment-message {
    color: #4a5568;
    line-height: 1.6;
    margin: 0;
}

.comment-input-container {
    margin-top: 20px;
}

.comment-input {
    width: 100%;
    padding: 12px;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 14px;
    font-family: inherit;
    resize: vertical;
    min-height: 80px;
    transition: border-color 0.2s;
}

.comment-input:focus {
    outline: none;
    border-color: #667eea;
}

.comment-submit {
    margin-top: 10px;
    background: #667eea;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.2s;
}

.comment-submit:hover {
    background: #5a67d8;
}

.comment-submit:disabled {
    background: #cbd5e0;
    cursor: not-allowed;
}

.no-comments {
    text-align: center;
    padding: 20px;
    color: #a0aec0;
    font-style: italic;
}
```

## 2. Modificar función showEventDetails()

En la línea ~500, al final del `details.innerHTML`, agregar:

```javascript
// ANTES (línea ~510):
${props.cta_link ? `<p><strong>🔗 Link:</strong> <a href="${props.cta_link}" target="_blank">${props.cta_link}</a></p>` : ''}
`;

// AGREGAR DESPUÉS:
details.innerHTML += `
    <div class="comments-section" id="comments-section">
        <div class="comments-header">
            <h4>💬 Comentarios</h4>
        </div>
        <div id="comments-list">
            <div class="no-comments">Cargando comentarios...</div>
        </div>
        <div class="comment-input-container">
            <textarea
                id="comment-input"
                class="comment-input"
                placeholder="Escribe un comentario sobre esta campaña..."
            ></textarea>
            <button onclick="postComment('${event.id}')" class="comment-submit">
                Enviar Comentario
            </button>
        </div>
    </div>
`;

// Cargar comentarios para este evento
loadComments(event.id);
```

## 3. Agregar funciones JavaScript (al final del script, antes de `</script>`)

```javascript
// ==================== COMMENTS FUNCTIONS ====================

/**
 * Load comments for an event
 */
async function loadComments(eventId) {
    const commentsList = document.getElementById('comments-list');

    try {
        const response = await fetch(
            `/.netlify/functions/comments-get?event_id=${eventId}`,
            {
                headers: { 'Authorization': `Bearer ${sessionToken}` }
            }
        );

        if (!response.ok) {
            throw new Error('Failed to load comments');
        }

        const data = await response.json();
        const comments = data.comments || [];

        if (comments.length === 0) {
            commentsList.innerHTML = '<div class="no-comments">No hay comentarios aún. ¡Sé el primero en comentar!</div>';
            return;
        }

        // Renderizar comentarios
        commentsList.innerHTML = comments.map(comment => {
            const timeAgo = getTimeAgo(new Date(comment.created_at));
            const badgeClass = comment.author_role === 'agency' ? 'agency' : 'client';
            const commentClass = comment.author_role === 'agency' ? 'comment agency-comment' : 'comment';

            return `
                <div class="${commentClass}">
                    <div class="comment-header">
                        <span class="comment-author">${comment.author_name}</span>
                        <span class="comment-badge ${badgeClass}">
                            ${comment.author_role === 'agency' ? 'Agencia' : 'Cliente'}
                        </span>
                        <span class="comment-time">${timeAgo}</span>
                    </div>
                    <p class="comment-message">${escapeHtml(comment.message)}</p>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error loading comments:', error);
        commentsList.innerHTML = '<div class="no-comments">Error al cargar comentarios</div>';
    }
}

/**
 * Post a new comment
 */
async function postComment(eventId) {
    const input = document.getElementById('comment-input');
    const message = input.value.trim();
    const submitBtn = event.target;

    if (!message) {
        alert('Por favor escribe un comentario');
        return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = 'Enviando...';

    try {
        const response = await fetch('/.netlify/functions/comments-post', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${sessionToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                event_id: eventId,
                message: message
            })
        });

        if (!response.ok) {
            throw new Error('Failed to post comment');
        }

        // Limpiar input
        input.value = '';

        // Recargar comentarios
        await loadComments(eventId);

        // Mostrar confirmación
        showNotification('✅ Comentario enviado');

    } catch (error) {
        console.error('Error posting comment:', error);
        alert('❌ Error al enviar comentario');
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Enviar Comentario';
    }
}

/**
 * Get relative time string
 */
function getTimeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);

    if (seconds < 60) return 'Hace un momento';
    if (seconds < 3600) return `Hace ${Math.floor(seconds / 60)} minutos`;
    if (seconds < 86400) return `Hace ${Math.floor(seconds / 3600)} horas`;
    if (seconds < 604800) return `Hace ${Math.floor(seconds / 86400)} días`;

    return date.toLocaleDateString('es-CL');
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Show notification toast
 */
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #48bb78;
        color: white;
        padding: 15px 20px;
        border-radius: 8px;
        font-weight: 600;
        z-index: 10000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// ==================== END COMMENTS FUNCTIONS ====================
```

## 4. Instrucciones de Aplicación

1. Abrir `calendar.html` en un editor
2. Copiar los estilos CSS y pegarlos antes de `</style>` (alrededor de línea 240)
3. Modificar la función `showEventDetails()` como se indica arriba (alrededor de línea 510)
4. Agregar las funciones JavaScript al final del script (antes de `</script>`, alrededor de línea 625)
5. Guardar el archivo

## 5. Testing

Después de aplicar los cambios:
- Abrir calendar.html
- Hacer click en un evento
- Debería aparecer una sección de comentarios
- Poder escribir y enviar comentarios
- Los comentarios se muestran diferenciados por rol (cliente vs agencia)
