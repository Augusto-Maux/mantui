# Mantuí 🐦 / Banco de Dados 💾

> Este repositório foi criado para o desenvolvimento do banco de dados e da camada do sistema Mantuí baseada nos conceitos de modelagem UML. A partir dos diagramas de entidade-relacionamento (DER) e de classes, foram implementadas as entidades, funções e rotas que estruturam esta etapa do projeto.

## 📌 Sobre o Projeto
Contexto do banco de dados:
- **Biblioteca Utilizada:** SQLAlchemy
- **Versão:** 2.0.52
- **Modelagem:** Relacional (DER)

---

## 🗂️ Estrutura do Repositório
```text
├── 📂 controllers/       # organiza o fluxo de dados e resposta pro Usuário
|   ├── Ave.py
│   ├── Avistamento.py
│   ├── Equipe.py 
│   ├── Especie.py 
│   ├── Projeto.py      
│   └── Usuario.py 
|      
├── 📂 migrations/        # Rastrear Histórico de alteração do Banco de Dados
|
├── 📂 static/            # Armazenar arquivos que não mudam
│   └── 📂 img/           # Armazenar imagens
│        ├── Diagrama-Entidade-Relacionamento.png
│        └── Diagrama-de-Classes.png 
│   
├── 📂 templates/         # Guarda os arquivos HTML
│   ├── ave_add.html
│   ├── ave_recovery.html 
│   ├── ave_update.html
|   | 
│   ├── avistamento_add.html
│   ├── avistamento_recovery.html 
│   ├── avistamento_update.html
|   | 
│   ├── equipe_add.html      
│   ├── equipe_recovery.html 
│   ├── equipe_update.html 
|   | 
│   ├── especie_add.html      
│   ├── especie_recovery.html
│   ├── especie_update.html
|   | 
│   ├── index.html 
|   | 
│   ├── projeto_add.html      
│   ├── projeto_recovery.html
│   ├── projeto_update.html
|   | 
│   ├── usuario_add.html      
│   ├── usuario_recovery.html
│   └── usuario_update.html
├── .gitignore              # Indicar ao Git quais arquivos e pastas não devem ser rastreados
├── README.md               # apresentar e explicar o projeto
├── requirements.txt        # Listar todas os pacotes externos que o projeto precisa para funcionar
└── utils.py                # armazenar funções de ajuda reutilizáveis e genéricas
```

---

## 📊 Modelo Entidade-Relacionamento (DER)
<p align="center">
  <img src="./static/img/Diagrama-Entidade-Relacionamento.png" alt="DiagraMA Entidade Relacionamento" width="100%">
</p>

---

## 📝 Sobre as Classes do sistema
Breve resumo das principais classes:

| Classe | Descrição |
| :--- | :--- |
| `Usuario` | Armazena informações de cadastro. |
| `CidadaoCientista(Usuario)` | Realiza os Avistamentos das Aves. |
| `Moderador(CidadaoCientista)` | Valida os avistamentos. |
| `SolicitacaoModerador` | CidadaoCientista solicita a permição para moderar. |
| `MembroEquipe` | Representa a participação de um usuário em uma equipe. |
| `Equipe` | Grupo de Usuários (ou um usuário individual) para realizar e armazenar os avistamentos. |
| `Projeto` | Junção de equipes e usários. |
| `Avistamento` | Coleta as informações observadas de determinada(s) Ave(s). |
| `Ave` | Determinado Animal observado isoladamente. |
| `Especie` | Grupo no qual as aves pertencem. |
| `Familia` | Grupo no qual as espécies pertencem. |
| `StatusConservacao` | Estatísticas sobre a conservação das espécies de aves, com base nos avistamentos. |
| `Midia` | Estrutura os arquivos presentes nos avistamentos (os registros) e complementa o StatusConservacao. |
| `GeradorRelatorio` | Cria relatórios com base nos dados dos avistamentos. |
| `GeradorGrafico` | Cria rGráficos com base nos dados dos avistamentos. |
| `MapaInterativo` | Representação visual dos dados coletados e construidos sobre as espécies. |

---