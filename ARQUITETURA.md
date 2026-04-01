# 🏗️ ESTRUTURA DO PROJETO

## 📁 Arquivos Criados

```
ia_master/
├── app.py                  # Aplicação principal Streamlit
├── db.py                   # Gerenciador de banco de dados
├── auth.py                 # Sistema de autenticação
├── config.py               # Configurações centralizadas
├── init.py                 # Script de inicialização
├── requirements.txt        # Dependências do projeto
├── livro_caixa.db         # Banco de dados SQLite (criado automaticamente)
├── README.md              # Documentação completa
└── GUIA_RAPIDO.md         # Guia de uso rápido
```

## 🔧 Descrição dos Arquivos

### `app.py` - Aplicação Principal
Arquivo principal do Streamlit com toda a interface do usuário.

**Componentes:**
- `tela_login()` - Interface de login
- `tela_dashboard()` - Dashboard com gráficos
- `tela_transacoes()` - Gerenciamento de transações
- `tela_usuarios()` - Gerenciamento de usuários (admin)
- `tela_perfil()` - Configurações de perfil do usuário
- `main()` - Função principal com navegação

**Como customizar:**
```python
# Mudar cores
COLORS['primary'] = "#NOVA_COR"

# Adicionar nova página
def tela_relatorios():
    st.markdown("...")

# Registrar na navegação (em main())
if st.button("📄 Relatórios", use_container_width=True):
    st.session_state.page = 'relatorios'
```

### `db.py` - Banco de Dados
Classe Database que gerencia todas as operações do SQLite.

**Métodos principais:**
```python
# Usuários
db.criar_usuario(email, nome, senha_hash)
db.get_usuario_por_email(email)
db.listar_usuarios()
db.atualizar_usuario(user_id, **kwargs)

# Transações
db.criar_transacao(data, descricao, tipo, valor, ...)
db.listar_transacoes(filtro_tipo, filtro_categoria, ...)
db.get_resumo_financeiro()
db.get_transacoes_por_categoria(tipo)

# Auditoria
db.registrar_auditoria(usuario_id, acao, descricao, ...)
db.listar_auditoria()
```

**Como adicionar nova tabela:**
```python
def init_db(self):
    # No método init_db, adicione:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nova_tabela (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            campo1 TEXT NOT NULL,
            campo2 REAL
        )
    ''')
    conn.commit()
```

### `auth.py` - Autenticação
Classe Auth que gerencia autenticação, validação e segurança.

**Métodos principais:**
```python
auth.registrar_usuario(email, nome, senha)
auth.autenticar(email, senha)
auth.validar_email(email)
auth.validar_senha(senha)
auth.alterar_senha(user_id, atual, nova)
auth.redefinir_senha(user_id, admin_id)
auth.convidar_usuario(email, nome, access_level)
auth.enviar_email_convite(email, nome, level, sender, password)
```

**Como customizar segurança:**
```python
# Aumentar requisitos de senha
def validar_senha(senha):
    if len(senha) < 12:  # Aumentar de 8 para 12
        return False, "Senha deve ter no mínimo 12 caracteres"
    
    if not any(c in "!@#$%^&*" for c in senha):
        return False, "Deve conter caracteres especiais"
    
    return True, "Válida"
```

### `config.py` - Configurações
Arquivo central de configurações do sistema.

**Variáveis principais:**
```python
COLORS           # Paleta de cores
DATABASE_PATH    # Caminho do banco de dados
CATEGORIAS_*     # Categorias padrão
ACCESS_LEVELS    # Níveis de permissão
SMTP_SERVER      # Configurações de email
```

**Como mudar as cores:**
```python
COLORS = {
    "primary": "#seunova_cor",
    "secondary": "#sua_cor",
    # ...
}
```

### `init.py` - Inicialização
Script que cria banco de dados, usuário admin e dados de exemplo.

**Executar:**
```bash
python init.py
```

**O que faz:**
1. Inicializa banco de dados
2. Cria usuário admin
3. Cria 10 transações de exemplo
4. Exibe resumo financeiro

## 🔄 Fluxo da Aplicação

```
┌─────────────────┐
│   Login/Auth    │
└────────┬────────┘
         │
    ✓ Válido?
         │ SIM
         ▼
┌─────────────────┐
│   Dashboard     │ ◄─┐
│  (Página Base)  │   │
└────┬────────────┘   │
     │                │
  ┌──┴─────────────────┘
  │
  ├─► 📊 Dashboard     ◄─┐
  │   └─► Transações   │  │ Navegação
  │       └─► Usuários │  │
  │           └─► Perfil ◄┤ (Sidebar)
  │
  └─► Banco de Dados
      └─► Auditoria
```

## 📊 Dados que o Sistema Rastreia

### Usuários
- Email, nome, nível de acesso
- Hash de senha (nunca armazena senha em texto)
- Status ativo/inativo
- Data de criação e último acesso

### Transações
- Data, descrição, tipo (receita/despesa)
- Valor e categoria
- Usuário que criou
- Notas opcionais
- Data de criação e atualização

### Auditoria
- Quem fez a ação
- Qual ação (CREATE, UPDATE, DELETE)
- Quando foi feito
- Em qual tabela

## 🔐 Segurança

### ✅ Implementado
- Hash SHA256 para senhas
- Validação de email
- Validação de força de senha
- Logs de auditoria
- Controle de permissões
- Session management do Streamlit

### ⚠️ Melhorias Recomendadas
- Usar bcrypt em vez de SHA256
- Implementar 2FA (autenticação em dois fatores)
- Criptografia do banco de dados
- Rate limiting de login
- Backup automático

**Para agregar bcrypt:**
```bash
pip install bcrypt
```

```python
# Em auth.py
import bcrypt

@staticmethod
def hash_senha(senha):
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

def autenticar(self, email, senha):
    usuario = self.db.get_usuario_por_email(email)
    if bcrypt.checkpw(senha.encode(), usuario['senha_hash'].encode()):
        # OK
```

## 🚀 Expandindo o Sistema

### Adicionar Nova Categoria

**Em config.py:**
```python
CATEGORIAS_RECEITA = [
    # ... existentes
    "Aluguel de Salas",  # Nova
]

CATEGORIAS_DESPESA = [
    # ... existentes
    "Seguro",  # Nova
]
```

### Adicionar Novo Relatório

**Em app.py:**
```python
def tela_relatorio_anual():
    st.markdown("<h2 style='color: #6366F1;'>📈 Relatório Anual</h2>", unsafe_allow_html=True)
    
    ano = st.selectbox("Escolha o ano", [2023, 2024, 2025])
    
    transacoes = db.listar_transacoes()
    # Filtrar por ano...
    # Criar gráficos...

# Na função main():
if st.button("📈 Relatório Anual", use_container_width=True):
    st.session_state.page = 'relatorio_anual'
```

### Adicionar Campo à Transação

**Em db.py (init_db):**
```python
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes (
        -- ... campos existentes
        comprovante TEXT,  # Novo campo
        -- ... resto
    )
''')
```

## 🧪 Testando o Sistema

### Teste de Login
```python
from auth import Auth
auth = Auth()
sucesso, usuario, msg = auth.autenticar("admin@igreja.com", "Admin123456")
print(sucesso)  # True
```

### Teste de Transação
```python
from db import Database
db = Database()
novo_id = db.criar_transacao(
    data="2024-01-15",
    descricao="Teste",
    tipo="receita",
    valor=100,
    categoria="Dízimos",
    usuario_id=1
)
print(novo_id)  # ID da transação criada
```

## 📋 Checklist de Deploy

- [ ] Alterar senha do admin padrão
- [ ] Configurar SMTP para envio de emails
- [ ] Fazer backup do banco de dados
- [ ] Testar todos os níveis de acesso
- [ ] Verificar logs de auditoria
- [ ] Criar guia para usuários finais
- [ ] Configurar SSL/HTTPS se online
- [ ] Definir política de backup automático

## 🔗 Links Úteis

- [Documentação Streamlit](https://docs.streamlit.io)
- [Documentação Plotly](https://plotly.com/python)
- [SQLite Python](https://docs.python.org/3/library/sqlite3.html)
- [Pandas Documentation](https://pandas.pydata.org/docs)

## 📝 Notas Importantes

1. **Backup Regular:** Execute regularmente:
   ```bash
   copy livro_caixa.db livro_caixa_backup_$(date +%Y%m%d).db
   ```

2. **Monitorar Banco:** Banco de dados SQLite é local, adequado para igrejas pequenas/médias

3. **Escalabilidade:** Para centenas de transações, funciona bem. Para milhões, considere PostgreSQL

4. **Performance:** Gráficos podem ficar lentos com milhares de transações. Adicione índices ao DB:
   ```python
   cursor.execute("CREATE INDEX idx_transacoes_data ON transacoes(data)")
   cursor.execute("CREATE INDEX idx_transacoes_tipo ON transacoes(tipo)")
   ```

---

**Desenvolvido com ❤️ para igrejas**
