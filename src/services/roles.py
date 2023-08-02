from typing import List

from fastapi import Depends, HTTPException, status, Request

from src.database.models import User, Role
from src.services.auth import auth_service


class RoleAccess:

    def __init__(self, allowed_roles: List[Role]):
        """
        The __init__ function is called when the class is instantiated.
            It sets up the instance of the class with a list of allowed roles.
        
        :param self: Represent the instance of the class
        :param allowed_roles: List[Role]: Specify the allowed roles for a command
        :return: The object created
        :doc-author: Trelent
        """
        self.allowed_roles = allowed_roles


    async def __call__(self, request:Request, current_user: User = Depends(auth_service.get_current_user)):
        """
        The __call__ function is the function that will be called when a user tries to access an endpoint.
            It checks if the current_user has one of the allowed roles, and if not it raises a 403 error.
        
        :param self: Access the class attributes
        :param request:Request: Get the request method and url
        :param current_user: User: Get the current user from the database
        :return: A response object
        :doc-author: Trelent
        """
        print(request.method, request.url)
        print(f'User role {current_user.roles}')
        print(f'Allowed roles: {self.allowed_roles}')
        if current_user.roles not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Operation forbidden')


allowed_operation_everyone = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_mod_and_admin = RoleAccess([Role.admin, Role.moderator])
allowed_operation_admin = RoleAccess([Role.admin])
