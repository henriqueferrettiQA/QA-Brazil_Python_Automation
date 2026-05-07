import data
import helpers
import time

from pages  import UrbanRoutesPage
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestUrbanRoutes:
    @classmethod
    def setup_class(cls):
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        cls.driver = Chrome(options=options)
        cls.driver.implicitly_wait(5)

        if helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            print('Conectado ao servidor Urban Routes')
        else:
            print('Não foi possível conectar ao Urban Routes.')

    def setup_method(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.page = UrbanRoutesPage(self.driver)


    def test_set_route(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.page.get_from_location() == data.ADDRESS_FROM
        assert self.page.get_to_location() == data.ADDRESS_TO


    def test_order_2_ice_creams(self):
        self.page.enter_locations(
            data.ADDRESS_FROM,
            data.ADDRESS_TO
        )

        self.page.click_taxi_opition()

        self.page.click_icon_comfort_selected()

        value = self.page.order_2_ice_creams()

        assert value == "2"


    import data

    def test_select_plan(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_taxi_opition()
        self.page.click_icon_comfort_selected()
        assert self.page.is_comfort_card_active()


    def test_fill_phone_number(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.click_taxi_opition()
        self.page.click_icon_comfort_selected()

        code = self.page.fill_phone_number(data.PHONE_NUMBER)

        assert code is not None




    def test_fill_card(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

        self.page.click_taxi_opition()

        # IMPORTANTE: selecionar plano primeiro
        self.page.click_icon_comfort_selected()

        result = self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)

        assert result is True


    def test_comment_for_driver(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

        self.page.click_taxi_opition()

        self.page.click_icon_comfort_selected()

        value = self.page.fill_comment_for_driver(
            data.MESSAGE_FOR_DRIVER
        )

        assert value == data.MESSAGE_FOR_DRIVER




    def test_order_blanket_and_handkerchiefs(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

        self.page.click_taxi_opition()

        self.page.click_icon_comfort_selected()

        result = self.page.order_blanket_and_handkerchiefs()


        assert result is True




    def test_car_search_model_appears(self):
        self.page.enter_locations(data.ADDRESS_FROM, data.ADDRESS_TO)

        self.page.click_taxi_opition()

        self.page.click_icon_comfort_selected()

        self.page.fill_phone_number(data.PHONE_NUMBER)

        self.page.fill_card(data.CARD_NUMBER, data.CARD_CODE)

        self.page.fill_comment_for_driver(data.MESSAGE_FOR_DRIVER)

        result = self.page.order_taxi_and_wait_search_modal()

        assert result is not None

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()




