from functools import wraps
from django.http import HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import redirect


def vendors_only(viewfunc):
    @wraps(viewfunc)
    def wrap(request,*args, **kwargs):
        
        user = request.user
        if user.is_vendor == True or user.is_superuser==True:
            return viewfunc(request,*args,**kwargs)
        else:
            return HttpResponseNotAllowed("You are not allowed")
    return wrap


def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('admin-login')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func