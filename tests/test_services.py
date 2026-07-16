import unittest
import os
from src.services.csv_service import gerar_csv
from src.services.pdf_service import gerar_pdf

class TestServicosRelatorios(unittest.TestCase):
    """
    Testes de QA para validar se a refatoração MVVM quebrou a geração de arquivos.
    Esses testes não rodam a tela gráfica do Flet, focam puramente nas regras de negócio.
    """

    def setUp(self):
        # Dicionário emulador do estado exato enviado pela Interface
        self.dados_luta_mock = {
            "categoria": "Combat", "naipe": "Masculino", "peso": "74",
            "red_name": "Gleyson Atanazio", "red_gym": "Leão do Norte", "red_score": 5,
            "blue_name": "Atleta Desafiante", "blue_gym": "Academia Alpha", "blue_score": 3,
            "resultado": "Vencedor Vermelho"
        }

    def test_geracao_csv_cria_arquivo(self):
        arquivo_csv = gerar_csv(self.dados_luta_mock)
        self.assertTrue(os.path.exists(arquivo_csv), "O serviço CSV falhou em criar o arquivo no disco.")

    def test_geracao_pdf_cria_arquivo(self):
        arquivo_pdf = gerar_pdf(self.dados_luta_mock)
        self.assertTrue(os.path.exists(arquivo_pdf), "O serviço PDF falhou em criar a súmula no disco.")
        # Limpeza para evitar acúmulo de arquivos falsos na máquina durante os testes
        if os.path.exists(arquivo_pdf):
            os.remove(arquivo_pdf)

if __name__ == '__main__':
    unittest.main()