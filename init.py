"""
Script de Inicialização do Sistema
Cria o usuário admin padrão e dados de exemplo
"""

from db import Database
from auth import Auth
from datetime import datetime, timedelta

def init_system():
    """Inicializa o sistema com dados de exemplo"""
    
    db = Database()
    auth = Auth()
    
    print("=" * 50)
    print("🏦 INICIALIZANDO LIVRO CAIXA DA IGREJA")
    print("=" * 50)
    
    # Verificar se já existe usuário admin
    admin = db.get_usuario_por_email("admin@igreja.com")
    
    if admin:
        print("\n✅ Usuário admin já existe!")
    else:
        print("\n📝 Criando usuário admin...")
        sucesso, mensagem = auth.registrar_usuario(
            email="admin@igreja.com",
            nome="Administrador",
            senha="Admin123456"
        )
        
        if sucesso:
            # Atualizar para nível admin
            db.atualizar_usuario(
                db.get_usuario_por_email("admin@igreja.com")['id'],
                access_level='admin'
            )
            print(f"✅ {mensagem}")
            print("   Email: admin@igreja.com")
            print("   Senha: Admin123456")
            print("   ⚠️  ALTERE ESTA SENHA NO PRIMEIRO ACESSO!")
        else:
            print(f"❌ {mensagem}")
            return
    
    # Criar dados de exemplo
    print("\n📊 Criando dados de exemplo...")
    
    admin_user = db.get_usuario_por_email("admin@igreja.com")
    admin_id = admin_user['id']
    
    exemplo_transacoes = [
        {
            'data': (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'),
            'descricao': 'Dízimo - Semana 1',
            'tipo': 'receita',
            'valor': 5000,
            'categoria': 'Dízimos',
            'notas': 'Arrecadação da semana'
        },
        {
            'data': (datetime.now() - timedelta(days=18)).strftime('%Y-%m-%d'),
            'descricao': 'Aluguel do Templo - Março',
            'tipo': 'despesa',
            'valor': 3000,
            'categoria': 'Aluguel',
            'notas': 'Aluguel mensal'
        },
        {
            'data': (datetime.now() - timedelta(days=16)).strftime('%Y-%m-%d'),
            'descricao': 'Oferta - Domingo',
            'tipo': 'receita',
            'valor': 2500,
            'categoria': 'Ofertas',
            'notas': 'Oferta do domingo'
        },
        {
            'data': (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'),
            'descricao': 'Contas - Água, Luz e Gás',
            'tipo': 'despesa',
            'valor': 1200,
            'categoria': 'Utilitários (água, luz, gás)',
            'notas': 'Contas do mês'
        },
        {
            'data': (datetime.now() - timedelta(days=12)).strftime('%Y-%m-%d'),
            'descricao': 'Dízimo - Semana 2',
            'tipo': 'receita',
            'valor': 5500,
            'categoria': 'Dízimos',
            'notas': 'Arrecadação da semana'
        },
        {
            'data': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
            'descricao': 'Manutenção - Reparo do Telhado',
            'tipo': 'despesa',
            'valor': 2000,
            'categoria': 'Manutenção',
            'notas': 'Reparo emergencial'
        },
        {
            'data': (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d'),
            'descricao': 'Evento - Festas Juninas',
            'tipo': 'receita',
            'valor': 3500,
            'categoria': 'Eventos',
            'notas': 'Arrecadação do evento'
        },
        {
            'data': (datetime.now() - timedelta(days=6)).strftime('%Y-%m-%d'),
            'descricao': 'Materiais - Limpeza e Higiene',
            'tipo': 'despesa',
            'valor': 400,
            'categoria': 'Materiais',
            'notas': 'Compra de materiais'
        },
        {
            'data': (datetime.now() - timedelta(days=4)).strftime('%Y-%m-%d'),
            'descricao': 'Dízimo - Semana 3',
            'tipo': 'receita',
            'valor': 6000,
            'categoria': 'Dízimos',
            'notas': 'Arrecadação da semana'
        },
        {
            'data': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
            'descricao': 'Doação - Membro Novo',
            'tipo': 'receita',
            'valor': 1000,
            'categoria': 'Doações',
            'notas': 'Doação de membro novo'
        },
    ]
    
    # Contar transações existentes
    transacoes_existentes = db.listar_transacoes()
    
    if len(transacoes_existentes) == 0:
        for t in exemplo_transacoes:
            db.criar_transacao(
                data=t['data'],
                descricao=t['descricao'],
                tipo=t['tipo'],
                valor=t['valor'],
                categoria=t['categoria'],
                usuario_id=admin_id,
                notas=t['notas']
            )
        print(f"✅ {len(exemplo_transacoes)} transações de exemplo criadas")
    else:
        print(f"✅ Sistema já possui {len(transacoes_existentes)} transações")
    
    # Resumo financeiro
    print("\n📈 RESUMO FINANCEIRO ATUAL")
    print("-" * 50)
    resumo = db.get_resumo_financeiro()
    print(f"Receitas Totais:  R$ {resumo['receitas']:>12,.2f}")
    print(f"Despesas Totais:  R$ {resumo['despesas']:>12,.2f}")
    print(f"Saldo:            R$ {resumo['saldo']:>12,.2f}")
    print("-" * 50)
    
    # Instruções finais
    print("\n" + "=" * 50)
    print("✨ SISTEMA INICIADO COM SUCESSO!")
    print("=" * 50)
    print("\n📋 Próximos Passos:")
    print("   1. Execute: streamlit run app.py")
    print("   2. Acesse: http://localhost:8501")
    print("   3. Login com:")
    print("      Email: admin@igreja.com")
    print("      Senha: Admin123456")
    print("\n⚠️  IMPORTANTE:")
    print("   - Altere a senha do admin no primeiro acesso")
    print("   - Configure os dados de email em config.py para enviar convites")
    print("   - Crie novos usuários através da aba de Usuários")
    print("\n" + "=" * 50)

if __name__ == "__main__":
    init_system()
