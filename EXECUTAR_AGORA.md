# 🚀 Execute Agora - GitHub + Vercel

## Opção 1: Script Automatizado (Recomendado)

Abra o **PowerShell** na pasta do projeto e execute:

```powershell
cd "d:\DOWLOADS PROGRAMAS 2025\Locutores IA"
.\setup-github.ps1
```

Siga as instruções interativas.

## Opção 2: Comandos Manuais

### Passo 1: Configurar Git

```bash
# Configure seu usuário
git config --global user.name "SEU_NOME"
git config --global user.email "seu.email@exemplo.com"
```

### Passo 2: Inicializar Repositório

```bash
# Na pasta do projeto
cd "d:\DOWLOADS PROGRAMAS 2025\Locutores IA"

# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "🎉 Initial commit - Locutores IA v1.0"
```

### Passo 3: Criar Repositório no GitHub

1. Acesse: https://github.com/new
2. **Repository name**: `locutores-ia`
3. **Description**: `Plataforma de geração de locuções com IA`
4. **Visibility**: Public (ou Private)
5. **NÃO** marque "Initialize this repository with a README"
6. Clique em **Create repository**

### Passo 4: Conectar e Enviar

```bash
# Substitua SEU_USUARIO pelo seu nome de usuário do GitHub
git remote add origin https://github.com/SEU_USUARIO/locutores-ia.git

# Enviar para o GitHub
git push -u origin main
```

### Passo 5: Deploy no Vercel

1. Acesse: https://vercel.com/new
2. Faça login com sua conta GitHub
3. Importe o repositório `locutores-ia`
4. Em **Environment Variables**, adicione:
   - Name: `GEMINI_API_KEY`
   - Value: `sua_chave_api_google_aqui`
5. Clique em **Deploy**

## ✅ Arquivos Criados

Os seguintes arquivos foram criados para o deploy:

- ✅ `vercel.json` - Configuração do Vercel
- ✅ `.gitignore` - Arquivos ignorados pelo Git
- ✅ `README_GITHUB.md` - README completo para GitHub
- ✅ `DEPLOY_VERCEL.md` - Guia detalhado de deploy
- ✅ `setup-github.ps1` - Script PowerShell automatizado
- ✅ `requirements.txt` - Atualizado com dependências

## 🔗 Links Importantes

- GitHub: https://github.com
- Vercel: https://vercel.com
- Google AI Studio: https://makersuite.google.com/app/apikey

## 📋 Checklist

- [ ] Configurar Git localmente
- [ ] Criar repositório no GitHub
- [ ] Enviar código para GitHub
- [ ] Obter API Key do Google Gemini
- [ ] Criar conta no Vercel
- [ ] Importar projeto no Vercel
- [ ] Configurar variável de ambiente `GEMINI_API_KEY`
- [ ] Fazer deploy

## 🆘 Suporte

Se encontrar problemas, consulte:
- `DEPLOY_VERCEL.md` - Guia completo
- Documentação oficial do Vercel: https://vercel.com/docs

---

🎉 **Boa sorte com o deploy!**
