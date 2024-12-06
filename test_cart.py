import requests
import allure
from selene import browser, have, by

login_test = "abc1241@example.com"
password_test = "qwerty"
url = "https://demowebshop.tricentis.com"


# регистрируемся через API
def test_login_successful():
    with allure.step("Login"):
        response = requests.post(
            url=url + "/login",
            data={"Email": login_test, "Password": password_test, "RememberMe": False},
            allow_redirects=False
        )
    with allure.step("Verify successful authorization"):
        assert response.status_code == 302

    # получаем token в куках
    with allure.step("Get token"):
        token = response.cookies.get("NOPCOMMERCE.AUTH")

    # добавляем товары в корзину через API
    with allure.step("Add to shopping cart"):
        response = requests.post(url=url + "/addproducttocart/catalog/31/1/1", cookies={"NOPCOMMERCE.AUTH": token})
        assert response.status_code == 200

        response = requests.post(url=url + "/addproducttocart/catalog/52/1/1", cookies={"NOPCOMMERCE.AUTH": token})
        assert response.status_code == 200

    # передаем куки
    with allure.step("Get cookie"):
        browser.open("https://demowebshop.tricentis.com/cart")
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": token})
        browser.driver.refresh()

    # проверяем, что товар в корзине
    with allure.step("Check shopping cart"):
        browser.all(".product-name").should(have.exact_texts("14.1-inch Laptop", "Music 2"))

    # чистим корзину
    with allure.step("Check shopping cart"):
        browser.element(".remove-from-cart").click()
        browser.element(by.xpath("//input[@name='updatecart']")).click()
        browser.element(".remove-from-cart").click()
        browser.element(by.xpath("//input[@name='updatecart']")).click()
        browser.element(".page-body").should(have.text("Your Shopping Cart is empty!"))
