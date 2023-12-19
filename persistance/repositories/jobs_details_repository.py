from domain.contracts.repositories.abstract_jobs_details_repository import AbstractJobsDetailsRepository
from domain.models.generation_job_details import GenerationJobDetails
from persistance.repositories.base_redis_repository import BaseRedisRepository


class JobsDetailsRepository(AbstractJobsDetailsRepository, BaseRedisRepository[GenerationJobDetails]):
    def __init__(self):
        super(JobsDetailsRepository, self).__init__(2, GenerationJobDetails)
