"""Entry point of the application for local development."""
from os import environ as env

import uvicorn

if __name__ == "__main__":
    # Reference: https://www.uvicorn.org/settings/
    port = int(env.get("PORT", 5000))
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        debug=True,
        reload=True,
        access_log=True,
    )
