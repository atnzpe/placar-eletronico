# **Documento de Requisitos do Produto (PRD)**

**Projeto:** Placar Eletrônico Multi-Esportes (Sambo FIAS)

**Gerente de Projeto:** Aline Cecilia

**Data:** Julho de 2026

## **1\. Visão do Produto**

Desenvolver um software de placar eletrônico de código aberto, de alta precisão e responsividade geométrica, capaz de atender campeonatos de diversas modalidades de artes marciais. O sistema inicial servirá como prova de conceito para o **Padrão Oficial da FIAS (Federação Internacional de Sambo) / CBSA**. O foco é garantir estabilidade extrema, permitindo que mesários e árbitros tenham controle absoluto sobre o tempo e pontuações durante eventos ao vivo.

## **2\. Público-Alvo**

* **Primário:** Mesários e operadores técnicos de campeonatos.  
* **Secundário:** Árbitros centrais (visualização passiva no tatame via tablets/smartwatches).  
* **Terciário:** Público do evento (visualização passiva em telões/TVs) e Federações/Organizadores.

## **3\. Modelo de Distribuição e Negócios**

* **Open Source & Comunitário:** O código será aberto e a distribuição do executável/versão web será 100% gratuita para fortalecer o esporte.  
* **Monetização Indireta:** Inserção de anúncios (Google AdSense) exclusivamente no site institucional de download do sistema, mantendo o software em si completamente limpo e livre de interrupções.  
* **Consultoria B2B (Futuro):** Oferecer versões customizadas (White-label) com módulos para inserção de patrocinadores privados das federações.

## **4\. Requisitos Funcionais (O que o sistema deve fazer)**

1. **Múltiplos Cronômetros Assíncronos:**  
   * Tempo Principal (regressivo).  
   * Tempo Médico (cumulativo até 2 minutos).  
   * Tempo de Imobilização (crescente até 20 segundos).  
   * Tempo de Finalização (1 minuto).  
2. **Gestão de Luta:** Controle ágil de pontuação, penalidades (cartões visuais) e identificação de atletas (nome, país/estado).  
3. **Roteamento de Interface Dupla:**  
   * *Tela de Controle (Mesa):* Interface interativa com botões e validação rigorosa de formulários.  
   * *Tela de Exibição (Telão):* Interface limpa, otimizada apenas para visualização do público.

## **5\. Requisitos Não Funcionais (Como o sistema deve se comportar)**

1. **Responsividade Extrema:** A interface abandonará tamanhos fixos em pixels, adotando geometria relativa (flexbox/expand) e redimensionamento dinâmico de fontes matemáticas para escalar perfeitamente de visores de 1.5" até telões de 100".  
2. **Resiliência a Erros:** Bloqueio de inputs incorretos na raiz (ex: letras em campos de peso) e uso de alertas amigáveis (SnackBar) sem fechamento abrupto do app.  
3. **Multiplataforma:** A mesma base de código gerará builds para Web, Windows (Desktop) e Android.

## **6\. Pilha Tecnológica**

* **Linguagem:** Python 3.10+  
* **Framework Frontend:** Flet (baseado em Flutter)  
* **Gerenciamento de Ambiente:** uv  
* **CI/CD:** GitHub Actions (Geração automatizada de versões e deploy)