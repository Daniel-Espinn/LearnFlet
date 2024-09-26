import flet as ft

def main(page: ft.Page):
    page.title = "Conversor de unidades"
    page.bgcolor = ft.colors.WHITE
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    
    input_field = ft.TextField(label="Ingrese el peso en Kg:")
    resultado = ft.Text(value="")
    
    def conversion(e):
        if input_field.value:
            resultado.value = f"{float(input_field.value) * 1000} gramos"
            page.update()
    
    container = ft.Container(
        width=300,
        bgcolor=ft.colors.BLUE_GREY_600,
        border_radius=20,
        padding=20,
        content=ft.Column(
            controls=[
                input_field,
                ft.ElevatedButton(text="Enviar", on_click=conversion),
                resultado
            ]
        )
    )
    
    page.add(container)
    
ft.app(target=main)
