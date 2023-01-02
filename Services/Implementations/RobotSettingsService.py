import logging
import platform
from abc import ABC
from typing import Optional

from automapper import mapper

from Models.Entities.Entity import Robots
from Models.ViewModels.RobotModelVM import RobotsModelVM
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase
from Repositories.DbRepositories.RepositoryBase import RepositoryBase
from Services.Abstractions.IRobotSettingsService import IRobotSettingsService


class RobotSettingsService(IRobotSettingsService, ABC):
    def __init__(self):
        self.robot_repo: IRepositoryBase = RepositoryBase(Robots)
        self.logger = logging.getLogger('ServerLog')

    async def add_async(self, robot_model: RobotsModelVM) -> Optional[RobotsModelVM]:
        try:
            if await self.robot_repo.get(Robots.id != robot_model.id, Robots.robot_name == robot_model.robot_name):
                raise Exception(f'Robot name {robot_model.robot_name} is already added')
            robot_entity = mapper.to(Robots).map(robot_model)
            robot_entity.id = None
            robot_entity.is_deleted = False
            robot_model = self.robot_repo.add(robot_entity)
            await self.robot_repo.commit()
            return robot_model
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'add_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            await self.robot_repo.rollback()
            return None

    async def update_async(self, robot_model: RobotsModelVM) -> Optional[RobotsModelVM]:
        try:
            if await self.robot_repo.get(Robots.id != robot_model.id, Robots.robot_name == robot_model.robot_name):
                raise Exception(f'Robot name {robot_model.robot_name} is unavailable')
            entity: Robots = await self.robot_repo.get(Robots.id == robot_model.id)
            if entity.is_deleted:
                raise Exception(f'Robot name {robot_model.robot_name} is unavailable')
            entity.robot_name = robot_model.robot_name
            entity.platform_selection = robot_model.platform_selection
            entity.browser_selection = robot_model.browser_selection
            entity.is_incognito = robot_model.is_incognito
            entity.is_headless = robot_model.is_headless
            entity.is_deleted = False
            await self.robot_repo.commit()
            return mapper.to(RobotsModelVM).map(entity)
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'update_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None

    async def delete_async(self, robot_id: int) -> Optional[bool]:
        try:
            entity: Robots = await self.robot_repo.get(Robots.id == robot_id)
            entity.is_deleted = True
            await self.robot_repo.commit()
            return True
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'delete_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None

    async def get_robot_async(self, robot_id: int) -> Optional[RobotsModelVM]:
        try:
            entity: Robots = await self.robot_repo.get(Robots.id == robot_id)
            return mapper.to(RobotsModelVM).map(entity)
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'get_robot_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None

    async def get_all_robots_async(self) -> Optional[list]:
        try:
            entities: list = await self.robot_repo.get_list(Robots.is_deleted == False)
            models = list()
            for robo in entities:
                models.append(mapper.to(RobotsModelVM).map(robo))
            return models
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'get_all_robots_async'}
            self.logger.error('Robot Settings Service: %s', str(ex), extra=details)
            return None
