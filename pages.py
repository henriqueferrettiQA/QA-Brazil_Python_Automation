from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

class UrbanRoutesPage:

        # Secao DE e PARA
        from_field = (By.ID, 'from')
        to_field = (By.ID, 'to')

        # Fluxo de chamada de taxi
        TAXI_OPTION = (By.XPATH, '//button[contains(., "Chamar")]')
        COMFORT_CARD = (By.XPATH, '//div[contains(@class,"tcard") and .//div[text()="Comfort"]]')
        COMFORT_ACTIVE = (By.XPATH, '//*[@id="root"]//div[contains(@class(),"active")]')


        def __init__(self, driver):
            self.driver = driver
            self.wait = WebDriverWait(driver, 10)


        # Metodos COR POM

        def _find(self, locator):
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )

        def _click(self, locator):
            self.wait.until(
                EC.element_to_be_clickable(locator)
            ).click()

        def _type(self, locator, text):
            element = self._find(locator)
            element.clear()
            element.send_keys(text)

        # Endereco

        def _get_text(self, locator):
            return self._find(locator).text

        def _get_value(self, locator):
            return self._find(locator).get_attribute('value')

        def enter_locations(self, from_text, to_text):
            self._type(self.from_field, from_text)
            self._type(self.to_field, to_text)

        def get_from_location(self):
            return self._get_value(self.from_field)

        def get_to_location(self):
            return self._get_value(self.to_field)

        # Chamar taxi

        def click_taxi_opition(self):
            self._click(self.TAXI_OPTION)

        def click_icon_comfort_selected(self):
            self.driver.find_element(*self.COMFORT_CARD).click()

        def is_comfort_card_active(self):
            try:
                element = self._find(self.COMFORT_CARD)
                classes = element.get_attribute("class")
                print("CLASSES:", classes)
                return "active" in classes
            except Exception as e:
                print("Erro ao verificar estado:", e)
                return False