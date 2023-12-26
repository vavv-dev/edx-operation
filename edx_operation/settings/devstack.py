from cryptography.fernet import Fernet

from edx_operation.settings.local import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "edx_operation"),
        "USER": os.environ.get("DB_USER", "root"),
        "PASSWORD": os.environ.get("DB_PASSWORD", ""),
        "HOST": os.environ.get("DB_HOST", "edx_operation.db"),
        "PORT": os.environ.get("DB_PORT", 5432),
        "ATOMIC_REQUESTS": False,
        "CONN_MAX_AGE": 60,
    }
}

# Generic OAuth2 variables irrespective of SSO/backend service key types.
OAUTH2_PROVIDER_URL = "http://edx.devstack.lms:18000/oauth2"

# OAuth2 variables specific to social-auth/SSO login use case.
SOCIAL_AUTH_EDX_OAUTH2_KEY = os.environ.get("SOCIAL_AUTH_EDX_OAUTH2_KEY", "edx_operation-sso-key")
SOCIAL_AUTH_EDX_OAUTH2_SECRET = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_SECRET", "edx_operation-sso-secret"
)
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_ISSUER", "http://localhost:18000"
)
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT", "http://edx.devstack.lms:18000"
)
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL", "http://localhost:18000/logout"
)
SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT",
    "http://localhost:18000",
)

# OAuth2 variables specific to backend service API calls.
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = os.environ.get(
    "BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL", "http://edx.devstack.lms:18000"
)
BACKEND_SERVICE_EDX_OAUTH2_KEY = os.environ.get(
    "BACKEND_SERVICE_EDX_OAUTH2_KEY", "edx_operation-backend-service-key"
)
BACKEND_SERVICE_EDX_OAUTH2_SECRET = os.environ.get(
    "BACKEND_SERVICE_EDX_OAUTH2_SECRET", "edx_operation-backend-service-secret"
)  # noqa: E501

JWT_AUTH.update(
    {
        "JWT_SECRET_KEY": "lms-secret",
        "JWT_ISSUER": "http://localhost:18000/oauth2",
        "JWT_AUDIENCE": None,
        "JWT_VERIFY_AUDIENCE": False,
        "JWT_PUBLIC_SIGNING_JWK_SET": """
        {
          "keys": [
            {
              "kty": "RSA",
              "kid": "devstack_key",
              "n": "smKFSYowG6nNUAdeqH1jQQnH1PmIHphzBmwJ5vRf1vu48BUI5VcVtUWIPqzRK_LDSlZYh9D0YFL0ZTxIrlb6Tn3Xz7pYvpIAeYuQv3_H5p8tbz7Fb8r63c1828wXPITVTv8f7oxx5W3lFFgpFAyYMmROC4Ee9qG5T38LFe8_oAuFCEntimWxN9F3P-FJQy43TL7wG54WodgiM0EgzkeLr5K6cDnyckWjTuZbWI-4ffcTgTZsL_Kq1owa_J2ngEfxMCObnzGy5ZLcTUomo4rZLjghVpq6KZxfS6I1Vz79ZsMVUWEdXOYePCKKsrQG20ogQEkmTf9FT_SouC6jPcHLXw",
              "e": "AQAB"
            }
          ]
        }
    """,  # noqa: E501
        "JWT_ISSUERS": [
            {
                "AUDIENCE": "lms-key",
                "ISSUER": "http://localhost:18000/oauth2",
                "SECRET_KEY": "lms-secret",
            }
        ],
    }
)

# api urls
LMS_BASE_URL = "http://edx.devstack.lms:18000"
CMS_BASE_URL = "http://edx.devstack.cms:18010"

# edx api key
EDX_API_KEY = "PUT_YOUR_API_KEY_HERE"

# event bus
EVENT_BUS_TOPIC_PREFIX = "dev"
EVENT_BUS_TOPIC_NAME = "operation_event.signals"
EVENT_BUS_CONSUMER = "edx_operation.apps.event_bus.service.OperationEventConsumer"
EVENT_BUS_KAFKA_SCHEMA_REGISTRY_URL = "http://edx.devstack.schema-registry:8081"
EVENT_BUS_KAFKA_BOOTSTRAP_SERVERS = "edx.devstack.kafka:29092"

# id number encryption
# Fernet.generate_key()
cipher_suite = Fernet(b"SWZ1eZKlH2xfiIO8sx0FMW5Zg-NEIA_8LEFZoA87mY0=")
