# This is the interface for primary controls of the robots
# In our case, we shall be in integrating fastapi to let user control the robot from web apis
# Any kind of User Interface integration is intended to be done here
from typing import Optional

from Services.Abstractions.IRobotOperationsService import IRobotOperationsService


class IRobotControlCenterService:
    async def initialize_robot(self, robot_id: int) -> None:
        raise NotImplementedError

    async def start_robot(self, robot_id: int) -> None:
        raise NotImplementedError

    async def stop_robot(self, robot_id: int) -> None:
        raise NotImplementedError

    async def terminate_robot(self, robot_id: int) -> None:
        raise NotImplementedError

    def get_all_alive_robots(self) -> list:
        raise NotImplementedError

    async def get_robot(self, robot_id: int) -> Optional[IRobotOperationsService]:
        raise NotImplementedError
