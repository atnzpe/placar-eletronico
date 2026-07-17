# Roadmap de Desenvolvimento: Placar Multi-Esportes

Este documento orienta o ciclo de vida do projeto, dividido em **Fases** (Macro Tarefas), **Entregáveis/Issues** (Micro Tarefas) e **Passos de Execução** (Subtarefas / Micros da Micro). 

O fluxo de trabalho padrão exigido no projeto é: `Criar Issue` -> `Criar Branch (feat/nome-da-tarefa)` -> `Desenvolver` -> `Testar` -> `Pull Request` -> `Merge`.

---

## 🏗️ Fase 1: Fundação & Infraestrutura (Setup) [CONCLUÍDO]
**Objetivo:** Garantir que o ambiente de desenvolvimento seja reproduzível, versionado e isolado.

* [x] **Micro 1.1:** Criar repositório no GitHub (`main`).
* [x] **Micro 1.2:** Estruturar arquivos de documentação base.
  * [x] *Micro da Micro:* Escrever `README.md` com visão geral.
  * [x] *Micro da Micro:* Escrever `ROADMAP.md` e regras de negócio (`PRD.md`).
  * [x] *Micro da Micro:* Escrever `SETUP_GUIDE.md` à prova de falhas para onboarding de devs.
* [x] **Micro 1.3:** Inicializar o motor do projeto.
  * [x] *Micro da Micro:* Rodar `uv init` e criar `pyproject.toml`.
* [x] **Micro 1.4:** Instalar e registrar dependências.
  * [x] *Micro da Micro:* Adicionar `flet[all]` e `fpdf` via terminal.
* [x] **Micro 1.5:** Criar arquitetura de pastas inicial.
  * [x] *Micro da Micro:* Estruturar `/assets`, `/src` e `/tests`.

---

## 🎨 Fase 2: Arquitetura MVVM e Layout Adaptativo
**Objetivo:** Estruturar o código em componentes modernos e construir o esqueleto visual responsivo sem travar a interface.

* [x] **Micro 2.1:** Refatoração para Padrão MVVM (Isolar Serviços).
  * [x] *Micro da Micro:* Criar subpastas `/models`, `/views`, `/components`, `/services`.
  * [x] *Micro da Micro:* Migrar geração de PDF para `pdf_service.py`.
  * [x] *Micro da Micro:* Migrar gravação de planilhas para `csv_service.py`.
  * [x] *Micro da Micro:* Escrever testes automatizados (QA) para geração de relatórios.
* [ ] **Micro 2.2:** Componentização da Interface de Usuário (Isolar UI).
  * [ ] *Micro da Micro:* Extrair visual do atleta para `src/components/athlete_panel.py`.
  * [ ] *Micro da Micro:* Isolar o relógio central em `src/components/timer_display.py`.
* [ ] **Micro 2.3:** Configuração Base e Roteamento (`page`).
  * [ ] *Micro da Micro:* Configurar `page.padding = 0` e injetar paleta global CBSA.
  * [ ] *Micro da Micro:* Ativar `SafeArea` para evitar cortes em smartphones (Android/iOS).
  * [ ] *Micro da Micro:* Criar sistema de rotas separando Visão da Mesa de Controle e Visão do Telão Público.
* [ ] **Micro 2.4:** Redimensionamento Dinâmico (Responsividade Extrema).
  * [ ] *Micro da Micro:* Mapear o gatilho de evento `page.on_resize`.
  * [ ] *Micro da Micro:* Criar fórmula matemática para calcular fontes baseada em `largura x altura`.

---

## ⚙️ Fase 3: O Motor Lógico (Backend de Tempo e Arbitragem)
**Objetivo:** Implementar o fluxo de regras de artes marciais (Padrão Sambo/FIAS) utilizando assincronicidade (Threads).

* [ ] **Micro 3.1:** Implementar Cronômetro Principal (Regressivo).
  * [ ] *Micro da Micro:* Adicionar botões play, pause e reset com injeção de estado.
  * [ ] *Micro da Micro:* Disparar alerta visual (e/ou sonoro) ao atingir 00:00.
* [ ] **Micro 3.2:** Implementar Cronômetro Médico.
  * [ ] *Micro da Micro:* Criar timer decrescente isolado do relógio principal.
  * [ ] *Micro da Micro:* Adicionar trava de limite (cumulativo máximo de 2 minutos).
* [ ] **Micro 3.3:** Implementar Cronômetro de Imobilização (Osaekomi).
  * [ ] *Micro da Micro:* Criar relógio progressivo que gera pontuação automática aos 10s e 20s.
* [ ] **Micro 3.4:** Gestão de Penalidades (Advertências).
  * [ ] *Micro da Micro:* Criar slots visuais para cartões amarelos e vermelhos.
  * [ ] *Micro da Micro:* Criar regra de penalização: advertência concede pontos automáticos ao adversário.

---

## 🛡️ Fase 4: Validação (QA) & Resiliência
**Objetivo:** Blindar a mesa operadora contra erros humanos na hora do campeonato.

* [ ] **Micro 4.1:** Blindagem de Formulários (InputFilters).
  * [ ] *Micro da Micro:* Bloquear letras em campos numéricos (peso, tempo).
  * [ ] *Micro da Micro:* Limitar caracteres no nome de atletas e academias.
* [ ] **Micro 4.2:** Tratamento Profundo de Exceções.
  * [ ] *Micro da Micro:* Mapear erros de leitura e garantir que o app não feche (crash) no Android.
  * [ ] *Micro da Micro:* Expandir o módulo `logging` para capturar falhas críticas.
* [ ] **Micro 4.3:** Feedback Visual Contínuo.
  * [ ] *Micro da Micro:* Parametrizar banners (`SnackBar`) com cores semânticas (verde = sucesso, vermelho = erro).

---

## 🚀 Fase 5: Compilação & CI/CD (Distribuição)
**Objetivo:** Automatizar a geração do software e publicar as versões para o usuário final.

* [ ] **Micro 5.1:** Bateria de Testes Finais de Domínio.
  * [ ] *Micro da Micro:* Rodar script global para testar matemática de pontos cruzados e exportação combinada.
* [ ] **Micro 5.2:** Configuração de Pipelines (GitHub Actions).
  * [ ] *Micro da Micro:* Criar arquivo `.github/workflows/build-windows.yml` para compilar `.exe`.
  * [ ] *Micro da Micro:* Criar pipeline para deploy Web em plataforma gratuita.
  * [ ] *Micro da Micro:* Gerar assinatura e compilação do APK/AAB para Android.
* [ ] **Micro 5.3:** Lançamento Oficial (Release).
  * [ ] *Micro da Micro:* Gerar Tag semântica `v1.0.0`.
  * [ ] *Micro da Micro:* Publicar release notes na aba oficial do GitHub.