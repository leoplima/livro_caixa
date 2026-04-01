import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from db import Database
from auth import Auth
from config import COLORS, CATEGORIAS_RECEITA, CATEGORIAS_DESPESA, ACCESS_LEVELS

# Configuração da página
st.set_page_config(
    page_title="Livro Caixa - Igreja",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para tema escuro
st.markdown(f"""
    <style>
        :root {{
            --primary-color: {COLORS['primary']};
            --text-color: {COLORS['text']};
            --background-color: {COLORS['background']};
        }}
        
        .stApp {{
            background-color: {COLORS['background']};
            color: {COLORS['text']};
        }}
        
        .main {{
            background-color: {COLORS['background']};
        }}
        
        .stMetric {{
            background-color: {COLORS['surface']};
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
        }}
        
        .stButton > button {{
            background-color: {COLORS['primary']};
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            background-color: {COLORS['secondary']};
        }}
        
        .success-box {{
            background-color: rgba(16, 185, 129, 0.2);
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid {COLORS['success']};
            margin-bottom: 15px;
        }}
        
        .error-box {{
            background-color: rgba(239, 68, 68, 0.2);
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid {COLORS['danger']};
            margin-bottom: 15px;
        }}
        
        .warning-box {{
            background-color: rgba(245, 158, 11, 0.2);
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid {COLORS['warning']};
            margin-bottom: 15px;
        }}
        
        .card {{
            background-color: {COLORS['surface']};
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .header {{
            color: {COLORS['primary']};
            border-bottom: 2px solid {COLORS['primary']};
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_id = None

if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'

# Instâncias
db = Database()
auth = Auth()

# ===== FUNÇÕES AUXILIARES =====
def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.user_id = None
    st.session_state.page = 'dashboard'
    st.rerun()

def has_permission(permissao):
    """Verifica se o usuário tem a permissão"""
    if not st.session_state.logged_in:
        return False
    
    access_level = st.session_state.user['access_level']
    return permissao in ACCESS_LEVELS[access_level]['permissoes']

def formato_moeda(valor):
    """Formata valor como moeda"""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

# ===== TELA DE LOGIN =====
def tela_login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("https://via.placeholder.com/300?text=Igreja+Caixa", use_column_width=True)
        st.markdown("<h1 style='text-align: center; color: #6366F1;'>Livro Caixa da Igreja</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94A3B8;'>Sistema de Gestão Financeira</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Primeiro Acesso"])
        
        # TAB LOGIN
        with tab1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            email = st.text_input("📧 Email", key="login_email")
            senha = st.text_input("🔑 Senha", type="password", key="login_senha")
            
            if st.button("Entrar", use_container_width=True):
                if not email or not senha:
                    st.error("Preencha todos os campos!")
                else:
                    sucesso, usuario, mensagem = auth.autenticar(email, senha)
                    if sucesso:
                        st.session_state.logged_in = True
                        st.session_state.user = usuario
                        st.session_state.user_id = usuario['id']
                        st.success(mensagem)
                        st.rerun()
                    else:
                        st.error(f"❌ {mensagem}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # TAB PRIMEIRO ACESSO
        with tab2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.info("Se você foi convidado, use o email de convite para acessar")
            st.markdown("</div>", unsafe_allow_html=True)

# ===== TELA DO DASHBOARD =====
def tela_dashboard():
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"### 👤 {st.session_state.user['nome']}")
    with col2:
        if st.button("Sair", key="btn_logout"):
            logout()
    
    st.divider()
    st.markdown("<h2 style='color: #6366F1;'>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        data_inicio = st.date_input("Data Inicial", datetime.now() - timedelta(days=30))
    with col2:
        data_fim = st.date_input("Data Final", datetime.now())
    with col3:
        st.write("")  # Espaçamento
    
    # Obter dados
    transacoes = db.listar_transacoes(
        data_inicio=data_inicio.strftime('%Y-%m-%d'),
        data_fim=data_fim.strftime('%Y-%m-%d')
    )
    
    resumo = db.get_resumo_financeiro()
    
    # Métricas principais
    st.markdown("<h3 style='color: #6366F1;'>Resumo Financeiro</h3>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "💰 Receitas",
            formato_moeda(resumo['receitas']),
            delta="+R$ 500,00",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "💸 Despesas",
            formato_moeda(resumo['despesas']),
            delta="+R$ 200,00",
            delta_color="inverse"
        )
    
    with col3:
        cor = "green" if resumo['saldo'] >= 0 else "red"
        st.metric(
            "📈 Saldo Total",
            formato_moeda(resumo['saldo']),
            delta=formato_moeda(resumo['saldo']),
            delta_color="normal"
        )
    
    # Gráficos
    st.divider()
    col1, col2 = st.columns(2)
    
    # Gráfico: Receitas por Categoria
    with col1:
        st.markdown("<h3 style='color: #6366F1;'>Receitas por Categoria</h3>", unsafe_allow_html=True)
        receitas_cat = db.get_transacoes_por_categoria('receita')
        if receitas_cat:
            df_receitas = pd.DataFrame(receitas_cat)
            fig = px.pie(
                df_receitas,
                values='total',
                names='categoria',
                color_discrete_sequence=[COLORS['primary'], COLORS['secondary'], COLORS['success'], COLORS['warning'], COLORS['info'], COLORS['danger']],
                hole=0
            )
            fig.update_layout(
                font=dict(color=COLORS['text']),
                paper_bgcolor=COLORS['surface'],
                plot_bgcolor=COLORS['background'],
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de receita")
    
    # Gráfico: Despesas por Categoria
    with col2:
        st.markdown("<h3 style='color: #6366F1;'>Despesas por Categoria</h3>", unsafe_allow_html=True)
        despesas_cat = db.get_transacoes_por_categoria('despesa')
        if despesas_cat:
            df_despesas = pd.DataFrame(despesas_cat)
            fig = px.pie(
                df_despesas,
                values='total',
                names='categoria',
                color_discrete_sequence=[COLORS['danger'], COLORS['warning'], COLORS['info'], COLORS['success'], COLORS['primary'], COLORS['secondary']],
                hole=0
            )
            fig.update_layout(
                font=dict(color=COLORS['text']),
                paper_bgcolor=COLORS['surface'],
                plot_bgcolor=COLORS['background'],
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Sem dados de despesa")
    
    # Gráfico: Evolução Temporal
    if transacoes:
        st.markdown("<h3 style='color: #6366F1;'>Evolução do Saldo</h3>", unsafe_allow_html=True)
        df = pd.DataFrame(transacoes)
        df['data'] = pd.to_datetime(df['data'])
        df = df.sort_values('data')
        
        # Calcular saldo acumulado
        df['valor_liquido'] = df.apply(lambda x: x['valor'] if x['tipo'] == 'receita' else -x['valor'], axis=1)
        df['saldo_acumulado'] = df['valor_liquido'].cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['data'],
            y=df['saldo_acumulado'],
            mode='lines+markers',
            name='Saldo',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=8, color=COLORS['secondary']),
            fill='tozeroy',
            fillcolor=f'rgba(99, 102, 241, 0.2)'
        ))
        
        fig.update_layout(
            title='Evolução do Saldo Acumulado',
            font=dict(color=COLORS['text']),
            paper_bgcolor=COLORS['surface'],
            plot_bgcolor=COLORS['background'],
            xaxis_title='Data',
            yaxis_title='Saldo (R$)',
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)

# ===== TELA DE TRANSAÇÕES =====
def tela_transacoes():
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"### 👤 {st.session_state.user['nome']}")
    with col2:
        if st.button("Sair", key="btn_logout_trans"):
            logout()
    
    st.divider()
    st.markdown("<h2 style='color: #6366F1;'>💳 Transações</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Ver Transações", "Nova Transação"])
    
    # TAB: VER TRANSAÇÕES
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_tipo = st.selectbox("Tipo", ["Todos", "receita", "despesa"], key="filtro_tipo")
        with col2:
            filtro_categoria = st.selectbox("Categoria", ["Todas"] + CATEGORIAS_RECEITA + CATEGORIAS_DESPESA, key="filtro_categoria")
        with col3:
            st.write("")
        
        transacoes = db.listar_transacoes(
            filtro_tipo=None if filtro_tipo == "Todos" else filtro_tipo,
            filtro_categoria=None if filtro_categoria == "Todas" else filtro_categoria
        )
        
        if transacoes:
            df = pd.DataFrame(transacoes)
            
            # Customizar exibição
            df_exibicao = df[['data', 'descricao', 'tipo', 'valor', 'categoria', 'notas']].copy()
            df_exibicao['valor'] = df_exibicao['valor'].apply(formato_moeda)
            df_exibicao['tipo'] = df_exibicao['tipo'].str.replace('receita', '📥 Receita').str.replace('despesa', '📤 Despesa')
            
            st.dataframe(df_exibicao, use_container_width=True)
            
            # Opções de edição/deleção se houver permissão
            if has_permission('edit') or has_permission('delete'):
                st.divider()
                st.markdown("<h3 style='color: #6366F1;'>Gerenciar Transações</h3>", unsafe_allow_html=True)
                
                transacao_id = st.selectbox(
                    "Selecione uma transação para editar/deletar",
                    options=[t['id'] for t in transacoes],
                    format_func=lambda x: f"{[t for t in transacoes if t['id'] == x][0]['data']} - {[t for t in transacoes if t['id'] == x][0]['descricao']}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    if has_permission('edit') and st.button("✏️ Editar", use_container_width=True):
                        st.session_state.editing_id = transacao_id
                        st.rerun()
                
                with col2:
                    if has_permission('delete') and st.button("🗑️ Deletar", use_container_width=True, help="Deletar esta transação"):
                        db.deletar_transacao(transacao_id, st.session_state.user_id)
                        st.success("Transação deletada com sucesso!")
                        st.rerun()
        else:
            st.info("Nenhuma transação encontrada")
    
    # TAB: NOVA TRANSAÇÃO
    with tab2:
        if not has_permission('edit'):
            st.error("Você não tem permissão para criar transações")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            
            with col1:
                tipo = st.radio("Tipo de Transação", ["receita", "despesa"], format_func=lambda x: "📥 Receita" if x == "receita" else "📤 Despesa")
            
            with col2:
                data = st.date_input("Data", datetime.now())
            
            descricao = st.text_input("Descrição")
            
            col1, col2 = st.columns(2)
            with col1:
                valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
            
            with col2:
                categorias = CATEGORIAS_RECEITA if tipo == "receita" else CATEGORIAS_DESPESA
                categoria = st.selectbox("Categoria", categorias)
            
            notas = st.text_area("Notas (opcional)")
            
            if st.button("💾 Salvar Transação", use_container_width=True):
                if not descricao or valor <= 0:
                    st.error("Preencha todos os campos obrigatórios")
                else:
                    db.criar_transacao(
                        data=data.strftime('%Y-%m-%d'),
                        descricao=descricao,
                        tipo=tipo,
                        valor=valor,
                        categoria=categoria,
                        usuario_id=st.session_state.user_id,
                        notas=notas
                    )
                    st.success("Transação criada com sucesso!")
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

# ===== TELA DE USUÁRIOS (ADMIN) =====
def tela_usuarios():
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"### 👤 {st.session_state.user['nome']}")
    with col2:
        if st.button("Sair", key="btn_logout_users"):
            logout()
    
    st.divider()
    
    if not has_permission('manage_users'):
        st.error("❌ Você não tem permissão para acessar esta página")
        return
    
    st.markdown("<h2 style='color: #6366F1;'>👥 Gerenciar Usuários</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Usuários", "Convidar Novo"])
    
    # TAB: LISTAR USUÁRIOS
    with tab1:
        usuarios = db.listar_usuarios()
        
        if usuarios:
            df = pd.DataFrame(usuarios)
            st.dataframe(df[['email', 'nome', 'access_level', 'ativo', 'data_criacao']], use_container_width=True)
            
            st.divider()
            st.markdown("<h3 style='color: #6366F1;'>Ações de Admin</h3>", unsafe_allow_html=True)
            
            usuario_id = st.selectbox(
                "Selecione um usuário",
                options=[u['id'] for u in usuarios],
                format_func=lambda x: f"{[u for u in usuarios if u['id'] == x][0]['email']} - {[u for u in usuarios if u['id'] == x][0]['nome']}"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔐 Resetar Senha"):
                    sucesso, mensagem = auth.redefinir_senha(usuario_id, st.session_state.user_id)
                    if sucesso:
                        st.success(mensagem)
                    else:
                        st.error(mensagem)
            
            with col2:
                novo_nivel = st.selectbox("Novo Nível", list(ACCESS_LEVELS.keys()))
                if st.button("📊 Alterar Nível"):
                    db.atualizar_usuario(usuario_id, access_level=novo_nivel)
                    st.success(f"Nível alterado para {novo_nivel}")
            
            with col3:
                if st.button("❌ Desativar Usuário"):
                    db.atualizar_usuario(usuario_id, ativo=0)
                    st.success("Usuário desativado")
        else:
            st.info("Nenhum usuário cadastrado")
    
    # TAB: CONVIDAR NOVO
    with tab2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        email = st.text_input("Email do novo usuário")
        nome = st.text_input("Nome completo")
        access_level = st.selectbox("Nível de Acesso", list(ACCESS_LEVELS.keys()), format_func=lambda x: ACCESS_LEVELS[x]['nome'])
        
        if st.button("📧 Enviar Convite", use_container_width=True):
            if not email or not nome:
                st.error("Preencha todos os campos")
            else:
                sucesso, mensagem = auth.convidar_usuario(email, nome, access_level)
                if sucesso:
                    st.success(mensagem)
                else:
                    st.error(mensagem)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ===== TELA DE PERFIL =====
def tela_perfil():
    # Header
    col1, col2 = st.columns([1, 5])
    with col1:
        st.markdown(f"### 👤 {st.session_state.user['nome']}")
    with col2:
        if st.button("Sair", key="btn_logout_perfil"):
            logout()
    
    st.divider()
    st.markdown("<h2 style='color: #6366F1;'>⚙️ Meu Perfil</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Informações Pessoais**")
        st.info(f"**Email:** {st.session_state.user['email']}")
        st.info(f"**Nome:** {st.session_state.user['nome']}")
        st.info(f"**Nível de Acesso:** {ACCESS_LEVELS[st.session_state.user['access_level']]['nome']}")
        st.info(f"**Membro desde:** {st.session_state.user['data_criacao']}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("**Alterar Senha**")
        
        senha_atual = st.text_input("Senha Atual", type="password")
        senha_nova = st.text_input("Nova Senha", type="password")
        senha_confirma = st.text_input("Confirmar Senha", type="password")
        
        if st.button("🔐 Alterar Senha", use_container_width=True):
            if not senha_atual or not senha_nova:
                st.error("Preencha todos os campos")
            elif senha_nova != senha_confirma:
                st.error("As senhas não correspondem")
            else:
                sucesso, mensagem = auth.alterar_senha(st.session_state.user_id, senha_atual, senha_nova)
                if sucesso:
                    st.success(mensagem)
                else:
                    st.error(mensagem)
        
        st.markdown("</div>", unsafe_allow_html=True)

# ===== MENU PRINCIPAL =====
def main():
    if not st.session_state.logged_in:
        tela_login()
    else:
        # Sidebar
        with st.sidebar:
            st.markdown(f"## 🏦 Livro Caixa")
            st.markdown(f"Bem-vindo, **{st.session_state.user['nome']}**!")
            st.divider()
            
            st.markdown("**Navegação**")
            
            if st.button("📊 Dashboard", use_container_width=True):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            if st.button("💳 Transações", use_container_width=True):
                st.session_state.page = 'transacoes'
                st.rerun()
            
            if st.button("⚙️ Meu Perfil", use_container_width=True):
                st.session_state.page = 'perfil'
                st.rerun()
            
            if has_permission('manage_users'):
                if st.button("👥 Usuários", use_container_width=True):
                    st.session_state.page = 'usuarios'
                    st.rerun()
            
            st.divider()
            st.markdown(f"**Nível:** {ACCESS_LEVELS[st.session_state.user['access_level']]['nome']}")
        
        # Conteúdo Principal
        if st.session_state.page == 'dashboard':
            tela_dashboard()
        elif st.session_state.page == 'transacoes':
            tela_transacoes()
        elif st.session_state.page == 'usuarios':
            tela_usuarios()
        elif st.session_state.page == 'perfil':
            tela_perfil()

if __name__ == "__main__":
    main()
