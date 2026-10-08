import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):

        # não modifique, pois precisamos do registro adicional habilitado para recuperar o código de confirmação do telefone
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    # 1. Definir o endereço
    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        page = UrbanRoutesPage(self.driver)
        page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert page.get_from() == data.ADDRESS_FROM
        assert page.get_to() == data.ADDRESS_TO

    # 2. Selecionar o plano Comfort
    def test_select_plan(self):
        page = UrbanRoutesPage(self.driver)
        page.click_call_taxi()
        page.select_comfort_plan()
        assert page.is_comfort_selected()

    # 3. Preencher o número de telefone
    def test_fill_phone_number(self):
        page = UrbanRoutesPage(self.driver)
        page.set_phone(data.PHONE_NUMBER)
        assert page.get_phone() == data.PHONE_NUMBER

    # 4. Adicionar um cartão de crédito
    def test_fill_card(self):
        page = UrbanRoutesPage(self.driver)
        page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert page.get_payment_method() == 'Cartão'

    # 5. Escrever um comentário para o motorista
    def test_comment_for_driver(self):
        page = UrbanRoutesPage(self.driver)
        page.set_comment(data.MESSAGE_FOR_DRIVER)
        assert page.get_comment() == data.MESSAGE_FOR_DRIVER

    # 6. Pedir um cobertor e lenços
    def test_order_blanket_and_handkerchiefs(self):
        page = UrbanRoutesPage(self.driver)
        page.order_blanket()
        assert page.is_blanket_selected()

    # 7. Pedir 2 sorvetes
    def test_order_2_ice_creams(self):
        page = UrbanRoutesPage(self.driver)
        page.order_ice_creams(2)
        assert page.get_ice_cream_count() == 2

    # 8. Pedir o táxi com a tarifa Comfort (com mensagem para o motorista)
    def test_car_search_model_appears(self):
        page = UrbanRoutesPage(self.driver)
        if not page.get_comment():
            page.set_comment(data.MESSAGE_FOR_DRIVER)
        page.click_order()
        assert page.is_order_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()