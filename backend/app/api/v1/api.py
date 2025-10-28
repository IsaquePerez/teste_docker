from fastapi import APIRouter
from .endpoints import sistemas
from .endpoints import modulo

# Cria o roteador principal da API v1
api_router = APIRouter()

# Inclui o roteador de 'sistemas'
# Todas as rotas de 'sistemas.py' serão prefixadas com '/sistemas'
# e agrupadas sob a tag 'Sistemas' na documentação do Swagger
api_router.include_router(sistemas.router, prefix="/sistemas", tags=["Sistemas"])
api_router.include_router(modulo.router, prefix="/modulos", tags=["Módulos"])

# Se tivéssemos um endpoint para 'modulos', adicionaríamos aqui:
# from .endpoints import modulos
# api_router.include_router(modulos.router, prefix="/modulos", tags=["Módulos"])