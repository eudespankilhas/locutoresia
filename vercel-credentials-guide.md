# Guia de Configuração de Credenciais na Vercel

## Credenciais Necessárias para o Locutores IA

### 1. LMNT API Key (OBRIGATÓRIO para clonagem de vozes)
```
LMNT_API_KEY=ak_AbZv3CzqvsHjHxRFj4oL9h
```

### 2. Google Gemini API Key (OBRIGATÓRIO para TTS principal)
```
GEMINI_API_KEY=sua_chave_gemini_aqui
```

### 3. Google AI Studio API Key (OBRIGATÓRIO para geração de vozes)
```
GOOGLE_AI_STUDIO_API_KEY=sua_chave_google_ai_studio_aqui
```

### 4. ElevenLabs API Key (OPCIONAL - clonagem alternativa)
```
ELEVENLABS_API_KEY=sua_chave_elevenlabs_aqui
```

## Como Configurar na Vercel

### Passo 1: Acessar Dashboard
1. Vá para: https://vercel.com/dashboard
2. Selecione o projeto "locutores-ia"
3. Clique em "Settings" (ícone de engrenagem)

### Passo 2: Environment Variables
1. No menu lateral, clique em "Environment Variables"
2. Clique em "Add New" para cada variável

### Passo 3: Adicionar as Credenciais

#### Variável 1: LMNT_API_KEY
- **Name**: `LMNT_API_KEY`
- **Value**: `ak_AbZv3CzqvsHjHxRFj4oL9h`
- **Environment**: Production, Preview, Development
- Clique em "Save"

#### Variável 2: GEMINI_API_KEY
- **Name**: `GEMINI_API_KEY`
- **Value**: `sua_chave_gemini_aqui`
- **Environment**: Production, Preview, Development
- Clique em "Save"

#### Variável 3: GOOGLE_AI_STUDIO_API_KEY
- **Name**: `GOOGLE_AI_STUDIO_API_KEY`
- **Value**: `sua_chave_google_ai_studio_aqui`
- **Environment**: Production, Preview, Development
- Clique em "Save"

### Passo 4: Redeploy Automático
Após salvar as variáveis, o Vercel fará redeploy automático.

## Onde Obter as Chaves

### LMNT API Key
- URL: https://console.lmnt.com
- Login e copiar a API Key do dashboard
- Já temos: `ak_AbZv3CzqvsHjHxRFj4oL9h`

### Google Gemini API Key
- URL: https://makersuite.google.com/app/apikey
- Criar nova chave ou usar existente
- Copiar a chave

### Google AI Studio API Key
- URL: https://aistudio.google.com/app/apikey
- Criar nova chave para geração de vozes
- Copiar a chave

### ElevenLabs API Key (Opcional)
- URL: https://elevenlabs.io/app/settings/api-keys
- Criar conta e gerar API Key
- Copiar a chave

## Teste Após Configuração

Após o redeploy, teste os endpoints:

```bash
# Testar status LMNT
curl https://locutores-ia.vercel.app/api/lmnt/status

# Testar lista de vozes
curl https://locutores-ia.vercel.app/api/lmnt/voices

# Testar página principal
curl https://locutores-ia.vercel.app/
```

## Problemas Comuns

### 1. Endpoints retornando 404
- **Causa**: Variáveis de ambiente não configuradas
- **Solução**: Verifique se todas as variáveis foram salvas corretamente

### 2. Erro de API Key inválida
- **Causa**: API Key incorreta ou expirada
- **Solução**: Verifique as chaves no dashboard de cada serviço

### 3. Deploy não atualiza
- **Causa**: Cache do Vercel
- **Solução**: Force novo deploy ou aguarde 5 minutos

## Resumo Rápido

**MÍNIMO NECESSÁRIO:**
```
LMNT_API_KEY=ak_AbZv3CzqvsHjHxRFj4oL9h
GEMINI_API_KEY=sua_chave_gemini_aqui
GOOGLE_AI_STUDIO_API_KEY=sua_chave_google_ai_studio_aqui
```

**OPCIONAL:**
```
ELEVENLABS_API_KEY=sua_chave_elevenlabs_aqui
```

Configure no dashboard Vercel e aguarde o redeploy automático!
