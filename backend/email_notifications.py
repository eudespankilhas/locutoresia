# Sistema de Notificações por Email - Gmail SMTP
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
from jinja2 import Template
import json

class EmailNotifier:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_EMAIL", "")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD", "")
        self.recipient_email = os.getenv("RECIPIENT_EMAIL", self.sender_email)
        
    def is_configured(self):
        """Verifica se as credenciais do Gmail estão configuradas"""
        return bool(self.sender_email and self.sender_password)
    
    def send_email(self, subject, body, html_body=None):
        """Envia email usando Gmail SMTP"""
        if not self.is_configured():
            print("Email não configurado. Defina GMAIL_EMAIL e GMAIL_APP_PASSWORD")
            return False
        
        try:
            # Criar mensagem
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = self.recipient_email
            
            # Adicionar corpo em texto plano
            text_part = MIMEText(body, "plain")
            message.attach(text_part)
            
            # Adicionar corpo em HTML se fornecido
            if html_body:
                html_part = MIMEText(html_body, "html")
                message.attach(html_part)
            
            # Criar contexto SSL e enviar
            context = ssl.create_default_context()
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, self.recipient_email, message.as_string())
            
            print(f"Email enviado: {subject}")
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def send_publication_success(self, publication_data):
        """Envia notificação de publicação bem-sucedida"""
        subject = "News Auto Post - Publicação Realizada com Sucesso! "
        
        # Template em texto plano
        text_template = """
News Auto Post - Publicação Realizada com Sucesso!

Detalhes da Publicação:
Título: {title}
Fonte: {source}
Publicado em: {published_to}
Data/Hora: {timestamp}
Hashtags: {hashtags}

Conteúdo:
{content}

---
News Auto Post System
https://locutoresia-2nq8.vercel.app
        """.format(
            title=publication_data.get('title', 'Sem título'),
            source=publication_data.get('source', 'Desconhecida'),
            published_to=publication_data.get('published_to', 'NewPost-IA'),
            timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            hashtags=', '.join(publication_data.get('hashtags', [])),
            content=publication_data.get('content', '')[:500] + '...' if len(publication_data.get('content', '')) > 500 else publication_data.get('content', '')
        )
        
        # Template em HTML
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>News Auto Post - Publicação Realizada</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #4CAF50; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .details { background: white; padding: 15px; border-left: 4px solid #4CAF50; margin: 10px 0; }
        .footer { text-align: center; padding: 20px; color: #666; }
        .success { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>News Auto Post - Publicação Realizada com Sucesso! </h1>
    </div>
    
    <div class="content">
        <div class="details">
            <h3>Detalhes da Publicação:</h3>
            <p><strong>Título:</strong> {title}</p>
            <p><strong>Fonte:</strong> {source}</p>
            <p><strong>Publicado em:</strong> {published_to}</p>
            <p><strong>Data/Hora:</strong> {timestamp}</p>
            <p><strong>Hashtags:</strong> {hashtags}</p>
        </div>
        
        <div class="details">
            <h3>Conteúdo:</h3>
            <p>{content}</p>
        </div>
        
        <div class="success">
            <p>Publicação realizada com sucesso na NewPost-IA!</p>
        </div>
    </div>
    
    <div class="footer">
        <p>News Auto Post System</p>
        <p><a href="https://locutoresia-2nq8.vercel.app">Acessar Dashboard</a></p>
    </div>
</body>
</html>
        """.format(
            title=publication_data.get('title', 'Sem título'),
            source=publication_data.get('source', 'Desconhecida'),
            published_to=publication_data.get('published_to', 'NewPost-IA'),
            timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            hashtags=', '.join(publication_data.get('hashtags', [])),
            content=publication_data.get('content', '')[:500] + '...' if len(publication_data.get('content', '')) > 500 else publication_data.get('content', '')
        )
        
        return self.send_email(subject, text_template, html_template)
    
    def send_error_notification(self, error_message, context=None):
        """Envia notificação de erro"""
        subject = "News Auto Post - Erro Detectado!"
        
        text_template = """
News Auto Post - Erro Detectado!

Erro: {error}
Contexto: {context}
Data/Hora: {timestamp}

Por favor, verifique o sistema para mais detalhes.

---
News Auto Post System
https://locutoresia-2nq8.vercel.app
        """.format(
            error=error_message,
            context=context or "N/A",
            timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )
        
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>News Auto Post - Erro Detectado</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #f44336; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .error { background: white; padding: 15px; border-left: 4px solid #f44336; margin: 10px 0; }
        .footer { text-align: center; padding: 20px; color: #666; }
        .error-text { color: #f44336; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>News Auto Post - Erro Detectado!</h1>
    </div>
    
    <div class="content">
        <div class="error">
            <h3>Detalhes do Erro:</h3>
            <p><strong>Erro:</strong> {error}</p>
            <p><strong>Contexto:</strong> {context}</p>
            <p><strong>Data/Hora:</strong> {timestamp}</p>
        </div>
        
        <div class="error-text">
            <p>Por favor, verifique o sistema para mais detalhes.</p>
        </div>
    </div>
    
    <div class="footer">
        <p>News Auto Post System</p>
        <p><a href="https://locutoresia-2nq8.vercel.app">Acessar Dashboard</a></p>
    </div>
</body>
</html>
        """.format(
            error=error_message,
            context=context or "N/A",
            timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        )
        
        return self.send_email(subject, text_template, html_template)
    
    def send_daily_report(self, stats):
        """Envia relatório diário"""
        subject = f"News Auto Post - Relatório Diário - {datetime.now().strftime('%d/%m/%Y')}"
        
        text_template = """
News Auto Post - Relatório Diário

Data: {date}
Total de Publicações: {total}
Publicações com Sucesso: {success}
Taxa de Sucesso: {success_rate}%
Fonte Mais Usada: {most_used_source}

Estatísticas Detalhadas:
{stats_details}

---
News Auto Post System
https://locutoresia-2nq8.vercel.app
        """.format(
            date=datetime.now().strftime('%d/%m/%Y'),
            total=stats.get('total_publications', 0),
            success=stats.get('success_count', 0),
            success_rate=round((stats.get('success_count', 0) / max(stats.get('total_publications', 1), 1)) * 100, 2),
            most_used_source=stats.get('most_used_source', 'N/A'),
            stats_details=json.dumps(stats, indent=2, ensure_ascii=False)
        )
        
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>News Auto Post - Relatório Diário</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #2196F3; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .stats { background: white; padding: 15px; border-left: 4px solid #2196F3; margin: 10px 0; }
        .footer { text-align: center; padding: 20px; color: #666; }
        .highlight { color: #2196F3; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>News Auto Post - Relatório Diário</h1>
        <p>{date}</p>
    </div>
    
    <div class="content">
        <div class="stats">
            <h3>Estatísticas do Dia:</h3>
            <p><strong>Total de Publicações:</strong> {total}</p>
            <p><strong>Publicações com Sucesso:</strong> {success}</p>
            <p><strong>Taxa de Sucesso:</strong> {success_rate}%</p>
            <p><strong>Fonte Mais Usada:</strong> {most_used_source}</p>
        </div>
        
        <div class="stats">
            <h3>Estatísticas Detalhadas:</h3>
            <pre>{stats_details}</pre>
        </div>
    </div>
    
    <div class="footer">
        <p>News Auto Post System</p>
        <p><a href="https://locutoresia-2nq8.vercel.app">Acessar Dashboard</a></p>
    </div>
</body>
</html>
        """.format(
            date=datetime.now().strftime('%d/%m/%Y'),
            total=stats.get('total_publications', 0),
            success=stats.get('success_count', 0),
            success_rate=round((stats.get('success_count', 0) / max(stats.get('total_publications', 1), 1)) * 100, 2),
            most_used_source=stats.get('most_used_source', 'N/A'),
            stats_details=json.dumps(stats, indent=2, ensure_ascii=False)
        )
        
        return self.send_email(subject, text_template, html_template)
    
    def send_test_email(self):
        """Envia email de teste"""
        subject = "News Auto Post - Teste de Notificações"
        
        text_template = """
News Auto Post - Teste de Notificações

Este é um email de teste para verificar se o sistema de notificações está funcionando corretamente.

Data/Hora do teste: {timestamp}

Se você recebeu este email, o sistema de notificações está configurado corretamente!

---
News Auto Post System
https://locutoresia-2nq8.vercel.app
        """.format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>News Auto Post - Teste de Notificações</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background: #FF9800; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9f9f9; }
        .test-info { background: white; padding: 15px; border-left: 4px solid #FF9800; margin: 10px 0; }
        .footer { text-align: center; padding: 20px; color: #666; }
        .success { color: #4CAF50; font-weight: bold; }
    </style>
</head>
<body>
    <div class="header">
        <h1>News Auto Post - Teste de Notificações</h1>
    </div>
    
    <div class="content">
        <div class="test-info">
            <h3>Informações do Teste:</h3>
            <p>Este é um email de teste para verificar se o sistema de notificações está funcionando corretamente.</p>
            <p><strong>Data/Hora do teste:</strong> {timestamp}</p>
        </div>
        
        <div class="success">
            <p>Se você recebeu este email, o sistema de notificações está configurado corretamente!</p>
        </div>
    </div>
    
    <div class="footer">
        <p>News Auto Post System</p>
        <p><a href="https://locutoresia-2nq8.vercel.app">Acessar Dashboard</a></p>
    </div>
</body>
</html>
        """.format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
        
        return self.send_email(subject, text_template, html_template)

# Instância global do notificador
email_notifier = EmailNotifier()
