# Roadmap de Desenvolvimento: Placar Multi-Esportes

Este documento orienta o ciclo de vida do projeto, dividido em Fases (Macro Tarefas) e Entregáveis (Micro Tarefas/Issues). O fluxo de trabalho padrão será: `Criar Issue` -> `Criar Branch (feat/nome-da-tarefa)` -> `Desenvolver` -> `Testar` -> `Pull Request`.

## Fase 1: Fundação & Infraestrutura (Setup)
**Objetivo:** Garantir que o ambiente de desenvolvimento seja reproduzível e isolado.
* [x] **Micro 1.1:** Criar repositório no GitHub (`main`).
* [x] **Micro 1.2:** Estruturar arquivos de documentação (`README.md`, `ROADMAP.md`, `SETUP_GUIDE.md`).
* [x] **Micro 1.3:** Inicializar o projeto com `uv init` e criar `pyproject.toml`.
* [x] **Micro 1.4:** Adicionar dependências essenciais (`flet[all]`).
* [x] **Micro 1.5:** Criar estrutura de pastas (`/assets`, `/src`, `/tests`).

## Fase 2: Layout Adaptativo (Frontend Base)
**Objetivo:** Construir o esqueleto visual responsivo sem ainda ligar a lógica de tempo.
* [ ] **Micro 2.1:** Configurar a `Page` inicial (cores globais, remoção de padding, SafeArea).
* [ ] **Micro 2.2:** Criar o layout dividido (Painel Vermelho e Painel Azul) usando proporção geométrica (`expand=1`).
* [ ] **Micro 2.3:** Implementar a lógica de redimensionamento dinâmico de fontes (`page.on_resize`).
* [ ] **Micro 2.4:** Adicionar componentes visuais de pontuação, país e nome.

## Fase 3: O Motor Lógico (Backend e Assincronicidade)
**Objetivo:** Fazer os cronômetros funcionarem de forma independente e sem travar a interface.
* [ ] **Micro 3.1:** Implementar cronômetro principal (regressivo).
* [ ] **Micro 3.2:** Implementar cronômetro médico (decrescente, cumulativo de 2 min).
* [ ] **Micro 3.3:** Implementar cronômetro de imobilização (crescente de 20s).
* [ ] **Micro 3.4:** Implementar lógica de pontuação e cartões (advertências).

## Fase 4: Validação & Resiliência
**Objetivo:** Blindar o sistema contra erros de operação da mesa de arbitragem.
* [ ] **Micro 4.1:** Aplicar `InputFilters` em campos de entrada de dados (peso, tempo).
* [ ] **Micro 4.2:** Implementar tratamento de exceções (evitar erros silenciosos).
* [ ] **Micro 4.3:** Criar alertas visuais (`SnackBar`) para feedback ao operador.

## Fase 5: Testes & CI/CD
**Objetivo:** Garantir a qualidade e automatizar a distribuição.
* [ ] **Micro 5.1:** Escrever testes de integração para as regras de cronometragem.
* [ ] **Micro 5.2:** Configurar GitHub Actions para build automatizado (Web e Windows).
* [ ] **Micro 5.3:** Publicar Release v1.0.0.