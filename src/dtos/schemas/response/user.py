from litestar.dto import DataclassDTO, DTOConfig

from src.dtos.models.user import User


class UserResponseDto(DataclassDTO[User]):
    config = DTOConfig(exclude={"password"}, partial=True)
