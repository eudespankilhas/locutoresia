# Configuração de Notificações por Email - Gmail SMTP

## Guia Passo a Passo para Configurar o Gmail

### 1. Habilitar Verificação em Duas Etapas
1. Acesse sua conta Google
2. Vá para: https://myaccount.google.com/security
3. Ative "Verificação em duas etapas" (2FA)
4. É obrigatório para usar App Passwords

### 2. Gerar App Password
1. Após ativar 2FA, vá para: https://myaccount.google.com/apppasswords
2. Selecione:
   - **App**: "Outro (nome personalizado)"
   - **Nome**: "News Auto Post"
3. Clique em "GERAR"
4. **Copie a senha gerada** (só aparece uma vez!)

### 3. Configurar Variáveis de Ambiente

#### Método 1: Arquivo .env (Recomendado)
Crie um arquivo `.env` na pasta do projeto:

```env
# Configuração Gmail SMTP
GMAIL_EMAIL=seuemail@gmail.com
GMAIL_APP_PASSWORD=sua_senha_gerada
RECIPIENT_EMAIL=email@destinatario.com  # Opcional, usa GMAIL_EMAIL se não definido
```

#### Método 2: Variáveis de Ambiente no Sistema
```bash
# Windows (PowerShell)
$env:GMAIL_EMAIL="seuemail@gmail.com"
$env:GMAIL_APP_PASSWORD="sua_senha_gerada"
$env:RECIPIENT_EMAIL="email@destinatario.com"

# Linux/Mac
export GMAIL_EMAIL="seuemail@gmail.com"
export GMAIL_APP_PASSWORD="sua_senha_gerada"
export RECIPIENT_EMAIL="email@destinatario.com"
```

#### Método 3: Vercel Environment Variables
1. Acesse: https://vercel.com/eudespankilhas-2/locutoresia-2nq8/settings/environment-variables
2. Adicione as variáveis:
   - `GMAIL_EMAIL`: seuemail@gmail.com
   - `GMAIL_APP_PASSWORD`: sua_senha_gerada
   - `RECIPIENT_EMAIL`: email@destinatario.com

### 4. Testar a Configuração

#### Via API
```bash
curl -X POST https://locutoresia-2nq8.vercel.app/api/notifications/test
```

#### Via Dashboard
1. Acesse: https://locutoresia-2nq8.vercel.app
2. Use o endpoint de teste de notificações

#### Verificar Status
```bash
curl -X GET https://locutoresia-2nq8.vercel.app/api/notifications/status
```

## Tipos de Notificações

### 1. Publicação Bem-Sucedida 
- **Assunto**: "News Auto Post - Publicação Realizada com Sucesso! "
- **Conteúdo**: Título, fonte, hashtags, preview do conteúdo
- **Template**: HTML profissional com cores verde

### 2. Erro Detectado
- **Assunto**: "News Auto Post - Erro Detectado!"
- **Conteúdo**: Mensagem de erro, contexto, timestamp
- **Template**: HTML com cores vermelhas de alerta

### 3. Relatório Diário
- **Assunto**: "News Auto Post - Relatório Diário - DD/MM/YYYY"
- **Conteúdo**: Estatísticas do dia, taxa de sucesso, fonte mais usada
- **Template**: HTML com cores azuis informativas

## Segurança

### Práticas Recomendadas:
- **Nunca** compartilhe sua App Password
- **Use** emails dedicados para automação
- **Monitore** atividades suspeitas na sua conta Google
- **Revogue** App Passwords quando não usar mais

### Revogar App Password:
1. Vá para: https://myaccount.google.com/apppasswords
2. Encontre "News Auto Post" na lista
3. Clique em "Revogar"

## Troubleshooting

### Erros Comuns:

#### "Email não configurado"
- Verifique se as variáveis de ambiente estão definidas
- Confirme se a App Password foi gerada corretamente

#### "Authentication failed"
- Verifique se 2FA está ativada
- Confirme se está usando App Password (não senha normal)
- Verifique se o email está correto

#### "SMTP error"
- Verifique conexão com internet
- Confirme se o Gmail não está bloqueando o acesso
- Tente gerar nova App Password

### Logs de Debug:
O sistema imprime logs no console que podem ajudar a diagnosticar problemas:
```
Email enviado: News Auto Post - Publicação Realizada com Sucesso! 
Erro ao enviar email: Authentication failed
```

## Configuração Avançada

### Alterar Servidor SMTP:
Edite `backend/email_notifications.py`:
```python
self.smtp_server = "smtp.gmail.com"  # Padrão Gmail
self.smtp_port = 587                  # Padrão Gmail
```

### Personalizar Templates:
Modifique os templates HTML/Texto em `email_notifications.py`:
- `send_publication_success()`
- `send_error_notification()`
- `send_daily_report()`

## Teste Completo

### 1. Verificar Configuração:
```bash
curl -X GET https://locutoresia-2nq8.vercel.app/api/notifications/status
```

### 2. Enviar Email de Teste:
```bash
curl -X POST https://locutoresia-2nq8.vercel.app/api/notifications/test
```

### 3. Publicar Notícia de Teste:
```bash
curl -X POST https://locutoresia-2nq8.vercel.app/api/newpost/publish \
  -H "Content-Type: application/json" \
  -d '{"content":"Teste de notificação","hashtags":["test"]}'
```

## Suporte

Se precisar de ajuda:
1. Verifique os logs do sistema
2. Confirme a configuração do Gmail
3. Teste com diferentes emails
4. Consulte a documentação do Gmail SMTP

---

**Pronto! Após configurar, você receberá notificações automáticas sempre que:** 
- Uma notícia for publicada com sucesso
- Ocorrer um erro no sistema
- Relatórios diários (se implementados)
