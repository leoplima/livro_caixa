"""
Script de Inicialização - Nova Versão (Multi-Igreja)
Cria igrejas padrão e usuários com acesso apropriado
"""

from db import Database
from auth import Auth
from datetime import datetime

def init_system():
    """Inicializa o sistema com igrejas e usuários"""
    
    db = Database()
    auth = Auth()
    
    print("=" * 60)
    print("🏦 INICIALIZANDO LIVRO CAIXA DA IGREJA (MULTI-TENANCY)")
    print("=" * 60)
    
    # ===== CRIAR IGREJAS =====
    print("\n🏛️ Criando igrejas...")
    
    igrejas_dados = [
        {
            'nome': 'Igreja Central',
            'cnpj': '12.345.678/0001-90',
            'endereco': 'Rua Principal, 100',
            'telefone': '(11) 9999-9999',
            'email': 'central@igreja.com'
        },
        {
            'nome': 'Igreja Filial',
            'cnpj': '12.345.678/0001-91',
            'endereco': 'Avenida Secundária, 200',
            'telefone': '(11) 8888-8888',
            'email': 'filial@igreja.com'
        }
    ]
    
    igrejas_ids = {}
    for dados in igrejas_dados:
        igreja_id = db.criar_igreja(**dados)
        if igreja_id:
            igrejas_ids[dados['nome']] = igreja_id
            print(f"  ✅ {dados['nome']} (ID: {igreja_id})")
        else:
            print(f"  ⚠️  {dados['nome']} já existe")
            igrejas = db.listar_igrejas()
            for ig in igrejas:
                if ig['nome'] == dados['nome']:
                    igrejas_ids[dados['nome']] = ig['id']
    
    # ===== CRIAR USUÁRIOS =====
    print("\n👥 Criando usuários...")
    
    usuarios_dados = [
        {'email': 'admin@igreja.com', 'nome': 'Administrador', 'senha': 'Admin123456', 'level': 'admin'},
        {'email': 'tesoureiro@gmail.com', 'nome': 'Tesoureiro', 'senha': 'Tesoureiro123', 'level': 'editor'},
        {'email': 'viewer@gmail.com', 'nome': 'Visualizador', 'senha': 'Viewer123', 'level': 'viewer'},
    ]
    
    usuarios_ids = {}
    for dados in usuarios_dados:
        sucesso, msg = auth.registrar_usuario(dados['email'], dados['nome'], dados['senha'])
        if sucesso:
            usuario = db.get_usuario_por_email(dados['email'])
            usuarios_ids[dados['email']] = usuario['id']
            db.atualizar_usuario(usuario['id'], access_level=dados['level'])
            print(f"  ✅ {dados['nome']} ({dados['email']})")
            print(f"     Nível: {dados['level']}")
        else:
            print(f"  ⚠️  {dados['email']} já existe")
            usuário = db.get_usuario_por_email(dados['email'])
            usuarios_ids[dados['email']] = usuário['id']
    
    # ===== ASSOCIAR USUÁRIOS ÀS IGREJAS =====
    print("\n🔗 Associando usuários às igrejas...")
    
    # Admin: acesso a todas as igrejas
    for church_id in igrejas_ids.values():
        db.adicionar_usuario_igreja(usuarios_ids['admin@igreja.com'], church_id, 'admin')
    print(f"  ✅ Admin: Acesso a todas as igrejas")
    
    # Tesoureiro: acesso à Igreja Central
    if 'Igreja Central' in igrejas_ids:
        db.adicionar_usuario_igreja(usuarios_ids['tesoureiro@gmail.com'], igrejas_ids['Igreja Central'], 'editor')
        print(f"  ✅ Tesoureiro: Acesso à Igreja Central")
    
    # Visualizador: acesso à Igreja Filial
    if 'Igreja Filial' in igrejas_ids:
        db.adicionar_usuario_igreja(usuarios_ids['viewer@gmail.com'], igrejas_ids['Igreja Filial'], 'viewer')
        print(f"  ✅ Visualizador: Acesso à Igreja Filial")
    
    # ===== CRIAR TRANSAÇÕES DE EXEMPLO =====
    print("\n📊 Criando transações de exemplo...")
    
    if igrejas_ids:
        primeira_igreja = list(igrejas_ids.values())[0]
        admin_id = usuarios_ids['admin@igreja.com']
        
        transacoes_exemplo = [
            ('2024-03-20', 'Dízimo - Semana 1', 'receita', 5000, 'Dízimos'),
            ('2024-03-21', 'Aluguel do Templo', 'despesa', 3000, 'Aluguel'),
            ('2024-03-22', 'Oferta - Domingo', 'receita', 2500, 'Ofertas'),
            ('2024-03-23', 'Contas - Água e Luz', 'despesa', 800, 'Utilitários (água, luz, gás)'),
            ('2024-03-24', 'Dízimo - Semana 2', 'receita', 5500, 'Dízimos'),
        ]
        
        for data, desc, tipo, valor, cat in transacoes_exemplo:
            db.criar_transacao(
                data=data,
                descricao=desc,
                tipo=tipo,
                valor=valor,
                categoria=cat,
                usuario_id=admin_id,
                igreja_id=primeira_igreja,
                notas='Transação de exemplo'
            )
        
        print(f"  ✅ {len(transacoes_exemplo)} transações criadas")
    
    # ===== RESUMO =====
    print("\n" + "=" * 60)
    print("✨ SISTEMA INICIALIZADO COM SUCESSO!")
    print("=" * 60)
    
    print("\n📋 IGREJAS CRIADAS:")
    for nome, church_id in igrejas_ids.items():
        print(f"  • {nome} (ID: {church_id})")
    
    print("\n👥 USUÁRIOS CRIADOS:")
    print(f"  • admin@igreja.com / Admin123456 → Nível: ADMIN")
    print(f"  • tesoureiro@gmail.com / Tesoureiro123 → Nível: EDITOR")
    print(f"  • viewer@gmail.com / Viewer123 → Nível: VIEWER")
    
    print("\n📜 PERMISSÕES:")
    print("  • Admin: Acesso a TODAS as igrejas + Gerenciar usuários")
    print("  • Tesoureiro: Acesso a Igreja Central + Criar transações")
    print("  • Visualizador: Acesso a Igreja Filial (somente leitura)")
    
    print("\n" + "=" * 60)
    print("🚀 PRÓXIMAS ETAPAS:")
    print("=" * 60)
    print("  1. Renomear app_new.py para app.py")
    print("  2. Executar: streamlit run app.py")
    print("  3. Acessar: http://localhost:8501")
    print("  4. Fazer login com qualquer credencial acima")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    init_system()
