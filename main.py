import flet as ft
import os
import asyncio
from views.upload_view import UploadView
from views.quiz_view import QuizView
from views.result_view import ResultView
from utils.pdf_processor import extract_text_from_pdf
from utils.ai_handler import generate_questions, evaluate_quiz, configure_ai
from utils.styles import DARK_BG, NEON_CYAN
from dotenv import load_dotenv

load_dotenv()

# IMPORTANTE: Establece tu API KEY aquí o en una variable de entorno "GEMINI_API_KEY"
# os.environ["GEMINI_API_KEY"] = "TU_CLAVE_AQUI"

async def main(page: ft.Page):
    page.title = "Ejemplo tipo notebooklm"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = DARK_BG
    page.padding = 0
    
    # Configurar IA
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # Respaldo para propósitos de demostración si falta la variable de entorno
        print("ADVERTENCIA: GEMINI_API_KEY no encontrada en el entorno.")
        # Podrías pedirla vía UI, pero por ahora advertimos.
    else:
        configure_ai(api_key)

    def route_change(route):
        page.views.clear()
        
        # RAÍZ: Vista de Carga
        if page.route == "/":
            view = UploadView(page, on_upload_complete=handle_upload)
            page.views.append(
                ft.View(
                    "/",
                    [view],
                    bgcolor=DARK_BG,
                    padding=0
                )
            )
        
        # QUIZ: Vista de Evaluación
        elif page.route == "/quiz":
             # Asumimos que las preguntas están guardadas en page.session
            questions = page.session.get("questions")
            if not questions:
                questions = []
            view = QuizView(questions, on_submit=handle_quiz_submit)
            page.views.append(
                ft.View(
                    "/quiz",
                    [view],
                    bgcolor=DARK_BG,
                    padding=0
                )
            )

        # RESULTADO: Vista de Resultados
        elif page.route == "/result":
            results = page.session.get("results")
            if not results:
                results = {}
            view = ResultView(results, on_restart=lambda _: page.go("/"))
            page.views.append(
                ft.View(
                    "/result",
                    [view],
                    bgcolor=DARK_BG,
                    padding=0
                )
            )
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # --- Manejadores ---

    async def handle_upload(file_path):
        # 1. Extraer Texto
        text = extract_text_from_pdf(file_path)
        if not text:
            # Mostrar error
            page.snack_bar = ft.SnackBar(ft.Text("No se pudo leer el texto del PDF."), bgcolor="red")
            page.snack_bar.open = True
            page.update()
            return

        # 2. Generar Preguntas
        # Verificar API Key de nuevo
        if not os.getenv("GEMINI_API_KEY"):
             page.snack_bar = ft.SnackBar(ft.Text("Por favor configura GEMINI_API_KEY en el entorno."), bgcolor="red")
             page.snack_bar.open = True
             page.update()
             return

        try:
            questions = await generate_questions(text)
            if not questions:
                page.snack_bar = ft.SnackBar(ft.Text("La IA falló al generar preguntas."), bgcolor="red")
                page.snack_bar.open = True
                page.update()
                return
            
            # Guardar en sesión
            page.session.set("questions", questions)
            page.go("/quiz")
            
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {e}"), bgcolor="red")
            page.snack_bar.open = True
            page.update()

    async def handle_quiz_submit(answers):
        questions = page.session.get("questions")
        if not questions:
             questions = []
        
        # Aquí se podría añadir un indicador de carga
        
        results = await evaluate_quiz(questions, answers)
        page.session.set("results", results)
        page.go("/result")

    # Configurar Enrutamiento
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target=main)
