from sqlalchemy import select

from app.core.security import hash_password
from app.database.session import async_session
from app.models.enums import UserRole
from app.models.user import User


async def create_admin() -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == "admin@example.com"))

        admin = result.scalar_one_or_none()

        if admin is not None:
            return

        admin = User(
            name="Admin",
            email="admin@example.com",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
        )

        session.add(admin)

        await session.commit()
