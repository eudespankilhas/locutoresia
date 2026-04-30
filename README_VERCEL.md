# Deploy na Vercel - News Auto Post

## Visão Geral
Sistema completo de publicação automática de notícias pronto para deploy na Vercel com backend serverless e frontend estático.

## Estrutura do Projeto
```
/
|-- api/index.py              # Backend serverless para Vercel
|-- backend/                   # Arquivos de configuração
|   |-- newpost_config.py     # Configuração da NewPost-IA
|-- news_dashboard.html       # Frontend principal
|-- vercel.json              # Configuração do deploy
|-- package.json             # Dependências do projeto
|-- requirements.txt         # Dependências Python
```

## Funcionalidades
- **Busca automática de notícias** de RSS feeds (Exame, Veja, Folha, Diário do Nordeste)
- **Publicação automática** na NewPost-IA (https://plugpost-ai.lovable.app/)
- **Intervalo configurável** (30 minutos entre publicações)
- **Dashboard completo** com logs e estatísticas
- **Fallback local** se a NewPost-IA estiver indisponível

## Como Fazer Deploy

### 1. Pré-requisitos
- Conta na Vercel
- Git com o projeto clonado

### 2. Deploy Automático
```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer login
vercel login

# Deploy
vercel --prod
```

### 3. Deploy via GitHub
1. Conecte seu repositório ao Vercel
2. Configure as variáveis de ambiente (se necessário)
3. Faça deploy automático a cada push

## Configuração da NewPost-IA

O sistema está configurado para publicar em:
- **URL**: https://plugpost-ai.lovable.app/api/posts
- **Fallback**: Armazenamento local se falhar

Para alterar, edite `backend/newpost_config.py`:
```python
NEWPOST_CONFIG = {
    "url": "https://sua-newpost-ia.com",
    "api_endpoint": "/api/posts",
    "timeout": 30,
    "headers": {
        "Content-Type": "application/json",
        "User-Agent": "NewsAutoPost/1.0"
    }
}
```

## Endpoints da API

### Health Check
```
GET /api/health
```

### Buscar Notícias
```
POST /api/news/execute
Content-Type: application/json

{
  "enabled_sources": {
    "exame": true,
    "veja": true,
    "folha": true,
    "diario_nordeste": true
  }
}
```

### Publicar Notícia
```
POST /api/newpost/publish
Content-Type: application/json

{
  "content": "Título da notícia\n\nResumo completo...",
  "hashtags": ["tecnologia", "ia"]
}
```

### Listar Publicações
```
GET /api/publications
```

### Fontes de Notícias
```
GET /api/news/sources
```

## Variáveis de Ambiente

O sistema funciona sem variáveis de ambiente obrigatórias, mas você pode configurar:

- `FLASK_ENV`: production (automático na Vercel)
- `VERCEL`: 1 (automático na Vercel)

## Monitoramento

Após o deploy, acesse:
- **Dashboard**: `https://seu-projeto.vercel.app/`
- **API Health**: `https://seu-projeto.vercel.app/api/health`

## Logs e Debug

O sistema inclui logs detalhados que aparecem no dashboard:
- Busca de notícias
- Tentativas de publicação
- Sucessos e falhas
- Respostas da API

## Limitações Serverless

- **Duração máxima**: 30 segundos por requisição
- **Estado**: Mantido em memória (reseta entre deploys)
- **Concorrência**: Múltiplas requisições simultâneas suportadas

## Troubleshooting

### Erro 404 na API
- Verifique se `vercel.json` está configurado corretamente
- Confirme se `api/index.py` existe

### Erro de CORS
- O sistema já inclui headers CORS
- Verifique se o frontend usa `window.location.origin`

### Publicação Falha
- Verifique a configuração em `backend/newpost_config.py`
- Confirme se a NewPost-IA está acessível

## Performance

- **Cold Start**: ~1-2 segundos (primeira requisição)
- **Warm Requests**: <500ms
- **RSS Parsing**: ~2-3 segundos por feed
- **Publicação**: ~1-5 segundos

## Escalabilidade

A Vercel escala automaticamente:
- Até 1000 requisições simultâneas
- Global CDN
- Auto-scaling baseado em tráfego

## Segurança

- CORS configurado para aceitar qualquer origem
- Validação de JSON em todos os endpoints
- Timeout de 30 segundos para evitar longas execuções
- Sem senhas ou chaves sensíveis no código

## Manutenção

- **Logs**: Acompanhe os logs no dashboard da Vercel
- **Updates**: Faça push para atualizar
- **Backup**: O estado é temporário (reseta no deploy)

## Suporte

Para problemas:
1. Verifique os logs na Vercel
2. Teste os endpoints individualmente
3. Confirme a configuração da NewPost-IA
4. Verifique os RSS feeds estão acessíveis
