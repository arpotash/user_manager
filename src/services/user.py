from typing import Optional

import advanced_alchemy.exceptions
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService
from advanced_alchemy.service.typing import ModelDictT
from src.exceptions import UserAlreadyExist, UserNotFound
from src.models import User
from src.repositories.user import UserRepo


class UserService(SQLAlchemyAsyncRepositoryService[User, UserRepo]):
    """User service."""

    repository_type = UserRepo
    match_fields = ["name"]

    async def create(self, data: "ModelDictT[User]", **kwargs) -> User:
        data = await self.to_model(data, "create")
        data.password = User.hash_password(data.password)
        try:
            return await super().create(data=data, **kwargs)
        except advanced_alchemy.exceptions.DuplicateKeyError:
            raise UserAlreadyExist()

    async def update(
        self, data: "ModelDictT[User]", item_id: Optional[int] = None, **kwargs
    ) -> User:
        data = await self.to_model(data, "update")
        updated_user = await super().update(data=data, item_id=item_id, **kwargs)
        if not updated_user:
            raise UserNotFound(item_id)

        return updated_user

    async def get(self, item_id: int, **kwargs) -> User:
        try:
            return await super().get(item_id=item_id, **kwargs)
        except advanced_alchemy.exceptions.NotFoundError:
            raise UserNotFound(item_id)
