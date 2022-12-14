import os
import uvicorn
# from automapper import mapper
from dotenv import find_dotenv, load_dotenv

from JobHandelers.Implementations.RobotControlCenterService import RobotControlCenterService
# from Models.Entities.Entity import Campaigns
# from Models.ViewModels.Campaigns import CampaignVM
# from Models.ViewModels.ContactsFileVM import ContactsFileVM
from WebApplication import app

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    RobotControlCenterService.initialize()
    # mapper.add_spec(ContactsFileVM, ContactsFileVM)
    # mapper.add(CampaignVM, Campaigns, fields_mapping={
    #     "campaign_id": "CampaignVM.campaign_id"
    # })
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app=app, host='0.0.0.0', port=port)
