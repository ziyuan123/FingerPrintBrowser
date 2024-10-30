from library.auto_web_lib.auto_web_operator import AutoWebOperator

def run_action(driver, account_info):
    auto_web_op = AutoWebOperator(driver)
    auto_web_op.driver.get("https://x.com/home")

    user_name_input = '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input'
    if auto_web_op.wait_find_xpath(user_name_input):
        auto_web_op.get_element(user_name_input).send_keys("123")
    input()