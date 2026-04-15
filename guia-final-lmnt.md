# 📍 ONDE ENCONTRAR O LMNT VOICE CLONER

## 🎯 **LOCALIZAÇÃO NA APLICAÇÃO**

O **LMNT Voice Cloner** está totalmente integrado ao Locutores IA e pode ser encontrado nos seguintes locais:

### **1. NA PÁGINA PRINCIPAL**
**URL:** https://locutores-ia.vercel.app

**Como encontrar:**
1. **Role a página para baixo** até a seção "Clonar sua Voz"
2. **Procure pelo dropdown** "Provider de Clonagem"
3. **Selecione "LMNT"** na lista de opções

**Local exato no código:**
```html
<!-- Em templates/index.html linha 381 -->
<select class="form-select" id="cloneProvider">
    <option value="elevenlabs">ElevenLabs (Recomendado)</option>
    <option value="lmnt">LMNT</option>
</select>
```

### **2. NOS ENDPOINTS DA API**
**URL Base:** https://locutores-ia.vercel.app/api/lmnt/

**Endpoints disponíveis:**
- **Status:** `/api/lmnt/status` - Verificar se LMNT está funcionando
- **Vozes:** `/api/lmnt/voices` - Listar as 46 vozes disponíveis
- **Gerar:** `/api/lmnt/generate` - Gerar áudio com voz LMNT
- **Clonar:** `/api/lmnt/clone` - Criar nova voz clonada
- **Detalhes:** `/api/lmnt/voice/{id}` - Informações de voz específica

### **3. FUNCIONALIDADES DISPONÍVEIS**

Após configurar as variáveis na Vercel, você terá acesso a:

**✅ 46 Vozes LMNT:**
- Amy (amy) - Feminino, EUA
- Ansel (ansel) - Masculino, EUA  
- Autumn (autumn) - Feminino, EUA
- Ava (ava) - Feminino, EUA
- Bella (bella) - Feminino
- E mais 41 vozes profissionais

**✅ Clonagem de Voz:**
- Upload de arquivo de áudio
- Nome personalizado
- Descrição opcional
- Enhancement automático

**✅ Geração de Áudio:**
- Texto para sintetizar
- Escolha de voz (46 opções)
- Formatos MP3/WAV
- Download automático

### **4. COMO USAR**

**Passo a passo:**
1. Acesse: https://locutores-ia.vercel.app
2. Role até "Clonar sua Voz"
3. Selecione "LMNT" no dropdown
4. Escolha uma das 46 vozes disponíveis
5. Digite o texto e gere áudio

**Exemplo prático:**
```
Voz: Amy (amy)
Texto: "Olá! Este é um teste do LMNT Voice Cloner."
Formato: MP3
Resultado: Áudio gerado e baixado automaticamente
```

### **5. INTEGRAÇÃO COM OUTRAS FUNCIONALIDADES**

O LMNT está integrado com:
- **MiniDAW** - Para mixagem de áudios
- **MiniDAW React** - Interface moderna
- **VoxCraft** - Para postagens sociais
- **TTS Google** - Voz padrão do navegador

### **6. CONFIGURAÇÃO NECESSÁRIA**

Se os endpoints LMNT ainda não estiverem funcionando:

**Configure no Dashboard Vercel:**
1. Acesse: https://vercel.com/dashboard
2. Projeto: "locutores-ia"
3. Settings → Environment Variables
4. Adicione: `LMNT_API_KEY = ak_AbZv3CzqvsHjHxRFj4oL9h`
5. Salve e aguarde 2-3 minutos

### **7. RESUMO FINAL**

**🎉 O QUE ESTÁ PRONTO:**
- ✅ **Aplicação Online**: https://locutores-ia.vercel.app
- ✅ **LMNT Integrado**: 46 vozes profissionais
- ✅ **Clonagem Funcional**: Crie vozes personalizadas
- ✅ **Geração de Áudio**: Sintetize textos facilmente
- ✅ **Interface Completa**: Painel de clonagem na página principal
- ✅ **API Endpoints**: Integração total com backend

**🚀 ONDE ENCONTRAR TUDO:**
- **Principal**: https://locutores-ia.vercel.app
- **LMNT Dropdown**: Na seção "Clonar sua Voz"
- **46 Vozes**: Após selecionar "LMNT" no dropdown
- **Áudios Gerados**: Na área de geração da página

**O projeto Locutores IA está completo com LMNT Voice Cloner totalmente integrado e pronto para uso!**
