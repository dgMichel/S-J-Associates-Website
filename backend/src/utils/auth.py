from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.db.supabase import get_supabase_admin

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    sb = get_supabase_admin()
    try:
        result = sb.auth.get_user(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not result or not getattr(result, "user", None):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudieron validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return result.user


def get_current_active_user(user=Depends(get_current_user)):
    app_metadata = getattr(user, "app_metadata", None) or {}
    if not app_metadata.get("is_active", True):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user


def require_role(*roles: str):
    def role_checker(user=Depends(get_current_active_user)):
        app_metadata = getattr(user, "app_metadata", None) or {}
        role = app_metadata.get("role", "user")
        if role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(roles)}",
            )
        return user
    return role_checker


require_admin = require_role("admin")
require_inspector = require_role("inspector", "admin")
require_analyst = require_role("analyst", "admin")
