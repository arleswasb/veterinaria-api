import re
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handler para os erros de validação do Pydantic, para fornecer uma resposta mais detalhada.
    """
    errors = []
    for error in exc.errors():
        # Constrói um caminho legível para o campo, ex: "user -> address -> street"
        field = " -> ".join(str(loc) for loc in error["loc"] if loc != 'body')
        errors.append({"field": field, "message": error["msg"]})
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Erro de validação.", "errors": errors},
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    """
    Handler para erros de integridade do banco de dados (ex: violações de constraints UNIQUE).
    """
    # Tenta extrair uma mensagem mais amigável da exceção original
    # (Isso depende muito do driver do banco de dados - exemplo para PostgreSQL/SQLite)
    error_info = str(exc.orig)
    detail = "Erro de integridade no banco de dados. Um valor duplicado pode ter sido enviado."

    # Regex para constraint UNIQUE (SQLite e PostgreSQL)
    unique_match = re.search(r"UNIQUE constraint failed: ([\w\.]+)", error_info, re.IGNORECASE)
    if unique_match:
        field = unique_match.group(1).split('.')[-1]
        detail = f"O valor fornecido para o campo '{field}' já existe e precisa ser único."

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": detail},
    )