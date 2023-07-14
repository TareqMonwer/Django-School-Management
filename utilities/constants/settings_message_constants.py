INCORRECT_PAYMENT_GATEWAY_SETUP_MESSAGE = str(
    "Please enter you Payment sandbox (Braintree/SSLCOMMERZ) credentials in settings.py or envs/.env file."
    "Visit this url if you don't have a sandbox account: https://sandbox.braintreegateway.com/login")

INCORRECT_CELERY_REDIS_SETUP_MESSAGE = str(
            'This project uses celery/redis.'
            'to skip this set USE_CELERY_REDIS=False envs/.env'
            'Otherwise, configure these as described '
            'here: https://github.com/TareqMonwer/Django-School-Management#celery-redis-setup')