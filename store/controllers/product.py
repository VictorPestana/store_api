from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4

from store.core.exceptions import NotFoundException
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

router = APIRouter(tags=["products"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductOut)
async def create_product(
    body: ProductIn = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    return await usecase.create(body)


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductOut)
async def get_product(
    id: UUID4 = Path(...),
    usecase: ProductUsecase = Depends(),
) -> ProductOut:
    try:
        return await usecase.get(id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[ProductOut])
async def list_products(
    usecase: ProductUsecase = Depends(),
) -> List[ProductOut]:
    return await usecase.query()


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=ProductUpdateOut)
async def update_product(
    id: UUID4 = Path(...),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    return await usecase.update(id, body)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: UUID4 = Path(...),
    usecase: ProductUsecase = Depends(),
) -> None:
    try:
        await usecase.delete(id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
