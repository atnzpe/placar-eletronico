
# timer_display.py
import flet as ft
import logging

# Configuração de telemetria isolada
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s')

COR_TEXTO_ESCURO = "#333333" #
COR_FUNDO_BRANCO = "#ffffff" #

def build_timer_display(timer_input, start_cb, pause_cb, finish_cb):
    """
    Constrói o componente visual do relógio central.
    Encapsula a interface do timer, isolando-a da lógica de orquestração do main.py.
    """
    logging.debug("Instanciando o Componente Visual do Relógio Central (TimerDisplay).")
    
    return ft.Column([
        ft.Text("Tempo de Luta:", size=24, color=COR_TEXTO_ESCURO, font_family="Montserrat", weight=ft.FontWeight.BOLD),
        
        # O TextField do relógio instanciado no main.py é injetado aqui
        timer_input,
        
        # Botões de controle atualizados para a nova API ft.Button
        ft.Row([
            ft.Button("Iniciar", on_click=start_cb, color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
            ft.Button("Parar", on_click=pause_cb, color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
            ft.Button("Terminar", on_click=finish_cb, color=COR_FUNDO_BRANCO, bgcolor=COR_TEXTO_ESCURO)
        ], alignment=ft.MainAxisAlignment.CENTER),
        
    ], alignment=ft.MainAxisAlignment.START, horizontal_alignment=ft.CrossAxisAlignment.CENTER)