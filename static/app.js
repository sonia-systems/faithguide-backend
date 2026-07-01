const chatForm = document.getElementById('chatForm');
const userInput = document.getElementById('userInput');
const chatBox = document.getElementById('chatBox');

// Generamos una sesión única para esta pestaña del chat
const sessionId = "session_" + Math.random().toString(36).substr(2, 9);

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const text = userInput.value.trim();
    if (!text) return;
    
    // 1. Pintar mensaje del usuario en pantalla
    appendMessage(text, 'user-message');
    userInput.value = '';
    
    // Guardamos la posición antes de que responda la IA
    chatBox.scrollTop = chatBox.scrollHeight;
    
    // 2. Crear una burbuja de "pensando..." de la IA
    const loadingMessage = appendMessage('Escribiendo...', 'ai-message');

    try {
        // 3. Llamamos a nuestro endpoint de Flask
        const response = await fetch(`/ask?session_id=${sessionId}&question=${encodeURIComponent(text)}`);
        const data = await response.json();
        
        // Mostramos la respuesta real de la IA
        loadingMessage.textContent = data.ai_response || "Lo siento, tuve un pequeño problema con mi conexión.";
        
        // NOTA: Eliminamos por completo la línea de chatBox.scrollTop = chatBox.scrollHeight;
        // De esta forma, el navegador no moverá la pantalla para nada cuando llegue el texto.
        
    } catch (error) {
        loadingMessage.textContent = "¡Ups! Ocurrió un error al intentar conectarme con el servidor.";
        console.error(error);
    }
});

function appendMessage(text, className) {
    const div = document.createElement('div');
    div.className = `message ${className}`;
    div.textContent = text;
    chatBox.appendChild(div);
    return div;
}