import flet as ft
import time
import threading
import csv
import os
from datetime import datetime
from fpdf import FPDF

# --- PALETA OFICIAL CBSA ---
COR_AZUL_CBSA = "#002776"
COR_VERDE_CBSA = "#009c3b"
COR_AMARELO_CBSA = "#ffdf00"
COR_VERMELHO_ALERTA = "#DB2E20"
COR_TEXTO_ESCURO = "#333333"
COR_FUNDO_CLARO = "#f4f4f5"
COR_FUNDO_BRANCO = "#ffffff"

def main(page: ft.Page):
    page.title = "Placar CBSA"
    page.bgcolor = COR_FUNDO_CLARO 
    page.padding = 10
    page.window.width = 1280
    page.window.height = 720
    
    page.fonts = {
        "Montserrat": "https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap",
        "Open Sans": "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap"
    }

    state = {
        "red_score": 0,
        "blue_score": 0,
        "timer_running": False,
        "time_left": 300 
    }

    dropdown_style = ft.TextStyle(font_family="Open Sans", color=COR_TEXTO_ESCURO)
    
    # --- CONTROLES DE RELATÓRIO (FLAG E FORMATO) ---
    # CORREÇÃO APLICADA: label_style alterado para label_text_style
    gerar_relatorio_flag = ft.Switch(
        label="Gerar Relatório Automático", 
        value=True, 
        label_text_style=ft.TextStyle(color=COR_FUNDO_BRANCO, font_family="Montserrat", size=14), 
        active_color=COR_AMARELO_CBSA
    )
    
    formato_relatorio = ft.Dropdown(
        options=[ft.dropdown.Option("CSV"), ft.dropdown.Option("PDF")], 
        value="CSV", width=100, height=45, bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, text_style=dropdown_style
    )

    cat_dropdown = ft.Dropdown(options=[ft.dropdown.Option("Escolar"), ft.dropdown.Option("Esportivo"), ft.dropdown.Option("Beach"), ft.dropdown.Option("Combat")], value="Escolar", width=150, text_style=dropdown_style, bgcolor=COR_FUNDO_BRANCO, border_color=COR_TEXTO_ESCURO)
    gen_dropdown = ft.Dropdown(options=[ft.dropdown.Option("Feminino"), ft.dropdown.Option("Masculino")], value="Feminino", width=150, text_style=dropdown_style, bgcolor=COR_FUNDO_BRANCO, border_color=COR_TEXTO_ESCURO)
    weight_input = ft.TextField(value="52", width=80, text_style=dropdown_style, bgcolor=COR_FUNDO_BRANCO, border_color=COR_TEXTO_ESCURO)
    
    red_name = ft.TextField(bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40, expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"))
    red_gym = ft.TextField(bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40, expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"))
    blue_name = ft.TextField(bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40, expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"))
    blue_gym = ft.TextField(bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40, expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"))
    
    red_score_display = ft.Text("0", size=150, color=COR_TEXTO_ESCURO, font_family="Montserrat")
    blue_score_display = ft.Text("0", size=150, color=COR_TEXTO_ESCURO, font_family="Montserrat")

    winner_display = ft.TextField(value="", text_align=ft.TextAlign.CENTER, text_size=20, text_style=ft.TextStyle(font_family="Montserrat", weight=ft.FontWeight.BOLD), bgcolor=COR_FUNDO_BRANCO, width=220, height=40, border_color=COR_TEXTO_ESCURO)
    arrow_display = ft.TextField(value="", text_align=ft.TextAlign.CENTER, text_size=20, text_style=ft.TextStyle(font_family="Montserrat", weight=ft.FontWeight.BOLD), bgcolor=COR_FUNDO_BRANCO, width=220, height=40, border_color=COR_TEXTO_ESCURO)

    def change_score(color, amount):
        if color == "red":
            state["red_score"] = max(0, state["red_score"] + amount)
            red_score_display.value = str(state["red_score"])
        else:
            state["blue_score"] = max(0, state["blue_score"] + amount)
            blue_score_display.value = str(state["blue_score"])
        page.update()

    def clear_data(color):
        if color == "red":
            state["red_score"] = 0
            red_score_display.value = "0"
            red_name.value = ""
            red_gym.value = ""
        else:
            state["blue_score"] = 0
            blue_score_display.value = "0"
            blue_name.value = ""
            blue_gym.value = ""
        winner_display.value = ""
        arrow_display.value = ""
        page.update()

    def gerar_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "Súmula Oficial de Luta - CBSA", ln=True, align='C')
        
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(0, 10, f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, align='C')
        pdf.cell(0, 10, f"Categoria: {cat_dropdown.value} | Naipe: {gen_dropdown.value} | Peso: {weight_input.value} Kg", ln=True, align='C')
        pdf.ln(10)
        
        pdf.set_font("Helvetica", 'B', 14)
        pdf.set_text_color(219, 46, 32)
        pdf.cell(95, 10, f"[VERMELHO] Atleta: {red_name.value or 'N/I'}", ln=False)
        pdf.set_text_color(0, 39, 118)
        pdf.cell(95, 10, f"[AZUL] Atleta: {blue_name.value or 'N/I'}", ln=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(95, 10, f"Academia: {red_gym.value or 'N/I'}", ln=False)
        pdf.cell(95, 10, f"Academia: {blue_gym.value or 'N/I'}", ln=True)
        
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(95, 10, f"Pontos Finais: {state['red_score']}", ln=False)
        pdf.cell(95, 10, f"Pontos Finais: {state['blue_score']}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 15, f"RESULTADO: {winner_display.value.upper()}", ln=True, align='C', border=1)
        
        nome_arquivo = f"Sumula_{red_name.value or 'V'}_vs_{blue_name.value or 'A'}_{datetime.now().strftime('%H%M%S')}.pdf".replace(" ", "_")
        pdf.output(nome_arquivo)
        return nome_arquivo

    def gerar_csv():
        file_path = "resultados_cbsa.csv"
        file_exists = os.path.isfile(file_path)
        with open(file_path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            if not file_exists:
                writer.writerow(["Data/Hora", "Categoria", "Naipe", "Peso(Kg)", "Atleta_Verm", "Acad_Verm", "Pts_Verm", "Atleta_Azul", "Acad_Azul", "Pts_Azul", "Resultado"])
            writer.writerow([
                datetime.now().strftime("%d/%m/%Y %H:%M"), cat_dropdown.value, gen_dropdown.value, weight_input.value,
                red_name.value, red_gym.value, state["red_score"], blue_name.value, blue_gym.value, state["blue_score"], winner_display.value
            ])
        return file_path

    def finish_match(e=None):
        state["timer_running"] = False
        
        if state["red_score"] > state["blue_score"]:
            winner_display.value = "Vencedor Vermelho"
            winner_display.color = COR_VERMELHO_ALERTA
            arrow_display.value = "<<===="
            arrow_display.color = COR_VERMELHO_ALERTA
        elif state["blue_score"] > state["red_score"]:
            winner_display.value = "Vencedor Azul"
            winner_display.color = COR_AZUL_CBSA
            arrow_display.value = "====>>"
            arrow_display.color = COR_AZUL_CBSA
        else:
            winner_display.value = "Empate"
            winner_display.color = COR_TEXTO_ESCURO
            arrow_display.value = "======"
            arrow_display.color = COR_TEXTO_ESCURO
            
        page.update()
        
        if gerar_relatorio_flag.value:
            if formato_relatorio.value == "CSV":
                arquivo_gerado = gerar_csv()
                mensagem = f"Luta salva na planilha: {arquivo_gerado}"
            else:
                arquivo_gerado = gerar_pdf()
                mensagem = f"Súmula PDF gerada: {arquivo_gerado}"
                
            page.snack_bar = ft.SnackBar(ft.Text(mensagem, color=COR_FUNDO_BRANCO, font_family="Open Sans"), bgcolor=COR_VERDE_CBSA)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Luta finalizada (Relatório NÃO foi gerado).", color=COR_FUNDO_BRANCO, font_family="Open Sans"), bgcolor=COR_TEXTO_ESCURO)
            
        page.snack_bar.open = True
        page.update()

    # --- LÓGICA DO CRONÔMETRO ---
    timer_input = ft.TextField(
        value="05:00", text_align=ft.TextAlign.CENTER, text_size=55, 
        text_style=ft.TextStyle(font_family="Montserrat", weight=ft.FontWeight.BOLD, color=COR_TEXTO_ESCURO),
        bgcolor=COR_FUNDO_BRANCO, border_color=COR_TEXTO_ESCURO, width=250, height=100
    )

    def update_timer_thread():
        while True:
            if state["timer_running"] and state["time_left"] > 0:
                state["time_left"] -= 1
                mins, secs = divmod(state["time_left"], 60)
                timer_input.value = f"{mins:02d}:{secs:02d}"
                page.update()
                
                if state["time_left"] == 0:
                    finish_match() 
                    
            time.sleep(1)

    threading.Thread(target=update_timer_thread, daemon=True).start()

    def start_timer(e):
        if not state["timer_running"]:
            try:
                parts = timer_input.value.split(":")
                state["time_left"] = int(parts[0]) * 60 + int(parts[1])
            except:
                pass
            state["timer_running"] = True
            winner_display.value = ""
            arrow_display.value = ""
            page.update()

    def pause_timer(e):
        state["timer_running"] = False
        page.update()

    # --- CONSTRUÇÃO DA INTERFACE ---
    
    menu = ft.Container(
        bgcolor=COR_VERDE_CBSA,
        padding=5,
        content=ft.Row([
            ft.Row([
                gerar_relatorio_flag,
                ft.Text("Formato:", color=COR_FUNDO_BRANCO, font_family="Montserrat", size=14),
                formato_relatorio
            ]),
            ft.Row([
                ft.TextButton("Informar", style=ft.ButtonStyle(color=COR_FUNDO_BRANCO)),
                ft.TextButton("Sair do Programa", style=ft.ButtonStyle(color=COR_FUNDO_BRANCO), on_click=lambda _: page.window.destroy())
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

    header = ft.Column([
        ft.Row([
            ft.Image(src="brand.png", height=90, fit=ft.ImageFit.CONTAIN),
            ft.Text("CONFEDERAÇÃO BRASILEIRA DE SAMBO", color=COR_VERDE_CBSA, size=32, font_family="Montserrat", weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER),
            ft.Image(src="upasa.jpg", height=90, fit=ft.ImageFit.CONTAIN),
            ft.Container(width=20), 
            ft.Image(src="cob.jpg", height=90, fit=ft.ImageFit.CONTAIN),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        
        ft.Row([
            ft.Text("Categoria:", color=COR_TEXTO_ESCURO, size=20, font_family="Montserrat", weight=ft.FontWeight.BOLD),
            cat_dropdown, gen_dropdown,
            ft.Text("Peso:", color=COR_TEXTO_ESCURO, size=20, font_family="Montserrat", weight=ft.FontWeight.BOLD),
            weight_input, ft.Text("Kg", color=COR_TEXTO_ESCURO, size=20, font_family="Montserrat", weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER)
    ])

    center_col = ft.Column([
        ft.Text("Tempo de Luta:", size=24, color=COR_TEXTO_ESCURO, font_family="Montserrat", weight=ft.FontWeight.BOLD),
        timer_input,
        ft.Row([
            ft.ElevatedButton("Iniciar", on_click=start_timer, color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
            ft.ElevatedButton("Parar", on_click=pause_timer, color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
            ft.ElevatedButton("Terminar", on_click=finish_match, color=COR_FUNDO_BRANCO, bgcolor=COR_TEXTO_ESCURO)
        ], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=10),
        winner_display,
        arrow_display
    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=1)

    def create_athlete_panel(color_bg, score_display, color_id, ref_name, ref_gym):
        return ft.Container(
            bgcolor=color_bg, padding=15, expand=2, border_radius=10, 
            content=ft.Column([
                ft.Row([ft.Text("Atleta:", size=18, color=COR_FUNDO_BRANCO, font_family="Montserrat"), ref_name]),
                ft.Row([ft.Text("Academia:", size=18, color=COR_FUNDO_BRANCO, font_family="Montserrat"), ref_gym]),
                ft.Row([
                    ft.Column([
                        ft.Text("== Pontos ==", size=20, color=COR_FUNDO_BRANCO, font_family="Montserrat"),
                        ft.Row([
                            ft.ElevatedButton("+1", on_click=lambda e, c=color_id: change_score(c, 1), color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
                            ft.ElevatedButton("+2", on_click=lambda e, c=color_id: change_score(c, 2), color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
                            ft.ElevatedButton("+4", on_click=lambda e, c=color_id: change_score(c, 4), color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
                        ]),
                        ft.ElevatedButton("- 1", on_click=lambda e, c=color_id: change_score(c, -1), color=COR_FUNDO_BRANCO, bgcolor=COR_TEXTO_ESCURO, width=150),
                        ft.Container(height=10),
                        ft.Text("Vantagem", size=16, color=COR_FUNDO_BRANCO, font_family="Montserrat"),
                        ft.TextField(value="0", text_align=ft.TextAlign.CENTER, text_size=25, width=100, height=60, bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, border_color=COR_TEXTO_ESCURO)
                    ], alignment=ft.MainAxisAlignment.START),
                    ft.Container(content=score_display, bgcolor=COR_FUNDO_BRANCO, border=ft.border.all(2, COR_TEXTO_ESCURO), border_radius=5, expand=True, alignment=ft.alignment.center)
                ], expand=True),
                ft.Row([
                    ft.ElevatedButton("Limpar Dados", on_click=lambda e, c=color_id: clear_data(c), color=COR_TEXTO_ESCURO, bgcolor=COR_AMARELO_CBSA), 
                    ft.Row([
                        ft.Text("Faltas", size=16, color=COR_FUNDO_BRANCO, font_family="Montserrat"),
                        ft.TextField(value="0", text_align=ft.TextAlign.CENTER, text_size=25, width=70, height=60, bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, border_color=COR_TEXTO_ESCURO)
                    ])
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ])
        )

    red_panel = create_athlete_panel(COR_VERMELHO_ALERTA, red_score_display, "red", red_name, red_gym)
    blue_panel = create_athlete_panel(COR_AZUL_CBSA, blue_score_display, "blue", blue_name, blue_gym)

    page.add(menu, ft.Container(height=5), header, ft.Container(height=10), ft.Row([red_panel, center_col, blue_panel], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN))

# CORREÇÃO APLICADA: ft.app alterado para ft.run 
ft.run(target=main, assets_dir=".")