import os
from typing import Type, List
import pickle
import redis
from pydantic import BaseModel

from domain.contracts.repositories.abstract_generic_repository import AbstractGenericRepository, RepoT


class BaseRedisRepository(AbstractGenericRepository[RepoT]):
    """
        Pydantic compatible base redis repository wrapper
    """

    def __init__(self, db: int, repo_model: Type[BaseModel]):
        password = os.getenv("REDIS_DEFAULT_PASS", None)
        port = int(os.getenv("REDIS_PORT", 6379))
        self.redis = redis.Redis(host='redis_db', port=port, db=db,password=password)
        self.repo_model = repo_model

    def get_from_cache(self, uuid: str) -> RepoT:
        loaded_params = self.redis.get(uuid)
        loaded_params = pickle.loads(loaded_params)
        return loaded_params

    def set_to_cache(self, uuid: str, value: RepoT) -> None:
        pkl_value = pickle.dumps(value, protocol=-1)
        self.redis.set(uuid, pkl_value)

    def get_all(self) -> List[RepoT]:
        return [self.get_from_cache(key) for key in self.redis.keys()]

    def delete(self, uuid: str):
        if self.redis.exists(uuid): self.redis.delete(uuid)

    def exists(self, uuid: str):
        return self.redis.exists(uuid)
