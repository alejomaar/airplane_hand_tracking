from pydantic import BaseModel


class Settings(BaseModel):
    ws_host_server: str = "ws://localhost:8000"
    ws_host_client: str = "ws://localhost:8001"
    ws_timeout: int = 45


settings = Settings()
