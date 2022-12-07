from typing import Optional

from Models.ViewModels.RobotModel import RobotsModel


class IRobotSettingsService:
    async def add_async(self, robot_model: RobotsModel) -> Optional[bool]:
        raise NotImplementedError

    async def update_async(self, robot_model: RobotsModel) -> Optional[RobotsModel]:
        raise NotImplementedError

    async def delete_async(self, robot_id: int) -> Optional[bool]:
        raise NotImplementedError

    async def get_robot_async(self, robot_id: int) -> Optional[RobotsModel]:
        raise NotImplementedError

    async def get_all_robots_async(self) -> Optional[list]:
        raise NotImplementedError
