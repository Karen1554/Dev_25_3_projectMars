from fastapi import APIRouter, HTTPException
from db import SessionDep
from models import Vet, VetCreate

router = APIRouter( tags=["vet"])


@router.post("/", response_model=Vet)
async def create_vet(new_vet: VetCreate, session:SessionDep):
    vet = Vet.model_validate(new_vet)
    session.add(vet)
    await session.commit()
    await session.refresh(vet)
    return vet
