import csv
import os
import logging
from datetime import datetime

# Configuração rigorosa de telemetria (QA/Debug)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s')

def gerar_csv(dados_luta: dict) -> str:
    """
    Serviço isolado para gravação de resultados no banco de dados local (CSV).
    Recebe um dicionário limpo contendo apenas as strings e inteiros da partida,
    desacoplando completamente a regra de negócio da interface gráfica (Flet).
    """
    logging.info("Iniciando serviço de exportação para CSV.")
    file_path = "resultados_cbsa.csv"
    file_exists = os.path.isfile(file_path)
    
    try:
        # Abertura do arquivo com utf-8-sig para garantir a acentuação correta no Excel
        with open(file_path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")
            
            # Se o arquivo não existe, injeta o cabeçalho
            if not file_exists:
                logging.debug("Arquivo CSV base não encontrado. Criando novos cabeçalhos.")
                writer.writerow([
                    "Data/Hora", "Categoria", "Naipe", "Peso(Kg)", 
                    "Atleta_Verm", "Acad_Verm", "Pts_Verm", 
                    "Atleta_Azul", "Acad_Azul", "Pts_Azul", "Resultado"
                ])
            
            # Escreve os dados consumindo o dicionário
            writer.writerow([
                datetime.now().strftime("%d/%m/%Y %H:%M"), 
                dados_luta.get("categoria", "N/I"), 
                dados_luta.get("naipe", "N/I"), 
                dados_luta.get("peso", "0"),
                dados_luta.get("red_name", "N/I"), 
                dados_luta.get("red_gym", "N/I"), 
                dados_luta.get("red_score", 0), 
                dados_luta.get("blue_name", "N/I"), 
                dados_luta.get("blue_gym", "N/I"), 
                dados_luta.get("blue_score", 0), 
                dados_luta.get("resultado", "N/I")
            ])
            
        logging.info(f"Dados consolidados com sucesso no CSV: {file_path}")
        return file_path
        
    except Exception as e:
        # Registra o erro no log para depuração em produção
        logging.error(f"Falha crítica no serviço de escrita CSV: {e}")
        raise e