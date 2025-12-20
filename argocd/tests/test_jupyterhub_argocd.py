# Run this test with Playwright Pytest args:
# https://playwright.dev/python/docs/test-runners
#
# pytest --browser firefox --base-url http://%K8S_HOSTNAME% [--headed --slowmo 1000]


def test_browser(page):
    # Go to <base-url>/, wait for redirect to login page
    page.goto("/")
    page.wait_for_url("/hub/login?next=%2Fhub%2F")

    # Fill username and password
    page.locator('input[name="username"]').fill("demo")
    page.locator('input[name="password"]').fill("anything")

    # Click "Sign in"
    page.locator('input:has-text("Sign in")').click()
    # page.wait_for_url("/hub/spawn-pending/*")

    # Server should be spawned, and should be redirected to JupyterLab
    page.wait_for_url("/user/demo/lab")
