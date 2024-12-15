import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as router_hotels
from src.database import *

app = FastAPI()

app.include_router(router_hotels)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
