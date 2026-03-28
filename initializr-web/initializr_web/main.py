"""
Uvicorn entry point for the web service.
"""

import uvicorn


def main():
    """Run the web service."""
    uvicorn.run(
        "initializr_web.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
