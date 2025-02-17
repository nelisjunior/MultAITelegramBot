import logging
from notion_client import Client, APIResponseError
from config import NOTION_TOKEN, NOTION_DATABASE_ID

logger = logging.getLogger(__name__)

class NotionManager:
    def __init__(self):
        if not NOTION_TOKEN:
            logger.error("NOTION_TOKEN não configurado")
            raise ValueError("Token do Notion não configurado")

        logger.info("Inicializando NotionManager")
        self.client = Client(auth=NOTION_TOKEN)
        self.default_database_id = NOTION_DATABASE_ID

        if not self.default_database_id:
            logger.warning("NOTION_DATABASE_ID não configurado, algumas funcionalidades podem estar limitadas")

    async def list_databases(self) -> list:
        """
        Lista todos os bancos de dados acessíveis
        """
        try:
            logger.info("Buscando lista de bancos de dados do Notion")
            results = self.client.search(
                filter={
                    "property": "object",
                    "value": "database"
                }
            ).get("results", [])

            if not results:
                logger.info("Nenhum banco de dados encontrado")
                return []

            databases = [{
                "id": db["id"],
                "title": db["title"][0]["plain_text"] if db.get("title") else "Sem título",
                "description": db.get("description", "Sem descrição")
            } for db in results]

            logger.info(f"Encontrados {len(databases)} bancos de dados")
            return databases

        except APIResponseError as e:
            error_msg = f"Erro na API do Notion ao listar bancos: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao listar bancos: {str(e)}"
            logger.error(error_msg)
            raise Exception("Erro ao listar bancos de dados do Notion")

    async def create_page(self, title: str, content: str, database_id: str = None) -> dict:
        """
        Cria uma nova página no banco de dados do Notion
        """
        try:
            database_id = database_id or self.default_database_id
            if not database_id:
                error_msg = "ID do banco de dados não fornecido"
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info(f"Criando página '{title}' no banco {database_id}")
            content_truncated = content[:2000]
            if len(content) > 2000:
                logger.warning(f"Conteúdo truncado de {len(content)} para 2000 caracteres")

            new_page = self.client.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Name": {
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "Content": {
                        "rich_text": [
                            {
                                "text": {
                                    "content": content_truncated
                                }
                            }
                        ]
                    }
                }
            )

            logger.info(f"Página criada com sucesso: {new_page['id']}")
            return {
                "id": new_page["id"],
                "url": new_page["url"],
                "title": title
            }

        except APIResponseError as e:
            error_msg = f"Erro na API do Notion ao criar página: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao criar página: {str(e)}"
            logger.error(error_msg)
            raise Exception("Erro ao criar página no Notion")

    async def search_pages(self, query: str) -> list:
        """
        Busca páginas no Notion
        """
        try:
            logger.info(f"Buscando páginas com query: '{query}'")
            results = self.client.search(
                query=query,
                filter={
                    "property": "object",
                    "value": "page"
                },
                sort={
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                }
            ).get("results", [])

            if not results:
                logger.info("Nenhuma página encontrada")
                return []

            formatted_results = []
            for page in results[:5]:  # Limitando a 5 resultados
                title = page["properties"].get("Name", {}).get("title", [])
                title_text = title[0]["plain_text"] if title else "Sem título"

                formatted_results.append({
                    "id": page["id"],
                    "title": title_text,
                    "url": page["url"],
                    "last_edited": page.get("last_edited_time", "Desconhecido")
                })

            logger.info(f"Encontradas {len(formatted_results)} páginas")
            return formatted_results

        except APIResponseError as e:
            error_msg = f"Erro na API do Notion ao buscar páginas: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Erro inesperado ao buscar páginas: {str(e)}"
            logger.error(error_msg)
            raise Exception("Erro ao buscar páginas no Notion")

    async def get_page_content(self, page_id: str) -> str:
        """
        Get the content of a specific page
        """
        try:
            logger.info(f"Getting content for page: {page_id}")
            blocks = self.client.blocks.children.list(block_id=page_id).get("results", [])
            content = []
            for block in blocks:
                if block["type"] == "paragraph":
                    text = block["paragraph"]["rich_text"]
                    if text:
                        content.append(text[0]["plain_text"])
            
            page_content = "\n".join(content)
            logger.info(f"Page content retrieved successfully.")
            return page_content

        except APIResponseError as e:
            error_msg = f"Notion API error getting page content: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error getting page content: {str(e)}"
            logger.error(error_msg)
            raise Exception("Erro ao obter conteúdo da página")


    async def get_database_schema(self, database_id: str = None) -> dict:
        """
        Get the schema of a specific database
        """
        try:
            database_id = database_id or self.default_database_id
            if not database_id:
                error_msg = "ID do banco de dados não fornecido"
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info(f"Getting schema for database: {database_id}")
            database = self.client.databases.retrieve(database_id=database_id)
            
            logger.info(f"Database schema retrieved successfully.")
            return {
                "id": database["id"],
                "title": database["title"][0]["plain_text"] if database.get("title") else "Untitled",
                "properties": database["properties"]
            }
        except APIResponseError as e:
            error_msg = f"Notion API error getting database schema: {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"Error getting database schema: {str(e)}"
            logger.error(error_msg)
            raise Exception("Erro ao obter esquema do banco de dados")