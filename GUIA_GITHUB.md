# 🚀 GUIA: FAZER PUSH PARA GITHUB COM SEGURANÇA

## 📋 Passo 1: Criar Repositório no GitHub

1. Acesse **[github.com](https://github.com)**
2. Clique em **"+" → "New repository"** (canto superior direito)
3. **Repository name:** `Livro-Caixa`
4. **Description:** `Sistema de gestão financeira para igrejas`
5. **Visibility:** Escolha **Public** (ou Private se preferir)
6. Clique em **"Create repository"**

⚠️ **NÃO inicialize com README, .gitignore ou license** (já temos localmente)

---

## 📋 Passo 2: Configurar Git Localmente

Abra o **Terminal/PowerShell** na pasta do projeto:

```powershell
cd c:\Users\Lekavi\Desktop\ia_master
```

### Se ainda NÃO tem Git instalado:

```powershell
# Instalar Git (Windows)
# Download em: https://git-scm.com/download/win
# Ou use Chocolatey:
choco install git
```

### Configurar seu nome e email (uma só vez):

```powershell
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@github.com"
```

---

## 📋 Passo 3: Enviar Projeto para GitHub

```powershell
# 1. Inicializar repositório (se ainda não tem)
git init

# 2. Adicionar arquivo de segurança
git add .gitignore .env.example

# 3. Adicionar todos os arquivos (exceto os no .gitignore)
git add .

# 4. Fazer primeiro commit
git commit -m "Initial commit - Livro Caixa v2.0"

# 5. Renomear branch principal para 'main'
git branch -M main

# 6. Conectar ao repositório do GitHub
git remote add origin https://github.com/SEU_USER/Livro-Caixa.git

# 7. Fazer push (enviar) para GitHub
git push -u origin main
```

⚠️ **IMPORTANTE:** Substitua `SEU_USER` pelo seu usuário do GitHub!

### Exemplo completo:
```powershell
git remote add origin https://github.com/lekavi/Livro-Caixa.git
git push -u origin main
```

---

## 🔐 Passo 4: Verificar Segurança

Acesse seu repositório no GitHub: 
```
https://github.com/SEU_USER/Livro-Caixa
```

✅ **Verifique se:**
- [ ] `livro_caixa.db` NÃO está lá (banco de dados)
- [ ] `uploads/` NÃO está lá (logos das igrejas)
- [ ] `.env` NÃO está lá (variáveis sensíveis)
- [ ] `.gitignore` ESTÁ lá (arquivo de proteção)
- [ ] `app.py`, `db.py`, `auth.py` estão lá
- [ ] `requirements.txt` está lá
- [ ] `.env.example` está lá (template seguro)

---

## 📝 Passo 5: Atualizar em Produção

Depois que fizer mudanças locais:

```powershell
# Ver quais arquivos foram alterados
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição da mudança"

# Fazer push
git push origin main
```

---

## 🔑 Autenticação GitHub (Token)

Quando Git pedir para "autenticar", você tem 2 opções:

### Opção A: Token Pessoal (Recomendado)

1. GitHub → Settings → Developer settings → Personal access tokens
2. Clique em "Generate new token"
3. Selecione `repo` (acesso a repositórios)
4. Copie o token gerado
5. Quando Git pedir senha, cole o token

[Guia Completo](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

### Opção B: SSH Key

Mais seguro, mas mais complexo:

```powershell
# 1. Gerar chave SSH
ssh-keygen -t ed25519 -C "seu.email@github.com"

# 2. Adicionar à SSH agent (automático no Windows 10+)

# 3. Colar a chave pública no GitHub
# Settings → SSH and GPG keys → New SSH key
```

[Guia Completo de SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

---

## ✅ CHECKLIST FINAL

Antes de compartilhar o link:

- [ ] Repositório criado no GitHub
- [ ] Arquivos feito push com sucesso
- [ ] `livro_caixa.db` NÃO aparece no repo
- [ ] `uploads/` NÃO aparece no repo
- [ ] `.env` NÃO aparece no repo
- [ ] `.gitignore` está visível no GitHub
- [ ] `README.md` está completo
- [ ] `requirements.txt` tem todas as dependências

---

## 🤝 Compartilhar com Outros

Agora você pode:

1. **Compartilhar o link:**
   ```
   https://github.com/SEU_USER/Livro-Caixa
   ```

2. **Outros podem clonar:**
   ```powershell
   git clone https://github.com/SEU_USER/Livro-Caixa.git
   cd Livro-Caixa
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   streamlit run app.py
   ```

---

## ⚠️ IMPORTANTE: DADOS SENSÍVEIS

Estes arquivos **NÃO devem NUNCA** ir para GitHub:

- ❌ `livro_caixa.db` - Contém usuários, senhas (hash), transações reais
- ❌ `uploads/` - Logos e marcas d'água privadas
- ❌ `.env` - Variáveis de ambiente com credenciais
- ❌ `/venv` - Ambiente virtual (recriado com pip install)

**O `.gitignore` protege esses arquivos automaticamente!**

---

## 💡 Dicas

1. **Nunca commitar dados sensíveis acidentalmente:**
   ```powershell
   # Ver o que será enviado:
   git diff --cached
   ```

2. **Se acidentalmente fez push de dados sensíveis:**
   - Altere todas as senhas imediatamente
   - Faça `git rm --cached arquivo` e novo commit
   - Use `git history` para limpar histórico (avançado)

3. **Manter repo atualizado:**
   ```powershell
   # Baixar atualizações de outros
   git pull origin main
   ```

---

## 🆘 Precisa de Ajuda?

- Erro ao fazer push? → Verifique o token/SSH key
- Arquivo indesejado foi enviado? → Abra uma Issue
- Dúvidas com Git? → [Git Docs](https://git-scm.com/doc)

---

**Pronto! 🚀 Seu projeto está seguro e disponível para o mundo!**
