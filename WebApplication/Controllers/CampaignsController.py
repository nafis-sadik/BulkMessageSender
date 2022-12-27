from fastapi import APIRouter, UploadFile

campaign_module = APIRouter(
    prefix='/campaign',
    tags=["Campaign Manager"],
    responses={
        404: {"description": "Not found"},
        200: {"description": "OK"}
    }
)

