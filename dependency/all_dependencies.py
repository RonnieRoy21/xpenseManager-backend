from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from database.supabase_database import SupabaseDatabase, get_db
from models.profiles import ProfilesModel

bearer = HTTPBearer()
auth_creds = Annotated[HTTPAuthorizationCredentials, Depends(bearer)]
db = Annotated[SupabaseDatabase, Depends(get_db)]


# auth dependency (for protecting routes)
def verify_client(creds: auth_creds, db: db):
    try:
        token = creds.credentials
        # if not oken passed raise error
        if not token:
            raise HTTPException(
                detail="Unauthenticated.", status_code=status.HTTP_401_UNAUTHORIZED
            )

        # if token passed ,authenticated it
        profile = db.getUser(access_token=token)
        if not profile:
            raise HTTPException(
                detail="No such user", status_code=status.HTTP_401_UNAUTHORIZED
            )
        return profile
    except Exception as e:
        raise HTTPException(
            detail="Access Permission Denied", status_code=status.HTTP_403_FORBIDDEN
        )


verified = Annotated[ProfilesModel, Depends(verify_client)]
