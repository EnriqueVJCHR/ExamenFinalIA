import flet as ft
from utils.styles import NEON_CYAN, NEON_PINK, get_neon_container, get_neon_button, TITLE_STYLE, SUBTITLE_STYLE

class UploadView(ft.Container):
    def __init__(self, page, on_upload_complete):
        super().__init__()
        self.page_ref = page # Renaming to avoid conflict if Container has page property
        self.on_upload_complete = on_upload_complete
        self.file_picker = ft.FilePicker(on_result=self.on_file_picked)
        self.status_text = ft.Text("", color=NEON_PINK)
        self.loading = ft.ProgressBar(width=400, color=NEON_CYAN, visible=False)
        
        # UI Setup
        self.alignment = ft.alignment.center
        self.padding = 50
        self.content = ft.Column(
                controls=[
                    ft.Text("Examen IA, Evaluador", style=TITLE_STYLE),
                    ft.Text("Sube un PDF para generar un examen", style=SUBTITLE_STYLE),
                    ft.Divider(height=20, color="transparent"),
                    get_neon_container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(name="upload_file", size=50, color=NEON_CYAN),
                                ft.Text("Arrastra y suelta o haz clic para subir", color="white"),
                                ft.Container(height=20),
                                get_neon_button("Seleccionar PDF", lambda _: self.file_picker.pick_files(allow_multiple=False, allowed_extensions=["pdf"])),
                                ft.Container(height=10),
                                self.status_text,
                                self.loading
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        )
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

    def did_mount(self):
        # We need to add the file picker to the page overlay
        # Since 'self.page' might be none until mounted, usage of 'page_ref' passed or self.page is tricky.
        # But 'did_mount' is called when attached.
        if self.page:
            self.page.overlay.append(self.file_picker)
            self.page.update()

    async def on_file_picked(self, e: ft.FilePickerResultEvent):
        if e.files:
            file_path = e.files[0].path
            self.status_text.value = f"Seleccionado: {e.files[0].name}"
            self.status_text.update()
            
            # Show loading
            self.loading.visible = True
            self.loading.update()
            
            # Trigger processing
            await self.on_upload_complete(file_path)
        else:
            self.status_text.value = "Cancelado"
            self.status_text.update()
