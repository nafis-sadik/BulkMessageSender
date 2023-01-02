from typing import Optional

from Models.ViewModels.RobotModelVM import RobotsModelVM


class IRobotSettingsService:
    async def add_async(self, robot_model: RobotsModelVM) -> Optional[RobotsModelVM]:
        raise NotImplementedError

    async def update_async(self, robot_model: RobotsModelVM) -> Optional[RobotsModelVM]:
        raise NotImplementedError

    async def delete_async(self, robot_id: int) -> Optional[bool]:
        raise NotImplementedError

    async def get_robot_async(self, robot_id: int) -> Optional[RobotsModelVM]:
        raise NotImplementedError

    async def get_all_robots_async(self) -> Optional[list]:
        raise NotImplementedError
