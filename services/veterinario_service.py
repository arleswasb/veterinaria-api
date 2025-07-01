# veterinaria/services/veterinario_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException
from repository import crud
from services import schemas

def create_new_veterinario(db: Session, veterinario: schemas.VeterinarioCreate):
    # Lógica de Negócio: Verificar se a clínica existe
    db_clinica = crud.get_clinica(db, clinica_id=veterinario.clinica_id)
    if not db_clinica:
        raise HTTPException(status_code=404, detail=f"Clínica com id {veterinario.clinica_id} não encontrada")

    # Lógica de Negócio: Verificar se o CRMV já existe
    db_veterinario = db.query(crud.models.Veterinario).filter(crud.models.Veterinario.crmv == veterinario.crmv).first()
    if db_veterinario:
        raise HTTPException(status_code=400, detail="CRMV já cadastrado no sistema.")
    
    # Se todas as regras de negócio passarem, chama a camada de repositório para criar o objeto
    return crud.create_veterinario(db=db, veterinario=veterinario)