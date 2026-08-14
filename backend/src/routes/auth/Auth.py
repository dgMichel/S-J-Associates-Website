from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.rate_limit import limiter
from src.routes.schemas import schemas_auth
from src.db.supabase import get_supabase_admin, get_supabase_anon
from src.utils.auth import get_current_user, require_admin

router = APIRouter(prefix="/auth", tags=["Authentication"])


def _serialize_user(user) -> dict:
    app_metadata = getattr(user, "app_metadata", None) or {}
    user_metadata = getattr(user, "user_metadata", None) or {}
    return {
        "id": user.id,
        "username": user_metadata.get("username", "") or (user.email or "").split("@")[0],
        "email": user.email or "",
        "role": app_metadata.get("role", "user"),
        "is_active": app_metadata.get("is_active", True),
    }


@limiter.limit("5/minute")
@router.post("/register", response_model=schemas_auth.UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: Request, body: schemas_auth.RegisterRequest):
    sb = get_supabase_admin()
    try:
        result = sb.auth.admin.create_user({
            "email": body.email,
            "password": body.password,
            "email_confirm": True,
            "user_metadata": {"username": body.username},
            "app_metadata": {"role": "user", "is_active": True},
        })
    except Exception as e:
        msg = str(e).lower()
        if "already" in msg or "exists" in msg or "duplicate" in msg:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está registrado")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return _serialize_user(result.user)


@limiter.limit("10/minute")
@router.post("/login", response_model=schemas_auth.Token)
async def login(request: Request, body: schemas_auth.UserLogin):
    sb_anon = get_supabase_anon()
    try:
        result = sb_anon.auth.sign_in_with_password({
            "email": body.email,
            "password": body.password,
        })
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not result.session or not result.session.access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": result.session.access_token, "token_type": "bearer"}


@limiter.limit("30/minute")
@router.get("/me", response_model=schemas_auth.UserResponse)
async def get_me(request: Request, user=Depends(get_current_user)):
    return _serialize_user(user)


@router.get("/users", response_model=list[schemas_auth.UserResponse])
async def list_users(_=Depends(require_admin)):
    sb = get_supabase_admin()
    result = sb.auth.admin.list_users()
    users = getattr(result, "users", result)
    return [_serialize_user(u) for u in users]


@router.patch("/users/{user_id}/role", response_model=schemas_auth.UserResponse)
async def update_role(user_id: str, body: schemas_auth.RoleUpdate, _=Depends(require_admin)):
    sb = get_supabase_admin()
    try:
        existing = sb.auth.admin.get_user_by_id(user_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    current_app = getattr(existing.user, "app_metadata", None) or {}
    new_app = {**current_app, "role": body.role}
    try:
        result = sb.auth.admin.update_user_by_id(user_id, {"app_metadata": new_app})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Rol inválido: {e}")

    return _serialize_user(result.user)
