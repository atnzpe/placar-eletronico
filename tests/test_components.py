import unittest
import flet as ft
from src.components.athlete_panel import build_athlete_panel
from src.components.timer_display import build_timer_display

class TestAthletePanelComponent(unittest.TestCase):
    """
    Testes de QA para garantir que a refatoração do UI Component
    não quebrou a instanciação do painel visual.
    """

    def setUp(self):
        # Mocks (Simulacros) dos objetos textuais do Flet
        self.mock_score_display = ft.Text("0")
        self.mock_name = ft.TextField(value="Atleta Teste")
        self.mock_gym = ft.TextField(value="Academia Teste")
        
        # Funções vazias para simular os callbacks
        self.mock_change_score = lambda color, amt: None
        self.mock_clear_data = lambda color: None

    def test_componente_retorna_container(self):
        """Valida se o construtor retorna a classe base correta do Flet (ft.Container)"""
        painel = build_athlete_panel(
            color_bg="#ff0000",
            score_display=self.mock_score_display,
            color_id="red",
            ref_name=self.mock_name,
            ref_gym=self.mock_gym,
            change_score_cb=self.mock_change_score,
            clear_data_cb=self.mock_clear_data
        )
        
        # Assegura que o retorno é um Container e não falhou no meio da montagem
        self.assertIsInstance(painel, ft.Container, "O componente falhou em retornar um ft.Container válido.")

    def test_timer_display_retorna_column(self):
        """Valida se o componente do relógio é instanciado sem erros e retorna uma ft.Column"""
        mock_timer_input = ft.TextField(value="05:00")
        
        relogio = build_timer_display(
            timer_input=mock_timer_input,
            start_cb=lambda e: None,
            pause_cb=lambda e: None,
            finish_cb=lambda e: None
        )
        
        # Assegura que o retorno é uma Column e não falhou no meio da montagem
        self.assertIsInstance(relogio, ft.Column, "O componente de timer falhou ao renderizar a base visual.")
    
if __name__ == '__main__':
    unittest.main()