from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(ABC, Generic[ModelType, RepositoryType]):
    def __init__(self, repository_class: type[RepositoryType], model: type[ModelType]):
        self.repository_class = repository_class
        self.model = model

    def _get_repository(self, db: Session) -> RepositoryType:
        return self.repository_class(self.model, db)

    def get_by_id(self, db: Session, id: int) -> Optional[ModelType]:
        repo = self._get_repository(db)
        return repo.get(id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[ModelType]:
        repo = self._get_repository(db)
        return repo.get_all(skip, limit)

    def create(self, db: Session, obj: ModelType) -> ModelType:
        self._validate_create(obj)
        repo = self._get_repository(db)
        return repo.create(obj)

    def update(self, db: Session, id: int, **kwargs) -> Optional[ModelType]:
        repo = self._get_repository(db)
        obj = repo.get(id)
        if not obj:
            return None
        self._validate_update(obj, kwargs)
        return repo.update(obj, **kwargs)

    def delete(self, db: Session, id: int) -> bool:
        repo = self._get_repository(db)
        obj = repo.get(id)
        if not obj:
            return False
        self._validate_delete(obj)
        repo.delete(obj)
        return True

    def exists(self, db: Session, id: int) -> bool:
        return self.get_by_id(db, id) is not None

    def count(self, db: Session) -> int:
        repo = self._get_repository(db)
        return len(repo.get_all())

    @abstractmethod
    def _validate_create(self, obj: ModelType) -> None:
        pass

    @abstractmethod
    def _validate_update(self, obj: ModelType, update_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def _validate_delete(self, obj: ModelType) -> None:
        pass
