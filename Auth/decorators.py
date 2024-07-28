
from django.http import HttpResponse

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            group= None
            grp = None
            if request.user.groups.exists():
                groups=request.user.groups.all()
                for group in groups: 
                    if group.name in allowed_roles:
                        grp=group.name
                        break
            if grp in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("You are not AUthorized")
        return wrapper_func
    return decorator