# Mantuí 🐦

> O Mantuí é um sistema web offline-first criado para apoiar o monitoramento e a conservação de aves limícolas migratórias no litoral do Rio Grande do Norte. A plataforma permite registrar avistamentos com geolocalização, organizar dados de campo, gerar relatórios e auxiliar no gerenciamento de equipes, mesmo em áreas com acesso limitado ou inexistente à internet.

> O projeto foi pensado para atender às necessidades de pesquisadores envolvidos em ações de conservação, especialmente diante dos desafios do monitoramento em regiões remotas e da importância ecológica dessas aves para a biodiversidade. Sua proposta está conectada ao contexto do Flyways Brasil, iniciativa da SAVE Brasil voltada à conservação de aves limícolas e seus habitats na Bacia Potiguar.

---

## 📌 Sobre o Projeto
Contexto do Frontend:
- **Linguagens de marcação e estilo Utilizadas:** HTML5, CSS
- **Framework Utilizado:** TailwindCSS
- **Versão:** 4.3.3
- **Bibliotecas:** anime.js
  
Contexto do Backend:
- **Linguagens de programação Utilizadas:** Python, JavaScript
- **Framework Utilizado:** Flask
- **Versão:** 3.1.x
- **Bibliotecas:** Flask-Migrate, Flask-Script, Flask-SQLAlchemy, Jinja2, PyMySQL, python-dotenv, utils

Contexto do banco de dados:
- **Biblioteca Utilizada:** SQLAlchemy
- **Versão:** 2.0.52
- **Modelagem:** Relacional (DER)

---

## 🚀 Como Executar o Projeto

Após clonar o repositório, instale as dependências do projeto:

**Backend (Python) - Terminal 1:**
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No Windows (Git Bash):
source venv/Scripts/activate
# No Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# No Linux/Mac:
source venv/bin/activate

# Instalar pacotes Python (Flask, SQLAlchemy, python-dotenv, etc.)
pip install -r requirements.txt

# Certifique-se de estar com a venv ativada (source venv/Scripts/activate)
python app.py
```

> Importante: Crie um arquivo .env na raiz do projeto com as credenciais do seu banco MySQL (veja o .env.example).
> ```bash
>FLASK_APP=app:app
>SECRET_KEY=sua-palavra-secreta
>DB_USERNAME=usuario_do_banco
>DB_PASSWORD=senha_do_banco
>DB_HOST=host_do_banco
>DB_DATABASE=nome_do_banco
>DB_PORT=porta_do_banco
> ```


**Frontend (Tailwind CLI) - Terminal 2:**
```bash
# Instalar dependências do Node.js (Tailwind CSS CLI registrado no package.json)
npm install

# Cria a pasta static/dist/output.css na primeira execução e monitora as alterações dos arquivos HTML em tempo real
npm run dev
```
> Importante: Para visualizar as classes enquanto programa instale a biblioteca de tailwind css do VScode

---

## 🗂️ Estrutura do Repositório
```text
├── 📂 controllers/       # organiza o fluxo de dados e resposta pro Usuário
│   ├── Avistamento.py
│   ├── ebird.py 
│   ├── Equipe.py 
│   ├── Especie.py 
│   ├── Projeto.py      
│   ├── StatusConservacao.py      
│   └── Usuario.py 
|      
├── 📂 migrations/        # Rastrear Histórico de alteração do Banco de Dados
|
├── 📂 static/            # Armazenar arquivos que não mudam
│   └── 📂 img/           # Armazenar imagens
│        ├── Diagrama-Entidade-Relacionamento.png
│        └── Diagrama-de-Classes.png 
│        └── 📂 assets
│        └── 📂 css
│        └── 📂 dist
│        └── 📂 img
│        └── 📂 src
│        └── 📂 uploads
│        └── 📂 vid
│   
├── 📂 templates/         # Guarda os arquivos HTML
|    │        
|    └── 📂 auth
│    |    ├── esqueci_senha_nova.html
│    |    └── esqueci_senha_validar.html 
|    └── 📂 avistamento
│    |    ├── avistamento_add.html
│    |    ├── avistamento_recovery.html 
│    |    └── avistamento_update.html
|    └── 📂 equipe
│    |    ├── equipe_add.html
│    |    ├── equipe_recovery.html 
│    |    └── equipe_update.html
|    └── 📂 especie
│    |    ├── 📂 partials
│    |    |   └── especie_card.html
│    |    ├── especie_add.html
│    |    ├── especie_recovery.html 
│    |    └── especie_update.html
|    └── 📂 legal
│    |    ├── privacidade.html 
│    |    └── termos.html
|    └── 📂 moderacao
│    |    ├── fila_avistamentos.html 
│    |    └── fila_projetos.html
|    └── 📂 partials_private
│    |    ├── footer_lock.html 
│    |    └── heador_lock.html
|    └── 📂 partials_public
│    |    ├── footer_public.html 
│    |    └── heador_public.html
|    └── 📂 projeto
│    |    ├── projeto_add.html
│    |    ├── projeto_recovery.html 
│    |    └── projeto_update.html
|    └── 📂 relatorio
│    |    └── avistamentos.html
|    └── 📂 status_conservacao
│    |    ├── status_conservacao_add.html
│    |    ├── status_conservacao_recovery.html 
│    |    └── status_conservacao_update.html
|    └── 📂 usuario
│    |    ├── cadastro.html
│    |    ├── configuracoes.html 
│    |    ├── login.html 
│    |    ├── perfil.html 
│    |    ├── tornar_moderador.html 
│    |    └── usuario_update.html
│    ├── base_private.html      
│    ├── base_public.html 
│    ├── busca_resultados.html 
│    ├── erro404.html 
│    ├── flashes_messages.html 
│    ├── home.html 
│    ├── index.html 
│    └── notificacoes.html 
|     
├── .gitignore              # Indicar ao Git quais arquivos e pastas não devem ser rastreados
├── app.py
├── models.py
├── package-lock.json
├── package.json
├── popular_especies.py
├── README.md               # apresentar e explicar o projeto
├── requirements.txt        # Listar todas os pacotes externos que o projeto precisa para funcionar
└── utils.py                # armazenar funções de ajuda reutilizáveis e genéricas
```

---

## 📊 Modelo Entidade-Relacionamento (DER)
<p align="center">
  <img src="./static/img/Diagrama Entidade Relacionamento.png" alt="DiagraMA Entidade Relacionamento" width="100%">
</p>

---

## Diagrama de Classe
<p align="center">
  <img src="./static/img/Diagrama de Classes.png" alt="DiagraMA Entidade Relacionamento" width="100%">
</p>

---

## 📝 Sobre as Classes do sistema
Principais classes:

| Classe | Descrição |
| :--- | :--- |
| `Usuario` | Armazena informações de cadastro. |
| `CidadaoCientista(Usuario)` | Realiza os Avistamentos das Aves. |
| `Moderador(CidadaoCientista)` | Valida os avistamentos. |
| `SolicitacaoModerador` | CidadaoCientista solicita a permição para moderar. |
| `MembroEquipe` | Representa a participação de um usuário em uma equipe. |
| `Grupo` | Grupo de Usuários (ou um usuário individual) para realizar e armazenar os avistamentos. |
| `Projeto` | Junção de equipes e usários. |
| `Avistamento` | Coleta as informações observadas de determinada(s) Ave(s). |
| `Ave` | Determinado Animal observado isoladamente. |
| `Especie` | Grupo no qual as aves pertencem. |
| `Familia` | Grupo no qual as espécies pertencem. |
| `StatusConservacao` | Estatísticas sobre a conservação das espécies de aves, com base nos avistamentos. |
| `Midia` | Estrutura os arquivos presentes nos avistamentos (os registros) e complementa o StatusConservacao. |
| `GeradorGrafico` | Cria rGráficos com base nos dados dos avistamentos. |
| `MapaInterativo` | Representação visual dos dados coletados e construidos sobre as espécies. |

---
