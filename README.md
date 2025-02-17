# Bot do Telegram com Integração DeepSeek e Eden AI 🤖

Bot do Telegram em Python que integra as APIs da DeepSeek e Eden AI para processamento de mensagens, além de recursos de integração com o Notion.

## Funcionalidades Principais 🌟

- Processamento de mensagens usando DeepSeek AI
- Integração com Eden AI para análise de sentimento
- Integração com Notion para salvar e buscar conteúdo
- Sistema de gerenciamento de IAs (ativar/desativar/alternar)
- Modo Dummy para desativar todas as IAs
- Análise de sentimento de mensagens

## Requisitos 📋

- Python 3.8+
- Token do Bot do Telegram
- Chave de API da DeepSeek
- Chave de API da Eden AI
- Token de integração do Notion
- ID do banco de dados do Notion

## Configuração ⚙️

1. Clone o repositório
2. Copie o arquivo `.env.example` para `.env`
3. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   NOTION_TOKEN=your_notion_integration_token_here
   NOTION_DATABASE_ID=your_notion_database_id_here
   EDEN_AI_API_KEY=your_eden_ai_api_key_here
   ```

## Comandos Disponíveis 🎮

- `/start` - Iniciar o bot
- `/help` - Mostrar mensagem de ajuda
- `/toggle_ai` - Ativar/Desativar processamento de mensagens com IA
- `/use_deepseek` - Alternar para DeepSeek AI
- `/use_eden` - Alternar para Eden AI
- `/use_dummy` - Ativar modo dummy (desativa todas as IAs)
- `/analyze_sentiment` - Analisar sentimento da próxima mensagem
- `/databases` - Listar bancos de dados do Notion disponíveis

## Como Usar 🚀

1. Inicie o bot com o comando `/start`
2. Use `/toggle_ai` para ativar o processamento de mensagens
3. Escolha qual IA usar com `/use_deepseek` ou `/use_eden`
4. Envie mensagens para interagir com a IA escolhida
5. Use `/analyze_sentiment` seguido de uma mensagem para análise
6. Use `/use_dummy` para desativar todas as IAs

## Estrutura do Projeto 📁

```
├── ai_manager.py          # Gerenciamento de IAs
├── bot.py                 # Código principal do bot
├── config.py             # Configurações e mensagens
├── deepseek_client.py    # Cliente DeepSeek AI
├── eden_client.py        # Cliente Eden AI
├── notion_manager.py     # Gerenciamento Notion
└── utils.py              # Utilitários e decorators
```

## Recursos Futuros 🔮

- [ ] Implementar sistema de cache para respostas
- [ ] Adicionar comandos personalizados
- [ ] Melhorar tratamento de erros com retry

## Contribuição 🤝

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença 📄

Este projeto está licenciado sob a MIT License.
