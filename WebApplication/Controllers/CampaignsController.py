from fastapi import APIRouter, HTTPException

from Models.ViewModels.Campaigns import CampaignVM
from Models.ViewModels.PaginationModel import PaginationModel
from Services.Abstractions.ICompaignService import ICampaignService
from Services.Implementations.CampaignService import CampaignService

campaign_module = APIRouter(
    prefix='/campaign',
    tags=["Campaign Manager"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"},
        500: {"description": "Internal Error"}
    }
)


@campaign_module.post('/pagination/')
async def get_campaigns(paging_data: PaginationModel):
    try:
        contacts_service: ICampaignService = CampaignService()
        return await contacts_service.get_campaign_list(paging_data)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@campaign_module.get('/{campaign_id}')
async def get_campaign_by_id(campaign_id: int):
    try:
        contacts_service: ICampaignService = CampaignService()
        return await contacts_service.get_campaign_by_id(campaign_id)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@campaign_module.post('/')
async def create_campaign(campaign_model: CampaignVM):
    try:
        contacts_service: ICampaignService = CampaignService()
        await contacts_service.create_campaign(campaign_model)
        return 'successful'
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@campaign_module.put('/')
async def update_campaign(campaign_model: CampaignVM):
    try:
        contacts_service: ICampaignService = CampaignService()
        await contacts_service.update_campaign(campaign_model)
        return 'successful'
    except Exception as ex:
        raise HTTPException(status_code=500, detail=str(ex))
