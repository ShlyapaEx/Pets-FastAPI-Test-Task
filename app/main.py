from fastapi import FastAPI, APIRouter
from api.pets.views import pets_router

app = FastAPI()

main_api_router = APIRouter()
main_api_router.include_router(pets_router, prefix="/pets", tags=["pets"])

app.include_router(main_api_router)


@app.get('/healthcheck/')
def healthcheck():
    return 'Health - OK'
