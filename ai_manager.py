import logging
from typing import Optional, Dict, Set
from enum import Enum, auto

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    """Enum for available AI providers"""
    DUMMY = auto()  # Modo dummy para desativar todas as IAs
    DEEPSEEK = auto()
    EDEN = auto()
    # Adicione novos providers aqui

class AIManager:
    def __init__(self):
        # Dicionário para armazenar o estado de ativação por usuário
        self._enabled_users: Set[int] = set()
        # Dicionário para armazenar o provider ativo por usuário
        self._active_providers: Dict[int, AIProvider] = {}

    def enable_ai(self, user_id: int, provider: Optional[AIProvider] = None) -> AIProvider:
        """
        Ativa a IA para um usuário e opcionalmente define o provider
        """
        self._enabled_users.add(user_id)
        if provider:
            self._active_providers[user_id] = provider
        elif user_id not in self._active_providers:
            # Define DeepSeek como provider padrão
            self._active_providers[user_id] = AIProvider.DEEPSEEK

        logger.info(f"AI enabled for user {user_id} with provider {self._active_providers[user_id]}")
        return self._active_providers[user_id]

    def disable_ai(self, user_id: int) -> None:
        """
        Desativa a IA para um usuário
        """
        self._enabled_users.discard(user_id)
        logger.info(f"AI disabled for user {user_id}")

    def switch_provider(self, user_id: int, provider: AIProvider) -> None:
        """
        Troca o provider ativo para um usuário
        """
        self._active_providers[user_id] = provider
        # Garante que a IA está ativa ao trocar o provider, exceto se for modo DUMMY
        if provider != AIProvider.DUMMY:
            self._enabled_users.add(user_id)
        else:
            self._enabled_users.discard(user_id)
        logger.info(f"Switched AI provider for user {user_id} to {provider}")

    def enable_dummy_mode(self, user_id: int) -> None:
        """
        Ativa o modo dummy para um usuário
        """
        self.switch_provider(user_id, AIProvider.DUMMY)
        logger.info(f"Dummy mode enabled for user {user_id}")

    def is_dummy_mode(self, user_id: int) -> bool:
        """
        Verifica se o usuário está em modo dummy
        """
        return self.get_active_provider(user_id) == AIProvider.DUMMY

    def is_enabled(self, user_id: int) -> bool:
        """
        Verifica se a IA está ativa para um usuário
        """
        return user_id in self._enabled_users

    def get_active_provider(self, user_id: int) -> Optional[AIProvider]:
        """
        Retorna o provider ativo para um usuário
        """
        return self._active_providers.get(user_id)

    def initialize_user(self, user_id: int) -> None:
        """
        Inicializa as configurações padrão para um novo usuário
        """
        self.enable_ai(user_id, AIProvider.DEEPSEEK)

    def list_available_providers(self) -> list:
        """
        Retorna lista de providers disponíveis (exceto DUMMY)
        """
        return [p for p in AIProvider if p != AIProvider.DUMMY]

    @staticmethod
    def get_provider_name(provider: AIProvider) -> str:
        """
        Retorna o nome amigável do provider
        """
        return {
            AIProvider.DUMMY: "Modo Dummy",
            AIProvider.DEEPSEEK: "DeepSeek",
            AIProvider.EDEN: "Eden"
        }.get(provider, "Unknown")