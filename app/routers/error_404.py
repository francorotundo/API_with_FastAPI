from fastapi import HTTPException, status


def error_404(name, data):
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{ name } not found.")