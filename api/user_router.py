from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from db.config import SessionLocal, get_db
from db.schema import UserSchema, RequestUser, Response, RequestLogin, RequestChangePassword
from api.user_views import get_user, get_user_by_email, create_user, update_user, delete_user, password_check, update_user_password

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


@router.get("/{email}")
async def user_get_by_(email: str, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, email)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"data": "User not found"})

        user.password = None
        return Response(data=user, message="User retrieved successfully", code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/register")
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


@router.post("/login")
async def user_login(request: RequestLogin, db: Session = Depends(get_db)):
    try:
        user = get_user_by_email(db, request.parameter.email)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"data": "User not found"})
        if password_check(request.parameter.password, user.password):
            user.password = None
            return Response(data=user, message="User login successfully", code=status.HTTP_200_OK)
        else:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED, content={"data": "Incorrect username/password"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/change/password")
async def user_change_password(request: RequestChangePassword, db: Session = Depends(get_db)):
    try:
        if request.parameter.new_password != request.parameter.confirm_password:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, content={"data": "New password and confirm password does not match"})

        user = get_user_by_email(db, request.parameter.email)
        if user is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, content={"data": "User not found"})

        if password_check(request.parameter.password, user.password):
            update_user_password(db, user, request.parameter.new_password)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"data": "Password changed successfully"})

        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"data": "Incorrect old password"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
