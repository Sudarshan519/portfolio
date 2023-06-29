from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Request
from fastapi.security.utils import get_authorization_scheme_param
from fastapi import HTTPException
from fastapi import status
from typing import Optional
from typing import Dict

from pyparsing import wraps

# from apis.v1.route_login import get_current_user_from_token


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("access_token")  #changed to accept access token from httpOnly Cookie
        print("access_token is",authorization)

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param
    

# def auth_required(handler):
#     @wraps(handler)
#     async def wrapper( *args, **kwargs):
#         # do_something_with_request_object(request)
#         # request=(kwargs.get('request'))
#         # db=(kwargs.get('db'))
#         # token=request.cookies.get("access_token")
#         # if token is None:
#         get_current_user_from_token
#         return   handler(*args, **kwargs)
#     return wrapper


def requires_employee(handler):
    @wraps(handler)
    async def wrapper(*args,**kwargs):
        user=(kwargs.get('current_user'))
        db=(kwargs.get('db'))
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")
        else:
            if user.is_employer is False:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not permitted!!!!")
            
        return wrapper
        
def auth_required(handler): 
        @wraps(handler)
        async def wrapper( *args, **kwargs):
            # do_something_with_request_object(request)
            user=(kwargs.get('current_user'))
            print(user)
            # db=(kwargs.get('db'))
        #     token=request.headers.get("access_token")
        #     if token is None:
        #         raise HTTPException(
        #     status_code=status.HTTP_401_UNAUTHORIZED,
        #     detail="Authentication required.",
        # )
            # get_current_user_from_token
            return  handler(*args, **kwargs)
        return wrapper
