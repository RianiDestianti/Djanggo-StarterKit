import math
from datetime import datetime
from urllib.parse import quote
from django.db.models import Q
from models.user_model import UserModel
from repositories.generate import to_int
from repositories.hash import hash_password
from repositories.validator import Validator


class UserController:
    def get_data(self, request):
        page    = to_int(request.GET.get('page'), 1)
        limit   = to_int(request.GET.get('limit'), 10)
        keyword = request.GET.get('keyword', '')
        role    = request.GET.get('role', '')
        offset  = (page - 1) * limit

        query = UserModel.objects.select_related('role').order_by('-created_at')

        if keyword:
            query = query.filter(
                Q(name__icontains=keyword) |
                Q(email__icontains=keyword) |
                Q(phone__icontains=keyword)
            )

        if role:
            query = query.filter(role_id=role)

        total  = query.count()
        result = query[offset:offset + limit]

        users = [{
            'id'      : item.id,
            'name'    : item.name,
            'phone'   : item.phone,
            'email'   : item.email,
            'avatar'  : item.avatar,
            'role'    : item.role.name if item.role else None
        } for item in result]

        return {
            'status'  : 200,
            'message' : 'Success return data user',
            'data'    : {
                'data'      : users,
                'page'      : page,
                'limit'     : limit,
                'total'     : {
                    'pages' : math.ceil(total / limit) if limit else 0,
                    'data'  : total
                },
            }
        }

    def action_data(self, request):
        body = request.json
        id   = body.get('id') or 0

        rules = {
            'name'      : 'required',
            'email'     : 'required|email',
            'role'      : 'required',
            'password'  : 'min:6' if id else 'required|min:6',
        }

        validation = Validator(body, rules)
        if validation.fails():
            return {
                'status'  : 422,
                'message' : 'Validation failed',
                'data'    : validation.errors.all()
            }

        check_email = UserModel.objects.filter(email=body['email']).exclude(id=id).first()
        if check_email:
            return {
                'status'  : 422,
                'message' : 'The email has been registered',
                'data'    : {
                    'email' : ['The email has been registered']
                }
            }

        try:
            data = UserModel.objects.filter(id=id).first()

            if data:

                data.name       = body['name']
                data.email      = body['email']
                data.phone      = body.get('phone')
                data.role_id    = body['role']

                if body.get('password'):
                    data.password = hash_password(body['password'])

                data.save()
            else:

                UserModel.objects.create(
                    name        = body['name'],
                    email       = body['email'],
                    phone       = body.get('phone'),
                    role_id     = body['role'],
                    password    = hash_password(body['password']),
                    avatar      = f"https://ui-avatars.com/api/?format=png&name={quote(str(body['name']))}",
                    verified_at = datetime.now(),
                )

            return {
                'status'  : 200,
                'message' : 'Success saved data'
            }
        except Exception as error:
            return {
                'status'  : 500,
                'message' : str(error) or 'Failed saved data'
            }

    def get_detail(self, request, id):

        tmp_data = UserModel.objects.select_related('role').filter(id=id).first()
        if tmp_data:

            data = {
                **tmp_data.to_dict(),
                'role'      : tmp_data.role_id,
                'roleName'  : tmp_data.role.name if tmp_data.role else None,
            }

            return {
                'status'  : 200,
                'message' : 'Success return detail data',
                'data'    : data
            }
        else:
            return {
                'status'  : 404,
                'message' : 'Data not found'
            }

    def delete_data(self, request, id):

        data = UserModel.objects.filter(id=id).first()
        if data:

            data.destroy()

            return {
                'status'  : 200,
                'message' : 'Success delete data'
            }
        else:
            return {
                'status'      : 404,
                'message'     : 'Data not found'
            }
