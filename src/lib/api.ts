const DEFAULT_BACKEND_URL = "http://localhost:8000/api/v1";

export function getBackendUrl(): string {
  const fromEnv = import.meta.env.PUBLIC_BACKEND_URL;
  return (fromEnv && fromEnv.replace(/\/$/, "")) || DEFAULT_BACKEND_URL;
}

export function getAuthUrl(): string {
  const fromEnv = import.meta.env.PUBLIC_AUTH_URL;
  return (fromEnv && fromEnv.replace(/\/$/, "")) || getBackendUrl();
}
