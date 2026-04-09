# 🚀 Guia de Deploy no Vercel

## Passo a Passo

### 1. Preparação do Projeto

Certifique-se de que todos os arquivos estão prontos:

```bash
# Liste os arquivos principais
ls -la
```

Arquivos necessários:
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `requirements.txt` - Dependências Python
- ✅ `backend/app.py` - Aplicação Flask
- ✅ `.gitignore` - Arquivos ignorados pelo Git

### 2. Criar Repositório no GitHub

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **New Repository** (+)
3. Nome do repositório: `locutores-ia`
4. Descrição: "Plataforma de geração de locuções com IA"
5. Selecione **Public** ou **Private**
6. **Não** inicialize com README (já temos um)
7. Clique em **Create repository**

### 3. Enviar Código para GitHub

```bash
# Inicializar Git (se não estiver inicializado)
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "🎉 Initial commit - Locutores IA v1.0"

# Adicionar remote origin
git remote add origin https://github.com/SEU_USUARIO/locutores-ia.git

# Enviar para o GitHub
git push -u origin main
```

### 4. Deploy no Vercel

#### Opção A: Via Dashboard (Recomendado)

1. Acesse [vercel.com](https://vercel.com) e faça login com GitHub
2. Clique em **Add New Project**
3. Selecione o repositório `locutores-ia`
4. Clique em **Import**
5. Configure:
   - **Framework Preset**: `Other`
   - **Root Directory**: `./`
   - **Build Command**: Deixe em branco
   - **Output Directory**: Deixe em branco
6. Clique em **Environment Variables** e adicione:
   - `GEMINI_API_KEY` = `sua_chave_api_aqui`
7. Clique em **Deploy**

#### Opção B: Via CLI

```bash
# Instalar Vercel CLI globalmente
npm i -g vercel

# Fazer login
vercel login

# Deploy
vercel

# Deploy em produção
vercel --prod
```

### 5. Configurar Variáveis de Ambiente no Vercel

Após o deploy, configure a API Key:

1. No Dashboard do Vercel, selecione o projeto
2. Vá em **Settings** > **Environment Variables**
3. Adicione:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: `sua_chave_api_google_gemini`
4. Clique em **Save**
5. Faça **Redeploy** para aplicar as mudanças

### 6. Testar a Aplicação

1. Acesse a URL fornecida pelo Vercel (ex: `https://locutores-ia.vercel.app`)
2. Teste a geração de áudio
3. Verifique a MiniDAW
4. Confirme o download de áudios

## 🛠️ Solução de Problemas

### Erro: "GEMINI_API_KEY not found"

- Verifique se a variável foi adicionada corretamente no Vercel
- Faça redeploy após adicionar a variável
- Certifique-se de que a chave é válida no Google AI Studio

### Erro: "Module not found"

- Verifique se `requirements.txt` está no root do projeto
- Confirme se todas as dependências estão listadas
- Tente adicionar `vercel.json` com a configuração correta

### Erro: "Build failed"

- Verifique os logs no Vercel Dashboard
- Confirme que `backend/app.py` está no caminho correto
- Certifique-se de que não há imports quebrados

## 📋 Checklist Pré-Deploy

- [ ] Criar conta no GitHub
- [ ] Criar repositório no GitHub
- [ ] Inicializar Git localmente (`git init`)
- [ ] Criar arquivo `.gitignore`
- [ ] Criar arquivo `vercel.json`
- [ ] Verificar `requirements.txt`
- [ ] Obter API Key do Google Gemini
- [ ] Commit inicial com todos os arquivos
- [ ] Push para GitHub
- [ ] Criar conta no Vercel
- [ ] Importar projeto do GitHub no Vercel
- [ ] Configurar `GEMINI_API_KEY` no Vercel
- [ ] Fazer deploy
- [ ] Testar aplicação

## 🔄 Atualizações

Para atualizar o projeto após alterações:

```bash
# Commit das mudanças
git add .
git commit -m "Descrição das mudanças"

# Push para GitHub
git push origin main

# O Vercel faz deploy automático (se conectado ao GitHub)
```

## 📞 Suporte

- [Documentação Vercel](https://vercel.com/docs)
- [Documentação Flask](https://flask.palletsprojects.com/)
- [Google AI Studio](https://makersuite.google.com/app/apikey)

---

🎉 **Parabéns!** Seu Locutores IA está no ar!
