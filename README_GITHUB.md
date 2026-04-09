# Locutores IA - Central de Vozes Inteligentes

Uma plataforma web para gerar locuções publicitárias usando Inteligência Artificial com vozes realistas e personalizáveis.

## 🎯 Funcionalidades

- **Catálogo de Vozes IA**: Múltiplas vozes com diferentes estilos (profissional, amigável, energético, calmo)
- **Geração de Áudio em Tempo Real**: Transforme texto em áudio de alta qualidade
- **Filtros Avançados**: Busque vozes por gênero, idioma e estilo
- **Player de Áudio Integrado**: Preview instantâneo das locuções geradas
- **Download de Áudios**: Exporte suas locuções em formato WAV
- **Interface Responsiva**: Funciona em desktop e dispositivos móveis
- **MiniDAW**: Mixagem profissional com Multi-track, Efeitos (Reverb, Delay, Compressor, EQ), Auto Fade 1.05s, Exportação WAV/MP3

## 🚀 Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **IA**: Google Gemini TTS (Text-to-Speech)
- **Áudio**: Web Audio API, Processamento WAV/MP3
- **Deploy**: Vercel

## 📁 Estrutura do Projeto

```
Locutores IA/
├── backend/              # Servidor Flask e APIs
│   └── app.py           # Aplicação principal
├── core/                # Módulo TTS
│   └── tts_generator.py # Gerador de áudio com IA
├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── script.js
│   ├── minidaw.js
│   └── minidaw-integrated.js
├── templates/           # Templates HTML
│   ├── index.html
│   └── minidaw.html
├── generated_audio/     # Áudios gerados
├── requirements.txt     # Dependências Python
├── vercel.json         # Configuração Vercel
└── README.md           # Documentação
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**:

```bash
git clone https://github.com/seu-usuario/locutores-ia.git
cd locutores-ia
```

2. **Crie um ambiente virtual**:

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**:

```bash
pip install -r requirements.txt
```

4. **Configure a API Key**:

```bash
# Copie .env.example para .env
cp .env.example .env

# Edite o arquivo .env e adicione sua chave da API Google Gemini:
# GEMINI_API_KEY=sua_chave_api_aqui
```

5. **Inicie a aplicação**:

```bash
cd backend
python app.py
```

6. **Acesse a aplicação**: Abra seu navegador em http://localhost:5000

## 🔧 Configuração da API Google Gemini

1. Acesse [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crie uma nova API Key
3. Adicione a chave ao arquivo `.env`

## 📖 Como Usar

1. **Escolha uma Voz**: Navegue pelo catálogo e selecione uma voz IA
2. **Digite o Texto**: Escreva o texto que deseja transformar em áudio
3. **Configure o Estilo**: Escolha entre normal, rápido, lento, alegre ou sério
4. **Gere o Áudio**: Clique em "Gerar Áudio" e aguarde o processamento
5. **MiniDAW**: Arraste o áudio gerado para a MiniDAW para mixagem profissional
6. **Preview e Download**: Ouça o resultado e faça o download se gostar

## 🎨 Vozes Disponíveis

- **Alex Professional**: Voz masculina corporativa
- **Maria Amigável**: Voz feminina calorosa
- **Carlos Energético**: Voz masculina vibrante
- **Ana Suave**: Voz feminina calma
- **James Corporate**: Voz masculina em inglês
- **Sophie Elegant**: Voz feminina sofisticada

## 🔐 Variáveis de Ambiente

| Variável | Descrição | Obrigatório |
|----------|-----------|-------------|
| `GEMINI_API_KEY` | Chave da API Google Gemini | Sim |
| `FLASK_ENV` | Ambiente Flask (development/production) | Não |
| `FLASK_DEBUG` | Modo debug (True/False) | Não |

## 🚀 Deploy no Vercel

### Deploy Automático

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/seu-usuario/locutores-ia)

### Deploy Manual

1. **Instale o Vercel CLI**:

```bash
npm i -g vercel
```

2. **Faça login**:

```bash
vercel login
```

3. **Deploy**:

```bash
vercel --prod
```

4. **Configure as variáveis de ambiente no Vercel**:
   - Acesse o Dashboard do Vercel
   - Vá em Settings > Environment Variables
   - Adicione `GEMINI_API_KEY` com sua chave

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- Google Gemini API pela tecnologia de Text-to-Speech
- Flask e comunidade Python
- Bootstrap pela interface responsiva

---

<p align="center">
  Feito com ❤️ para locutores e produtores de áudio
</p>
