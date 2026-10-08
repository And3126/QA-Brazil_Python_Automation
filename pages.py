from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import helpers


class UrbanRoutesPage:
    # --- Localizadores ---
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(text(),'Chamar')]")
    COMFORT_PLAN = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']")
    COMFORT_PLAN_CARD = (By.XPATH, "//div[@class='tcard-title' and text()='Comfort']/ancestor::div[contains(@class,'tcard')]")

    PHONE_BUTTON = (By.CLASS_NAME, 'np-button')
    PHONE_INPUT = (By.ID, 'phone')
    PHONE_NEXT_BUTTON = (By.XPATH, "//button[contains(@class,'button full')][text()='Próximo']")
    SMS_CODE_INPUT = (By.XPATH, "//div[@class='section active']//input[@id='code']")
    SMS_CONFIRM_BUTTON = (By.XPATH, "//button[text()='Confirmar']")

    PAYMENT_BUTTON = (By.CLASS_NAME, 'pp-button')
    ADD_CARD_OPTION = (By.XPATH, "//div[@class='pp-title' and text()='Adicionar cartão']")
    CARD_NUMBER_INPUT = (By.ID, 'number')
    CARD_CVV_INPUT = (By.XPATH, "//div[@class='card-code-input']/input[@id='code']")
    CARD_LINK_BUTTON = (By.XPATH, "//button[text()='Adicionar']")
    PAYMENT_CLOSE_BUTTON = (By.XPATH, "//div[@class='payment-picker open']//button[@class='close-button section-close']")
    PAYMENT_METHOD_TEXT = (By.CLASS_NAME, 'pp-value-text')

    COMMENT_INPUT = (By.ID, 'comment')
    BLANKET_SWITCH = (By.CSS_SELECTOR, ".switch")
    BLANKET_CHECKBOX = (By.CSS_SELECTOR, ".switch-input")
    ICE_CREAM_PLUS = (By.XPATH, "//div[text()='Sorvete']/ancestor::div[@class='r-group-items']//div[@class='counter-plus']")
    ICE_CREAM_COUNT = (By.XPATH, "//div[text()='Sorvete']/ancestor::div[@class='r-group-items']//div[@class='counter-value']")

    ORDER_BUTTON = (By.CLASS_NAME, 'smart-button-main')
    ORDER_MODAL_TITLE = (By.CLASS_NAME, 'order-header-title')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Rota
    def set_from(self, address):
        self.wait.until(EC.visibility_of_element_located(self.FROM_FIELD)).send_keys(address)

    def set_to(self, address):
        self.wait.until(EC.visibility_of_element_located(self.TO_FIELD)).send_keys(address)

    def get_from(self):
        return self.driver.find_element(*self.FROM_FIELD).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.TO_FIELD).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    # Tarifa
    def click_call_taxi(self):
        self.wait.until(EC.element_to_be_clickable(self.CALL_TAXI_BUTTON)).click()

    def select_comfort_plan(self):
        self.wait.until(EC.element_to_be_clickable(self.COMFORT_PLAN)).click()

    def is_comfort_selected(self):
        card = self.wait.until(EC.presence_of_element_located(self.COMFORT_PLAN_CARD))
        return 'active' in card.get_attribute('class')

    # Telefone
    def set_phone(self, phone):
        self.wait.until(EC.element_to_be_clickable(self.PHONE_BUTTON)).click()
        phone_input = self.wait.until(EC.visibility_of_element_located(self.PHONE_INPUT))
        phone_input.send_keys(phone.replace(' ', ''))  # sem espaços: a máscara do campo formata sozinha
        self.wait.until(EC.element_to_be_clickable(self.PHONE_NEXT_BUTTON)).click()
        code_input = self.wait.until(EC.visibility_of_element_located(self.SMS_CODE_INPUT))
        code = helpers.retrieve_phone_code(self.driver)
        code_input.send_keys(code)
        self.driver.find_element(*self.SMS_CONFIRM_BUTTON).click()

    def get_phone(self):
        return self.wait.until(EC.visibility_of_element_located(self.PHONE_BUTTON)).text

    # Cartão
    def add_card(self, number, cvv):
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.ADD_CARD_OPTION)).click()
        number_input = self.wait.until(EC.visibility_of_element_located(self.CARD_NUMBER_INPUT))
        number_input.send_keys(number)
        cvv_input = self.driver.find_element(*self.CARD_CVV_INPUT)
        cvv_input.send_keys(cvv)
        cvv_input.send_keys(Keys.TAB)
        self.wait.until(EC.element_to_be_clickable(self.CARD_LINK_BUTTON)).click()
        self.wait.until(EC.element_to_be_clickable(self.PAYMENT_CLOSE_BUTTON)).click()

    def get_payment_method(self):
        return self.driver.find_element(*self.PAYMENT_METHOD_TEXT).text

    # Comentário
    def set_comment(self, message):
        self.wait.until(EC.visibility_of_element_located(self.COMMENT_INPUT)).send_keys(message)

    def get_comment(self):
        return self.driver.find_element(*self.COMMENT_INPUT).get_property('value')

    # Extras
    def order_blanket(self):
        switch = self.wait.until(EC.presence_of_element_located(self.BLANKET_SWITCH))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", switch)
        self.wait.until(EC.element_to_be_clickable(self.BLANKET_SWITCH)).click()

    def is_blanket_selected(self):
        return self.driver.find_element(*self.BLANKET_CHECKBOX).get_property('checked')

    def order_ice_creams(self, quantity=2):
        plus = self.wait.until(EC.element_to_be_clickable(self.ICE_CREAM_PLUS))
        for _ in range(quantity):  # o ciclo que estava no main.py agora vive aqui
            plus.click()

    def get_ice_cream_count(self):
        return int(self.driver.find_element(*self.ICE_CREAM_COUNT).text)

    # Pedido
    def click_order(self):
        self.wait.until(EC.element_to_be_clickable(self.ORDER_BUTTON)).click()

    def is_order_modal_visible(self):
        return self.wait.until(EC.visibility_of_element_located(self.ORDER_MODAL_TITLE)).is_displayed()