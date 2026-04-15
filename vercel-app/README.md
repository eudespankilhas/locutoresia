# LMNT Voice Cloner - Web App

Aplicação web completa para clonagem e síntese de vozes usando a API oficial LMNT, pronta para deploy na Vercel.

## Funcionalidades

- **Síntese de Voz**: Gere áudio a partir de texto usando 44+ vozes disponíveis
- **Clonagem de Voz**: Crie vozes personalizadas a partir de arquivos de áudio
- **Gerenciamento**: Liste, visualize e gerencie suas vozes
- **Interface Moderna**: UI responsiva com Tailwind CSS
- **Download de Áudio**: Baixe os áudios gerados em MP3/WAV

## Estrutura do Projeto

```
vercel-app/
|-- api/
|   |-- lmnt.py              # API Backend (Serverless Function)
|-- index.html               # Frontend HTML
|-- app.js                   # Frontend JavaScript
|-- package.json             # Dependências
|-- vercel.json              # Configuração Vercel
|-- README.md                # Este arquivo
```

## Como Usar

### 1. Testar Localmente

```bash
# Entrar na pasta do projeto
cd vercel-app

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

Acesse `http://localhost:3000` para testar.

### 2. Deploy na Vercel

#### Opção A: Via CLI (Recomendado)

```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer login
vercel login

# Deploy
vercel --prod
```

#### Opção B: Via Dashboard Vercel

1. Conecte seu repositório Git ao Vercel
2. Importe o projeto da pasta `vercel-app`
3. Configure as variáveis de ambiente
4. Clique em "Deploy"

## Configuração de Variáveis de Ambiente

No Vercel Dashboard ou via CLI:

```bash
# Configurar API Key do LMNT
vercel env add lmnt-api-key

# Ou no dashboard:
# LMNT_API_KEY = ak_AbZv3CzqvsHjHxRFj4oL9h
```

## API Endpoints

### GET `/api/lmnt/health`
Verifica conexão com API LMNT

### GET `/api/lmnt/voices`
Lista todas as vozes disponíveis

### GET `/api/lmnt/voice/{id}`
Obtém informações de uma voz específica

### GET `/api/lmnt/account`
Obtém informações da conta

### POST `/api/lmnt/generate`
Gera áudio a partir de texto

```json
{
  "voice_id": "amy",
  "text": "Olá mundo!",
  "format": "mp3"
}
```

### POST `/api/lmnt/clone`
Cria uma nova voz clonada

```json
{
  "name": "Minha Voz",
  "audio_base64": "base64_audio_data",
  "description": "Descrição opcional",
  "enhance": true
}
```

## Funcionalidades do Frontend

### 1. Geração de Áudio
- Selecione uma voz disponível
- Digite o texto para sintetizar
- Escolha o formato (MP3/WAV)
- Gere e baixe o áudio

### 2. Clonagem de Voz
- Nomeie sua voz personalizada
- Faça upload de um arquivo de áudio
- Adicione descrição opcional
- Clone e use imediatamente

### 3. Gerenciamento
- Visualize informações da conta
- Liste todas as vozes disponíveis
- Veja detalhes de cada voz
- Selecione vozes para uso rápido

## Tecnologias Utilizadas

- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **UI Framework**: Tailwind CSS
- **Backend**: Python Serverless Functions
- **API**: LMNT Official SDK
- **Deployment**: Vercel
- **Icons**: Font Awesome

## Limitações

- **Plano Free**: 15.000 caracteres por mês
- **Formatos Suportados**: MP3, WAV
- **Tamanho Máximo**: 1MB para arquivos de clonagem
- **Duração Máxima**: 30 segundos por requisição

## Troubleshooting

### Erro de Conexão
- Verifique se `LMNT_API_KEY` está configurada
- Confirme se a API Key é válida

### Erro de Geração
- Verifique o limite de caracteres da conta
- Confirme se o texto não está vazio

### Erro de Clonagem
- Verifique o formato do arquivo de áudio (WAV/MP3)
- Confirme o tamanho do arquivo (< 1MB)

## Exemplos de Uso

### Gerar Áudio via API

```javascript
const response = await fetch('/api/lmnt/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    voice_id: 'amy',
    text: 'Olá! Este é um teste.',
    format: 'mp3'
  })
});

const data = await response.json();
// data.audio_base64 contém o áudio em base64
```

### Clonar Voz via API

```javascript
const audioBase64 = "base64_audio_data_here";

const response = await fetch('/api/lmnt/clone', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'Voz Teste',
    audio_base64: audioBase64,
    description: 'Voz de teste',
    enhance: true
  })
});

const voice = await response.json();
// voice.id contém o ID da nova voz
```

## Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

MIT License - Veja o arquivo LICENSE para detalhes.

## Suporte

- **Documentação LMNT**: https://docs.lmnt.com
- **Console LMNT**: https://console.lmnt.com
- **Suporte Vercel**: https://vercel.com/docs
