from abc import ABCMeta, ABC

from domain.contracts.repositories.abstract_generic_repository import AbstractGenericRepository
from domain.models.generation_job_details import GenerationJobDetails


class AbstractJobsDetailsRepository(AbstractGenericRepository[GenerationJobDetails], ABC):
    __metaclass__ = ABCMeta
