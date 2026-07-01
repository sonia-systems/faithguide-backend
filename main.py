import os
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# Coloca aquí tu API Key real de Gemini directamente entre las comillas
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Leemos la clave de forma segura desde las variables de entorno del sistema operativo
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_KEY:
    # Si no existe, dejamos un mensaje de error claro en la consola
    print("ERROR CRÍTICO: No se encontró la variable de entorno GEMINI_API_KEY")
SYSTEM_INSTRUCTION = """
Eres "FaithGuide AI", un mentor espiritual virtual enfocado en adolescentes y jóvenes de un Oratorio Salesiano. 
Tu tono debe ser juvenil, dinámico, empático, comprensivo y alegre, usando un lenguaje cercano pero respetuoso.
Debes ofrecer orientación basada en valores cristianos y humanos, sin juzgar, infundiendo siempre esperanza y motivación.
Evita sonar aburrido, rígido o excesivamente teológico; en su lugar, usa analogías de la vida cotidiana de los jóvenes (estudios, amigos, metas, deportes).

CRÍTICO: Tienes la capacidad de recordar toda la conversación actual. Si el usuario te dice su nombre, edad o problemas en mensajes anteriores, recuérdalos y úsalos para dar respuestas de seguimiento personalizadas. Nunca le digas al usuario que olvidas las cosas o que tu cerebro se reinicia.
"""

# Diccionario global para almacenar los historiales en el formato que pide Google de forma nativa
# Estructura: { "id_sesion": [ {"role": "user", "parts": [...]}, {"role": "model", "parts": [...]} ] }
sessions = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['GET'])
def ask_ai():
    question = request.args.get('question', '')
    session_id = request.args.get('session_id', 'default_user')
    
    if not question.strip():
        return jsonify({"error": "La pregunta no puede estar vacía"}), 400
        
    try:
        # 1. Si la sesión es nueva, inicializamos su historial incluyendo la instrucción del sistema
        if session_id not in sessions:
            sessions[session_id] = []
            
        historial = sessions[session_id]
        
        # 2. Añadimos la pregunta del usuario al historial de la sesión
        historial.append({
            "role": "user",
            "parts": [{"text": question}]
        })
        
        # 3. Construimos la petición HTTP directa al endpoint oficial de Gemini 2.5 Flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_KEY}"
        
        payload = {
            "systemInstruction": {
                "parts": [{"text": SYSTEM_INSTRUCTION}]
            },
            "contents": historial,
            "generationConfig": {
                "temperature": 0.7
            }
        }
        
        # Enviamos la petición sin usar librerías raras de terceros
        response = requests.post(url, json=payload)
        response_data = response.json()
        
        # Verificamos si Google devolvió algún error
        if "error" in response_data:
            return jsonify({"error": response_data["error"]["message"]}), response.status_code
            
        # Extraemos el texto de la respuesta de la IA
        ai_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
        
        # 4. Guardamos la respuesta del modelo en el historial para que mantenga la memoria
        historial.append({
            "role": "model",
            "parts": [{"text": ai_text}]
        })
        
        return jsonify({
            "session_id": session_id,
            "user_question": question,
            "ai_response": ai_text
        })
        
    except Exception as e:
        return jsonify({"error": f"Error en la comunicación directa: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)