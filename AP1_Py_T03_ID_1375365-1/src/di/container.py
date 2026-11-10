from datasource.repository.storage import Storage
from datasource.repository.game_repository import GameRepository
from domain.service.game_service_impl import GameServiceImpl


class Container:
    def __init__(self):
        self._storage = None
        self._repository = None
        self._service = None

    @property
    def storage(self) -> Storage:
        if self._storage is None:
            self._storage = Storage()
        return self._storage

    @property
    def repository(self) -> GameRepository:
        if self._repository is None:
            self._repository = GameRepository(self.storage)
        return self._repository

    @property
    def service(self) -> GameServiceImpl:
        if self._service is None:
            self._service = GameServiceImpl(self.repository)
        return self._service