import logging
logger = logging.getLogger( __name__ )

def signup_validator(request):
    try:
        data=request.data
        json_keys=['user_name' , 'password' , 'role_id' , 'confirm_password' ,'email','phone_number','date_of_birth','gender','profile_picture']
        for val in json_keys:
            if  val not in dict.keys(data):
                return False
        return True
    except Exception as e:
        logger.info(e)
        return False
    