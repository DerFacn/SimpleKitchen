from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class Repository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session
        
    @abstractmethod
    async def get_by_id(self, entity_id):
        ...
        
    @abstractmethod
    async def create(self, entity):
        ...
        
    @abstractmethod
    async def update(self, entity):
        ...
        
    @abstractmethod
    async def delete(self, entity):
        ...
