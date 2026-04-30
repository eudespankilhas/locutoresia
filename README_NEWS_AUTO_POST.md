# News Auto Post - NewPost-IA

Sistema automatizado de coleta e publicação de notícias brasileiras em tempo real.

## 🚀 Funcionalidades

- **Coleta Automatizada**: Busca notícias reais das principais fontes brasileiras
- **Publicação Inteligente**: Formata e publica automaticamente na NewPost-IA
- **Agendamento**: Executa a cada 1 hora automaticamente
- **Interface Web**: Painel de controle React para monitoramento
- **Fontes Configuráveis**: Exame, Veja, Folha, Diário do Nordeste

## 📋 Pré-requisitos

### Backend (Python)
- Python 3.8+
- pip
- Variáveis de ambiente configuradas

### Frontend (React)
- Node.js 16+
- npm ou yarn

## 🔧 Configuração

### 1. Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```env
SUPABASE_URL=sua_url_supabase
SUPABASE_SERVICE_ROLE_KEY=sua_chave_servico_supabase
```

### 2. Instalar Dependências do Backend

```bash
cd backend
pip install -r requirements.txt
```

### 3. Instalar Dependências do Frontend

```bash
# No diretório raiz do projeto React
npm install
# ou
yarn install
```

## 🚀 Executando o Sistema

### Backend

#### Opção 1: Script de Inicialização (Recomendado)
```bash
cd backend
python start_server.py
```

#### Opção 2: Direto via Flask
```bash
cd backend
python news_api_server.py
```

O servidor backend estará disponível em: `http://localhost:5000`

### Frontend

```bash
# No diretório do projeto React
npm start
# ou
yarn start
```

A interface estará disponível em: `http://localhost:3000`

## 📡 API Endpoints

### Controle da Automação
- `GET /api/news/status` - Status atual da automação
- `POST /api/news/start` - Iniciar automação
- `POST /api/news/stop` - Parar automação
- `POST /api/news/execute` - Executar ciclo manualmente

### Publicação
- `POST /api/newpost/publish` - Publicar conteúdo na NewPost-IA

### Utilitários
- `GET /api/news/sources` - Listar fontes disponíveis
- `POST /api/news/logs/clear` - Limpar logs
- `GET /api/health` - Health check

## 🗂️ Estrutura do Projeto

```
├── backend/
│   ├── news_agent.py              # Agente principal de coleta
│   ├── news_api_server.py         # Servidor Flask API
│   ├── news_utils.py              # Utilitários de processamento
│   ├── start_server.py            # Script de inicialização
│   └── requirements.txt           # Dependências Python
├── components/
│   └── newpost/
│       └── newpostApi.js          # Cliente API para frontend
└── [arquivos React existentes]
```

## 🔄 Fluxo de Funcionamento

1. **Coleta**: O sistema busca notícias dos sites configurados usando RSS feeds e web scraping
2. **Filtragem**: Apenas notícias do dia atual são consideradas
3. **Processamento**: IA formata o conteúdo em estilo jornalístico
4. **Validação**: Verifica duplicatas no banco de dados
5. **Publicação**: Publica automaticamente na NewPost-IA
6. **Agendamento**: Repete o processo a cada hora

## 📊 Fontes de Notícias

- **Exame** (📊): Tecnologia, Negócios, Economia
- **Veja** (📖): Economia, Política, Brasil
- **Folha de S.Paulo** (📰): Mercado, Cotidiano, Brasil
- **Diário do Nordeste** (🌵): Política, Economia, Brasil

## 🛠️ Customização

### Adicionar Nova Fonte

1. Adicione em `backend/news_agent.py`:
```python
"nova_fonte": {
    "domain": "site.com.br",
    "url": "https://site.com.br",
    "categories": ["categoria1", "categoria2"],
    "name": "Nome da Fonte"
}
```

2. Adicione RSS feed em `core/news_utils.py`:
```python
"nova_fonte": "https://site.com.br/feed/"
```

### Ajustar Intervalo

Modifique `INTERVAL_MS` no componente React:
```javascript
const INTERVAL_MS = 30 * 60 * 1000; // 30 minutos
```

## 🐛 Troubleshooting

### Backend não inicia
- Verifique se as variáveis de ambiente estão configuradas
- Instale as dependências: `pip install -r requirements.txt`
- Verifique se a porta 5000 está livre

### Frontend não conecta ao backend
- Confirme se o backend está rodando em `http://localhost:5000`
- Verifique CORS no backend (já configurado)
- Configure `REACT_APP_API_URL` se necessário

### Não publica notícias
- Verifique logs no painel web
- Confirme credenciais do Supabase
- Teste endpoints manualmente com curl/Postman

## 📝 Logs e Monitoramento

- **Logs em tempo real**: Painel web mostra últimas 50 execuções
- **Estatísticas**: Total de ciclos, sucessos, falhas
- **Health check**: `/api/health` para monitoramento

## 🔐 Segurança

- Use variáveis de ambiente para credenciais
- Configure CORS adequadamente em produção
- Limite rate dos endpoints em produção
- Valide dados de entrada

## 📈 Escalabilidade

- **Horizontal**: Multiple backend instances com load balancer
- **Vertical**: Increase memory/CPU para scraping intensivo
- **Database**: Use connection pooling para Supabase
- **Cache**: Redis para cache de notícias recentes

## 🤝 Contribuição

1. Fork o projeto
2. Crie branch para feature
3. Commit suas mudanças
4. Abra Pull Request

## 📄 Licença

MIT License - Ver arquivo LICENSE para detalhes
