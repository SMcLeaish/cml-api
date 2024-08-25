from keycloak import KeycloakOpenID
import logging

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("keycloak_debug")

try:
    # Initialize the KeycloakOpenID client
    server_url = "https://auth.civmillabs.com/"
    realm_name = "civmillabs"

    keycloak_openid = KeycloakOpenID(
        server_url=server_url,
        client_id="api",
        realm_name=realm_name,
        client_secret_key="0Wrdh3lkRWzMJ56AW7532Td8uCDTt5rx",
        verify=True,  # or False if using self-signed certificates
    )

    logger.debug("KeycloakOpenID object created successfully.")

    # Manually construct the URLs using the provided information
    well_known_url = f"{server_url}realms/{realm_name}/.well-known/openid-configuration"
    token_url = f"{server_url}realms/{realm_name}/protocol/openid-connect/token"

    logger.debug(f"Well-known URL: {well_known_url}")
    logger.debug(f"Token URL: {token_url}")
    print(f"Connecting to: {token_url}")

    # Get a token using resource owner password credentials grant
    token = keycloak_openid.token(
        grant_type="password", username="smcleaish", password="honesty1"
    )

    logger.debug("Token retrieved successfully.")
    print("Access Token:", token["access_token"])

except Exception as e:
    logger.error(f"An error occurred: {e}")

