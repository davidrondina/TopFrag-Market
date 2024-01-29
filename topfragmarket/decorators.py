from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import *

def profile_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        user = request.user
        user_has_profile = Profile.objects.filter(user_id=user.id).count() > 0
        
        if not user_has_profile:
            # If user does not have profile, make them create one
            messages.error(request, 'Finish profile setup to proceed')
            return redirect('topfragmarket:create_profile')
        else:
            # Proceed to the view function
            return view_function(request, *args, **kwargs)

    return wrapper