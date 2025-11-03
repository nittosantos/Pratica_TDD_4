# Prática TDD 4

Desafio técnico para os alunos da disciplina "Desenvolvimento Web 3"

## 📋 Sobre o Projeto

Este projeto implementa uma **Agenda de Contatos** completa com sistema de autenticação e CRUD (Create, Read, Update, Delete) de contatos, desenvolvido em Django seguindo a metodologia TDD (Test-Driven Development).

### Funcionalidades Implementadas

#### Sprint 1 - Sistema de Autenticação
- ✅ Login com e-mail institucional (@fatec.sp.gov.br)
- ✅ Logout seguro
- ✅ Proteção de rotas com autenticação
- ✅ Interface responsiva com Bootstrap

#### Sprint 2 - CRUD de Contatos
- ✅ Cadastro de contatos
- ✅ Listagem de contatos
- ✅ Edição de contatos
- ✅ Exclusão de contatos
- ✅ Formulários com validação
- ✅ Interface em português brasileiro

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação no Windows

```console
# 1. Clone o repositório
git clone https://github.com/orlandosaraivajr/Pratica_TDD_4.git
cd Pratica_TDD_4/

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
venv\Scripts\activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Entre no diretório do projeto Django
cd agenda/

# 6. Execute as migrações do banco de dados
python manage.py migrate

# 7. Crie o superusuário (veja credenciais abaixo)
python manage.py createsuperuser

# 8. Execute os testes (opcional)
python manage.py test

# 9. Inicie o servidor
python manage.py runserver
```

### Instalação no Linux/Mac

```console
# 1. Clone o repositório
git clone https://github.com/orlandosaraivajr/Pratica_TDD_4.git
cd Pratica_TDD_4/

# 2. Crie o ambiente virtual
virtualenv -p python3 venv

# 3. Ative o ambiente virtual
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Entre no diretório do projeto Django
cd agenda/

# 6. Execute as migrações do banco de dados
python manage.py migrate

# 7. Crie o superusuário (veja credenciais abaixo)
python manage.py createsuperuser

# 8. Execute os testes (opcional)
python manage.py test

# 9. Inicie o servidor
python manage.py runserver
```

### Credenciais de Acesso

**⚠️ IMPORTANTE:** Para acessar o sistema, você precisa criar um superusuário com as seguintes credenciais:

- **Username:** `admin`
- **E-mail:** `wellyngton.santos@fatec.sp.gov.br` (ou seu e-mail institucional)
- **Password:** `fatec`

Após criar o superusuário, acesse o sistema em: `http://127.0.0.1:8000/login/`

### Comandos Úteis

```console
# Executar todos os testes
python manage.py test

# Verificar cobertura de testes
coverage run --source='.' manage.py test
coverage report
coverage html  # Gera relatório HTML em htmlcov/

# Criar migrações (se houver alterações no modelo)
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Acessar o shell do Django
python manage.py shell
```

## 📚 Documentação do Projeto

### Estrutura do Projeto

```
Pratica_TDD_4/
├── agenda/                    # Projeto Django principal
│   ├── agenda/               # Configurações do projeto
│   │   ├── settings.py       # Configurações Django
│   │   ├── urls.py           # URLs principais
│   │   └── ...
│   ├── core/                 # App principal
│   │   ├── models.py         # Modelo Agenda
│   │   ├── forms.py          # Formulários (LoginForm, AgendaForm)
│   │   ├── views.py          # Views do CRUD
│   │   ├── urls.py           # URLs do app
│   │   ├── templates/        # Templates HTML
│   │   │   ├── login.html
│   │   │   ├── logout.html
│   │   │   ├── index.html
│   │   │   ├── create_contact.html
│   │   │   ├── list_contacts.html
│   │   │   └── update_contact.html
│   │   └── tests/            # Testes automatizados
│   │       ├── test_model_agenda.py
│   │       ├── test_form_agenda.py
│   │       ├── test_form_login.py
│   │       ├── test_crud_agenda.py
│   │       └── ...
│   └── manage.py
├── requirements.txt           # Dependências do projeto
└── README.md                 # Este arquivo
```

### Modelo de Dados

O modelo `Agenda` possui os seguintes campos:

- **nome_completo** (CharField, max_length=150): Nome completo do contato (obrigatório)
- **telefone** (CharField, max_length=20): Número de telefone (obrigatório)
- **email** (EmailField): Endereço de e-mail (obrigatório, validado)
- **observacao** (TextField, blank=True): Observações sobre o contato (opcional)

### Funcionalidades Detalhadas

#### 1. Sistema de Login/Logout

- **Login:** Apenas usuários com e-mail institucional `@fatec.sp.gov.br` podem fazer login
- **Validação:** O sistema valida o formato do e-mail e verifica se o usuário existe
- **Proteção:** Todas as rotas protegidas redirecionam para login se o usuário não estiver autenticado

#### 2. CRUD de Contatos

- **Create (Criar):** Formulário para cadastrar novo contato com validação de campos obrigatórios
- **Read (Listar):** Tabela com todos os contatos, exibindo nome, telefone, e-mail e observação
- **Update (Editar):** Formulário pré-preenchido para editar contato existente
- **Delete (Excluir):** Confirmação antes de excluir contato

#### 3. Validações Implementadas

- Campos obrigatórios: `nome_completo`, `telefone`, `email`
- Formato de e-mail válido (validação automática do Django)
- Tamanho máximo de campos respeitado
- Mensagens de erro em português brasileiro

### Rotas do Sistema

| Rota | Descrição | Autenticação |
|------|-----------|--------------|
| `/` ou `/index/` | Página inicial | ✅ Requerida |
| `/login/` | Tela de login | ❌ Não requerida |
| `/logout/` | Logout | ✅ Requerida |
| `/contacts/` | Lista de contatos | ✅ Requerida |
| `/contacts/create/` | Criar contato | ✅ Requerida |
| `/contacts/<id>/update/` | Editar contato | ✅ Requerida |
| `/contacts/<id>/delete/` | Excluir contato | ✅ Requerida |

### Tecnologias Utilizadas

- **Django 5.2.1:** Framework web Python
- **Bootstrap 5.3.3:** Framework CSS para interface
- **Font Awesome 6.5.0:** Ícones
- **Coverage 7.8.0:** Análise de cobertura de testes
- **SQLite:** Banco de dados (desenvolvimento)

## 🧪 Testes e Cobertura

### Cobertura de Testes Atual: **98%** ✅

```
Name                                        Stmts   Miss  Cover
---------------------------------------------------------------
core\forms.py                                  37      0   100%
core\models.py                                  8      0   100%
core\views.py                                  55      1    98%
core\tests\test_crud_agenda.py                122      0   100%
core\tests\test_form_agenda.py                 51      0   100%
core\tests\test_form_login.py                  36      0   100%
---------------------------------------------------------------
TOTAL                                         476     11    98%
```

### Testes Implementados

- ✅ **Testes de Modelo:** Validação do modelo Agenda
- ✅ **Testes de Formulário:** Validação de campos e dados
- ✅ **Testes de CRUD:** Todas as operações (Create, Read, Update, Delete)
- ✅ **Testes de Autenticação:** Login, logout e proteção de rotas
- ✅ **Testes de Interface:** Templates e renderização

**Total de Testes:** 47 testes, todos passando ✅

### Executar Testes

```console
# Executar todos os testes
python manage.py test

# Executar testes específicos
python manage.py test core.tests.test_crud_agenda
python manage.py test core.tests.test_form_agenda

# Com cobertura
coverage run --source='.' manage.py test
coverage report
coverage html  # Abre htmlcov/index.html no navegador
```

## 📸 Imagens do Projeto

### Sprint 1 - Autenticação

<img src="caso_uso.png">

A expectativa do projeto é que tenha-se uma agenda. O que foi priorizado na primeira sprint foi o sistema de login/logout.
O login somente pode ocorrer com o e-mail institucional @fatec.sp.gov.br

<img src="login.png">
Imagem 1: Tela de Login

<img src="index.png">
Imagem 2: Tela index

<img src="logout.png">
Imagem 3: Tela logout

### Sprint 2 - CRUD

<img src="model.png">

## ✅ Requisitos Implementados

### Sprint 1 ✅
- ✅ Sistema de login/logout
- ✅ Validação de e-mail institucional
- ✅ Proteção de rotas
- ✅ Interface responsiva

### Sprint 2 ✅
- ✅ Formulário para o modelo Agenda (ModelForm)
- ✅ Cadastrar contato
- ✅ Listar contatos
- ✅ Atualizar contato
- ✅ Remover contato
- ✅ Proteção de todas as funcionalidades com autenticação
- ✅ Cobertura de testes mantida acima de 90% (98% atual)

## 📝 Ajustes nos Testes

O código fonte passou por atualizações para acomodar os novos requisitos. Os testes foram ajustados e novos testes criados:

- ✅ Testes existentes ajustados e mantidos
- ✅ Novos testes para CRUD completo
- ✅ Testes de formulário de contatos
- ✅ Cobertura mantida acima de 90% (objetivo alcançado: **98%**)

<img src="cobertura_testes.png">

## 👤 Desenvolvido por

Projeto desenvolvido como prática acadêmica da disciplina "Desenvolvimento Web 3" - FATEC.

## 📄 Licença

Este projeto é parte de uma atividade acadêmica.
