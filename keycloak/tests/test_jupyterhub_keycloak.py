# Run this test with Playwright Pytest args:
# https://playwright.dev/python/docs/test-runners
#
# pytest --browser firefox --base-url http://%K8S_HOSTNAME% [--headed --slowmo 1000]
import json


def test_browser(page):
    # Go to <base-url>/jupyter/, wait for redirect to login page
    page.goto("/jupyter/")
    page.wait_for_selector("text=Sign in with keycloak")

    # Click "Sign in with keycloak", wait for redirect to keycloak
    page.locator("text=Sign in with keycloak").click()
    page.wait_for_url("/keycloak/realms/master/protocol/openid-connect/auth?*")

    # Fill username and password
    page.locator('input[name="username"]').fill("example@example.com")
    page.locator('input[name="password"]').fill("secret")

    # Click "Sign In"
    page.locator('button:has-text("Sign In")').click()
    # page.wait_for_url("/jupyter/hub/spawn-pending/*")

    # Server should be spawned, and should be redirected to JupyterLab
    page.wait_for_url("/jupyter/user/example@example.com/lab")


def test_admin(page):
    # Go to <base-url>/jupyter/hub/home, wait for redirect to login page
    page.goto("/jupyter/hub/home")
    page.wait_for_selector("text=Sign in with keycloak")

    # Click "Sign in with keycloak", wait for redirect to keycloak
    page.locator("text=Sign in with keycloak").click()
    page.wait_for_url("/keycloak/realms/master/protocol/openid-connect/auth?*")

    # Fill username and password
    page.locator('input[name="username"]').fill("admin")
    page.locator('input[name="password"]').fill("admin")

    # Click "Sign In"
    page.locator('button:has-text("Sign In")').click()

    # Should be redirected to /hub/home
    page.wait_for_url("/jupyter/hub/home")

    # List all groups via API, should match the Keycloak roles
    page.goto("/jupyter/hub/api/groups")
    content = page.locator("body").text_content()
    groups = json.loads(content)
    assert set(g["name"] for g in groups) == {"jupyterhub-admins", "jupyterhub-users"}
