from drf_spectacular.authentication import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object

from rest_framework_social_oauth2.authentication import SocialAuthentication


class TokenScheme(OpenApiAuthenticationExtension):
    target_class = SocialAuthentication
    name = 'SocialAuthentication'
    match_subclasses = True


    def get_security_definition(self, auto_schema):
        return build_bearer_security_scheme_object(
            header_name='Authorization',
            token_prefix="Bearer",
        )
