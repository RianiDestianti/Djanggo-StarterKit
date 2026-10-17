from models.user_model import UserModel
from repositories.hash import hash_password
from repositories.validator import Validator


class ProfileController:
    def get_profile(self, request):
        user = request.user

        get_user = UserModel.objects.filter(id=user['id']).first()

        return {
            'status'  : 200,
            'message' : 'Success return data user',
            'data'    : {
                **user,
                'verified'  : True if get_user and get_user.verified_at else False
            }
        }

    def action(self, request):
        body      = request.json
        auth_user = request.user

        rules = {
            'name'      : 'required',
            'password'  : 'min:6'
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        try:
            user = UserModel.objects.filter(id=auth_user['id']).first()
            if not user:
                return {
                    'status'  : 404,
                    'message' : 'Data not found'
                }

            user.name   = body['name']
            user.phone  = body.get('phone', user.phone)
            user.avatar = body.get('avatar', user.avatar)

            if body.get('password'):
                user.password = hash_password(body['password'])

            user.save()

            return {
                'status'  : 200,
                'message' : 'Success saved data'
            }
        except Exception as error:
            return {
                'status'  : 500,
                'message' : str(error) or 'Failed saved data'
            }
