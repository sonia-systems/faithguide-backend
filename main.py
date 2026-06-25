import os
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Cargamos las variables de entorno del archivo .env
load_dotenv()

app = FastAPI(title="FaithGuide AI API")

# Inicializamos el cliente de Gemini usando la API Key segura
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Falta la variable GEMINI_API_KEY en el archivo .env")

client = genai.Client(api_key=api_key)

# Definimos la personalidad de la IA mediante instrucciones del sistema
SYSTEM_INSTRUCTION = """
Eres "FaithGuide AI", un mentor espiritual virtual enfocado en adolescentes y jóvenes de un Oratorio Salesiano. 
Tu tono debe ser juvenil, dinámico, empático, comprensivo y alegre, usando un lenguaje cercano pero respetuoso.
Debes ofrecer orientación basada en valores cristianos y humanos, sin juzgar, infundiendo siempre esperanza y motivación.
Evita sonar aburrido, rígido o excesivamente teológico; en su lugar, usa analogías de la vida cotidiana de los jóvenes (estudios, amigos, metas, deportes).
"""

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FaithGuide AI Engine",
        "status": "Active"
    }

@app.get("/ask")
def ask_ai(question: str):
    if not question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
        
    try:
        # Llamamos al modelo Gemini 1.5 Flash configurando su rol
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7, # Balance entre creatividad y coherencia
            ),
        )
        
        return {
            "user_question": question,
            "ai_response": response.text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con la IA: {str(e)}")