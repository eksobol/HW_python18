import requests
import allure
from selene import browser, have, by

login_test = "abc1241@example.com"
password_test = "qwerty"
url = "https://demowebshop.tricentis.com"


# регистрируемся через API
def test_login_successful():
    with allure.step("Open Page"):
        response = requests.get(url + "/login")

    # получаем token в куках
    with allure.step("Get cookie"):
        notoken = response.cookies.get("Nop.customer")

    # добавляем товары в корзину через API
    with allure.step("Add to shopping cart"):
        response = requests.post(url=url + "/addproducttocart/catalog/31/1/1", cookies={"Nop.customer": notoken})
        assert response.status_code == 200

    # передаем куки
    with allure.step("Send cookie"):
        browser.open("https://demowebshop.tricentis.com/cart")
        browser.driver.add_cookie({"name": "Nop.customer", "value": notoken})
        browser.driver.refresh()

    # проверяем, что товар в корзине
    with allure.step("Check shopping cart"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))

    # чистим корзину
    with allure.step("Check shopping cart"):
        browser.element(".remove-from-cart").click()
        browser.element(by.xpath("//input[@name='updatecart']")).click()
        browser.element(".page-body").should(have.text("Your Shopping Cart is empty!"))
