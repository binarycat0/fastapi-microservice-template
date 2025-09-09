from db.session import DbSessionManager


class EntitiesRepository:
    session_manager: DbSessionManager

    async def batch_add_entities(self, user_id):
        pass
