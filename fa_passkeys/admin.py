# admin.py

from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fa_passkeys.models import User
from fa_passkeys.config import settings
from fa_passkeys.app_logging import logger

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login")
async def admin_login_page(request: Request):
    return templates.TemplateResponse("admin_login.html", {"request": request})


@router.post("/login")
async def admin_login(
    request: Request, username: str = Form(...), password: str = Form(...)
):
    if username == settings.admin_username and password == settings.admin_password:
        request.session["admin"] = True
        return RedirectResponse(url="/admin/users", status_code=303)
    else:
        return templates.TemplateResponse(
            "admin_login.html", {"request": request, "error": "Invalid credentials"}
        )


def admin_required(request: Request):
    if not request.session.get("admin"):
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.get("/users")
async def admin_users(request: Request):
    admin_required(request)
    users = await User.find_all().to_list()
    return templates.TemplateResponse(
        "admin_users.html", {"request": request, "users": users}
    )


@router.get("/users/{user_id}")
async def admin_user_detail(request: Request, user_id: str):
    admin_required(request)
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse(
        "admin_user_detail.html", {"request": request, "user": user}
    )


@router.post("/users/{user_id}/delete")
async def admin_delete_user(request: Request, user_id: str):
    admin_required(request)
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await user.delete()
    logger.info(f"Admin deleted user {user.username}")
    return RedirectResponse(url="/admin/users", status_code=303)
