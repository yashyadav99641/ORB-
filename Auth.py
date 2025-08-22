from fyers_apiv3 import accessToken
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
secret_key = os.getenv("SECRET_KEY")
redirect_uri = os.getenv("REDIRECT_URI")

session = accessToken.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type="code",
    grant_type="authorization_code"
)

print("Login URL:", session.generate_authcode())

auth_code = ""  # paste here after login

if auth_code:
    session.set_token(auth_code)
    response = session.generate_token()
    print(response)
