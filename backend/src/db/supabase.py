from supabase import create_client, Client
from src.config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_ANON_KEY

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL must be set in the environment")
if not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY must be set in the environment")

_admin: Client | None = None
_anon: Client | None = None


def get_supabase_admin() -> Client:
    global _admin
    if _admin is None:
        _admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    return _admin


def get_supabase_anon() -> Client:
    global _anon
    if _anon is None:
        if not SUPABASE_ANON_KEY:
            raise RuntimeError("SUPABASE_ANON_KEY is required for this operation")
        _anon = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    return _anon
