from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from src.models import User


class UserRepo(SQLAlchemyAsyncRepository[User]):
    """User repository."""

    model_type = User
