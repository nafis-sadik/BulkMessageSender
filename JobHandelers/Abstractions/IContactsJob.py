from typing import Optional


class IContactsJob:
    async def sync_contacts(self, file_path: str) -> None:
        raise NotImplementedError
