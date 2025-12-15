import flet as ft
from utils.styles import NEON_CYAN, NEON_PINK, NEON_GREEN, get_neon_container, get_neon_button, TITLE_STYLE

class ResultView(ft.Container):
    def __init__(self, results, on_restart):
        super().__init__()
        self.results = results
        self.on_restart = on_restart
        
        self.alignment = ft.alignment.center
        self.padding = 20
        
        self.setup_ui()

    def setup_ui(self):
        score = self.results['score']
        total = self.results['total']
        percentage = (score / total) * 100
        color = NEON_GREEN if percentage >= 60 else NEON_PINK

        details_controls = []
        for detail in self.results['details']:
            icon_name = "check_circle" if detail['is_correct'] else "cancel"
            icon_color = NEON_GREEN if detail['is_correct'] else NEON_PINK
            
            details_controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(name=icon_name, color=icon_color),
                            ft.Text(detail['question'], weight=ft.FontWeight.BOLD, color="white", width=400),
                        ]),
                        ft.Text(f"Tu respuesta: {detail['user_answer']}", color="white", size=12),
                        ft.Text(f"Correcta: {detail['correct_answer']}", color=NEON_GREEN if not detail['is_correct'] else "transparent", size=12),
                    ]),
                    border=ft.border.only(bottom=ft.border.BorderSide(1, "grey")),
                    padding=10
                )
            )

        self.content = ft.Column(
            controls=[
                ft.Text("Resultados de la Evaluación", style=TITLE_STYLE),
                get_neon_container(
                    content=ft.Column(
                        controls=[
                            ft.Text(f"Puntaje: {score} / {total}", size=40, color=color, weight=ft.FontWeight.BOLD),
                            ft.Text(self.results['feedback'], italic=True, color="white"),
                            ft.Divider(color=NEON_CYAN),
                            ft.Container(
                                content=ft.Column(details_controls, scroll=ft.ScrollMode.AUTO),
                                height=300 
                            ),
                            ft.Container(height=20),
                            get_neon_button("Iniciar Nueva Evaluación", self.on_restart)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
