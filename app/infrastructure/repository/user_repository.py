from app.models import User
from sqlalchemy import select
from app.core.repository import Repository


class UsersRepository(Repository):
    async def get_by_id(self, user_id: str) -> User | None:
        stmt = select(User).where(User.id == user_id)
        user = await self.session.scalar(stmt)
        return user
    
    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        user = await self.session.scalar(stmt)
        return user
    
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        return user
    
    async def update(self, user: User) -> User:
        result = await self.session.get(User, user.id)
        
        if not result:
            self.session.add(user)
            await self.session.commit()
            return user
        
        result.username = user.username
        result.password = user.password
        
        await self.session.commit()
        return result
    
    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.commit()
