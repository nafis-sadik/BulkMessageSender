from abc import ABC
from typing import Optional
from automapper import mapper
import logging
import platform

from Models.Entities.Entity import Robots
from Models.ViewModels.RobotModel import RobotsModel
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase
from Repositories.DbRepositories.RepositoryBase import RepositoryBase
from Services.Abstractions.IRobotSettingsService import IRobotSettingsService


class RobotSettingsService(IRobotSettingsService, ABC):
    def __init__(self):
        self.robot_repo: IRepositoryBase = RepositoryBase(Robots)
        self.logger = logging.getLogger('ServerLog')

    async def add_async(self, robot_model: RobotsModel) -> Optional[bool]:
        try:
            await self.robot_repo.add(mapper.to(Robots).map(robot_model))
            return True
        except Exception as ex:
            details = {'clientip': platform.node(), 'target': 'add_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return False

    async def update_async(self, robot_model: RobotsModel) -> Optional[RobotsModel]:
        try:
            entity: Robots = await self.robot_repo.get_first(robot_model.id)
            entity.robot_name = robot_model.robot_name
            entity.platform_selection = robot_model.platform_selection
            entity.browser_selection = robot_model.browser_selection
            entity.is_incognito = robot_model.is_incognito
            entity.is_headless = robot_model.is_headless
            await self.robot_repo.commit()
            return mapper.to(RobotsModel).map(entity)
        except Exception as ex:
            details = {'clientip': platform.node(), 'target': 'update_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None

    async def delete_async(self, robot_model: RobotsModel) -> Optional[bool]:
        try:
            await self.robot_repo.delete(mapper.to(Robots).map(robot_model))
            return True
        except Exception as ex:
            details = {'clientip': platform.node(), 'target': 'delete_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return False

    async def get_robot_async(self, robot_id: int) -> Optional[RobotsModel]:
        try:
            entity: list = await self.robot_repo.get_first(robot_id)
            return mapper.to(RobotsModel).map(entity)
        except Exception as ex:
            details = {'clientip': platform.node(), 'target': 'get_robot_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None

    async def get_all_robots_async(self) -> Optional[list]:
        try:
            entities: list = await self.robot_repo.get_all()
            models = list()
            for robo in entities:
                models.append(mapper.to(RobotsModel).map(robo))
            return models
        except Exception as ex:
            details = {'clientip': platform.node(), 'target': 'get_all_robots_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None
