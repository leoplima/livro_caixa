# 🏛️ Como Associar Usuários a Igrejas

## 📋 Visão Geral

Seu sistema agora permite que **administradores** controlem totalmente quais **igrejas** cada **usuário** pode acessar. Cada usuário pode ter acesso a uma ou múltiplas igrejas.

---

## 🚀 Como Fazer

### Passo 1️⃣: Acessar Admin (Usuário Admin)

```
Email:    admin@igreja.com
Senha:    Admin123456
```

Clique em **👥 Usuários** no menu

---

### Passo 2️⃣: Selecionar um Usuário

Na aba **👤 Usuários**, você verá uma tabela com:

| Email | Nome | Acesso a | Nível | Status |
|-------|------|----------|-------|--------|
| tesoureiro@gmail.com | Tesoureiro | Igreja Central | editor | ✅ Ativo |

Selecione o usuário na caixa **"Selecione um usuário"**

---

### Passo 3️⃣: Clicar em "✏️ Editar Usuário"

Aparecerá uma interface com:
- 📝 Nome e Email
- 🔐 Nível de Acesso  
- ✅ Status (Ativo/Inativo)
- **🏛️ Gerenciar Igrejas** (NOVO!)

---

### Passo 4️⃣: Gerenciar Igrejas (NOVO!)

Você verá **2 abas**:

#### ✅ **ABA 1: Igrejas com Acesso**

Mostra todas as igrejas que o usuário **JÁ TEM** acesso:

```
🏛️ Igreja Central

        [🗑️ Remover]
```

**Ações:**
- Clique em **🗑️ Remover** para tirar acesso do usuário dessa igreja

---

#### ➕ **ABA 2: Adicionar Igreja**

Mostra igrejas que o usuário **NÃO TEM** acesso:

```
🏛️ Igreja Filial

        [➕ Adicionar]
```

**Ações:**
- Clique em **➕ Adicionar** para dar acesso do usuário a essa igreja

---

## 📊 Exemplos Práticos

### Exemplo 1: Adicionar acesso a nova igreja

**Situação:**
- Tesoureiro tem acesso apenas a "Igreja Central"
- Precisa acessar também "Igreja Filial"

**Solução:**
1. Login: admin@igreja.com
2. Menu: **👥 Usuários**
3. Selecione: tesoureiro@gmail.com
4. Clique: **✏️ Editar Usuário**
5. Aba: **➕ Adicionar Igreja**
6. Clique: **➕ Adicionar** próximo a "Igreja Filial"
7. Clique: **💾 Salvar Alterações**

**Resultado:** ✅ Tesoureiro agora tem acesso a ambas igrejas!

---

### Exemplo 2: Remover acesso de uma igreja

**Situação:**
- Tesoureiro tem acesso a 2 igrejas
- Precisa remover acesso a "Igreja Central"

**Solução:**
1. Login: admin@igreja.com
2. Menu: **👥 Usuários**
3. Selecione: tesoureiro@gmail.com
4. Clique: **✏️ Editar Usuário**
5. Aba: **✅ Igrejas com Acesso**
6. Clique: **🗑️ Remover** próximo a "Igreja Central"
7. Clique: **💾 Salvar Alterações**

**Resultado:** ✅ Tesoureiro agora tem acesso apenas a "Igreja Filial"!

---

### Exemplo 3: Novo usuário com múltiplas igrejas

**Situação:**
- Criar novo usuário "Gerente de Tesouraria"
- Deve ter acesso a TODAS as igrejas

**Solução:**

1. Login: admin@igreja.com
2. Menu: **👥 Usuários**
3. Aba: **📧 Convidar**
4. Preencha:
   - Email: `gerente@igreja.com`
   - Nome: `Gerente de Tesouraria`
   - Nível: `editor`
5. Clique: **📧 Enviar Convite**
6. **Agora** selecione o novo usuário e clique **✏️ Editar Usuário**
7. Aba: **➕ Adicionar Igreja**
8. Clique **➕ Adicionar** para CADA igreja desejada
9. Clique: **💾 Salvar Alterações**

**Resultado:** ✅ Novo usuário com acesso a todas as igrejas!

---

## 🔐 Permissões

### Quem pode gerenciar igrejas de usuários?

✅ **Admin** - Pode fazer tudo!
❌ **Editor** - Não pode acessar
❌ **Viewer** - Não pode acessar

---

## 📱 Na Tabela de Usuários

A coluna **"Acesso a"** mostra uma lista das igrejas que cada usuário tem acesso:

```
Email                    | Nome       | Acesso a                      | Nível   | Status
tesoureiro@gmail.com     | Tesoureiro | Igreja Central, Igreja Filial | editor  | ✅ Ativo
viewer@gmail.com         | Visualizador| Igreja Filial               | viewer  | ✅ Ativo
```

---

## 🎯 Casos de Uso

### Estrutura Típica de Igreja

```
👨‍💼 ADMIN (seu@email.com)
    └─ Acesso: Todas as igrejas
    └─ Pode: Criar usuários, gerir igrejas, ver tudo

📊 TESOUREIRO (tesoureiro@email.com)
    └─ Acesso: Igreja Central + Igreja Filial
    └─ Pode: Criar/editar transações

👁️ VISUALIZADOR (relatorio@email.com)
    └─ Acesso: Igreja Central
    └─ Pode: Ver dados (somente leitura)
```

### Estrutura com Múltiplos Distritos

```
🏛️ IGREJA CENTRAL
    ├─ Tesoureiro Central (acesso: Igreja Central)
    └─ Gerente Geral (acesso: TODAS)

🏛️ IGREJA FILIAL
    ├─ Tesoureiro Filial (acesso: Igreja Filial)
    └─ Gerente Geral (acesso: TODAS)

👨‍💼 SUPER ADMIN (seu@email.com)
    └─ Acesso: TODAS as igrejas
```

---

## ❓ Dúvidas Frequentes

### P: Um usuário pode ter acesso a múltiplas igrejas?
**R:** Sim! Adicione acesso a quantas igrejas quiser na aba **➕ Adicionar Igreja**

---

### P: O que acontece se remover acesso a uma igreja?
**R:** O usuário não poderá mais:
- Ver dados dessa igreja
- Criar transações lá
- Acessar o dashboard dela
- Ainda pode acessar suas outras igrejas normalmente

---

### P: Um usuário novo já tem acesso automático?
**R:** Não. Você precisa:
1. Convidar o usuário (aba **📧 Convidar**)
2. Depois editar e adicionar as igrejas que ele pode acessar

---

### P: Posso mudar o nível de acesso ao mesmo tempo?
**R:** Sim! Enquanto está editando, você pode:
- Mudar nome
- Mudar email
- Mudar nível (admin/editor/viewer)
- **Gerenciar igrejas**
- Ativar/Desativar

Tudo ao mesmo tempo! Basta clicar **💾 Salvar Alterações** uma única vez.

---

### P: E se houver apenas 1 igreja?
**R:** A aba **➕ Adicionar Igreja** aparecerá assim:

```
✅ Usuário já tem acesso a todas as igrejas!
```

Você só pode remover nesse caso.

---

## 🔄 Fluxo Visual Completo

```
ADMIN ACESSA O SISTEMA
        ↓
    Menu → 👥 Usuários
        ↓
    Aba: 👤 Usuários
        ↓
    📊 Tabela mostra "Acesso a" para cada usuário
        ↓
    Seleciona usuário
        ↓
    Clica: ✏️ Editar Usuário
        ↓
    Abre interface com:
    ┌─────────────────────────────────────┐
    │ 📝 Editar Usuário e Igrejas         │
    ├─────────────────────────────────────┤
    │ Nome: ____________                  │
    │ Email: ___________                  │
    │ Nível: [Editor    ▼]                │
    │ ☐ Usuário Ativo                     │
    ├─────────────────────────────────────┤
    │ 🏛️ Gerenciar Igrejas                │
    │ ┌─────────────────────────────────┐ │
    │ │ ✅ Com Acesso  │ ➕ Adicionar  │ │
    │ └─────────────────────────────────┘ │
    ├─────────────────────────────────────┤
    │ [💾 Salvar] [❌ Cancelar]           │
    └─────────────────────────────────────┘
        ↓
    Admin gerencia igrejas
        ↓
    Clica: 💾 Salvar Alterações
        ↓
    ✅ Usuário atualizado com sucesso!
```

---

## 🛡️ Segurança

- ✅ Apenas **Admin** pode gerenciar igrejas
- ✅ Cada usuário vê apenas suas igrejas
- ✅ Dados de igrejas diferentes **nunca** se misturam
- ✅ Log de auditoria registra todas as mudanças

---

## 📞 Suporte

Se tiver dúvidas:
1. Leia **COMECE_NOVO_SISTEMA.txt** para contexto geral
2. Consulte **GERENCIAR_IGREJAS_USUARIOS.md** (este arquivo)
3. Contate o administrador

---

**Desenvolvido para facilitar a gestão multi-igreja! 🙏**
