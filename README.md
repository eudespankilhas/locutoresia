# Locutores IA - Central de Vozes Inteligentes

Uma plataforma web para gerar locuções publicitárias usando Inteligência Artificial com vozes realistas e personalizáveis.

## 🎯 Funcionalidades

- **Catálogo de Vozes IA**: Múltiplas vozes com diferentes estilos (profissional, amigável, energético, calmo)
- **Geração de Áudio em Tempo Real**: Transforme texto em áudio de alta qualidade
- **Filtros Avançados**: Busque vozes por gênero, idioma e estilo
- **Player de Áudio Integrado**: Preview instantâneo das locuções geradas
- **Download de Áudios**: Exporte suas locuções em formato WAV
- **Interface Responsiva**: Funciona em desktop e dispositivos móveis

## 🚀 Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **IA**: Google Gemini TTS (Text-to-Speech)
- **Áudio**: Processamento e conversão WAV

## 📁 Estrutura do Projeto

```
Locutores IA/
├── backend/              # Servidor Flask e APIs
│   └── app.py           # Aplicação principal
├── core/                # Módulo TTS
│   └── tts_generator.py # Gerador de áudio com IA
├── frontend/            # Arquivos JavaScript
│   └── script.js        # Lógica da interface
├── templates/           # Templates HTML
│   └── index.html       # Página principal
├── static/              # Arquivos estáticos
├── generated_audio/     # Áudios gerados
├── requirements.txt     # Dependências Python
└── README.md           # Documentação
```

## 🛠️ Instalação e Configuração

### Pré-requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório**:
   ```bash
   git clone <repositorio>
   cd "Locutores IA"
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
   - Copie `.env.example` para `.env`
   - Adicione sua chave da API Google Gemini:
   ```
   GEMINI_API_KEY=sua_chave_api_aqui
   ```

5. **Inicie a aplicação**:
   ```bash
   cd backend
   python app.py
   ```

6. **Acesse a aplicação**:
   Abra seu navegador em `http://localhost:5000`

## 🔧 Configuração da API Google Gemini

1. Acesse [Google AI Studio](https://aistudio.google.com/)
2. Crie uma nova API Key
3. Adicione a chave ao arquivo `.env`

## 📖 Como Usar

1. **Escolha uma Voz**: Navegue pelo catálogo e selecione uma voz IA
2. **Digite o Texto**: Escreva o texto que deseja transformar em áudio
3. **Configure o Estilo**: Escolha entre normal, rápido, lento, alegre ou sério
4. **Gere o Áudio**: Clique em "Gerar Áudio" e aguarde o processamento
5. **Preview e Download**: Ouça o resultado e faça o download se gostar

## 🎨 Vozes Disponíveis

- **Alex Professional**: Voz masculina corporativa
- **Maria Amigável**: Voz feminina calorosa
- **Carlos Energético**: Voz masculina vibrante
- **Ana Suave**: Voz feminina calma
- **James Corporate**: Voz masculina em inglês
- **Sophie Elegant**: Voz feminina sofisticada

## 🔒 Variáveis de Ambiente

- `GEMINI_API_KEY`: Chave da API Google Gemini (obrigatória)
- `FLASK_ENV`: Ambiente Flask (development/production)
- `FLASK_DEBUG`: Modo debug (True/False)

## 🚀 Deploy

Para produção:

1. Configure `FLASK_ENV=production`
2. Use um servidor WSGI como Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 backend.app:app
   ```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Entre em contato através do formulário na plataforma

---

**Desenvolvido com ❤️ usando Inteligência Artificial**
