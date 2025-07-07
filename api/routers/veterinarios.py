from fastapi import APIRouter

router = APIRouter(
    prefix="/veterinarios",
    tags=["Veterinários"],
    responses={404: {"description": "Not found"}},
)

# Mova as rotas relacionadas a Veterinários (CRUD) para este arquivo.
# Exemplo:
# @router.post("/")
# def create_veterinario(...):
#     ...