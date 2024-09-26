import flet as ft

def main(page=ft.Page):
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.title = "Lesson-01"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def agregar_tarea(e):
        if input.value:
            tarea = ft.ListTile( title=ft.Text(input.value),
                                leading=ft.Checkbox(on_change=seleccionar_tarea))
            tareas.append(tarea)
            input.value = ""
            actualizar_lista()
            
    def seleccionar_tarea(e):
        seleccionadas = [t.title.value for t in tareas if t.leading.value]
        tareas_seleccionadas.value = "Tareas seleccionadas: " + ", ".join(seleccionadas)
        page.update()
    
    def actualizar_lista():
        lista_tareas.controls.clear()
        lista_tareas.controls.extend(tareas)
        page.update()
    
    titulo = ft.Text(value="Lista de tareas", size=30, weight=ft.FontWeight.BOLD)
    input = ft.TextField(hint_text="Escribe aqui")
    add_button = ft.FilledButton(text="Agregar tarea", on_click=agregar_tarea)
    
    lista_tareas = ft.ListView(expand=1, spacing=3)
    tareas = []
    tareas_seleccionadas = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    
    page.add(titulo, input, add_button, lista_tareas, tareas_seleccionadas)
    
ft.app(target=main)