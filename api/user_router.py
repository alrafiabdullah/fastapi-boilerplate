from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.config import SessionLocal, get_db
from db.schema import UserSchema, RequestUser, Response
from api.user_views import get_user, get_user_by_id, create_user, update_user, delete_user

router = APIRouter()


@router.get("/")
async def user_get(db: Session = Depends(get_db)):
    try:
        users = get_user(db, skip=0, limit=100)
        for user in users:
            user.password = None

        return Response(data=users, message="Users retrieved successfully", code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/{user_id}")
async def user_get_by_id(user_id: int, db: Session = Depends(get_db)):
    try:
        user = get_user_by_id(db, user_id)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"data": "User not found"})

        user.password = None
        return Response(data=user, message="User retrieved successfully", code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/create")
async def user_create(request: RequestUser, db: Session = Depends(get_db)):
    try:
        user = create_user(db, request.parameter)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"data": "User with email already exists"})

        user.password = None
        return Response(data=user, message="User created successfully", code=status.HTTP_201_CREATED)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/update")
async def user_update(request: RequestUser, db: Session = Depends(get_db)):
    try:
        user = update_user(db, request.parameter)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"data": "User not found"})
        user.password = None

        return Response(data=user, message="User updated successfully", code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/delete")
async def user_delete(request: RequestUser, db: Session = Depends(get_db)):
    try:
        user = delete_user(db, request.parameter.id)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"data": "User not found"})

        return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "SUCCESS", "data": "User deleted successfully"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
