from rest_framework.throttling import UserRateThrottle

class RequestRateThrottle(UserRateThrottle):
    scope = 'social_media'