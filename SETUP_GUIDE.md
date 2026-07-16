# Guia de Configuração do Ambiente de Desenvolvimento

Siga os passos abaixo para configurar sua máquina e começar a codificar o Placar Eletrônico.

## 1. Pré-requisitos
* **Python:** Versão 3.10 ou superior instalada na máquina.
* **Git:** Para controle de versão.
* **uv:** O gerenciador de pacotes rápido escrito em Rust.

### Instalando o `uv` (Windows - PowerShell)
Abra o PowerShell e execute o comando abaixo:
```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

## 2. Clonando e Inicializando
Abra o terminal no diretório onde deseja manter seus projetos e execute:


### Clone o repositório para a sua máquina
```bash
git clone [https://github.com/atnzpe/placar-eletronico.git](https://github.com/atnzpe/placar-eletronico.git)
```

### Entre na pasta do projeto
```bash
cd placar-eletronico
```

### Sincronize o projeto e instale todas as dependências automaticamente
```bash
uv sync
```

3. Ativando o Ambiente Virtual
Sempre que for trabalhar no código, ative o ambiente virtual para garantir que as ferramentas corretas estão sendo usadas:

### No Windows (PowerShell/CMD):

```bash
.venv\Scripts\activate
```

### No Linux/macOS:

```bash
source .venv/bin/activate
```

4. Rodando o Projeto
Com o ambiente ativado (você verá (.venv) no início da linha do terminal), execute o comando abaixo para iniciar a interface do placar:

```bash
uv run flet run main.py
```

## Dica: Para fechar a aplicação e voltar ao terminal normal, basta clicar na janela do terminal e pressionar Ctrl+C.