# 🚀 GUIA DE DEPLOYMENT NO STREAMLIT CLOUD

## ✅ Pré-requisitos
1. Conta no [Streamlit Cloud](https://streamlit.io/cloud)
2. Repositório no GitHub (seu projeto tem .git/)
3. As credenciais de email configuradas

## 📋 Passos para Deploy

### 1️⃣ Preparar seu repositório GitHub
```bash
git add .
git commit -m "Preparação para Streamlit Cloud deployment"
git push origin main
```

### 2️⃣ Acessar Streamlit Cloud
- Abra https://share.streamlit.io
- Clique em "New app"

### 3️⃣ Configurar a Nova App
- **GitHub repository**: Selecione seu repositório
- **Branch**: main (ou a branch desejada)
- **Main file path**: app.py
- Clique em "Deploy"

### 4️⃣ Configurar Secrets (IMPORTANTE!)
1. Na página da sua app, clique no ☰ (menu) no canto superior direito
2. Selecione "Settings" → "Secrets"
3. Copie e cole o conteúdo do `.streamlit/secrets.toml`:

```toml
SENDER_EMAIL = "seu_email@gmail.com"
SENDER_PASSWORD = "sua_senha_de_app"
SECRET_KEY = "sua_chave_secreta_muito_segura_aqui_123456"
```

## 🔐 Criando Senhas de App para Gmail
Se usar Gmail SMTP:
1. Acesse https://myaccount.google.com/security
2. Ative "Verificação em 2 etapas"
3. Procure por "Senhas de app"
4. Selecione "Mail" e "Windows Computer"
5. Copie a senha gerada (16 caracteres)
6. Use essa senha como SENDER_PASSWORD nos secrets

## 📝 Problemas Comuns

### ❌ "Error installing requirements"
Isso foi resolvido! Os arquivos foram atualizados para:
- ✅ requirements.txt comentado adequadamente
- ✅ .streamlit/config.toml criado
- ✅ .streamlit/secrets.toml criado
- ✅ config.py atualizado para usar st.secrets

### ❌ "ModuleNotFoundError"
Certifique-se que:
- Todos os .py estão no raiz ou em pastas importáveis
- requirements.txt tem todas as dependências
- Nenhuma dependência tem versão incompatível

### ❌ "SQLite database is locked"
No Streamlit Cloud, SQLite pode ter problemas de concorrência.
Se tiver erros, considere:
- Aumentar timeout nas conexões
- Usar um banco de dados em nuvem (PostgreSQL)
- Adicionar lógica de fila/cache

## 🔄 Após o Deploy
- A app será ativaizada automaticamente quando você fizer push
- Logs disponíveis no botão "Manage app" → "View logs"
- Se houver erro, aparecer um erro em vermelho que mostra o terminal

## 📚 Documentação Importante
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Secrets Management](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources-secrets-management)
- [Troubleshooting](https://docs.streamlit.io/streamlit-cloud/troubleshoot)
