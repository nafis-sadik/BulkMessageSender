from Models.ViewModels.Campaigns import CampaignVM
from Models.ViewModels.PaginationModel import PaginationModel


class ICampaignService:
    async def create_campaign(self, campaign_model: CampaignVM) -> None:
        raise NotImplementedError

    async def update_campaign(self, campaign_model: CampaignVM) -> None:
        raise NotImplementedError

    async def get_campaign_list(self, paging_data: PaginationModel) -> PaginationModel:
        raise NotImplementedError

    async def get_campaign_by_id(self, campaign_id: int) -> CampaignVM:
        raise NotImplementedError
