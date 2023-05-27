from apps.user.serializers import *
import logging
from apps.user.models import *
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

logger = logging.getLogger( __name__ )

#create jwt token for a user
def auth_token(user):
    emp_id=Profile.objects.get(email=user.email).id
    access = AccessToken.for_user(user)
    refresh=RefreshToken.for_user(user)

    access['email']=user.email
    access['user_id']=emp_id
    refresh['email']=user.email
    refresh['user_id']=emp_id
   
    #sAVE LAST LOGIN TIME
    login_time = Profile.objects.filter(id=emp_id).update(last_login=datetime.now())
      
    return {"access_token": str(access),
    "refresh_token":str(refresh)}

def login_details(user):
    try:
        user_details = {}
        get_jwt = auth_token(user)
        user_details['access_token'] = get_jwt['access_token']
        user_details['refresh_token'] = get_jwt['refresh_token']
        user_details['role'] = [user.role.id]
        user_details['email'] = user.email
        user_details['user_id'] = user.id
        user_details['user_name'] = user.first_name + user.last_name
        return user_details
        
    except Exception as e:
        logger.info(f"{e}: login details func")
        raise Exception
    
def remove_duplicates(dictionaries, keys):
        seen = set()
        unique_dicts = []
        for dictionary in dictionaries:
            selected_values = tuple(dictionary[key] for key in keys)
            if selected_values not in seen:
                seen.add(selected_values)
                unique_dicts.append(dictionary)

        return unique_dicts