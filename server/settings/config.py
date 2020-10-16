"""
Configurazioni servizio
"""
from datetime import datetime as dt, timedelta as td
from os import environ as env
from flask import Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

app = Flask(__name__)

app.config['JWT_TOKEN_LOCATION'] = ('headers',)
#
# Options for JWTs when the TOKEN_LOCATION is headers
app.config['JWT_HEADER_NAME'] = env.get("JWT_HEADER_NAME", 'Authorization')
app.config['JWT_HEADER_TYPE'] = env.get("JWT_HEADER_TYPE", 'Bearer')
#
# Options for JWTs then the TOKEN_LOCATION is query_string
# app.config['JWT_QUERY_STRING_NAME', 'jwt')
#
# Option for JWTs when the TOKEN_LOCATION is cookies
# app.config['JWT_ACCESS_COOKIE_NAME', 'access_token_cookie')
# app.config['JWT_REFRESH_COOKIE_NAME', 'refresh_token_cookie')
# app.config['JWT_ACCESS_COOKIE_PATH', '/')
# app.config['JWT_REFRESH_COOKIE_PATH', '/')
# app.config['JWT_COOKIE_SECURE', False)
# app.config['JWT_COOKIE_DOMAIN', None)
# app.config['JWT_SESSION_COOKIE', True)
# app.config['JWT_COOKIE_SAMESITE', None)
#
# Option for JWTs when the TOKEN_LOCATION is json
# app.config['JWT_JSON_KEY', 'access_token')
# app.config['JWT_REFRESH_JSON_KEY', 'refresh_token')
#
# Options for using double submit csrf protection
# app.config['JWT_COOKIE_CSRF_PROTECT', True)
# app.config['JWT_CSRF_METHODS', ['POST', 'PUT', 'PATCH', 'DELETE'])
# app.config['JWT_ACCESS_CSRF_HEADER_NAME', 'X-CSRF-TOKEN')
# app.config['JWT_REFRESH_CSRF_HEADER_NAME', 'X-CSRF-TOKEN')
# app.config['JWT_CSRF_IN_COOKIES', True)
# app.config['JWT_ACCESS_CSRF_COOKIE_NAME', 'csrf_access_token')
# app.config['JWT_REFRESH_CSRF_COOKIE_NAME', 'csrf_refresh_token')
# app.config['JWT_ACCESS_CSRF_COOKIE_PATH', '/')
# app.config['JWT_REFRESH_CSRF_COOKIE_PATH', '/')
# app.config['JWT_CSRF_CHECK_FORM', False)
# app.config['JWT_ACCESS_CSRF_FIELD_NAME', 'csrf_token')
# app.config['JWT_REFRESH_CSRF_FIELD_NAME', 'csrf_token')
#
# How long an a token will live before they expire.
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = td(**env.get("JWT_ACCESS_TOKEN_EXPIRES", dict(hours=12)))
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = td(**env.get("JWT_REFRESH_TOKEN_EXPIRES", dict(days=1)))
#
# What algorithm to use to sign the token. See here for a list of options:
# https://github.com/jpadilla/pyjwt/blob/master/jwt/api_jwt.py
app.config['JWT_ALGORITHM'] = env.get("JWT_ALGORITHM", 'HS256')
#
# What algorithms are allowed to decode a token
app.config['JWT_DECODE_ALGORITHMS'] = env.get("JWT_DECODE_ALGORITHM", None)
#
# Secret key to sign JWTs with. Only used if a symmetric algorithm is
# used (such as the HS* algorithms). We will use the app secret key
# if this is not set.
app.config['JWT_SECRET_KEY'] = env.get('JWT_SECRET_KEY', 'super-secret')  # Change this!
#
# Keys to sign JWTs with when use when using an asymmetric
# (public/private key) algorithm, such as RS* or EC*
# app.config['JWT_PRIVATE_KEY', None)
# app.config['JWT_PUBLIC_KEY', None)
print("ENV",env.get('JWT_PRIVATE_KEY', None))
app.config['JWT_PRIVATE_KEY'] = env.get('JWT_PRIVATE_KEY', None)
if app.config["JWT_PRIVATE_KEY"] is not None:
    app.config['JWT_PRIVATE_KEY']=open(app.config['JWT_PRIVATE_KEY']).read()
app.config['JWT_PUBLIC_KEY'] = env.get('JWT_PUBLIC_KEY', None)
if app.config["JWT_PUBLIC_KEY"] is not None:
    app.config['JWT_PUBLIC_KEY']=open(app.config['JWT_PUBLIC_KEY']).read()
#
# Options for blacklisting/revoking tokens
# app.config['JWT_BLACKLIST_ENABLED', False)
# app.config['JWT_BLACKLIST_TOKEN_CHECKS', ('access', 'refresh'))
#
# app.config['JWT_IDENTITY_CLAIM', 'identity')
# app.config['JWT_USER_CLAIMS', 'user_claims')
# app.config['JWT_DECODE_AUDIENCE', None)
# app.config['JWT_DECODE_ISSUER', None)
# app.config['JWT_DECODE_LEEWAY', 0)
#
# app.config['JWT_CLAIMS_IN_REFRESH_TOKEN', False)
#
# app.config['JWT_ERROR_MESSAGE_KEY', 'msg')

jwt = JWTManager(app)
