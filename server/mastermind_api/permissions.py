from rest_framework import permissions
from typing import Dict
from rest_framework.views import APIView
from .models import Game



class IsCodebreaker(permissions.BasePermission):
    """Custom permission class to only allow the codebreaker access to their games."""

    def has_object_permission(self, request: Dict, view: APIView, obj: Game) -> bool:
        """Return true if the user making the request is the codebreaker of the game."""
        return obj.codebreaker == request.user
