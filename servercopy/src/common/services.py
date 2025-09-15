class UserIdentificationService:

    @staticmethod
    def get_user_identifier(request):
        return {'user': request.user}
