from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from crud import atendimento as atendimento_crud, pet as pet_crud, veterinario as veterinario_crud
from schemas import atendimento as atendimento_schema

def create_new_atendimento(db: Session, atendimento: atendimento_schema.AtendimentoCreate):
    """
    Serviço para criar um novo atendimento com validação de regras de negócio.
    """
    # 1. Valida se o Pet existe
    db_pet = pet_crud.get_pet(db, pet_id=atendimento.pet_id)
    if not db_pet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pet com id {atendimento.pet_id} não encontrado."
        )

    # 2. Valida se o Veterinário existe
    db_veterinario = veterinario_crud.get_veterinario(db, veterinario_id=atendimento.veterinario_id)
    if not db_veterinario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Veterinário com id {atendimento.veterinario_id} não encontrado."
        )

    # 3. Se todas as validações passarem, cria o atendimento
    return atendimento_crud.create_atendimento(db=db, atendimento=atendimento)