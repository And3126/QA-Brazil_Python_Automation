import data
import helpers
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages import UrbanRoutesPage


class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        # Não modifique: o registro de desempenho é necessário para recuperar o código de confirmação do telefone
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print("Conectado ao servidor Urban Routes")
        else:
            print("Não foi possível conectar ao Urban Routes. Verifique se o servidor está ligado e ainda em execução.")

    def setup_method(self):
        # Antes de cada teste: abre a página do zero, para os testes serem independentes
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)

    def _prepare_ride(self):
        # Passos comuns para chegar ao estado em que as opções da corrida aparecem
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_call_taxi()
        self.page.select_comfort_plan()

    # 1. Definir o endereço
    def test_set_route(self):
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.page.get_from() == data.ADDRESS_FROM
        assert self.page.get_to() == data.ADDRESS_TO

    # 2. Selecionar o plano Comfort
    def test_select_plan(self):
        self._prepare_ride()
        assert self.page.is_comfort_selected()

    # 3. Preencher o número de telefone
    def test_fill_phone_number(self):
        self._prepare_ride()
        self.page.set_phone(data.PHONE_NUMBER)
        assert self.page.get_phone() == data.PHONE_NUMBER

    # 4. Adicionar um cartão de crédito
    def test_fill_card(self):
        self._prepare_ride()
        self.page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.get_payment_method() == 'Cartão'

    # 5. Escrever um comentário para o motorista
    def test_comment_for_driver(self):
        self._prepare_ride()
        self.page.set_comment(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_comment() == data.MESSAGE_FOR_DRIVER

    # 6. Pedir um cobertor e lenços
    def test_order_blanket_and_handkerchiefs(self):
        self._prepare_ride()
        self.page.order_blanket()
        assert self.page.is_blanket_selected()

    # 7. Pedir 2 sorvetes
    def test_order_2_ice_creams(self):
        self._prepare_ride()
        self.page.order_ice_creams(2)
        assert self.page.get_ice_cream_count() == 2

    # 8. Pedir o táxi com a tarifa Comfort (com mensagem para o motorista)
    def test_car_search_model_appears(self):
        self._prepare_ride()
        self.page.set_phone(data.PHONE_NUMBER)
        self.page.set_comment(data.MESSAGE_FOR_DRIVER)
        self.page.click_order()
        assert self.page.is_order_modal_visible()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()