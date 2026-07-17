import flet as ft
import logging

# Configuração de telemetria isolada para este componente visual
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s')

COR_FUNDO_BRANCO = "#ffffff"
COR_TEXTO_ESCURO = "#333333"
COR_AMARELO_CBSA = "#ffdf00"

def build_athlete_panel(color_bg, score_display, color_id, ref_name, ref_gym, change_score_cb, clear_data_cb):
    """
    Constrói e retorna o painel visual do atleta (Vermelho ou Azul).
    A arquitetura foi atualizada para compatibilidade com as novas APIs de Button, Border e Alignment do Flet.
    """
    logging.debug(f"Instanciando o Componente Visual (AthletePanel) para o lado: {color_id.upper()}")
    
    # Construção explícita da borda para evitar AttributeError na API do Flet
    borda_padrao = ft.Border(
        top=ft.BorderSide(width=2, color=COR_TEXTO_ESCURO),
        right=ft.BorderSide(width=2, color=COR_TEXTO_ESCURO),
        bottom=ft.BorderSide(width=2, color=COR_TEXTO_ESCURO),
        left=ft.BorderSide(width=2, color=COR_TEXTO_ESCURO)
    )
    
    # Alinhamento central explícito usando coordenadas matemáticas (x=0, y=0)
    alinhamento_central = ft.Alignment(x=0, y=0)
    
    return ft.Container(
        bgcolor=color_bg, 
        padding=15, 
        expand=2, 
        border_radius=10, 
        content=ft.Column([
            
            # --- Seção de Identificação ---
            ft.Row([ft.Text("Atleta:", size=18, color=COR_FUNDO_BRANCO, font_family="Montserrat"), ref_name]),
            ft.Row([ft.Text("Academia:", size=18, color=COR_FUNDO_BRANCO, font_family="Montserrat"), ref_gym]),
            
            # --- Seção Central: Botões de Ponto e Display ---
            ft.Row([
                ft.Column([
                    ft.Text("== Pontos ==", size=20, color=COR_FUNDO_BRANCO, font_family="Montserrat"),
                    
                    # Correção: Uso da nova API ft.Button
                    ft.Row([
                        ft.Button("+1", on_click=lambda e, c=color_id: change_score_cb(c, 1), color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
                        ft.Button("+2", on_click=lambda e, c=color_id: change_score_cb(c, 2), color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
                        ft.Button("+4", on_click=lambda e, c=color_id: change_score_cb(c, 4), color=COR_TEXTO_ESCURO, bgcolor=COR_FUNDO_BRANCO),
                    ]),
                    
                    # Botão de decremento atualizado
                    ft.Button("- 1", on_click=lambda e, c=color_id: change_score_cb(c, -1), color=COR_FUNDO_BRANCO, bgcolor=COR_TEXTO_ESCURO, width=150),
                    
                    ft.Container(height=10),
                    
                    ft.Text("Vantagem", size=16, color=COR_FUNDO_BRANCO, font_family="Montserrat"),
                    ft.TextField(value="0", text_align=ft.TextAlign.CENTER, text_size=25, width=100, height=60, bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, border_color=COR_TEXTO_ESCURO)
                ], alignment=ft.MainAxisAlignment.START),
                
                # Caixote de pontuação com a nova declaração explícita de borda e alinhamento
                ft.Container(
                    content=score_display, 
                    bgcolor=COR_FUNDO_BRANCO, 
                    border=borda_padrao, 
                    border_radius=5, 
                    expand=True, 
                    alignment=alinhamento_central
                )
            ], expand=True),
            
            # --- Seção Inferior: Faltas e Limpeza ---
            ft.Row([
                # Botão de limpeza atualizado
                ft.Button("Limpar Dados", on_click=lambda e, c=color_id: clear_data_cb(c), color=COR_TEXTO_ESCURO, bgcolor=COR_AMARELO_CBSA), 
                
                ft.Row([
                    ft.Text("Faltas", size=16, color=COR_FUNDO_BRANCO, font_family="Montserrat"),
                    ft.TextField(value="0", text_align=ft.TextAlign.CENTER, text_size=25, width=70, height=60, bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, border_color=COR_TEXTO_ESCURO)
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])
    )