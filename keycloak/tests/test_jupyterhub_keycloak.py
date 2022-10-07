# Run this test with Playwright Pytest args:
# https://playwright.dev/python/docs/test-runners
#
# pytest --browser firefox --base-url http://%K8S_HOSTNAME% [--headed --slowmo 1000]


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
    page.locator('input:has-text("Sign In")').click()
    # page.wait_for_url("/jupyter/hub/spawn-pending/*")

    # Server should be spawned, and should be redirected to JupyterLab
    page.wait_for_url("/jupyter/user/example@example.com/lab")
