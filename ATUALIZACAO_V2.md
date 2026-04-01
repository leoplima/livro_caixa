# 🚀 Atualização do Sistema - Multi-Igreja com Interface Moderna

## ✨ Novidades Implementadas

### 1. **Multi-Tenancy (Múltiplas Igrejas)**
- ✅ Criar e gerenciar múltiplas igrejas
- ✅ Cada usuário tem acesso apenas às igrejas permitidas pelo admin
- ✅ Dados completamente isolados por igreja
- ✅ Seletor de igreja dinâmico no dashboard

### 2. **Marca D'água Dinâmica**
- ✅ Cada igreja pode adicionar sua própria marca d'água/logo
- ✅ A marca muda automaticamente quando o usuário troca de igreja
- ✅ Suporte para imagens PNG, JPG e JPEG

### 3. **Interface Totalmente Moderna e Responsiva**
- ✅ Design mobile-first 100% responsivo
- ✅ Funcionará perfeitamente em celulares, tablets e desktops
- ✅ Animações suaves em transições
- ✅ Botões, cards e elementos com efeitos hover modernos
- ✅ Fonte moderna (Google Fonts: Plus Jakarta Sans)

### 4. **Nova Paleta de Cores Vibrante**
```
Primária:    Roxo Vibrante (#7C3AED)
Secundária:  Ciano (#06B6D4)
Accent:      Magenta/Pink (#FF006E)
Sucesso:     Verde Esmeralda (#10B981)
Perigo:      Vermelho Vibrante (#EF4444)
Aviso:       Laranja (#F59E0B)
```

### 5. **Animações e Transições**
- ✅ Slide in: Elementos aparecem com movimento suave
- ✅ Fade in: Desvanecimento gradual
- ✅ Hover effects: Botões e cards reagem ao mouse
- ✅ Transições CSS fluidas (cubic-bezier)

## 📁 Arquivos Modificados/Criados

| Arquivo | Mudança |
|---------|---------|
| `config.py` | Paleta de cores atualizada |
| `db.py` | Tabelas de igrejas e acesso de usuários |
| `app_new.py` | ⭐ Nova aplicação (renomear para app.py) |
| `init_v2.py` | ⭐ Novo inicializador (usar este) |

## 🚀 Como Atualizar

### Opção 1: Fresh Start (Recomendado)

```bash
# 1. Backup do banco antigo
copy livro_caixa.db livro_caixa_backup.db

# 2. Deletar banco antigo
del livro_caixa.db

# 3. Renomear nova app
move app.py app_old.py
move app_new.py app.py

# 4. Inicializar novo sistema
python init_v2.py

# 5. Iniciar
streamlit run app.py
```

### Opção 2: Usar o script

```bash
# Backup
copy livro_caixa.db livro_caixa_backup.db

# Atualizar
python init_v2.py
move app.py app_old.py
move app_new.py app.py
streamlit run app.py
```

## 📋 Dados de Exemplo Pré-configurados

### Igrejas
1. **Igreja Central** (ID: 1)
   - CNPJ: 12.345.678/0001-90
   - Endereço: Rua Principal, 100

2. **Igreja Filial** (ID: 2)
   - CNPJ: 12.345.678/0001-91
   - Endereço: Avenida Secundária, 200

### Usuários

| Email | Senha | Nível | Acesso |
|-------|-------|-------|--------|
| admin@igreja.com | Admin123456 | Admin | Todas as igrejas |
| tesoureiro@gmail.com | Tesoureiro123 | Editor | Igreja Central |
| viewer@gmail.com | Viewer123 | Viewer | Igreja Filial |

## 🎨 Melhorias Visuais

### Botões
- Gradiente colorido
- Sombra dinâmica
- Efeito hover com elevação (translateY)
- Transição suave

### Cards/Métricas
- Fundo degradê
- Borda esquerda colorida
- Hover lift (eleva 5px)
- Sombra responsiva

### Inputs
- Fundo escuro com borda
- Focus ring colorido
- Transição suave de cores
- Placeholders informativos

### Animações
- Slide in ao carregar página
- Fade in para elementos
- Pulse para carregamento
- Transições entre abas

## 📱 Responsividade

A interface agora é **100% responsiva**:

```css
/* Mobile (< 768px) */
- Buttons: 10px 16px
- Font size reduzido
- Cards com padding menor

/* Tablet (768px - 1024px) */
- Layout otimizado
- Colunas duplas ajustadas

/* Desktop (> 1024px) */
- Layout completo
- 3 colunas em dashboards
```

## 🔐 Controle de Acesso Multi-Igreja

### Admin
```
✅ Criar/editar igrejas
✅ Convidar usuários
✅ Gerenciar permissões
✅ Acesso a todas as igrejas
```

### Editor
```
✅ Criar/editar transações
✅ Ver dashboard
⚠️ Apenas igrejas atribuídas
```

### Viewer
```
✅ Ver dashboard
✅ Ver transações
⚠️ Sem criar/editar
⚠️ Apenas igrejas atribuídas
```

## 💾 Marca D'água

### Como Adicionar

1. Fazer login como **Admin**
2. Ir em **🏛️ Igrejas** (menu lateral)
3. Clicar em **➕ Nova Igreja**
4. Fazer upload da imagem (PNG/JPG)
5. A imagem aparecerá como fundo (15% opacidade)

A marca d'água muda **automaticamente** quando o usuário troca de igreja.

## 🎯 Recursos Novos

### Dashboard
- ✅ Seletor de igreja (se tiver acesso a múltiplas)
- ✅ Nome da igreja no topo
- ✅ Gráficos com nova paleta
- ✅ Cards com novos efeitos

### Menu Lateral
- ✅ Mostra Igreja Atual
- ✅ Botões com animação
- ✅ Icones descritivos
- ✅ Menu dividido por seções

### Transações
- ✅ Nova interface
- ✅ Ícones modernos
- ✅ Animações ao salvar
- ✅ Confirmação visual

### Usuários
- ✅ Gerenciamento por igreja
- ✅ Associação de acesso
- ✅ Novo design de convite

## 🛠️ Mudanças Técnicas

### Database
```sql
-- Novas tabelas:
CREATE TABLE igrejas (
  id INTEGER PRIMARY KEY,
  nome TEXT UNIQUE,
  marca_agua_path TEXT,
  cor_primaria TEXT,
  ...
)

CREATE TABLE usuario_igrejas (
  usuario_id INTEGER,
  igreja_id INTEGER,
  access_level TEXT,
  UNIQUE(usuario_id, igreja_id)
)

-- Campos adicionados:
ALTER TABLE transacoes ADD COLUMN igreja_id INTEGER;
ALTER TABLE usuarios ADD COLUMN igreja_padrao INTEGER;
ALTER TABLE auditoria ADD COLUMN igreja_id INTEGER;
```

### Métodos DB
```python
db.criar_igreja(nome, cnpj, endereco, ...)
db.get_igrejas_usuario(user_id)
db.adicionar_usuario_igreja(user_id, church_id, level)
db.get_resumo_financeiro(church_id)
db.listar_transacoes(church_id, ...)
```

## 📊 Estrutura de Diretórios

```
projeto/
├── app.py (renomeado de app_new.py)
├── app_old.py (backup)
├── db.py (atualizado)
├── auth.py
├── config.py (cores atualizadas)
├── init_v2.py (novo inicializador)
├── init.py (antigo)
├── livro_caixa.db (novo banco)
├── livro_caixa_backup.db (backup)
└── uploads/ (novo: marca d'água)
```

## 🎓 Exemplos de Uso

### Criar Nova Igreja
```python
igreja_id = db.criar_igreja(
    nome="Igreja Nova",
    cnpj="12.345.678/0001-92",
    endereco="Rua X, 123"
)
```

### Dar Acesso a Usuario
```python
db.adicionar_usuario_igreja(
    usuario_id=1,
    igreja_id=2,
    access_level='editor'
)
```

### Obter Igrejas do Usuário
```python
igrejas = db.get_igrejas_usuario(user_id=1)
# Retorna apenas igrejas que o usuário tem acesso
```

## ⚠️ Importante

1. **Antiga app.py**: Renomeie para `app_old.py` (backup)
2. **Nova app_new.py**: Renomeie para `app.py`
3. **init_v2.py**: Use este para inicializar o novo banco
4. **Banco antigo**: Delete ou faça backup antes

## 🐛 Troubleshooting

### Porta em uso?
```bash
streamlit run app.py --server.port 8502
```

### Erro de módulo?
```bash
pip install -r requirements.txt
```

### Resetar tudo?
```bash
del livro_caixa.db
python init_v2.py
streamlit run app.py
```

## 📞 Próximas Melhorias

- [ ] Exportar relatórios em PDF
- [ ] Autenticação 2FA
- [ ] Integração com email real
- [ ] Backup automático na nuvem
- [ ] API REST
- [ ] App mobile nativa
- [ ] Dark mode/Light mode toggle
- [ ] Previsões com IA

## ✅ Checklist

- [ ] Backup do banco antigo
- [ ] Deletar `livro_caixa.db`
- [ ] Renomear `app.py` → `app_old.py`
- [ ] Renomear `app_new.py` → `app.py`
- [ ] Executar `python init_v2.py`
- [ ] Executar `streamlit run app.py`
- [ ] Testar login com cada usuário
- [ ] Verificar marca d'água
- [ ] Testar transações por igreja

---

**Aproveite o novo sistema modernizado! 🚀**

Desenvolvido com ❤️ para igrejas
