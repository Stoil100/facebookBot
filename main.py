# # def solve_captcha(driver):
# #     solver = recaptchaV2Proxyless()
# #     solver.set_verbose(1)
# #     solver.set_key(captcha_api_key)
# #     solver.set_website_url(driver.current_url)
# #     solver.set_website_key("6Lc_aX0UAAAAA...")
# #
# #     g_response = solver.solve_and_return_solution()
# #     if g_response != 0:
# #         print(f"Captcha solved: {g_response}")
# #         driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{g_response}";')
# #         driver.execute_script('___grecaptcha_cfg.clients[0].l.l.callback("{g_response}");')
# #         time.sleep(5)
# #     else:
# #         print("CAPTCHA solving failed.")
# #

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Setup Chrome options
browser_options = Options()
# chrome_options.add_argument("--headless")  # Run in headless mode
browser_options.add_argument("--disable-gpu")
browser_options.add_argument("--window-size=1920x1080")

prefs = {
    "profile.default_content_setting_values.notifications": 2  # 2 - block, 1 - allow
}
browser_options.add_experimental_option("prefs", prefs)

# Path to your Browser
browser_options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
# Path to your ChromeDriver
chrome_driver_path = r'C:\Users\User\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe'

accounts = [
    {
        "email": "dromedromov@gmail.com",
        "password": "123456aA!",
        "groups": [
            "https://www.facebook.com/groups/998796888695197",
            "https://www.facebook.com/groups/902726761667546",
        ]
    },
]

post_link = "https://www.facebook.com/share/p/95hdrhRVbJ4Fo2HQ/"


def reject_cookies(driver):
    try:
        cookie_reject_button = driver.find_element(By.CSS_SELECTOR,
                                                   'div[aria-label="Decline optional cookies"][role="button"]')
        cookie_reject_button.click()
        time.sleep(2)
        print("Cookies rejected.")
    except Exception as e:
        print("No cookie consent screen found or failed to reject cookies:", e)


def login_facebook(driver, email, password):
    driver.get("https://www.facebook.com/login")
    time.sleep(random.uniform(3, 5))

    reject_cookies(driver)

    email_input = driver.find_element(By.ID, "email")
    email_input.clear()
    email_input.send_keys(email)

    password_input = driver.find_element(By.ID, "pass")
    password_input.clear()
    password_input.send_keys(password)

    login_button = driver.find_element(By.NAME, "login")
    login_button.click()
    time.sleep(random.uniform(5, 7))

    # Check for CAPTCHA
    if "captcha" in driver.current_url.lower():
        print("CAPTCHA detected. Please solve it manually in the browser window.")
        input("Press Enter after solving the CAPTCHA to continue...")


def share_post_to_group(driver, group_url, post_link):
    driver.get(group_url)
    time.sleep(random.uniform(5, 10))

    post_box_button = driver.find_element(By.CSS_SELECTOR,
                                          ".x6s0dn4.x78zum5.x1l90r2v.x1pi30zi.x1swvt13.xz9dl7a > span.x1emribx + div.x1i10hfl")
    post_box_button.click()
    time.sleep(random.uniform(2, 4))

    # When the post box is active, send the post link
    post_box = driver.switch_to.active_element
    post_box.send_keys(post_link)
    time.sleep(random.uniform(3, 5))

    post_button = driver.find_element(By.CSS_SELECTOR,
                                      '[aria-label="Post"][role="button"], [aria-label="Publicar"][role="button"]')
    post_button.click()
    time.sleep(random.uniform(5, 10))


def logout_facebook(driver):
    try:
        profile_icon = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Your profile"][role="button"]')
        profile_icon.click()
        time.sleep(random.uniform(2, 4))

        logout_button = driver.find_element(By.XPATH,
                                            '//span[contains(text(), "Log out") or contains(text(), "Log Out")]')
        logout_button.click()
        time.sleep(random.uniform(3, 5))
        print("Logged out successfully.")
    except Exception as e:
        print(f"Failed to log out: {e}")


def main():
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=browser_options)

    for account in accounts:
        try:
            login_facebook(driver, account['email'], account['password'])

            for idx, group_url in enumerate(account['groups']):
                if idx >= 10:  # Ensure the account only posts to a maximum of 10 groups
                    print(f"Reached the 10 group limit for {account['email']}")
                    break

                try:
                    share_post_to_group(driver, group_url, post_link)
                    time.sleep(random.uniform(5, 10))  # Rate limiting between posts
                except Exception as e:
                    print(f"Failed to post to group {group_url}: {e}")

            logout_facebook(driver)

        except Exception as e:
            print(f"Failed to login with {account['email']}: {e}")

    driver.quit()


if __name__ == "__main__":
    main()
