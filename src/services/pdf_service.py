import logging
from datetime import datetime
from fpdf import FPDF

# Configuração de telemetria
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s')

def gerar_pdf(dados_luta: dict) -> str:
    """
    Serviço isolado para montagem do layout e compilação do relatório em PDF.
    Recebe os dados da camada de UI (View) através de um dicionário padronizado.
    """
    logging.info("Iniciando serviço de renderização do PDF Oficial CBSA.")
    try:
        pdf = FPDF()
        pdf.add_page()
        
        # Cabeçalho Principal
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 10, "Súmula Oficial de Luta - CBSA", ln=True, align='C')
        
        # Metadados do Evento
        pdf.set_font("Helvetica", '', 12)
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        pdf.cell(0, 10, f"Data/Hora: {data_hora}", ln=True, align='C')
        
        cat = dados_luta.get("categoria", "N/I")
        naipe = dados_luta.get("naipe", "N/I")
        peso = dados_luta.get("peso", "0")
        pdf.cell(0, 10, f"Categoria: {cat} | Naipe: {naipe} | Peso: {peso} Kg", ln=True, align='C')
        pdf.ln(10)
        
        # Identificação dos Atletas e Cores
        red_name = dados_luta.get("red_name", "N/I") or "N/I"
        blue_name = dados_luta.get("blue_name", "N/I") or "N/I"
        
        pdf.set_font("Helvetica", 'B', 14)
        pdf.set_text_color(219, 46, 32) # Hex: DB2E20
        pdf.cell(95, 10, f"[VERMELHO] Atleta: {red_name}", ln=False)
        
        pdf.set_text_color(0, 39, 118) # Hex: 002776
        pdf.cell(95, 10, f"[AZUL] Atleta: {blue_name}", ln=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", '', 12)
        pdf.cell(95, 10, f"Academia: {dados_luta.get('red_gym', 'N/I') or 'N/I'}", ln=False)
        pdf.cell(95, 10, f"Academia: {dados_luta.get('blue_gym', 'N/I') or 'N/I'}", ln=True)
        
        # Pontuações e Resultado Final
        pdf.set_font("Helvetica", 'B', 14)
        pdf.cell(95, 10, f"Pontos Finais: {dados_luta.get('red_score', 0)}", ln=False)
        pdf.cell(95, 10, f"Pontos Finais: {dados_luta.get('blue_score', 0)}", ln=True)
        
        pdf.ln(10)
        pdf.set_font("Helvetica", 'B', 16)
        pdf.cell(0, 15, f"RESULTADO: {dados_luta.get('resultado', '').upper()}", ln=True, align='C', border=1)
        
        # Estruturação e higienização do nome do arquivo salvo
        nome_base_red = red_name.replace(" ", "") if red_name != "N/I" else "Verm"
        nome_base_blue = blue_name.replace(" ", "") if blue_name != "N/I" else "Azul"
        nome_arquivo = f"Sumula_{nome_base_red}_vs_{nome_base_blue}_{datetime.now().strftime('%H%M%S')}.pdf"
        
        pdf.output(nome_arquivo)
        logging.info(f"Súmula PDF gerada com sucesso e salva como: {nome_arquivo}")
        return nome_arquivo
        
    except Exception as e:
        logging.error(f"Falha de compilação FPDF: {e}")
        raise e