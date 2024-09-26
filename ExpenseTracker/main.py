import flet as ft
import sqlite3
from datetime import datetime, timedelta
import calendar

class ExpenseTracker:
    def __init__(self):
        self.conn = sqlite3.connect('expenses.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                date TEXT,
                description TEXT,
                amount REAL,
                type TEXT
            )
        ''')
        self.conn.commit()

    def add_transaction(self, date, description, amount, type):
        self.cursor.execute('''
            INSERT INTO expenses (date, description, amount, type)
            VALUES (?, ?, ?, ?)
        ''', (date, description, amount, type))
        self.conn.commit()

    def get_monthly_data(self, year, month):
        start_date = f"{year}-{month:02d}-01"
        _, last_day = calendar.monthrange(year, month)
        end_date = f"{year}-{month:02d}-{last_day}"
        
        self.cursor.execute('''
            SELECT date, type, amount FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        ''', (start_date, end_date))
        
        return self.cursor.fetchall()

    def get_all_transactions(self):
        self.cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
        return self.cursor.fetchall()

    def get_total_balance(self, year, month):
        start_date = f"{year}-{month:02d}-01"
        _, last_day = calendar.monthrange(year, month)
        end_date = f"{year}-{month:02d}-{last_day}"
        
        self.cursor.execute('''
            SELECT 
                SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_income,
                SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_expense
            FROM expenses
            WHERE date BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_income, total_expense = self.cursor.fetchone()
        return total_income or 0, total_expense or 0

def main(page: ft.Page):
    page.title = "Control de Caja"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = True
    page.bgcolor = ft.colors.BLUE_GREY_900
    page.scroll = "auto"
    page.fonts = {
        "Roboto": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf",
        "RobotoBold": "https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Bold.ttf"
    }

    tracker = ExpenseTracker()
    current_date = datetime.now()

    title = ft.Text("Control de Caja", size=32, weight=ft.FontWeight.BOLD, font_family="RobotoBold", color=ft.colors.BLUE_200)

    date_picker = ft.DatePicker(
        on_change=lambda _: date_picker_changed(_.control.value)
    )
    page.overlay.append(date_picker)

    def date_picker_changed(date):
        selected_date.value = date.strftime("%Y-%m-%d")
        page.update()

    selected_date = ft.TextField(label="Fecha Seleccionada", read_only=True, expand=1, bgcolor=ft.colors.BLUE_GREY_800, border_color=ft.colors.BLUE_200)
    date_button = ft.ElevatedButton(
        "Seleccionar Fecha",
        icon=ft.icons.CALENDAR_TODAY,
        on_click=lambda _: date_picker.pick_date(),
        style=ft.ButtonStyle(color=ft.colors.BLUE_200)
    )

    description = ft.TextField(label="Descripcion", expand=1, bgcolor=ft.colors.BLUE_GREY_800, border_color=ft.colors.BLUE_200)
    amount = ft.TextField(label="Cantidad $", expand=1, bgcolor=ft.colors.BLUE_GREY_800, border_color=ft.colors.BLUE_200)
    transaction_type = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("Ingreso"),
            ft.dropdown.Option("Gasto"),
        ],
        expand=1,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_color=ft.colors.BLUE_200
    )

    def add_transaction(e):
        if not selected_date.value or not description.value or not amount.value or not transaction_type.value:
            page.snack_bar = ft.SnackBar(ft.Text("Por favor completa todos los campos", color=ft.colors.RED_400))
            page.snack_bar.open = True
            page.update()
            return
        
        tracker.add_transaction(
            selected_date.value,
            description.value,
            float(amount.value),
            transaction_type.value
        )
        
        description.value = ""
        amount.value = ""
        transaction_type.value = None
        update_chart()
        update_table()
        update_balance()
        page.update()

    add_button = ft.ElevatedButton(
        "Añadir", 
        on_click=add_transaction, 
        style=ft.ButtonStyle(
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLUE_700,
            padding=15
        )
    )

    balance_text = ft.Text("", size=20, color=ft.colors.BLUE_200)

    def update_balance():
        total_income, total_expense = tracker.get_total_balance(current_date.year, current_date.month)
        balance = total_income - total_expense
        balance_text.value = f"Balance General: ${balance:.2f}\nIngresos Totales: ${total_income:.2f}\nEgresos Totales: ${total_expense:.2f}"
        page.update()

    chart = ft.LineChart(
        data_series=[],
        left_axis=ft.ChartAxis(
            labels_size=40, 
            title_size=40
        ),
        bottom_axis=ft.ChartAxis(
            labels_size=40, 
            title=ft.Text("Día"), 
            title_size=40
        ),
        tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY_700),
        expand=True,
        min_y=0,
        min_x=1,
        max_x=31,
        interactive=True,
    )

    chart_legend = ft.Row([
        ft.Container(bgcolor=ft.colors.GREEN, width=20, height=20),
        ft.Text("Ingresos", color=ft.colors.GREEN),
        ft.Container(bgcolor=ft.colors.RED, width=20, height=20),
        ft.Text("Gastos", color=ft.colors.RED),
        ft.Container(bgcolor=ft.colors.YELLOW, width=20, height=20),
        ft.Text("Balance", color=ft.colors.YELLOW),
    ], alignment=ft.MainAxisAlignment.CENTER, wrap=True)

    def update_chart():
        data = tracker.get_monthly_data(current_date.year, current_date.month)
        
        income_series = [0] * 31
        expense_series = [0] * 31
        balance_series = [0] * 31
        
        for transaction in data:
            day = int(transaction[0].split('-')[2])
            amount = transaction[2]
            if transaction[1] == 'Ingreso':
                income_series[day-1] += amount
            else:
                expense_series[day-1] += amount
            
        for i in range(31):
            balance_series[i] = income_series[i] - expense_series[i]
            if i > 0:
                income_series[i] += income_series[i-1]
                expense_series[i] += expense_series[i-1]
                balance_series[i] += balance_series[i-1]
        
        chart.data_series = [
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(x, y) for x, y in enumerate(income_series, 1)],
                stroke_width=2,
                color=ft.colors.GREEN,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(x, y) for x, y in enumerate(expense_series, 1)],
                stroke_width=2,
                color=ft.colors.RED,
                curved=True,
                stroke_cap_round=True,
            ),
            ft.LineChartData(
                data_points=[ft.LineChartDataPoint(x, y) for x, y in enumerate(balance_series, 1)],
                stroke_width=2,
                color=ft.colors.YELLOW,
                curved=True,
                stroke_cap_round=True,
            ),
        ]
        chart.max_y = max(max(income_series), max(expense_series), max(balance_series)) * 1.1
        page.update()

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Descripcion")),
            ft.DataColumn(ft.Text("Cantidad $")),
            ft.DataColumn(ft.Text("Tipo")),
        ],
        rows=[],
    )

    def update_table():
        transactions = tracker.get_all_transactions()
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(trans[1])),
                    ft.DataCell(ft.Text(trans[2])),
                    ft.DataCell(ft.Text(f"${trans[3]:.2f}")),
                    ft.DataCell(ft.Text(trans[4])),
                ],
                color=ft.colors.GREEN_200 if trans[4] == 'ingreso' else ft.colors.RED_200
            ) for trans in transactions
        ]
        page.update()

    def filter_transactions(e):
        transactions = tracker.get_all_transactions()
        filtered = transactions
        if type_filter.value:
            filtered = [t for t in filtered if t[4] == type_filter.value]
        if date_filter.value:
            filtered = [t for t in filtered if t[1].startswith(date_filter.value)]
        
        table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(trans[1])),
                    ft.DataCell(ft.Text(trans[2])),
                    ft.DataCell(ft.Text(f"${trans[3]:.2f}")),
                    ft.DataCell(ft.Text(trans[4])),
                ],
                color=ft.colors.GREEN_200 if trans[4] == 'ingreso' else ft.colors.RED_200
            ) for trans in filtered
        ]
        page.update()

    type_filter = ft.Dropdown(
        label="Filtrar por tipo",
        options=[
            ft.dropdown.Option("Todos"),
            ft.dropdown.Option("Ingreso"),
            ft.dropdown.Option("Gasto"),
        ],
        on_change=filter_transactions,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_color=ft.colors.BLUE_200
    )

    date_filter = ft.TextField(
        label="Filtrar por fecha (YYYY-MM-DD)", 
        on_change=filter_transactions,
        bgcolor=ft.colors.BLUE_GREY_800,
        border_color=ft.colors.BLUE_200
    )

    def change_month(delta):
        nonlocal current_date
        current_date = (current_date.replace(day=1) + timedelta(days=32 * delta)).replace(day=1)
        month_year.value = current_date.strftime("%B %Y")
        update_chart()
        update_balance()
        page.update()

    prev_month = ft.IconButton(
        icon=ft.icons.ARROW_BACK,
        on_click=lambda _: change_month(-1),
        icon_color=ft.colors.BLUE_200
    )

    next_month = ft.IconButton(
        icon=ft.icons.ARROW_FORWARD,
        on_click=lambda _: change_month(1),
        icon_color=ft.colors.BLUE_200
    )

    month_year = ft.Text(
        current_date.strftime("%B %Y"),
        size=20,
        color=ft.colors.BLUE_200,
        text_align=ft.TextAlign.CENTER,
    )

    month_navigation = ft.Row(
        [prev_month, month_year, next_month],
        alignment=ft.MainAxisAlignment.CENTER
    )

    update_chart()
    update_table()
    update_balance()

    page.add(
        ft.ResponsiveRow([
            ft.Column([
                title,
                ft.Row([date_button, selected_date], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([description, amount, transaction_type], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([add_button], alignment=ft.MainAxisAlignment.CENTER),
                balance_text,
                month_navigation,
                ft.Container(chart, padding=20, bgcolor=ft.colors.BLUE_GREY_800, border_radius=10),
                chart_legend,
                ft.Text("Transactions", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_200),
                ft.Row([type_filter, date_filter], wrap=True),
                ft.Container(
                    content=table,                    
                    height=300,
                    expand=True
                )
            ], col={"sm": 12, "md": 12, "lg": 12})
        ])
    )

ft.app(target=main)