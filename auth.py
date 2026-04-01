import hashlib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from db import Database
from config import HASH_ALGORITHM, SECRET_KEY, SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD

class Auth:
    def __init__(self):
        self.db = Database()
    
    @staticmethod
    def hash_senha(senha):
        """Cria hash da senha"""
        return hashlib.sha256((senha + SECRET_KEY).encode()).hexdigest()
    
    @staticmethod
    def validar_email(email):
        """Valida formato do email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validar_senha(senha):
        """Valida requisitos de senha"""
        if len(senha) < 8:
            return False, "Senha deve ter no mínimo 8 caracteres"
        
        if not any(c.isupper() for c in senha):
            return False, "Senha deve conter pelo menos uma letra maiúscula"
        
        if not any(c.isdigit() for c in senha):
            return False, "Senha deve conter pelo menos um número"
        
        return True, "Senha válida"
    
    def registrar_usuario(self, email, nome, senha):
        """Registra um novo usuário"""
        # Validar email
        if not self.validar_email(email):
            return False, "Email inválido"
        
        # Validar senha
        valido, mensagem = self.validar_senha(senha)
        if not valido:
            return False, mensagem
        
        # Verificar se email já existe
        if self.db.get_usuario_por_email(email):
            return False, "Email já cadastrado"
        
        # Criar usuário
        senha_hash = self.hash_senha(senha)
        usuario_id = self.db.criar_usuario(email, nome, senha_hash, 'viewer')
        
        if usuario_id:
            return True, f"Usuário criado com sucesso! ID: {usuario_id}"
        else:
            return False, "Erro ao criar usuário"
    
    def autenticar(self, email, senha):
        """Autentica um usuário"""
        usuario = self.db.get_usuario_por_email(email)
        
        if not usuario:
            return False, None, "Email não encontrado"
        
        if not usuario['ativo']:
            return False, None, "Usuário desativado"
        
        senha_hash = self.hash_senha(senha)
        
        if usuario['senha_hash'] != senha_hash:
            return False, None, "Senha incorreta"
        
        # Registrar último acesso
        self.db.registrar_ultimo_acesso(usuario['id'])
        
        return True, usuario, "Autenticado com sucesso"
    
    def convidar_usuario(self, email, nome, access_level='viewer', sender_email=None, sender_password=None):
        """
        Envia convite para novo usuário
        O usuário deve completar o registro com uma senha
        """
        # Validar email
        if not self.validar_email(email):
            return False, "Email inválido"
        
        # Verificar se email já existe
        if self.db.get_usuario_por_email(email):
            return False, "Email já cadastrado"
        
        # Criar usuario com senha padrão (a ser alterada no primeiro acesso)
        senha_padrao = "Temp123456"
        senha_hash = self.hash_senha(senha_padrao)
        usuario_id = self.db.criar_usuario(email, nome, senha_hash, access_level)
        
        if not usuario_id:
            return False, "Erro ao criar usuário"
        
        # Tentar enviar email
        try:
            if sender_email and sender_password:
                self.enviar_email_convite(email, nome, access_level, sender_email, sender_password)
                return True, "Convite enviado com sucesso para o email"
            else:
                return True, f"Usuário criado. Senha temporária: {senha_padrao} (mude na primeira inscrição)"
        except Exception as e:
            return True, f"Usuário criado mas erro ao enviar email: {str(e)}"
    
    def enviar_email_convite(self, email_destino, nome, access_level, sender_email, sender_password):
        """Envia email de convite"""
        try:
            assunto = "Convite - Livro Caixa da Igreja"
            
            corpo_html = f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; }}
                        .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 8px; }}
                        .header {{ color: #6366F1; padding-bottom: 20px; border-bottom: 2px solid #6366F1; }}
                        .content {{ padding: 20px 0; }}
                        .button {{ background-color: #6366F1; color: white; padding: 12px 30px; border-radius: 5px; text-decoration: none; display: inline-block; margin: 20px 0; }}
                        .footer {{ color: #666; font-size: 12px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #eee; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Bem-vindo ao Livro Caixa da Igreja</h1>
                        </div>
                        <div class="content">
                            <p>Olá {nome},</p>
                            <p>Você foi convidado para acessar o sistema de Livro Caixa da Igreja!</p>
                            <p><strong>Seu nível de acesso:</strong> {access_level}</p>
                            <p>Acesse o sistema e altere sua senha no primeiro acesso.</p>
                            <p>Email: <strong>{email_destino}</strong></p>
                            <p>Senha temporária: <strong>Temp123456</strong></p>
                        </div>
                        <div class="footer">
                            <p>Este é um email automático. Não responda este email.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            mensagem = MIMEMultipart("alternative")
            mensagem["Subject"] = assunto
            mensagem["From"] = sender_email
            mensagem["To"] = email_destino
            
            parte_html = MIMEText(corpo_html, "html")
            mensagem.attach(parte_html)
            
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_destino, mensagem.as_string())
            
            return True
        
        except Exception as e:
            print(f"Erro ao enviar email: {str(e)}")
            return False
    
    def alterar_senha(self, user_id, senha_atual, senha_nova):
        """Altera a senha do usuário"""
        usuario = self.db.get_usuario_por_id(user_id)
        
        if not usuario:
            return False, "Usuário não encontrado"
        
        # Verificar senha atual
        senha_atual_hash = self.hash_senha(senha_atual)
        if usuario['senha_hash'] != senha_atual_hash:
            return False, "Senha atual incorreta"
        
        # Validar nova senha
        valido, mensagem = self.validar_senha(senha_nova)
        if not valido:
            return False, mensagem
        
        # Atualizar senha
        senha_nova_hash = self.hash_senha(senha_nova)
        self.db.atualizar_usuario(user_id, senha_hash=senha_nova_hash)
        self.db.registrar_auditoria(user_id, 'SECURITY', 'Senha alterada', 'usuarios', user_id)
        
        return True, "Senha alterada com sucesso"
    
    def redefinir_senha(self, user_id, admin_id):
        """Redefine a senha do usuário (apenas admin)"""
        usuario = self.db.get_usuario_por_id(user_id)
        
        if not usuario:
            return False, "Usuário não encontrado"
        
        # Definir senha temporária
        senha_temporaria = "Temp123456"
        senha_hash = self.hash_senha(senha_temporaria)
        self.db.atualizar_usuario(user_id, senha_hash=senha_hash)
        self.db.registrar_auditoria(admin_id, 'SECURITY', f'Senha resetada para usuário {usuario["email"]}', 'usuarios', user_id)
        
        return True, f"Senha redefinida para: {senha_temporaria}"
