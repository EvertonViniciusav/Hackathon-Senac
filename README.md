# 🚛 Movix - Sistema de Gestão de Frotas e Documentos

O **Movix** é um sistema desenvolvido em **Python (Flask)** que tem como objetivo **automatizar o controle de vencimentos de documentos de veículos, aeronaves e embarcações**, enviando notificações automáticas por **e-mail** para cada responsável.

O sistema foi desenvolvido para o **Hackathon Senac**, com foco em **eficiência, escalabilidade e automação de processos logísticos**.

---

## 🧩 Funcionalidades

- 🔐 **Login de Usuários**
  - Cada usuário acessa apenas sua própria frota.
  - Usuário **Master** pode gerenciar todos os usuários (criar, editar e excluir).

- 🚘 **Gestão de Frotas**
  - Cadastro de veículos, caminhões, motos, aviões, trens e embarcações.
  - Cada frota vinculada a um usuário.

- 📄 **Gestão de Documentos**
  - Registro de documentos por frota (ex: licenciamento, seguro, inspeção).
  - Alteração de data de vencimento e exclusão de documentos.

- 📬 **Notificações Automáticas**
  - Envio de **e-mails automáticos** informando documentos que vencem nos próximos **X dias** (configurável).
  - Envio de relatórios detalhados em formato HTML diretamente ao e-mail do usuário.

- 👨‍💼 **Painel Master**
  - Visualização de todos os usuários cadastrados.
  - Criação, edição e exclusão de contas.
  - Acesso completo a todas as frotas e documentos do sistema.

---

## 🧱 Estrutura do Projeto

```
/HACKATHON SENAC/
│
├── app.py                 # Arquivo principal Flask
├── notificacoes.py        # Envio automático de e-mails de vencimentos
├── templates/             # Páginas HTML (login, dashboard, frotas, usuários etc)
├── static/                # CSS, JS e imagens
├── .env                   # Credenciais
├── .gitignore             # Arquivos ignorados pelo Git
├── requirements.txt       # Dependências do projeto
└── README.md              # Este arquivo
```

---

## ⚙️ Tecnologias Utilizadas

- **Python 3.11+**
- **Flask** – Framework web
- **MySQL** – Banco de dados
- **HTML, CSS, JavaScript**
- **Bootstrap 5** – Interface responsiva
- **smtplib / email.mime** – Envio de e-mails automáticos
- **python-dotenv** – Leitura das variáveis de ambiente

---

## 🚀 Instalação e Execução

### 1️⃣ Clonar o projeto
```bash
git clone https://github.com/EvertonViniciusav/Hackathon-Senac.git
cd Hackathon-Senac
```

### 2️⃣ (Opcional) Criar e ativar o ambiente virtual
Recomendado, mas opcional em testes:
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Instalar dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Criar o banco de dados MySQL
Execute o script SQL disponível em `scripts/criar_banco.sql` manualmente no MySQL Workbench.

### 5️⃣ Configurar variáveis de ambiente (.env)

Crie um arquivo **.env** na raiz do projeto com o seguinte conteúdo:

```
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=hackathon
EMAIL_USER=seuemail@gmail.com
EMAIL_PASS=senha_de_aplicativo_gmail
```

> ⚠️ Para o Gmail, use **senha de aplicativo**, não sua senha pessoal.  
> Crie em: https://myaccount.google.com/apppasswords

### 6️⃣ Executar o servidor Flask
```bash
python app.py
```

O sistema estará disponível em:
```
http://127.0.0.1:5000/
```

---

## ⏰ Agendamento das Notificações

O arquivo `notificacoes.py` pode ser executado automaticamente para enviar os e-mails de vencimento.

### Opção 1 — Executar manualmente:
```bash
python notificacoes.py
```

### Opção 2 — Agendar automaticamente:
No **Windows**, use o **Agendador de Tarefas** para executar o script uma vez por dia.  
No **Linux**, adicione ao **crontab**:
```bash
0 8 * * * /usr/bin/python3 /caminho/do/projeto/notificacoes.py
```

---

## 🔄 Fluxo do Sistema

1. Usuário acessa o sistema e faz login.  
2. No primeiro acesso, o **usuário master** pode criar novos usuários.  
3. Cada usuário cadastra sua própria frota e documentos.  
4. O sistema verifica os vencimentos e envia **notificações automáticas** (e-mail; WhatsApp opcional).  
5. O usuário pode alterar, excluir e gerenciar seus próprios dados.  
6. O master tem acesso total a todos os registros.

---

## 🧭 Cronograma de Funcionamento

| Etapa | Descrição | Status |
|-------|------------|--------|
| Backend Flask | Estrutura e rotas principais | ✅ Concluído |
| Banco de Dados | Criação e relações | ✅ Concluído |
| Login / Sessão | Controle de usuários | ✅ Concluído |
| Painel de Frotas | Cadastro e visualização | ✅ Concluído |
| Documentos | Cadastro e alteração de vencimentos | ✅ Concluído |
| Notificações por E-mail | Relatórios automáticos | ✅ Concluído |
| Dashboard Master | Gestão de usuários | ✅ Concluído |

---

## 👤 Usuário Master (acesso inicial)
Após criar o banco, o usuário master no banco:
- **E-mail:** master@admin.com  
- **Senha:** master

---

## 🧾 Arquivo .gitignore sugerido

Inclua na raiz:
```
__pycache__/
venv/
.env
*.db
.DS_Store
.vscode/
node_modules/
```