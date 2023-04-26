from fastapi import FastAPI, APIRouter
from api.pets.views import pets_router

app = FastAPI(title='Consyst-OS FastAPI Test Task')

main_api_router = APIRouter()
main_api_router.include_router(pets_router, prefix="/pets", tags=["pets"])

app.include_router(main_api_router)
