# Multi AI Telegram Bot APP

## Descrição

O Multi AI Telegram Bot APP é um aplicativo de bot para Telegram que integra múltiplas inteligências artificiais para fornecer uma variedade de funcionalidades automatizadas. Este projeto é desenvolvido principalmente em Python.

## Funcionalidades

- Integração com múltiplas APIs de IA
- Respostas automatizadas no Telegram
- Personalização de comandos

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/nelisjunior/MultAITelegramBot.git
    cd MultAITelegramBot
    ```

2. Crie um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Configuração

Edite o arquivo de configuração `config.yaml` (ou `config.json`) com suas credenciais e configurações específicas. Exemplo de `config.yaml`:

```yaml
telegram_token: 'YOUR_TELEGRAM_BOT_TOKEN'
api_keys:
  openai: 'YOUR_OPENAI_API_KEY'
  another_ai: 'YOUR_ANOTHER_AI_API_KEY'
```

## Uso

Para iniciar o bot, execute:
```bash
python main.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Contato

Para mais informações, entre em contato com [seu e-mail](mailto:your-email@example.com).