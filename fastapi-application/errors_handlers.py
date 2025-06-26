from fastapi import FastAPI, Request,status
from pydantic import ValidationError
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import DatabaseError

import logging

log = logging.getLogger(__name__)

def register_errorsr_handlers(app: FastAPI) -> None:    
    
    @app.exception_handler(ValidationError)
    def handle_pydantic_validation_error(
        request: Request,
        exc: ValidationError,
    ) -> ORJSONResponse:
        return ORJSONResponse(
            status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "message": "Unhandled error",
                "error": exc.errors(),
            }
        )
        
    @app.exception_handler(DatabaseError)
    def handle_db_error(
        request: Request,
        exc: ValidationError,
    ) -> ORJSONResponse:
        log.error("Unhandled DB error",
                  exc_info=exc,
                )
        return ORJSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                              content={
                                  "message": "An unexpected error has occured."
                                  "Our admins are already working on it"
                              })