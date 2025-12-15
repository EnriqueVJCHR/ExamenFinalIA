import flet as ft
from utils.styles import NEON_CYAN, NEON_GREEN, get_neon_container, get_neon_button, TITLE_STYLE

class QuizView(ft.Container):
    def __init__(self, questions, on_submit):
        super().__init__()
        self.questions = questions
        self.on_submit = on_submit
        self.answers = {}
        self.current_question_index = 0
        
        self.padding = 20
        self.alignment = ft.alignment.center

        if not self.questions:
            self.content = ft.Text("No se generaron preguntas.", color="red")
        else:
            self.question_container = ft.Column(spacing=20)
            self.setup_ui()
            self.update_question_view()

    def setup_ui(self):
        self.content = ft.Column(
            controls=[
                ft.Text("Evaluación", style=TITLE_STYLE),
                ft.ProgressBar(value=0, color=NEON_GREEN, ref=ft.Ref()), 
                # Note: keeping simple ref or accessing by index might be easier for update.
                # Accessing via self.content.controls[1]
                
                ft.Container(height=20),
                get_neon_container(self.question_container)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.progress_bar = self.content.controls[1]

    def update_question_view(self):
        q = self.questions[self.current_question_index]
        self.question_container.controls.clear()
        
        # Update Progress
        self.progress_bar.value = (self.current_question_index + 1) / len(self.questions)
        
        # Question Text
        self.question_container.controls.append(
            ft.Text(f"Pregunta {self.current_question_index + 1}:", color=NEON_CYAN, weight=ft.FontWeight.BOLD)
        )
        self.question_container.controls.append(
            ft.Text(q['question'], size=18, color="white")
        )

        # Options using RadioGroup
        self.radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value=opt, label=opt, fill_color=NEON_GREEN) for opt in q['options']
            ]),
            on_change=self.on_option_change
        )
        
        # Pre-select if already answered
        if q['id'] in self.answers:
            self.radio_group.value = self.answers[q['id']]

        self.question_container.controls.append(self.radio_group)

        # Navigation Buttons
        row_controls = []
        if self.current_question_index > 0:
            row_controls.append(ft.ElevatedButton("Anterior", on_click=self.prev_question))
        
        if self.current_question_index < len(self.questions) - 1:
            row_controls.append(get_neon_button("Siguiente", on_click=self.next_question))
        else:
            row_controls.append(get_neon_button("Enviar", on_click=self.submit_quiz, color=NEON_GREEN))

        self.question_container.controls.append(
            ft.Row(row_controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        
        if self.page:
            self.page.update()

    def on_option_change(self, e):
        q_id = self.questions[self.current_question_index]['id']
        self.answers[q_id] = e.control.value

    def next_question(self, e):
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.update_question_view()

    def prev_question(self, e):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question_view()

    async def submit_quiz(self, e):
        await self.on_submit(self.answers)
