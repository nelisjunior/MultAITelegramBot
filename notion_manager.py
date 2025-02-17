import logging
from notion_client import Client
from config import NOTION_TOKEN

logger = logging.getLogger(__name__)

class NotionManager:
    def __init__(self):
        self.client = Client(auth=NOTION_TOKEN)

    async def list_databases(self) -> list:
        """
        List all accessible databases
        """
        try:
            results = self.client.search(
                filter={
                    "property": "object",
                    "value": "database"
                }
            ).get("results", [])
            return [{
                "id": db["id"],
                "title": db["title"][0]["plain_text"] if db.get("title") else "Untitled",
                "description": db.get("description", "No description")
            } for db in results]
        except Exception as e:
            logger.error(f"Error listing Notion databases: {str(e)}")
            raise Exception(f"Failed to list Notion databases: {str(e)}")

    async def create_page(self, database_id: str, title: str, content: str) -> dict:
        """
        Create a new page in a Notion database
        """
        try:
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
                                    "content": content
                                }
                            }
                        ]
                    }
                }
            )
            return new_page
        except Exception as e:
            logger.error(f"Error creating Notion page: {str(e)}")
            raise Exception(f"Failed to create Notion page: {str(e)}")

    async def search_pages(self, query: str) -> list:
        """
        Search for pages in Notion
        """
        try:
            results = self.client.search(
                query=query,
                sort={
                    "direction": "descending",
                    "timestamp": "last_edited_time"
                }
            ).get("results", [])
            return results
        except Exception as e:
            logger.error(f"Error searching Notion pages: {str(e)}")
            raise Exception(f"Failed to search Notion pages: {str(e)}")

    async def get_database_schema(self, database_id: str) -> dict:
        """
        Get the schema of a specific database
        """
        try:
            database = self.client.databases.retrieve(database_id=database_id)
            return {
                "id": database["id"],
                "title": database["title"][0]["plain_text"] if database.get("title") else "Untitled",
                "properties": database["properties"]
            }
        except Exception as e:
            logger.error(f"Error getting database schema: {str(e)}")
            raise Exception(f"Failed to get database schema: {str(e)}")
