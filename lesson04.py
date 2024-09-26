import flet as ft 

def main (page:ft.Page):
    page.title = "Lista de compras"
    page.bgcolor = ft.colors.BLUE_GREY_800
    page.padding = 20
    
    title = ft.Text(value="Lista de Compras", size=30, weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE, text_align=ft.TextAlign.CENTER)
    
    list = ft.Column(scroll=ft.ScrollMode.AUTO)
    
    item_input = ft.TextField(
        hint_text="Añadir Articulo",
        border_color=ft.colors.AMBER,
        color=ft.colors.WHITE,
        width=300,
        text_align=ft.TextAlign.CENTER,
    )
    
    quantity_input = ft.TextField(
        hint_text="Cantidad",
        border_color=ft.colors.AMBER,
        color=ft.colors.WHITE,
        width=100,
        text_align=ft.TextAlign.CENTER,
    )
    
    categorias = ["Sin categoría", "Alimentos", "Limpieza", "Electrónica"]
    
    def add_item(e):
        if item_input.value:
            quantity = quantity_input.value if quantity_input.value else "1"
            
            def update_category(e):
                category_text.value = f"Categoría: {e.control.value}"
                page.update()
                
            category_dropdown = ft.Dropdown(
                options=[ft.dropdown.Option(category) for category in categorias],
                value=categorias[0],
                on_change=update_category,
                color=ft.colors.AMBER,
                width=150
            )
            
            category_text = ft.Text(value=f"Categoría: {categorias[0]}",
                                    color=ft.colors.AMBER)
    
    page.add(title)
    
ft.app(target=main)