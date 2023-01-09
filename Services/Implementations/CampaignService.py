import logging
import platform
from abc import ABC

from automapper import mapper

from Models.Entities.Entity import Campaigns
from Models.ViewModels.Campaigns import CampaignVM
from Models.ViewModels.PaginationModel import PaginationModel
from Repositories.DbRepositories.IRepositoryBase import IRepositoryBase
from Repositories.DbRepositories.RepositoryBase import RepositoryBase
from Services.Abstractions.ICompaignService import ICampaignService


class CampaignService(ICampaignService, ABC):
    def __init__(self):
        self.campaign_repo: IRepositoryBase = RepositoryBase(Campaigns)
        self.logger = logging.getLogger('ServerLog')

    async def create_campaign(self, campaign_model: CampaignVM) -> None:
        try:
            self.campaign_repo.add(Campaigns(
                campaign_name=campaign_model.campaign_name,
                content_text=campaign_model.content_text,
                content_media=campaign_model.content_media,
                date=campaign_model.date
            ))

            await self.campaign_repo.commit()
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'create_campaign'}
            self.logger.error('Campaign Service: %s', str(ex), extra=details)

    async def update_campaign(self, campaign_model: CampaignVM) -> None:
        try:
            existing_campaign: Campaigns = await self.campaign_repo.get(
                Campaigns.campaign_id == campaign_model.campaign_id)

            if existing_campaign is None:
                raise Exception(f'{campaign_model.campaign_id} does not exist')

            existing_campaign.campaign_name = campaign_model.campaign_name
            existing_campaign.content_text = campaign_model.content_text
            existing_campaign.content_media = campaign_model.content_media
            existing_campaign.date = campaign_model.date

            await self.campaign_repo.commit()
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'update_campaign'}
            self.logger.error('Campaign Service: %s', str(ex), extra=details)

    async def get_campaign_list(self, paging_data: PaginationModel) -> PaginationModel:
        try:
            paged_campaign_list: PaginationModel = await self.campaign_repo.get_paged_list(paging_data)
            return paged_campaign_list
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'get_campaign_list'}
            self.logger.error('Campaign Service: %s', str(ex), extra=details)

    async def get_campaign_by_id(self, campaign_id: int) -> CampaignVM:
        try:
            existing_campaign: Campaigns = await self.campaign_repo.get(
                Campaigns.campaign_id == campaign_id)

            if existing_campaign is None:
                raise Exception(f'{campaign_id} does not exist')

            return mapper.to(CampaignVM).map(existing_campaign)
        except Exception as ex:
            details = {'platform': platform.node(), 'target': 'get_campaign_by_id'}
            self.logger.error('Campaign Service: %s', str(ex), extra=details)
