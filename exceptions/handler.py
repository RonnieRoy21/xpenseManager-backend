from pydantic import ValidationError
from supabase import SupabaseException


def get_error_type(
    e: Exception | ValidationError | SupabaseException,
) -> dict[str, str]:
    err_type = type(e)
    match (err_type.__name__):
        case "ValidationError":

            return {"message": f"Invalid request data.{e.errors()[0]['msg']}", "status": "422"}  # type: ignore
        case "SupabaseException":
            return {"message": f"Server Error.{e.message}", "status": "500"}  # type: ignore
        case "TypeError":
            return {"message": "Invalid data type in your request.", "status": "422"}
        case "ValueError":
            return {"message": f"Value Error : {e.args}", "status": "422"}
        case _:
            return {"message": f"{e.args}", "status": "500"}
