from abc import abstractmethod, ABC, ABCMeta

from domain.models.api_paths import ApiPaths


class AbstractPathService(ABC):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def paths(self) -> ApiPaths: raise NotImplementedError
