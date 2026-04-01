# 🏦 Livro Caixa da Igreja - Sistema Web

Sistema de gestão financeira para igrejas com dashboard interativo, controle de usuários e banco de dados SQLite.

## 📋 Funcionalidades

- ✅ **Dashboard Interativo** - Visualize resumo financeiro, gráficos de receitas e despesas
- ✅ **Gerenciamento de Transações** - Crie, edite e delete transações facilmente
- ✅ **Controle de Usuários** - Gerencie acesso com diferentes níveis de permissão
- ✅ **Autenticação Segura** - Login com email e senha com hash SHA256
- ✅ **Auditoria Completa** - Registre todas as ações no sistema
- ✅ **Interface Moderna** - Tema escuro profissional com gráficos dinâmicos
- ✅ **Dados Persistentes** - Banco de dados SQLite local

## 🚀 Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passo 1: Instalar Dependências

```bash
pip install -r requirements.txt
```

## 🎯 Como Usar

### Iniciar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá em `http://localhost:8501`

### Primeiro Acesso

1. **Criar Usuário Admin**
   - Na tela de login, use a aba "Primeiro Acesso"
   - Email: `admin@igreja.com`
   - Senha: `Admin123456`

2. **Fazer Login**
   - Insira suas credenciais na tela de login
   - Clique em "Entrar"

## 📊 Seções da Aplicação

### Dashboard
- Resumo financeiro (receitas, despesas, saldo)
- Gráficos de distribuição por categoria
- Evolução do saldo acumulado

### Transações
- Visualizar todas as transações
- Filtrar por tipo e categoria
- Criar nova transação
- Editar transações (com permissão)
- Deletar transações (com permissão)

### Usuários (Admin)
- Listar todos os usuários
- Convidar novos usuários por email
- Resetar senhas
- Alterar níveis de acesso
- Ativar/Desativar usuários

### Meu Perfil
- Visualizar informações pessoais
- Alterar senha
- Ver nível de acesso

## 👥 Níveis de Acesso

### 👁️ Visualizador
- Ver dashboard e relatórios
- Ver transações

### ✏️ Editor
- Todas as permissões de visualizador
- Criar transações
- Editar transações

### 🔑 Administrador
- Todas as permissões
- Gerenciar usuários
- Resetar senhas
- Alterar níveis de acesso

## 🗄️ Banco de Dados

O sistema usa SQLite com as seguintes tabelas:

### usuarios
- id (INTEGER PRIMARY KEY)
- email (TEXT UNIQUE)
- nome (TEXT)
- senha_hash (TEXT)
- access_level (viewer/editor/admin)
- ativo (BOOLEAN)
- data_criacao (TIMESTAMP)
- ultimo_acesso (TIMESTAMP)

### transacoes
- id (INTEGER PRIMARY KEY)
- data (DATE)
- descricao (TEXT)
- tipo (receita/despesa)
- valor (REAL)
- categoria (TEXT)
- usuario_id (FOREIGN KEY)
- notas (TEXT)
- data_criacao (TIMESTAMP)
- data_atualizacao (TIMESTAMP)

### auditoria
- id (INTEGER PRIMARY KEY)
- usuario_id (FOREIGN KEY)
- acao (TEXT)
- descricao (TEXT)
- tabela_alvo (TEXT)
- id_alvo (INTEGER)
- data_hora (TIMESTAMP)

### configuracoes
- id (INTEGER PRIMARY KEY)
- chave (TEXT UNIQUE)
- valor (TEXT)
- data_atualizacao (TIMESTAMP)

## 🔐 Segurança

- Senhas são armazenadas com hash SHA256
- Cada usuário tem acesso apenas às funcionalidades permitidas
- Todas as ações são registradas em auditoria
- Validação de email e senha

## 🎨 Paleta de Cores

- **Primário:** Roxo/Índigo (#6366F1)
- **Secundário:** Verde (#10B981)
- **Perigo:** Vermelho (#EF4444)
- **Aviso:** Laranja (#F59E0B)
- **Sucesso:** Verde (#10B981)
- **Info:** Azul (#3B82F6)
- **Background:** Azul muito escuro (#0F172A)
- **Superfície:** Cinza escuro (#1E293B)

## 📧 Configuração de Email (Opcional)

Para enviar convites por email, configure as credenciais no arquivo `config.py`:

```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "seu_email@gmail.com"
SENDER_PASSWORD = "sua_senha_de_app"
```

## 🐛 Troubleshooting

### Erro: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Erro: Banco de dados locked
- Feche outras instâncias da aplicação
- Delete o arquivo `livro_caixa.db` para reiniciar

### Erro: Porta 8501 em uso
```bash
streamlit run app.py --server.port 8502
```

## 📝 Categorias Padrão

### Receitas
- Dízimos
- Ofertas
- Eventos
- Doações
- Aluguel de Espaços
- Outras Receitas

### Despesas
- Salários e Encargos
- Aluguel
- Utilitários (água, luz, gás)
- Manutenção
- Materiais
- Comunicação
- Transporte
- Outras Despesas

## 🚀 Melhorias Futuras

- [ ] Exportar relatórios em PDF
- [ ] Integração com métodos de pagamento
- [ ] Backup automático
- [ ] Notificações por email
- [ ] API REST para integração
- [ ] Múltiplas igrejas na mesma instância
- [ ] Gráficos de tendências
- [ ] Dashboard em tempo real

## 📞 Suporte

Para dúvidas ou problemas, entre em contato com o administrador do sistema.

## 📄 Licença

Este projeto é de código aberto e pode ser utilizado livremente.

---

**Desenvolvido com ❤️ para igrejas**
