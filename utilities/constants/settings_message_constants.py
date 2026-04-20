INCORRECT_PAYMENT_GATEWAY_SETUP_MESSAGE = str(
    "Please enter you Payment sandbox (Braintree/SSLCOMMERZ) credentials in settings.py or envs/.env file."
    "Visit this url if you don't have a sandbox account: https://sandbox.braintreegateway.com/login")

INCORRECT_CELERY_REDIS_SETUP_MESSAGE = str(
            'This project uses celery/redis.'
            'configure CELERY_BROKER_URL and CELERY_RESULT_BACKEND in envs/.env')

INCORRECT_STRIPE_SETUP_MESSAGE = str(
    "Please enter you Stripe credentials in envs/.env file.")
