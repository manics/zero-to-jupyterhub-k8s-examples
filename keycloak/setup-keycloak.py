#!/usr/bin/env python
# coding: utf-8
# https://github.com/marcospereirampj/python-keycloak
from argparse import ArgumentParser
from keycloak import KeycloakAdmin

parser = ArgumentParser()
parser.add_argument("--external-host", default="http://localhost:8080")
parser.add_argument("--keycloak-url", default="{external_host}/keycloak/")
parser.add_argument("--jupyterhub-url", default="{external_host}/jupyter/")
parser.add_argument("--keycloak-admin", default="admin")
parser.add_argument("--keycloak-password", default="admin")
parser.add_argument("--user", default="example@example.com")
parser.add_argument("--password", default="secret")
parser.add_argument("--firstname", default="Example")
parser.add_argument("--lastname", default="User")
parser.add_argument("--client", default="jupyterhub")
parser.add_argument("--client-secret", default="jupyterhub-client-secret")

args = parser.parse_args()
jupyterhub_url = args.jupyterhub_url.format(external_host=args.external_host)

keycloak_admin = KeycloakAdmin(
    server_url=args.keycloak_url.format(external_host=args.external_host),
    username=args.keycloak_admin,
    password=args.keycloak_password,
    realm_name="master",
    verify=True,
)

# Create a user
user_payload = {
    "email": args.user,
    "username": args.user,
    "enabled": True,
    "firstName": "Example",
    "lastName": "User",
    "credentials": [
        {
            "value": args.password,
            "type": "password",
        }
    ],
}
uid = keycloak_admin.get_user_id(args.user)
if uid:
    print(f"Updating user {args.user} ({uid}) {user_payload}")
    keycloak_admin.update_user(uid, user_payload)
else:
    print(f"Creating user {args.user} {user_payload}")
    keycloak_admin.create_user(user_payload)

# Create an OAuth client for JupyterHub
client_payload = {
    "clientId": args.client,
    "name": args.client,
    "redirectUris": [
        args.jupyterhub_url.format(external_host=args.external_host)
        + "hub/oauth_callback"
    ],
    "clientAuthenticatorType": "client-secret",
    "secret": args.client_secret,
}
cid = keycloak_admin.get_client_id(args.client)
if cid:
    print(f"Updating client {args.client} ({cid}) {client_payload}")
    keycloak_admin.update_client(cid, client_payload)
else:
    print(f"Creating client {args.client} {client_payload}")
    keycloak_admin.create_client(client_payload)
