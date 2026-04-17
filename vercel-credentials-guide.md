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

### 5. Supabase (OBRIGATÓRIO para publicação de notícias)
```
SUPABASE_URL=https://ykswhzqdjoshjoaruhqs.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8
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

#### Variável 4: SUPABASE_URL
- **Name**: `SUPABASE_URL`
- **Value**: `https://ykswhzqdjoshjoaruhqs.supabase.co`
- **Environment**: Production, Preview, Development
- Clique em "Save"

#### Variável 5: SUPABASE_ANON_KEY
- **Name**: `SUPABASE_ANON_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo`
- **Environment**: Production, Preview, Development
- Clique em "Save"

#### Variável 6: SUPABASE_SERVICE_KEY (Opcional)
- **Name**: `SUPABASE_SERVICE_KEY`
- **Value**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8`
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

### Supabase (Projeto já criado)
- URL: https://supabase.com/dashboard
- Projeto: `ykswhzqdjoshjoaruhqs`
- URL do projeto: `https://ykswhzqdjoshjoaruhqs.supabase.co`
- As chaves já estão configuradas no projeto

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
SUPABASE_URL=https://ykswhzqdjoshjoaruhqs.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE2MTA4MjYsImV4cCI6MjA4NzE4NjgyNn0.yzezm6VZ5U_O7Txaj8B4_TD0PFVSpjZspYcZ1CYD0jo
```

**OPCIONAL:**
```
ELEVENLABS_API_KEY=sua_chave_elevenlabs_aqui
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inlrc3doenFkam9zaGpvYXJ1aHFzIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3MTYxMDgyNiwiZXhwIjoyMDg3MTg2ODI2fQ.jnVoRruRPlMpcskHU0ofEdH5hEY8_5tvT89HT6lKWK8
```

Configure no dashboard Vercel e aguarde o redeploy automático!
