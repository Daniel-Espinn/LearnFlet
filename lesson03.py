import flet as ft 
import random

def main (page = ft.Page):
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.title = "lesson-03"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    titulo = ft.Text(value="Ejemplo de Tabs en Flet", size=24, color=ft.colors.WHITE)
    
    # Contenido de Pestaña de Tareas
    
    def generar_tareas():
        tareas = ["Hacer la comida", "Tender la ropa", "Hacer ejercicio", "Leer un libro", "Limpiar la pieza"]
        return random.sample(tareas, k=4)
   
    def actualizar_tareas():
        lista_tareas.controls.clear()
        for tarea in generar_tareas():
            lista_tareas.controls.append(ft.Text(tarea, color=ft.colors.WHITE))
        page.update()
    
    lista_tareas = ft.ListView(spacing=10, padding=20)
    
    actualizar_tareas()
    boton_actualizar = ft.ElevatedButton(text="Actualizar", on_click=lambda _: actualizar_tareas())
    contenido_tareas = ft.Column([lista_tareas, boton_actualizar])
    
    # Contenido Pestaña de Perfil
    campo_nombre = ft.TextField(label="Nombre", bgcolor=ft.colors.BLUE_GREY_800)
    campo_email = ft.TextField(label="Email", bgcolor=ft.colors.BLUE_GREY_800)
    boton_guardar = ft.ElevatedButton("Guardar Perfil")
    contenido_perfil = ft.Column([campo_nombre, campo_email, boton_guardar])
    
    # Contenido Pestaña de Configuracion
    switch_notificaciones = ft.Switch(label="Notificaciones", value=True)
    slider_volumen = ft.Slider(min=0, max=100, divisions=20, label="Volumen")
    contenido_notificaciones = ft.Column([switch_notificaciones, slider_volumen])
    
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration = 300,
        tabs=[
            ft.Tab(text="Tareas", icon=ft.icons.LIST_ALT, content=contenido_tareas),
            ft.Tab(text="Tareas", icon=ft.icons.PERSON, content=contenido_perfil),
            ft.Tab(text="Tareas", icon=ft.icons.SETTINGS, content=contenido_notificaciones),
        ],
        expand=1
    )
    
    page.add(titulo, tabs)
    
ft.app(target=main)