from rest_framework.exceptions import ValidationError
import uuid
from typing import Dict, Any


class UserIdentificationService:
    @staticmethod
    def get_user_identifier(request) -> Dict[str, Any]:
        if request.user.is_authenticated:
            return {'user': request.user}

        guest_id = request.headers.get('Guest-Id')
        if not guest_id:
            raise ValidationError(
                {'guest_id': 'Guest-Id header is required for anonymous users'})

        try:
            guest_uuid = uuid.UUID(guest_id)
            return {'guest_id': guest_uuid}
        except (ValueError, TypeError):
            raise ValidationError({'guest_id': 'Invalid guest ID format'})
