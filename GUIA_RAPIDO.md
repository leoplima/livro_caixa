# 🚀 GUIA RÁPIDO DE USO - Livro Caixa da Igreja

## ⚡ Começando em 5 Minutos

### 1️⃣ Iniciar a Aplicação

Abra um terminal na pasta do projeto e execute:

```bash
streamlit run app.py
```

Ou use o PowerShell:

```powershell
cd c:\Users\Lekavi\Desktop\ia_master
streamlit run app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

### 2️⃣ Fazer Login

**Credenciais de Acesso:**
- 📧 Email: `admin@igreja.com`
- 🔑 Senha: `Admin123456`

### 3️⃣ Explorar o Dashboard

Após fazer login, você verá:

#### 📊 Dashboard Principal
- **Resumo Financeiro:** Receitas, Despesas e Saldo Total
- **Gráficos de Receitas:** Distribuição por categoria
- **Gráficos de Despesas:** Distribuição por categoria
- **Evolução do Saldo:** Gráfico de linha com evolução temporal

#### 💳 Transações
- **Ver Transações:** Lista completa com filtros
- **Nova Transação:** Criar receitas e despesas

#### 👥 Usuários (Apenas Admin)
- **Gerenciar Usuários:** Ver todos os usuários
- **Convidar Novo:** Adicionar novos usuários com níveis de acesso

#### ⚙️ Meu Perfil
- **Alterar Senha:** Mude sua senha de acesso
- **Ver Informações:** Email, nome e nível de acesso

## 📊 Exemplo de Uso Completo

### Passo 1: Criar um Novo Usuário

1. Vá para **👥 Usuários** (menu lateral)
2. Clique em **Convidar Novo**
3. Preencha:
   - Email: `mariana@igreja.com`
   - Nome: `Mariana Santos`
   - Nível: `Editor`
4. Clique **📧 Enviar Convite**

### Passo 2: Registrar uma Receita

1. Vá para **💳 Transações**
2. Clique na aba **Nova Transação**
3. Preencha:
   - Tipo: 📥 Receita
   - Data: Selecione a data
   - Descrição: `Dízimo da Semana`
   - Valor: `1500`
   - Categoria: `Dízimos`
   - Notas: `Arrecadação de domingo`
4. Clique **💾 Salvar Transação**

### Passo 3: Registrar uma Despesa

1. Vá para **💳 Transações**
2. Clique na aba **Nova Transação**
3. Preencha:
   - Tipo: 📤 Despesa
   - Data: Selecione a data
   - Descrição: `Contas de Água e Luz`
   - Valor: `800`
   - Categoria: `Utilitários (água, luz, gás)`
   - Notas: `Conta do mês de março`
4. Clique **💾 Salvar Transação**

### Passo 4: Visualizar Dados no Dashboard

1. Vá para **📊 Dashboard**
2. Veja:
   - Resumo atualizado com novas transações
   - Gráficos atualizados automaticamente
   - Evolução do saldo

## 🔐 Gerenciamento de Usuários (Admin)

### Criar Novo Usuário

1. Menu → **👥 Usuários**
2. Aba **Convidar Novo**
3. Preencha email, nome e nível de acesso
4. Clique em **Enviar Convite**

### Níveis de Acesso

**👁️ Visualizador**
- Apenas visualizar dashboard e transações
- Sem permissão de criar/editar

**✏️ Editor**
- Ver dashboard e transações
- Criar novas transações
- Editar transações

**🔑 Administrador**
- Acesso total
- Gerenciar usuários
- Resetar senhas

### Resetar Senha de Usuário

1. Menu → **👥 Usuários**
2. Aba **Usuários**
3. Selecione o usuário
4. Clique **🔐 Resetar Senha**
5. A nova senha aparecerá na tela

## 💡 Dicas Importantes

### ✅ Boas Práticas

1. **Altere a Senha do Admin:** Na primeira vez que logar, mude a senha padrão
2. **Crie Usuários por Nível:** Use visualizadores para consultas, editores para registros
3. **Registre Tudo:** Sempre adicione notas nas transações
4. **Faça Backup:** De tempos em tempos, faça cópia do arquivo `livro_caixa.db`
5. **Use Categorias Corretamente:** Facilita análise nos gráficos

### 🔍 Filtros e Buscas

No menu **💳 Transações**:
- Filtre por **Tipo** (Receita/Despesa)
- Filtre por **Categoria**
- Ordene por **Data**

### 📈 Dashboard

No menu **📊 Dashboard**:
- Use os **Filtros de Data** para análises específicas
- Observe os **Gráficos de Pizza** para distribuição
- Acompanhe a **Evolução do Saldo** no gráfico de linha

## 🐛 Se Algo Não Funcionar

### Erro: Porta em uso

```bash
streamlit run app.py --server.port 8502
```

### Erro: Módulo não encontrado

```bash
pip install -r requirements.txt
```

### Resetar o Sistema

```bash
# Delete o banco de dados
del livro_caixa.db

# Reinitialize
python init.py

# Reinicie a aplicação
streamlit run app.py
```

## 📱 Responsividade

A aplicação funciona bem em:
- ✅ Desktop e Laptop
- ✅ Tablets
- ✅ Celulares (versão mobile)

## 🌙 Tema Escuro

O sistema usa automaticamente um tema escuro profissional:
- Cores suaves e modernas
- Fácil para os olhos
- Gráficos dinamicamente coloridos

## 📞 Precisa de Ajuda?

1. Consulte o arquivo `README.md`
2. Verifique a configuração em `config.py`
3. Revise os logs de auditoria em Usuários → **Ver Transações**

---

**Aproveite o sistema! 🎉**

Para iniciar: `streamlit run app.py`
