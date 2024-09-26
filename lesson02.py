import flet as ft
import time

def main (page = ft.Page):
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.title = "Lesson-02"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text(value="Lesson - 2", size=24, color=ft.colors.WHITE)
    files = ft.Text(value="Selecciona los archivos", size=16, color=ft.colors.WHITE70)
    file_list = ft.Column([
        ft.Checkbox(label="Documento.pdf (2.5 MB)", value=False),
        ft.Checkbox(label="Imagen.jpg (0.5 MB)", value=False),
        ft.Checkbox(label="Video.mp4 (4.5 MB)", value=False),
        ft.Checkbox(label="Archivo.zip (8.5 MB)", value=False),
    ])
    
    def load(e):
        selected_files = [checkbox for checkbox in file_list.controls if checkbox.value]
        if not selected_files:
            status_text.value = "Por favor selecciona un archivo"
            page.update()
            return
        progress_bar.value = 0
        progress_ring.value = 0
        page.update()
        
        total_size = sum([float(file.label.split("(")[1].split(" MB")[0]) for file in selected_files])
        downloaded = 0
        for file in selected_files:
            file_size = float(file.label.split("(")[1].split(" MB")[0])
            status_text.value = f"Descargando {file.label}..."
            
            for _ in range(10):
                time.sleep(0.3)
                downloaded += file_size / 10
                progress = min(downloaded / total_size, 1)
                progress_bar.value = progress
                progress_ring.value = progress
                page.update()
            
        progress_bar.value = 1
        progress_ring.value = 1
        status_text.value = "Descarga completada"
        page.update()
        
        time.sleep(1)
        progress_bar.value = 0
        progress_ring.value = 0
        status_text.value = ""
        for checkbox in file_list.controls:
            checkbox.value = False
        page.update()
    
    container = ft.Container(content=file_list, padding=20)
    progress_bar = ft.ProgressBar(width=400, color="amber", bgcolor="#263238", value=0)
    progress_ring = ft.ProgressRing(stroke_width=5, color="amber", value=0)
    fila = ft.Row(
        controls=[
            progress_bar,
            progress_ring        
        ],
        alignment=ft.MainAxisAlignment.CENTER
    )
    status_text = ft.Text(value="", color=ft.colors.WHITE)
    boton_descargar = ft.ElevatedButton("Iniciar Descarga", on_click=load, bgcolor=ft.colors.AMBER, color=ft.colors.BLACK)
    
    page.add(title, files, container, fila, status_text, boton_descargar)
    
ft.app(target = main)
    