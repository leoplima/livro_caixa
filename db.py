import sqlite3
import json
from datetime import datetime
from config import DATABASE_PATH

class Database:
    def __init__(self):
        self.db_path = DATABASE_PATH
        self.init_db()
    
    def get_connection(self):
        """Retorna uma conexão com o banco de dados"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Inicializa o banco de dados com as tabelas necessárias"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabela de Igrejas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS igrejas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL,
                cnpj TEXT,
                endereco TEXT,
                telefone TEXT,
                email TEXT,
                logo_path TEXT,
                marca_agua_path TEXT,
                cor_primaria TEXT DEFAULT '#7C3AED',
                ativa BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP
            )
        ''')
        
        # Tabela de Usuários
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                senha_hash TEXT NOT NULL,
                access_level TEXT DEFAULT 'viewer',
                ativo BOOLEAN DEFAULT 1,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultimo_acesso TIMESTAMP,
                igreja_padrao INTEGER,
                FOREIGN KEY (igreja_padrao) REFERENCES igrejas(id)
            )
        ''')
        
        # Tabela de Acesso de Usuários a Igrejas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuario_igrejas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                igreja_id INTEGER NOT NULL,
                access_level TEXT DEFAULT 'viewer',
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (igreja_id) REFERENCES igrejas(id),
                UNIQUE(usuario_id, igreja_id)
            )
        ''')
        
        # Tabela de Transações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data DATE NOT NULL,
                descricao TEXT NOT NULL,
                tipo TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                usuario_id INTEGER NOT NULL,
                igreja_id INTEGER NOT NULL,
                notas TEXT,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                data_atualizacao TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (igreja_id) REFERENCES igrejas(id)
            )
        ''')
        
        # Tabela de Logs de Auditoria
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                igreja_id INTEGER,
                acao TEXT NOT NULL,
                descricao TEXT,
                tabela_alvo TEXT,
                id_alvo INTEGER,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
                FOREIGN KEY (igreja_id) REFERENCES igrejas(id)
            )
        ''')
        
        # Tabela de Configurações
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chave TEXT UNIQUE NOT NULL,
                valor TEXT NOT NULL,
                data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # ===== FUNÇÕES DE IGREJAS =====
    def criar_igreja(self, nome, cnpj='', endereco='', telefone='', email='', cor_primaria='#7C3AED'):
        """Cria uma nova igreja"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO igrejas (nome, cnpj, endereco, telefone, email, cor_primaria)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, cnpj, endereco, telefone, email, cor_primaria))
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_igreja(self, igreja_id):
        """Busca uma igreja por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM igrejas WHERE id = ? AND ativa = 1', (igreja_id,))
        igreja = cursor.fetchone()
        conn.close()
        return dict(igreja) if igreja else None
    
    def listar_igrejas(self):
        """Lista todas as igrejas ativas"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, nome, cnpj, endereco, telefone, email FROM igrejas WHERE ativa = 1 ORDER BY nome')
        igrejas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return igrejas
    
    def get_igrejas_usuario(self, user_id):
        """Busca todas as igrejas que um usuário tem acesso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.* FROM igrejas i
            JOIN usuario_igrejas ui ON i.id = ui.igreja_id
            WHERE ui.usuario_id = ? AND i.ativa = 1
            ORDER BY i.nome
        ''', (user_id,))
        igrejas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return igrejas
    
    def adicionar_usuario_igreja(self, usuario_id, igreja_id, access_level='viewer'):
        """Adiciona um usuário a uma igreja"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuario_igrejas (usuario_id, igreja_id, access_level)
                VALUES (?, ?, ?)
            ''', (usuario_id, igreja_id, access_level))
            
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def remover_usuario_igreja(self, usuario_id, igreja_id):
        """Remove o acesso de um usuário a uma igreja"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                DELETE FROM usuario_igrejas
                WHERE usuario_id = ? AND igreja_id = ?
            ''', (usuario_id, igreja_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao remover usuário da igreja: {e}")
            return False
        finally:
            conn.close()
    
    def get_igrejas_usuario_nao_tem_acesso(self, user_id):
        """Busca igrejas que o usuário NÃO tem acesso"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.* FROM igrejas i
            WHERE i.ativa = 1 AND i.id NOT IN (
                SELECT igreja_id FROM usuario_igrejas WHERE usuario_id = ?
            )
            ORDER BY i.nome
        ''', (user_id,))
        igrejas = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return igrejas
    
    def atualizar_Igreja(self, igreja_id, **kwargs):
        """Atualiza dados da igreja"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        campos = ['data_atualizacao = CURRENT_TIMESTAMP']
        valores = []
        for chave, valor in kwargs.items():
            campos.append(f'{chave} = ?')
            valores.append(valor)
        
        valores.append(igreja_id)
        sql = f'UPDATE igrejas SET {", ".join(campos)} WHERE id = ?'
        
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()
    
    def deletar_igreja(self, igreja_id):
        """Deleta uma igreja e seus dados relacionados"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Deletar relações de usuários e igrejas
            cursor.execute('DELETE FROM usuario_igrejas WHERE igreja_id = ?', (igreja_id,))
            
            # Deletar transações da igreja
            cursor.execute('DELETE FROM transacoes WHERE igreja_id = ?', (igreja_id,))
            
            # Deletar auditoria da igreja
            cursor.execute('DELETE FROM auditoria WHERE igreja_id = ?', (igreja_id,))
            
            # Deletar a igreja
            cursor.execute('DELETE FROM igrejas WHERE id = ?', (igreja_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Erro ao deletar igreja: {e}")
            return False
    
    def get_Igreja(self, igreja_id):
        """Obtém dados de uma Igreja específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM igrejas WHERE id = ?', (igreja_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'nome': result[1],
                'cnpj': result[2],
                'endereco': result[3],
                'telefone': result[4],
                'email': result[5],
                'logo_path': result[6],
                'marca_agua_path': result[7],
                'cor_primaria': result[8],
                'ativa': result[9],
                'data_criacao': result[10],
                'data_atualizacao': result[11]
            }
        return None
    
    
    # ===== FUNÇÕES DE USUÁRIOS (MODIFICADAS) =====
    def criar_usuario(self, email, nome, senha_hash, access_level='viewer'):
        """Cria um novo usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO usuarios (email, nome, senha_hash, access_level)
                VALUES (?, ?, ?, ?)
            ''', (email, nome, senha_hash, access_level))
            
            conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            return None
        finally:
            conn.close()
    
    def get_usuario_por_email(self, email):
        """Busca usuário por email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        conn.close()
        return dict(usuario) if usuario else None
    
    def get_usuario_por_id(self, user_id):
        """Busca usuário por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
        usuario = cursor.fetchone()
        conn.close()
        return dict(usuario) if usuario else None
    
    def listar_usuarios(self, igreja_id=None):
        """Lista todos os usuários ou apenas de uma igreja específica"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if igreja_id:
            cursor.execute('''
                SELECT DISTINCT u.id, u.email, u.nome, u.access_level, u.ativo, 
                       u.data_criacao, ui.access_level as igreja_access_level
                FROM usuarios u
                JOIN usuario_igrejas ui ON u.id = ui.usuario_id
                WHERE ui.igreja_id = ?
                ORDER BY u.data_criacao DESC
            ''', (igreja_id,))
        else:
            cursor.execute('SELECT id, email, nome, access_level, ativo, data_criacao FROM usuarios ORDER BY data_criacao DESC')
        
        usuarios = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return usuarios
    
    def atualizar_usuario(self, user_id, **kwargs):
        """Atualiza dados do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        campos = []
        valores = []
        for chave, valor in kwargs.items():
            campos.append(f'{chave} = ?')
            valores.append(valor)
        
        valores.append(user_id)
        sql = f'UPDATE usuarios SET {", ".join(campos)} WHERE id = ?'
        
        cursor.execute(sql, valores)
        conn.commit()
        conn.close()
    
    def deletar_usuario(self, user_id):
        """Deleta um usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    def registrar_ultimo_acesso(self, user_id):
        """Registra o último acesso do usuário"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE usuarios SET ultimo_acesso = CURRENT_TIMESTAMP WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
    
    # ===== FUNÇÕES DE TRANSAÇÕES =====
    def criar_transacao(self, data, descricao, tipo, valor, categoria, usuario_id, igreja_id, notas=''):
        """Cria uma nova transação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transacoes (data, descricao, tipo, valor, categoria, usuario_id, igreja_id, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (data, descricao, tipo, valor, categoria, usuario_id, igreja_id, notas))
        
        conn.commit()
        transacao_id = cursor.lastrowid
        
        # Registrar auditoria
        self.registrar_auditoria(usuario_id, 'CREATE', 'Transação criada', 'transacoes', transacao_id, igreja_id)
        
        conn.close()
        return transacao_id
    
    def listar_transacoes(self, igreja_id, filtro_tipo=None, filtro_categoria=None, data_inicio=None, data_fim=None):
        """Lista transações de uma igreja com filtros opcionais"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        sql = 'SELECT * FROM transacoes WHERE igreja_id = ?'
        params = [igreja_id]
        
        if filtro_tipo:
            sql += ' AND tipo = ?'
            params.append(filtro_tipo)
        
        if filtro_categoria:
            sql += ' AND categoria = ?'
            params.append(filtro_categoria)
        
        if data_inicio:
            sql += ' AND data >= ?'
            params.append(data_inicio)
        
        if data_fim:
            sql += ' AND data <= ?'
            params.append(data_fim)
        
        sql += ' ORDER BY data DESC'
        
        cursor.execute(sql, params)
        transacoes = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return transacoes
    
    def get_transacao(self, transacao_id):
        """Busca uma transação por ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM transacoes WHERE id = ?', (transacao_id,))
        transacao = cursor.fetchone()
        conn.close()
        return dict(transacao) if transacao else None
    
    def atualizar_transacao(self, transacao_id, usuario_id, igreja_id, **kwargs):
        """Atualiza uma transação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        campos = ['data_atualizacao = CURRENT_TIMESTAMP']
        valores = []
        
        for chave, valor in kwargs.items():
            campos.append(f'{chave} = ?')
            valores.append(valor)
        
        valores.append(transacao_id)
        sql = f'UPDATE transacoes SET {", ".join(campos)} WHERE id = ?'
        
        cursor.execute(sql, valores)
        conn.commit()
        
        # Registrar auditoria
        self.registrar_auditoria(usuario_id, 'UPDATE', 'Transação atualizada', 'transacoes', transacao_id, igreja_id)
        
        conn.close()
    
    def deletar_transacao(self, transacao_id, usuario_id, igreja_id):
        """Deleta uma transação"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM transacoes WHERE id = ?', (transacao_id,))
        conn.commit()
        
        # Registrar auditoria
        self.registrar_auditoria(usuario_id, 'DELETE', 'Transação deletada', 'transacoes', transacao_id, igreja_id)
        
        conn.close()
    
    def get_resumo_financeiro(self, igreja_id):
        """Retorna resumo financeiro de uma igreja (receitas, despesas, saldo)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Total de receitas
        cursor.execute('SELECT COALESCE(SUM(valor), 0) as total FROM transacoes WHERE tipo = "receita" AND igreja_id = ?', (igreja_id,))
        total_receitas = cursor.fetchone()[0]
        
        # Total de despesas
        cursor.execute('SELECT COALESCE(SUM(valor), 0) as total FROM transacoes WHERE tipo = "despesa" AND igreja_id = ?', (igreja_id,))
        total_despesas = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'receitas': total_receitas,
            'despesas': total_despesas,
            'saldo': total_receitas - total_despesas
        }
    
    def get_transacoes_por_categoria(self, igreja_id, tipo):
        """Retorna distribuição de transações por categoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT categoria, SUM(valor) as total, COUNT(*) as quantidade
            FROM transacoes
            WHERE tipo = ? AND igreja_id = ?
            GROUP BY categoria
            ORDER BY total DESC
        ''', (tipo, igreja_id))
        
        resultado = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return resultado
    
    # ===== FUNÇÕES DE AUDITORIA =====
    def registrar_auditoria(self, usuario_id, acao, descricao, tabela_alvo, id_alvo, igreja_id=None):
        """Registra uma ação de auditoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO auditoria (usuario_id, acao, descricao, tabela_alvo, id_alvo, igreja_id)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (usuario_id, acao, descricao, tabela_alvo, id_alvo, igreja_id))
        
        conn.commit()
        conn.close()
    
    def listar_auditoria(self, limite=100):
        """Lista logs de auditoria"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, u.email, u.nome
            FROM auditoria a
            JOIN usuarios u ON a.usuario_id = u.id
            ORDER BY a.data_hora DESC
            LIMIT ?
        ''', (limite,))
        
        logs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return logs
    
    # ===== FUNÇÕES DE CONFIGURAÇÃO =====
    def get_config(self, chave):
        """Busca uma configuração"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM configuracoes WHERE chave = ?', (chave,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado else None
    
    def set_config(self, chave, valor):
        """Define uma configuração"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM configuracoes WHERE chave = ?', (chave,))
        existe = cursor.fetchone()
        
        if existe:
            cursor.execute('UPDATE configuracoes SET valor = ? WHERE chave = ?', (valor, chave))
        else:
            cursor.execute('INSERT INTO configuracoes (chave, valor) VALUES (?, ?)', (chave, valor))
        
        conn.commit()
        conn.close()
