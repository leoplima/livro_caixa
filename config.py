# Configurações da Aplicação

# Tema de cores moderno e vibrante
COLORS = {
    "primary": "#7C3AED",        # Roxo vibrante
    "secondary": "#06B6D4",      # Ciano
    "danger": "#EF4444",         # Vermelho vibrante
    "warning": "#F59E0B",        # Laranja vibrante
    "success": "#10B981",        # Verde esmeralda
    "info": "#0EA5E9",           # Azul celeste
    "gradient_1": "#7C3AED",     # Graduação 1
    "gradient_2": "#06B6D4",     # Graduação 2
    "background": "#0F172A",     # Azul muito escuro
    "surface": "#1E293B",        # Cinza escuro
    "surface_light": "#334155",  # Cinza mais claro
    "text": "#F1F5F9",           # Branco quebrado
    "text_secondary": "#94A3B8", # Cinza claro
    "accent": "#FF006E",         # Magenta/Pink
}

# Configurações do banco de dados
DATABASE_PATH = "livro_caixa.db"

# Configurações de segurança
HASH_ALGORITHM = "sha256"
SECRET_KEY = "sua_chave_secreta_muito_segura_aqui_123456"

# Configurações de email (para notificações)
# Usando secrets do Streamlit para credenciais seguras
import streamlit as st

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Carrega credenciais dos secrets (local: .streamlit/secrets.toml, cloud: configuração web)
try:
    SENDER_EMAIL = st.secrets.get("SENDER_EMAIL", "seu_email@gmail.com")
    SENDER_PASSWORD = st.secrets.get("SENDER_PASSWORD", "sua_senha_de_app")
except:
    SENDER_EMAIL = "seu_email@gmail.com"
    SENDER_PASSWORD = "sua_senha_de_app"

# Categorias de receita padrão
CATEGORIAS_RECEITA = [
    "Dízimos",
    "Ofertas",
    "Eventos",
    "Doações",
    "Aluguel de Espaços",
    "Outras Receitas"
]

# Categorias de despesa padrão
CATEGORIAS_DESPESA = [
    "Salários e Encargos",
    "Aluguel",
    "Utilitários (água, luz, gás)",
    "Manutenção",
    "Materiais",
    "Comunicação",
    "Transporte",
    "Outras Despesas"
]

# Níveis de acesso
ACCESS_LEVELS = {
    "viewer": {"nome": "Visualizador", "permissoes": ["view"]},
    "editor": {"nome": "Editor", "permissoes": ["view", "edit"]},
    "admin": {"nome": "Administrador", "permissoes": ["view", "edit", "delete", "manage_users"]}
}
