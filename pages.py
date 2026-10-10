from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import helpers


class UrbanRoutesPage:

    # Localizadores
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
    BLANKET_SWITCH = (By.CSS_SELECTOR, "span.slider.round")
    BLANKET_CHECKBOX = (By.XPATH, "//span[contains(@class,'slider')]/parent::*/input[@type='checkbox']")
    ICE_CREAM_PLUS = (By.XPATH, "//div[text()='Sorvete']/ancestor::div[@class='r-group-items']//div[@class='counter-plus']")
    ICE_CREAM_COUNT = (By.XPATH, "//div[text()='Sorvete']/ancestor::div[@class='r-group-items']//div[@class='counter-value']")

    ORDER_BUTTON = (By.CLASS_NAME, 'smart-button-main')
    ORDER_MODAL_TITLE = (By.CLASS_NAME, 'order-header-title')

    OVERLAY = (By.CSS_SELECTOR, 'div.overlay')

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Métodos privados de espera (centralizam WebDriverWait e EC)
    def _find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _present(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def _click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def _type(self, locator, text, clear=True):
        element = self._find(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def _wait_overlay_gone(self):
        self.wait.until(EC.invisibility_of_element_located(self.OVERLAY))

    # Rota
    def set_from(self, address):
        self._type(self.FROM_FIELD, address)

    def set_to(self, address):
        self._type(self.TO_FIELD, address)

    def get_from(self):
        return self._find(self.FROM_FIELD).get_property('value')

    def get_to(self):
        return self._find(self.TO_FIELD).get_property('value')

    def set_route(self, address_from, address_to):
        self.set_from(address_from)
        self.set_to(address_to)

    # Tarifa
    def click_call_taxi(self):
        self._click(self.CALL_TAXI_BUTTON)

    def is_comfort_selected(self):
        card = self._present(self.COMFORT_PLAN_CARD)
        return 'active' in card.get_attribute('class')

    def select_comfort_plan(self):
        if not self.is_comfort_selected():
            self._click(self.COMFORT_PLAN)

    # Telefone
    def set_phone(self, phone):
        self._click(self.PHONE_BUTTON)
        self._type(self.PHONE_INPUT, phone, clear=False)
        self._click(self.PHONE_NEXT_BUTTON)
        self._find(self.SMS_CODE_INPUT)
        code = helpers.retrieve_phone_code(self.driver)
        self._type(self.SMS_CODE_INPUT, code, clear=False)
        self._click(self.SMS_CONFIRM_BUTTON)
        self._wait_overlay_gone()

    def get_phone(self):
        return self._find(self.PHONE_BUTTON).text

    # Cartão
    def add_card(self, number, cvv):
        self._click(self.PAYMENT_BUTTON)
        self._click(self.ADD_CARD_OPTION)
        self._type(self.CARD_NUMBER_INPUT, number, clear=False)
        self._type(self.CARD_CVV_INPUT, cvv, clear=False)
        self._find(self.CARD_CVV_INPUT).send_keys(Keys.TAB)  # tira o foco do CVV para habilitar o botão "Adicionar"
        self._click(self.CARD_LINK_BUTTON)
        self._click(self.PAYMENT_CLOSE_BUTTON)
        self._wait_overlay_gone()

    def get_payment_method(self):
        return self._find(self.PAYMENT_METHOD_TEXT).text

    # Comentário
    def set_comment(self, message):
        self._type(self.COMMENT_INPUT, message)

    def get_comment(self):
        return self._find(self.COMMENT_INPUT).get_property('value')

    # Extras
    def order_blanket(self):
        self._click(self.BLANKET_SWITCH)

    def is_blanket_selected(self):
        return self._present(self.BLANKET_CHECKBOX).get_property('checked')

    def order_ice_creams(self, quantity=2):
        for _ in range(quantity):
            self._click(self.ICE_CREAM_PLUS)

    def get_ice_cream_count(self):
        return int(self._find(self.ICE_CREAM_COUNT).text)

    # Pedido
    def click_order(self):
        self._click(self.ORDER_BUTTON)

    def is_order_modal_visible(self):
        return self._find(self.ORDER_MODAL_TITLE).is_displayed()