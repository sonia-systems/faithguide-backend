from fastapi import FastAPI

app = FastAPI(title="FaithGuide AI API")

@app.get("/")
def read_root():
    return {
        "message": "Welcome to FaithGuide AI",
        "status": "Active",
        "target_audience": "Youth"
    }

@app.get("/ask")
def ask_question(question: str):
    return {
        "user_question": question,
        "ai_response": f"¡Hola! Tu pregunta sobre '{question}' es muy importante. Pronto te daré una respuesta basada en la fe con un tono dinámico."
    }