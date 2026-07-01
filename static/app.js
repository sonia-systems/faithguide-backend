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
    
    // 2. Crear una burbuja de "pensando..." de la IA
    const loadingMessage = appendMessage('Escribiendo...', 'ai-message');
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // 3. Llamamos a nuestro endpoint de Flask
        const response = await fetch(`/ask?session_id=${sessionId}&question=${encodeURIComponent(text)}`);
        const data = await response.json();
        
        // Mostramos la respuesta real quitando el texto de carga
        loadingMessage.textContent = data.ai_response || "Lo siento, tuve un pequeño problema con mi conexión.";
    } catch (error) {
        loadingMessage.textContent = "¡Ups! Ocurrió un error al intentar conectarme con el servidor.";
        console.error(error);
    }
    
    // Auto-scroll hacia abajo
    chatBox.scrollTop = chatBox.scrollHeight;
});

function appendMessage(text, className) {
    const div = document.createElement('div');
    div.className = `message ${className}`;
    div.textContent = text;
    chatBox.appendChild(div);
    return div;
}