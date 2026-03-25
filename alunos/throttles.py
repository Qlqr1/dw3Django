from rest_framework.throttling import UserRateThrottle


class MatriculaRateThrottle(UserRateThrottle):
    # Escopo personalizado — referenciado no settings
    scope = 'matriculas'