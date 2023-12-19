from abc import ABC, ABCMeta
from typing import List, TypeVar, Generic

RepoT = TypeVar("RepoT")


class AbstractGenericRepository(ABC, Generic[RepoT]):
    """
        Generic repository to abstract CRUD operations
    """
    __metaclass__ = ABCMeta

    def get_from_cache(self, uuid: str) -> RepoT: raise NotImplementedError

    def set_to_cache(self, uuid: str, value: RepoT) -> None: raise NotImplementedError

    def get_all(self) -> List[RepoT]: raise NotImplementedError

    def delete(self, uuid: str): raise NotImplementedError

    def exists(self, uuid: str) -> bool: raise NotImplementedError
