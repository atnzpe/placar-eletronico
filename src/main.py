"""
Placar CBSA — Interface Gráfica Principal.

Este módulo constrói a mesa operadora (placar eletrônico) usando Flet e
implementa o sistema de navegação multi-telas via page.on_route_change.

Diretrizes aplicadas neste arquivo (por decisão da equipe):
    1. Toda função possui logging claro (INFO para eventos de negócio,
       DEBUG para detalhes de UI, ERROR para falhas).
    2. Toda função possui try/except, sem exceção, registrando o erro
       de forma explícita (nunca falhamos em silêncio — Zen of Python:
       "Errors should never pass silently. Unless explicitly silenced.").
    3. Toda função é comentada explicitamente, para leitura por qualquer
       pessoa da equipe.
    4. Seguimos o Zen of Python (import this): explícito é melhor que
       implícito, simples é melhor que complexo, plano é melhor que
       aninhado, legibilidade conta.
"""

import logging
import threading
import time

import flet as ft

# IMPORTAÇÃO DA NOSSA ARQUITETURA (SERVIÇOS E COMPONENTES)
from services.pdf_service import gerar_pdf
from services.csv_service import gerar_csv
from components.athlete_panel import build_athlete_panel
from components.timer_display import build_timer_display

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO DE LOGGING
# Log claro e padronizado: hora, nível, nome da função e mensagem.
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s",
)

# ---------------------------------------------------------------------------
# PALETA DE CORES DA CBSA
# Mantidas como constantes explícitas no topo do módulo (fácil de localizar
# e alterar sem precisar caçar valores mágicos espalhados pelo código).
# ---------------------------------------------------------------------------
COR_AZUL_CBSA = "#002776"
COR_VERDE_CBSA = "#009c3b"
COR_AMARELO_CBSA = "#ffdf00"
COR_VERMELHO_ALERTA = "#DB2E20"
COR_TEXTO_ESCURO = "#333333"
COR_FUNDO_CLARO = "#f4f4f5"
COR_FUNDO_BRANCO = "#ffffff"


def main(page: ft.Page) -> None:
    """
    Ponto de entrada da aplicação Flet.

    Monta todos os controles visuais, registra os callbacks de negócio
    (pontuação, timer, relatórios) e configura o sistema de rotas
    (page.on_route_change / page.on_view_pop) que permite múltiplas telas
    (ex.: mesa operadora em "/" e telão público em "/telao").
    """
    try:
        logging.info("Inicializando a Interface Gráfica Principal (View).")

        # -------------------------------------------------------------
        # CONFIGURAÇÕES GERAIS DA JANELA/PÁGINA
        # -------------------------------------------------------------
        page.title = "Placar CBSA"
        page.bgcolor = COR_FUNDO_CLARO
        page.padding = 0  # Controle total das margens da janela.
        page.window.width = 1280
        page.window.height = 720
        page.fonts = {
            "Montserrat": "https://fonts.googleapis.com/css2?family=Montserrat:wght@700&display=swap",
            "Open Sans": "https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap",
        }
    except Exception as erro:
        # Se a própria configuração básica da página falhar, não há como
        # continuar — registramos e propagamos o erro.
        logging.error(
            f"Falha ao configurar propriedades básicas da página: {erro}")
        raise

    # -------------------------------------------------------------------
    # ESTADO CENTRAL DA APLICAÇÃO
    # Um único dicionário mutável compartilhado pelos callbacks (closures).
    # Explícito é melhor que implícito: todo estado mutável vive aqui.
    # -------------------------------------------------------------------
    state = {
        "red_score": 0,
        "blue_score": 0,
        "timer_running": False,
        "time_left": 300,
    }

    dropdown_style = ft.TextStyle(
        font_family="Open Sans", color=COR_TEXTO_ESCURO)

    gerar_relatorio_flag = ft.Switch(
        label="Gerar Relatório Automático",
        value=True,
        label_text_style=ft.TextStyle(
            color=COR_FUNDO_BRANCO, font_family="Montserrat", size=14
        ),
        active_color=COR_AMARELO_CBSA,
    )

    formato_relatorio = ft.Dropdown(
        options=[ft.dropdown.Option("CSV"), ft.dropdown.Option("PDF")],
        value="CSV",
        width=100,
        height=45,
        bgcolor=COR_FUNDO_BRANCO,
        color=COR_TEXTO_ESCURO,
        text_style=dropdown_style,
    )

    cat_dropdown = ft.Dropdown(
        options=[
            ft.dropdown.Option("Escolar"),
            ft.dropdown.Option("Esportivo"),
            ft.dropdown.Option("Beach"),
            ft.dropdown.Option("Combat"),
        ],
        value="Escolar",
        width=150,
        text_style=dropdown_style,
        bgcolor=COR_FUNDO_BRANCO,
        border_color=COR_TEXTO_ESCURO,
    )
    gen_dropdown = ft.Dropdown(
        options=[ft.dropdown.Option("Feminino"),
                 ft.dropdown.Option("Masculino")],
        value="Feminino",
        width=150,
        text_style=dropdown_style,
        bgcolor=COR_FUNDO_BRANCO,
        border_color=COR_TEXTO_ESCURO,
    )
    weight_input = ft.TextField(
        value="52",
        width=80,
        text_style=dropdown_style,
        bgcolor=COR_FUNDO_BRANCO,
        border_color=COR_TEXTO_ESCURO,
    )

    # Referências Visuais dos Atletas.
    red_name = ft.TextField(
        bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40,
        expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"),
    )
    red_gym = ft.TextField(
        bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40,
        expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"),
    )
    blue_name = ft.TextField(
        bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40,
        expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"),
    )
    blue_gym = ft.TextField(
        bgcolor=COR_FUNDO_BRANCO, color=COR_TEXTO_ESCURO, height=40,
        expand=True, content_padding=5, text_style=ft.TextStyle(font_family="Open Sans"),
    )

    red_score_display = ft.Text(
        "0", size=150, color=COR_TEXTO_ESCURO, font_family="Montserrat")
    blue_score_display = ft.Text(
        "0", size=150, color=COR_TEXTO_ESCURO, font_family="Montserrat")

    winner_display = ft.TextField(
        value="", text_align=ft.TextAlign.CENTER, text_size=20,
        text_style=ft.TextStyle(font_family="Montserrat",
                                weight=ft.FontWeight.BOLD),
        bgcolor=COR_FUNDO_BRANCO, width=220, height=40, border_color=COR_TEXTO_ESCURO,
    )
    arrow_display = ft.TextField(
        value="", text_align=ft.TextAlign.CENTER, text_size=20,
        text_style=ft.TextStyle(font_family="Montserrat",
                                weight=ft.FontWeight.BOLD),
        bgcolor=COR_FUNDO_BRANCO, width=220, height=40, border_color=COR_TEXTO_ESCURO,
    )

    timer_input = ft.TextField(
        value="05:00", text_align=ft.TextAlign.CENTER, text_size=55,
        text_style=ft.TextStyle(
            font_family="Montserrat", weight=ft.FontWeight.BOLD, color=COR_TEXTO_ESCURO),
        bgcolor=COR_FUNDO_BRANCO, border_color=COR_TEXTO_ESCURO, width=250, height=100,
    )

    # =====================================================================
    # REGRAS DE NEGÓCIO (callbacks)
    # =====================================================================

    def change_score(color: str, amount: int) -> None:
        """Altera a pontuação (soma/subtrai) de um dos atletas e atualiza a tela."""
        try:
            logging.debug(
                f"Alterando score via evento do componente: {color} | Valor: {amount}")
            if color == "red":
                state["red_score"] = max(0, state["red_score"] + amount)
                red_score_display.value = str(state["red_score"])
            else:
                state["blue_score"] = max(0, state["blue_score"] + amount)
                blue_score_display.value = str(state["blue_score"])
            page.update()
        except Exception as erro:
            # Nunca falhamos em silêncio: registramos o erro com contexto
            # suficiente para diagnosticar (cor e valor recebidos).
            logging.error(
                f"Falha ao alterar score (color={color}, amount={amount}): {erro}")

    async def fechar_aplicacao(e) -> None:
        await page.window.close()

    def clear_data(color: str) -> None:
        """Zera a pontuação e limpa os dados (nome/academia) de um atleta."""
        try:
            logging.info(f"Limpando dados via evento do componente: {color}")
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
        except Exception as erro:
            logging.error(
                f"Falha ao limpar dados do atleta (color={color}): {erro}")

    def finish_match(e=None) -> None:
        """
        Encerra a luta: define o vencedor, atualiza a tela e, se solicitado,
        gera o relatório (CSV ou PDF) com os dados da luta.
        """
        try:
            logging.info("Luta encerrada. Disparando geração de relatórios.")
            state["timer_running"] = False
            # Destrava o campo de tempo para permitir configurar a próxima luta.
            timer_input.read_only = False

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
        except Exception as erro:
            logging.error(
                f"Falha ao calcular/exibir o resultado da luta: {erro}")
            return  # Sem resultado calculado, não faz sentido gerar relatório.

        # A geração de relatório é isolada em seu próprio bloco try/except
        # para que uma falha no serviço de PDF/CSV não impeça o restante
        # da função de já ter atualizado a tela com o vencedor.
        try:
            dados_luta = {
                "categoria": cat_dropdown.value, "naipe": gen_dropdown.value, "peso": weight_input.value,
                "red_name": red_name.value, "red_gym": red_gym.value, "red_score": state["red_score"],
                "blue_name": blue_name.value, "blue_gym": blue_gym.value, "blue_score": state["blue_score"],
                "resultado": winner_display.value,
            }

            if gerar_relatorio_flag.value:
                if formato_relatorio.value == "CSV":
                    arquivo_gerado = gerar_csv(dados_luta)
                    mensagem = f"Luta salva na planilha: {arquivo_gerado}"
                else:
                    arquivo_gerado = gerar_pdf(dados_luta)
                    mensagem = f"Súmula PDF gerada: {arquivo_gerado}"

                page.snack_bar = ft.SnackBar(
                    ft.Text(mensagem, color=COR_FUNDO_BRANCO,
                            font_family="Open Sans"),
                    bgcolor=COR_VERDE_CBSA,
                )
            else:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Luta finalizada (Relatório NÃO foi gerado).",
                            color=COR_FUNDO_BRANCO, font_family="Open Sans"),
                    bgcolor=COR_TEXTO_ESCURO,
                )

            page.snack_bar.open = True
            page.update()
            logging.info("Relatório processado com sucesso.")
        except Exception as erro:
            logging.error(f"Falha ao gerar/exibir relatório da luta: {erro}")
            try:
                page.snack_bar = ft.SnackBar(
                    ft.Text("Erro ao gerar relatório. Veja os logs.",
                            color=COR_FUNDO_BRANCO),
                    bgcolor=COR_VERMELHO_ALERTA,
                )
                page.snack_bar.open = True
                page.update()
            except Exception as erro_snackbar:
                logging.error(
                    f"Falha até ao exibir o aviso de erro: {erro_snackbar}")

    def update_timer_thread() -> None:
        """
        Loop de background (thread daemon) responsável por decrementar o
        cronômetro a cada segundo e refletir o valor na tela em tempo real.

        CORREÇÃO DO BUG "timer não atualiza em tempo real":
        Antes, este loop não possuía try/except. Se `page.update()` falhasse
        por qualquer motivo (ex.: conexão do cliente momentaneamente
        instável, sessão sendo recriada, etc.), a exceção não tratada
        matava a thread SILENCIOSAMENTE — o cronômetro simplesmente parava
        de atualizar na tela e nenhum log indicava o motivo.
        Agora, qualquer erro de uma iteração é logado e a thread continua
        viva, tentando novamente no próximo segundo (Zen of Python:
        "Errors should never pass silently").
        """
        while True:
            try:
                if state["timer_running"] and state["time_left"] > 0:
                    state["time_left"] -= 1
                    mins, secs = divmod(state["time_left"], 60)
                    timer_input.value = f"{mins:02d}:{secs:02d}"
                    # Atualizamos o CONTROLE especificamente (timer_input.update()),
                    # além de page.update(). Isso é necessário porque, com o campo
                    # travado (read_only=True, ver start_timer), o cliente aceita a
                    # sobrescrita do valor vindo do servidor — mas o disparo do
                    # patch específico do controle garante o repaint imediato.
                    timer_input.update()
                    logging.debug(f"Timer atualizado: {timer_input.value}")
                    if state["time_left"] == 0:
                        logging.info(
                            "Tempo esgotado. Encerrando luta automaticamente.")
                        finish_match()
            except Exception as erro:
                # Registramos o erro mas NÃO interrompemos o loop: a thread
                # deve continuar tentando atualizar o timer no próximo tick.
                logging.error(
                    f"Falha ao atualizar o timer em tempo real: {erro}")
            finally:
                # O sleep fica no finally para garantir o ritmo de 1s mesmo
                # quando ocorre uma exceção acima.
                time.sleep(1)

    def start_timer(e) -> None:
        """Inicia a contagem regressiva, lendo o valor informado em timer_input."""
        try:
            if state["timer_running"]:
                logging.debug(
                    "Tentativa de iniciar timer que já está em execução — ignorado.")
                return

            try:
                parts = timer_input.value.split(":")
                state["time_left"] = int(parts[0]) * 60 + int(parts[1])
            except (ValueError, IndexError) as erro_parse:
                # Formato inválido digitado pelo usuário (ex.: "abc").
                # Não silenciamos: logamos e mantemos o time_left anterior.
                logging.error(
                    f"Formato de tempo inválido em timer_input ('{timer_input.value}'): {erro_parse}")

            state["timer_running"] = True
            winner_display.value = ""
            arrow_display.value = ""

            # CORREÇÃO DO BUG "timer só atualiza no terminal, não na janela":
            # Enquanto o TextField está editável e já recebeu foco/interação
            # do operador, o cliente (Flutter) protege o texto digitado e
            # ignora atualizações de 'value' vindas do servidor — por isso o
            # log mostrava o valor correto, mas a tela ficava parada.
            # Travando o campo (read_only=True) durante a contagem, o
            # cliente deixa de reter esse estado local e volta a aceitar
            # (e exibir) os updates enviados pelo servidor a cada segundo.
            timer_input.read_only = True

            page.update()
            logging.info(
                f"Timer iniciado com time_left={state['time_left']}s.")
        except Exception as erro:
            logging.error(f"Falha inesperada ao iniciar o timer: {erro}")

    def pause_timer(e) -> None:
        """Pausa a contagem regressiva do cronômetro."""
        try:
            state["timer_running"] = False
            # Destrava o campo para que o operador possa ajustar manualmente
            # o tempo antes de um novo início (start_timer volta a travá-lo).
            timer_input.read_only = False
            page.update()
            logging.info("Timer pausado.")
        except Exception as erro:
            logging.error(f"Falha ao pausar o timer: {erro}")

    # =====================================================================
    # MONTAGEM DOS CONTROLES VISUAIS (menu, header, painéis)
    # =====================================================================
    try:
        menu = ft.Container(
            bgcolor=COR_VERDE_CBSA, padding=5,
            content=ft.Row([
                ft.Row([gerar_relatorio_flag, ft.Text("Formato:", color=COR_FUNDO_BRANCO,
                       font_family="Montserrat", size=14), formato_relatorio]),
                ft.Row([ft.TextButton("Informar", style=ft.ButtonStyle(color=COR_FUNDO_BRANCO)),
                        ft.TextButton(
                    "Sair do Programa",
                    style=ft.ButtonStyle(color=COR_FUNDO_BRANCO),
                    on_click=fechar_aplicacao
                )])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )

        header = ft.Column([
            ft.Row([
                ft.Image(src="brand.png", height=90, fit=ft.BoxFit.CONTAIN),
                ft.Text("CONFEDERAÇÃO BRASILEIRA DE SAMBO", color=COR_VERDE_CBSA, size=32, font_family="Montserrat",
                        weight=ft.FontWeight.BOLD, expand=True, text_align=ft.TextAlign.CENTER),
                ft.Image(src="upasa.jpg", height=90, fit=ft.BoxFit.CONTAIN),
                ft.Container(width=20), ft.Image(
                    src="cob.jpg", height=90, fit=ft.BoxFit.CONTAIN),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Row([
                ft.Text("Categoria:", color=COR_TEXTO_ESCURO, size=20, font_family="Montserrat",
                        weight=ft.FontWeight.BOLD), cat_dropdown, gen_dropdown,
                ft.Text("Peso:", color=COR_TEXTO_ESCURO, size=20,
                        font_family="Montserrat", weight=ft.FontWeight.BOLD),
                weight_input,
                ft.Text("Kg", color=COR_TEXTO_ESCURO, size=20,
                        font_family="Montserrat", weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.CENTER)
        ])

        # Instanciação dos componentes visuais isolados (painéis de atleta e timer).
        red_panel = build_athlete_panel(
            color_bg=COR_VERMELHO_ALERTA, score_display=red_score_display, color_id="red",
            ref_name=red_name, ref_gym=red_gym, change_score_cb=change_score, clear_data_cb=clear_data,
        )
        blue_panel = build_athlete_panel(
            color_bg=COR_AZUL_CBSA, score_display=blue_score_display, color_id="blue",
            ref_name=blue_name, ref_gym=blue_gym, change_score_cb=change_score, clear_data_cb=clear_data,
        )
        timer_panel = build_timer_display(
            timer_input=timer_input, start_cb=start_timer, pause_cb=pause_timer, finish_cb=finish_match,
        )

        center_col = ft.Column(
            [timer_panel, ft.Container(
                height=10), winner_display, arrow_display],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=1,
        )

        # Empacotamos todo o layout da mesa operadora em uma coluna mestre.
        conteudo_mesa_operadora = ft.Column([
            menu,
            ft.Container(height=5),
            header,
            ft.Container(height=10),
            ft.Row([red_panel, center_col, blue_panel], expand=True,
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ], expand=True)
    except Exception as erro:
        logging.error(
            f"Falha ao montar os controles visuais da mesa operadora: {erro}")
        raise  # Sem os controles, a aplicação não pode continuar.

    # =====================================================================
    # SISTEMA DE ROTAS / NAVEGAÇÃO MULTI-TELAS
    # =====================================================================

    def route_change(e=None) -> None:
        """
        Reconstrói a pilha de views (page.views) de acordo com a rota atual
        (page.route). 'e=None' permite chamar esta função manualmente na
        inicialização, sem precisar de um evento de rota real.

        Rotas suportadas:
            "/"       -> Mesa de Controle (operador da luta).
            "/telao"  -> Telão Público (placeholder, será expandido depois).
        """
        try:
            logging.info(f"Navegando para a rota: {page.route}")
            page.views.clear()

            # ROTA PRINCIPAL: Mesa de Controle.
            view_principal = ft.View(
                route="/",
                controls=[ft.SafeArea(conteudo_mesa_operadora, expand=True)],
                bgcolor=COR_FUNDO_CLARO,
                padding=0,
            )
            page.views.append(view_principal)
            logging.debug("View principal ('/') adicionada à pilha de rotas.")

            # ROTA SECUNDÁRIA: Telão Público (base para o futuro).
            if page.route == "/telao":
                view_telao = ft.View(
                    route="/telao",
                    controls=[
                        ft.SafeArea(
                            ft.Container(
                                content=ft.Text(
                                    "Visão do Telão Público - Em Breve",
                                    size=40, color=COR_TEXTO_ESCURO, font_family="Montserrat",
                                ),
                                alignment=ft.alignment.center,
                                expand=True,
                            ),
                            expand=True,
                        )
                    ],
                    bgcolor=COR_FUNDO_BRANCO,
                    padding=0,
                )
                page.views.append(view_telao)
                logging.debug(
                    "View secundária ('/telao') adicionada à pilha de rotas.")

            page.update()
            logging.info(
                f"Pilha de rotas atualizada com sucesso. Total de views: {len(page.views)}")
        except Exception as erro:
            logging.error(
                f"Falha ao processar a mudança de rota ({page.route}): {erro}")

    def view_pop(e) -> None:
        """
        Callback disparado quando o usuário volta uma view (botão 'voltar').
        Remove a view do topo da pilha e navega para a nova view do topo.
        """
        try:
            if e.view is None:
                logging.debug(
                    "view_pop chamado sem view associada — nada a fazer.")
                return
            page.views.remove(e.view)
            top_view = page.views[-1]
            page.push_route(top_view.route)
            logging.info(
                f"View removida. Nova rota no topo da pilha: {top_view.route}")
        except Exception as erro:
            logging.error(f"Falha ao processar view_pop: {erro}")

    try:
        # Conecta os eventos de rota à página principal.
        page.on_route_change = route_change
        page.on_view_pop = view_pop

        # Inicia a thread do cronômetro (daemon: morre junto com o processo principal).
        threading.Thread(target=update_timer_thread, daemon=True).start()
        logging.info("Thread do timer iniciada.")

        # Chama a função manualmente para renderizar a view inicial
        # (garante que a página não fique em branco na primeira carga).
        route_change()
    except Exception as erro:
        logging.error(
            f"Falha crítica na inicialização de rotas/thread do timer: {erro}")
        raise


try:
    ft.run(main, assets_dir=".")
except Exception as erro_fatal:
    logging.error(f"Falha fatal ao iniciar a aplicação Flet: {erro_fatal}")
    raise
