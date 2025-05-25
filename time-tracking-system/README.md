\OneDrive\Python Projetos\PONTO_ONLINE\time-tracking-system\README.md
# 🕒 Sistema de Controle de Ponto Online

Um sistema completo de controle de ponto desenvolvido em Python com Flask, Firebase e Dropbox.

## 🚀 Funcionalidades

### 👥 **Tipos de Usuário**
- **ADMINISTRADOR**: Acesso total ao sistema
- **TRABALHADOR**: 8h diárias (+ 1h almoço)
- **ESTAGIÁRIO**: 6h diárias (+ 1h almoço)

### 🔐 **Autenticação**
- Login/Logout seguro
- Cadastro de usuários
- Recuperação de senha
- Hash de senhas com bcrypt

### ⏰ **Controle de Ponto**
- Registro de entrada/saída
- Controle de almoço
- Ajuste de horários
- Cálculo automático de horas extras

### 📊 **Relatórios**
- Relatórios individuais
- Relatórios administrativos
- Exportação em CSV
- Gráficos interativos

### 📱 **Interface Moderna**
- Design responsivo
- Dashboard intuitivo
- Notificações em tempo real
- Upload de fotos de perfil

## 🛠️ **Tecnologias**

- **Backend**: Python 3.11+, Flask
- **Banco de Dados**: Firebase Firestore
- **Armazenamento**: Dropbox API
- **Frontend**: HTML5, CSS3, JavaScript
- **Deploy**: Render.com
- **Autenticação**: Flask-Bcrypt
- **Gráficos**: Plotly.js

## ⚙️ **Configuração**

### 1. **Clonagem do Repositório**
```bash
git clone https://github.com/G437SG/skponto.git
cd skponto
```

### 2. **Instalação de Dependências**
```bash
pip install -r requirements.txt
```

### 3. **Configuração das Variáveis de Ambiente**
Crie um arquivo `.env` na raiz do projeto:
```env
SECRET_KEY=sua-chave-secreta-aqui
FIREBASE_PROJECT_ID=seu-projeto-firebase
FIREBASE_PRIVATE_KEY_ID=sua-private-key-id
FIREBASE_PRIVATE_KEY=sua-private-key
FIREBASE_CLIENT_EMAIL=seu-client-email
FIREBASE_CLIENT_ID=seu-client-id
FIREBASE_CLIENT_CERT_URL=sua-client-cert-url
DROPBOX_ACCESS_TOKEN=seu-token-dropbox
```

### 4. **Execução Local**
```bash
python app.py
```

### 5. **Deploy no Render.com**
1. Conecte seu repositório GitHub ao Render
2. Configure as variáveis de ambiente
3. Deploy automático a cada push

## 📁 **Estrutura do Projeto**

```
skponto/
├── app/
│   ├── models/          # Modelos de dados
│   ├── routes/          # Rotas da aplicação
│   ├── services/        # Serviços (Firebase, Dropbox)
│   └── utils/           # Utilitários
├── config/              # Configurações
├── static/              # Arquivos estáticos
├── templates/           # Templates HTML
├── requirements.txt     # Dependências
├── Procfile            # Configuração Render
└── app.py              # Aplicação principal
```

## 🔧 **Configuração do Firebase**

1. Crie um projeto no [Firebase Console](https://console.firebase.google.com)
2. Ative o Firestore Database
3. Gere uma chave de serviço
4. Configure as variáveis de ambiente

## 📦 **Configuração do Dropbox**

1. Crie um app no [Dropbox Developers](https://www.dropbox.com/developers/apps)
2. Gere um Access Token
3. Configure as permissões necessárias
4. Adicione o token nas variáveis de ambiente

## 🚀 **Deploy**

O sistema está configurado para deploy automático no Render.com:

1. Fork este repositório
2. Conecte ao Render.com
3. Configure as variáveis de ambiente
4. Deploy automático!

## 📈 **Funcionalidades Avançadas**

- **Notificações**: Sistema completo de notificações
- **Relatórios Avançados**: Filtros por período e usuário
- **Gráficos**: Visualização de horas trabalhadas
- **Upload de Arquivos**: Fotos de perfil via Dropbox
- **Exportação**: Relatórios em CSV
- **Responsivo**: Funciona em desktop e mobile

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 **Suporte**

Se você encontrar algum problema ou tiver dúvidas:

1. Verifique as [Issues](https://github.com/G437SG/skponto/issues) existentes
2. Abra uma nova issue se necessário
3. Forneça detalhes sobre o problema

---

Desenvolvido com ❤️ para facilitar o controle de ponto empresarial.