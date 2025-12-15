import os
import google.generativeai as genai
import json
import typing
import asyncio

# Configurar la clave API.
# IMPORTANTE: En un escenario real, esto debería ser una variable de entorno.
def configure_ai(api_key: str):
    genai.configure(api_key=api_key)

def get_best_model():
    """
    Encuentra dinámicamente un modelo que soporte generación.
    Devuelve el primer modelo disponible de una lista estable conocida.
    """
    known_models = [
        'gemini-flash-latest',
        'gemini-pro-latest',
        'gemini-2.0-flash',
        'gemini-2.0-flash-001',
        'gemini-1.5-flash',
        'gemini-1.5-flash-001',
        'gemini-1.5-pro',
        'gemini-1.5-pro-001',
        'gemini-pro'
    ]
    
    try:
        # Obtener lista de modelos disponibles para el usuario
        available_names = set()
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                # Almacenar nombre simple y nombre completo
                available_names.add(m.name)
                available_names.add(m.name.replace('models/', ''))
        
        print(f"DEBUG: Modelos disponibles: {available_names}")

        # Buscar modelos estables conocidos
        for km in known_models:
            if km in available_names or f"models/{km}" in available_names:
                print(f"DEBUG: Modelo seleccionado: {km}")
                return genai.GenerativeModel(km)
                
    except Exception as e:
        print(f"Error listando modelos: {e}")
    
    # Respaldo
    print("DEBUG: Retorno a gemini-2.0-flash")
    return genai.GenerativeModel('gemini-2.0-flash')

async def generate_questions(text: str) -> typing.List[dict]:
    """
    Genera 5 preguntas basadas en el texto proporcionado usando Gemini.
    """
    model = get_best_model()
    
    prompt = f"""
    Analiza el siguiente texto y genera 5 preguntas de opción múltiple para evaluar la comprensión.
    Devuelve la salida estrictamente como un arreglo JSON válido de objetos.
    Cada objeto debe tener:
    - "id": entero
    - "question": cadena (en español)
    - "options": lista de 4 cadenas (en español)
    - "correct_answer": cadena (debe coincidir exactamente con una de las opciones)

    Texto:
    {text[:8000]} 
    """ 

    try:
        response = await model.generate_content_async(prompt, generation_config={"response_mime_type": "application/json"})
        return json.loads(response.text)
    except Exception as e:
        print(f"Error generando preguntas: {e}")
        return []

async def evaluate_quiz(questions: list, user_answers: dict) -> dict:
    """
    Evalúa las respuestas.
    """
    score = 0
    total = len(questions)
    correct_details = []
    
    context_text = "Questions and User Answers:\n"
    
    for q in questions:
        q_id = q.get("id")
        user_ans = user_answers.get(q_id)
        correct_ans = q.get("correct_answer")
        
        is_correct = (user_ans == correct_ans)
        if is_correct:
            score += 1
            
        correct_details.append({
            "question": q["question"],
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct
        })
        
        context_text += f"Q: {q['question']}\nCorrect: {correct_ans}\nUser Answered: {user_ans}\n\n"

    # Generar Feedback con IA
    model = get_best_model() 
    feedback_prompt = f"""
    Basado en los siguientes resultados del cuestionario, proporciona un resumen de retroalimentación breve, alentador y constructivo (máximo 3 oraciones) 
    sobre el desempeño del usuario y qué debería repasar si se equivocó. Responde en español.
    
    {context_text}
    """
    
    try:
        feedback_resp = await model.generate_content_async(feedback_prompt)
        ai_feedback = feedback_resp.text
    except Exception as e:
        print(f"Error generando feedback: {e}")
        ai_feedback = "¡Buen trabajo completando el cuestionario!"

    return {
        "score": score,
        "total": total,
        "feedback": ai_feedback,
        "details": correct_details
    }
