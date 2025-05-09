from typing import Sequence

import litestar as ls

from advanced_alchemy.extensions.litestar.providers import create_service_dependencies
from src.dtos.models.user import User
from src.dtos.schemas.request.user import UserCreateModel, UserUpdateModel
from src.dtos.schemas.response.user import UserResponseDto
from src.services.user import UserService


class UserController(ls.Controller):
    path = "/users"
    return_dto = UserResponseDto
    dependencies = create_service_dependencies(
        UserService,
        key="users_service",
    )
    tags = ["Users"]

    @ls.get(sync_to_thread=False)
    async def get_users(self, users_service: UserService) -> Sequence[User]:
        return await users_service.list()

    @ls.get(path="/{user_id:int}", sync_to_thread=False)
    async def get_user(self, user_id: int, users_service: UserService) -> User:
        return await users_service.get(user_id)

    @ls.post(status_code=201, sync_to_thread=False)
    async def create_user(
        self, data: UserCreateModel, users_service: UserService
    ) -> User:
        return await users_service.create(data)

    @ls.patch(path="/{user_id:int}", status_code=200, sync_to_thread=False)
    async def update_user(
        self, user_id: int, data: UserUpdateModel, users_service: UserService
    ) -> User:
        return await users_service.update(data, user_id)

    @ls.delete(path="/{user_id:int}", status_code=204, sync_to_thread=False)
    async def delete_user(self, user_id: int, users_service: UserService) -> None:
        await users_service.delete(user_id)
