# SKPONTO - Sistema de Controle de Ponto

## ✅ STATUS: SISTEMA COMPLETO E OPERACIONAL

Um sistema completo de controle de ponto desenvolvido em Flask, com funcionalidades avançadas para gestão de funcionários, registros de ponto, atestados médicos e relatórios.

**🎉 TODAS AS FUNCIONALIDADES IMPLEMENTADAS E TESTADAS**

## ⚡ Quick Start

**O sistema está pronto para uso! Para testar rapidamente:**

1. **Ativar ambiente virtual**: `.venv\Scripts\activate` (Windows) 
2. **Iniciar servidor**: `flask run`
3. **Acessar**: http://localhost:5000
4. **Login Admin**: 
   - Email: `admin@skponto.com` ou `ADMIN@SKBORGES.COM.BR`
   - Senha: A definida durante a criação do admin

**Ver arquivo [STATUS_FINAL.md](STATUS_FINAL.md) para guia completo de deploy.**

## 🚀 Funcionalidades Principais

### 🔐 Autenticação e Segurança
- Login seguro com email e senha
- Cadastro de usuários com diferentes tipos (Admin, Trabalhador, Estagiário)
- Recuperação de senha por email + CPF
- Rate limiting para prevenir ataques
- Logs de segurança completos

### ⏰ Controle de Ponto
- Registro de entrada e saída com um clique
- Cálculo automático de horas trabalhadas e extras
- Registro manual para correções
- Visualização do histórico completo
- Edição de registros com justificativa

### 👥 Gestão de Usuários
- Perfil pessoal editável
- Gestão completa de funcionários (admin)
- Upload de foto de perfil
- Controle de permissões por tipo de usuário

### 📋 Atestados Médicos (NOVA FUNCIONALIDADE)
- Upload de atestados em PDF/Imagem
- Aprovação/rejeição pelos administradores
- Histórico completo de atestados
- Notificações automáticas

### 📊 Relatórios e Dashboards
- Dashboard interativo para usuários
- Dashboard administrativo completo
- Relatórios em PDF e Excel
- Gráficos e estatísticas
- Exportação de dados

### 🔔 Sistema de Notificações
- Notificações em tempo real
- Envio para grupos específicos
- Marcação como lida/não lida
- Diferentes tipos e prioridades

### 💾 Backup e Segurança
- Backup automático do banco de dados
- Integração com Dropbox
- Logs de auditoria
- Monitoramento de atividades

## 🛠️ Tecnologias Utilizadas

- **Backend**: Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Frontend**: Bootstrap 5, jQuery, Font Awesome
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Relatórios**: ReportLab (PDF), XlsxWriter (Excel)
- **Upload**: Pillow (processamento de imagens)
- **Segurança**: bcrypt, CSRF protection, Rate limiting

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd SKPONTO_
```

### 2. Crie um ambiente virtual
```bash
python -m venv venv

# No Windows
venv\Scripts\activate

# No Linux/Mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env com suas configurações
```

### 5. Inicialize o banco de dados
```bash
flask init-db
```

### 6. Crie o primeiro administrador
```bash
flask create-admin
```

### 7. Execute a aplicação
```bash
# Desenvolvimento
python app.py

# Ou usando flask
flask run
```

A aplicação estará disponível em `http://localhost:5000`

## 🚀 Deploy no Render.com

### 1. Prepare o repositório
- Certifique-se de que todos os arquivos estão commitados
- O arquivo `requirements.txt` deve estar atualizado
- Configure as variáveis de ambiente no Render

### 2. Configurações no Render
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`
- **Environment**: Python 3

### 3. Variáveis de Ambiente no Render
```
FLASK_ENV=production
FLASK_CONFIG=production
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=postgresql://... (fornecido pelo Render)
```

### 4. Banco de Dados
- Adicione um PostgreSQL database no Render
- A URL será automaticamente definida em `DATABASE_URL`

## 📱 Como Usar

### Para Funcionários
1. **Login**: Use seu email e senha para acessar
2. **Registrar Ponto**: Clique em "Registrar Ponto" para entrada/saída
3. **Visualizar Registros**: Acesse "Meus Registros" para ver histórico
4. **Enviar Atestados**: Use "Atestados" para enviar documentos médicos
5. **Perfil**: Atualize suas informações pessoais

### Para Administradores
1. **Dashboard Admin**: Visão geral do sistema
2. **Gestão de Usuários**: Criar, editar e gerenciar funcionários
3. **Aprovar Atestados**: Revisar e aprovar/rejeitar atestados
4. **Relatórios**: Gerar relatórios em PDF/Excel
5. **Notificações**: Enviar comunicados para funcionários
6. **Logs**: Monitorar atividades do sistema

## 🔧 Comandos CLI Úteis

```bash
# Criar administrador
flask create-admin

# Fazer backup
flask backup

# Limpar logs antigos
flask cleanup-logs --days 30

# Ver estatísticas
flask stats

# Listar usuários
flask list-users

# Promover usuário a admin
flask promote-admin --email usuario@exemplo.com
```

## 📋 Estrutura do Projeto

```
SKPONTO_/
├── app/
│   ├── auth/           # Autenticação
│   ├── main/           # Rotas principais
│   ├── admin/          # Administração
│   ├── api/            # API REST
│   ├── errors/         # Tratamento de erros
│   ├── static/         # CSS, JS, imagens
│   ├── templates/      # Templates HTML
│   ├── models.py       # Modelos de dados
│   ├── forms.py        # Formulários WTF
│   ├── utils.py        # Utilitários
│   └── cli.py          # Comandos CLI
├── migrations/         # Migrações do banco
├── config.py          # Configurações
├── app.py             # Aplicação principal
├── requirements.txt   # Dependências
└── README.md          # Este arquivo
```

## 🔒 Segurança

- Senhas hasheadas com bcrypt
- Proteção CSRF em todos os formulários
- Rate limiting para prevenir ataques
- Validação de uploads de arquivo
- Logs de auditoria completos
- Sessões seguras com cookies HTTPOnly

## 📊 Relatórios Disponíveis

- **Relatório de Ponto**: Registros por período e funcionário
- **Relatório de Horas Extras**: Análise de horas extras
- **Relatório de Atestados**: Licenças médicas
- **Relatório de Atividades**: Logs do sistema
- **Exportação Excel**: Dados para análise externa

## 🎯 Tipos de Usuário

### Estagiário
- Registro de ponto
- Visualização de registros pessoais
- Upload de atestados
- Perfil pessoal

### Trabalhador
- Todas as funcionalidades do estagiário
- Edição limitada de registros

### Administrador
- Todas as funcionalidades anteriores
- Gestão completa de usuários
- Aprovação de atestados
- Acesso a relatórios
- Configurações do sistema
- Logs de segurança

## 🆘 Suporte

Para suporte técnico:
1. Verifique os logs do sistema
2. Consulte a documentação
3. Entre em contato com o administrador

## 📄 Licença

Este projeto é proprietário. Todos os direitos reservados.

---

**SKPONTO** - Sistema de Controle de Ponto Profissional
Desenvolvido com ❤️ usando Flask e Python
