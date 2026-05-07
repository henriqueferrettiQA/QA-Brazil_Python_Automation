from html.parser import commentclose

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import helpers

class UrbanRoutesPage:

        # Secao DE e PARA
        from_field = (By.ID, 'from')
        to_field = (By.ID, 'to')

        # Fluxo de chamada de taxi
        TAXI_OPTION = (By.XPATH, '//button[contains(., "Chamar")]')
        COMFORT_CARD = (By.XPATH, '//div[contains(@class,"tcard") and .//div[text()="Comfort"]]')
        COMFORT_ACTIVE = (By.XPATH, '//*[@id="root"]//div[contains(@class,"active")]')


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
            if not self.is_comfort_card_active():
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

        # Preencher o número de telefone

        # Telefone
        PHONE_BUTTON = (By.XPATH, '//div[contains(@class,"np-button")][.//*[contains(text(),"Número de telefone")]]')
        PHONE_INPUT = (By.ID, 'phone')
        PHONE_NEXT_BUTTON = (By.XPATH, '//button[contains(.,"Próximo")]')
        SMS_CONFIRM_BUTTON = (By.XPATH, '//button[contains(.,"Confirmar")]')

        def fill_phone_number(self, phone_number):
            print("Abrindo telefone...")

            self._click(self.PHONE_BUTTON)

            phone_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "phone"))
            )
            phone_input.clear()
            phone_input.send_keys(phone_number)

            print("Número preenchido")

            self._click(self.PHONE_NEXT_BUTTON)

            print("Tela de SMS aberta")

            sms_input = self.wait.until(
                lambda driver: next(
                    (
                        el for el in driver.find_elements(By.TAG_NAME, "input")
                        if el.is_displayed() and el.is_enabled()
                    ),
                    None
                )
            )

            print("Input SMS encontrado")

            code = helpers.retrieve_phone_code(self.driver)
            print("Código SMS:", code)

            sms_input.clear()
            sms_input.send_keys(code)

            self._click(self.SMS_CONFIRM_BUTTON)

            return code

        # Cartão
        PAYMENT_METHOD_BUTTON = (By.XPATH,
                                 '//div[contains(@class,"pp-button")][.//*[contains(text(),"Método de pagamento")]]')
        ADD_CARD_BUTTON = (By.XPATH, '//div[contains(@class,"pp-plus-container")]')
        CARD_NUMBER_INPUT = (By.ID, 'number')
        CARD_CODE_INPUT = (By.ID, 'code')
        LINK_CARD_BUTTON = (By.XPATH, '//button[contains(.,"Adicionar")]')
        CLOSE_PAYMENT_MODAL = (By.XPATH, '//button[contains(@class,"close-button")]')

        def fill_card(self, card_number, card_code):
            print("Abrindo método de pagamento...")

            self._click(self.PAYMENT_METHOD_BUTTON)

            print("Clicando em adicionar cartão...")

            self._click(self.ADD_CARD_BUTTON)

            inputs = self.wait.until(
                lambda driver: [
                    el for el in driver.find_elements(By.TAG_NAME, "input")
                    if el.is_displayed() and el.is_enabled()
                ]
            )

            number_input = inputs[0]
            code_input = inputs[1]

            number_input.clear()
            number_input.send_keys(card_number)

            code_input.click()
            code_input.send_keys(card_code)
            self.driver.find_element(By.TAG_NAME, "body").click()

            print("Cartão preenchido")

            self._click(self.LINK_CARD_BUTTON)

            print("Cartão adicionado")

            return True

        # Comentário motorista
        COMMENT_INPUT = (
            By.XPATH,
            '//input[contains(@placeholder,"Comentário")]'
        )

        def fill_comment_for_driver(self, message):
            print("Procurando campo de comentário...")

            comment = self.wait.until(
                lambda driver: next(
                    (
                        el for el in driver.find_elements(By.TAG_NAME, "input")
                        if el.is_displayed()
                           and el.is_enabled()
                           and el.get_attribute("value") == ""
                           and el.get_attribute("id") not in ["from", "to"]
                    ),
                    None
                )
            )

            comment.clear()
            comment.send_keys(message)

            print("Comentário preenchido")

            return comment.get_attribute("value")

        # Cobertor e lenços
        BLANKET_SWITCH = (
            By.XPATH,
            '//div[contains(.,"Cobertor") or contains(.,"Lenços")]//span[contains(@class,"slider")]'
        )

        BLANKET_SWITCH_ACTIVE = (
            By.XPATH,
            '//div[contains(.,"Cobertor") or contains(.,"Lenços")]//input[@checked]'
        )

        # Sorvete
        ICE_CREAM_PLUS = (
            By.XPATH,
            '(//div[contains(@class,"counter-plus")])[1]'
        )

        ICE_CREAM_VALUE = (
            By.XPATH,
            '(//div[contains(@class,"counter-value")])[1]'
        )

        # Pedir taxi
        # Pedido do táxi
        ORDER_TAXI_BUTTON = (
            By.XPATH,
            '//button[contains(.,"Pedir")]'
        )

        CAR_SEARCH_MODAL = (
            By.XPATH,
            '//*[contains(text(),"Buscar carro") or contains(text(),"Procurando carro")]'
        )

        def order_blanket_and_handkerchiefs(self):
            container = self.wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//*[contains(text(),"Cobertor") or contains(text(),"Lenços")]'
                    )
                )
            )

            switch = container.find_element(
                By.XPATH,
                './/following::span[contains(@class,"slider")][1]'
            )

            self.driver.execute_script(
                "arguments[0].click();",
                switch
            )

            time.sleep(3)

            return True

        def order_2_ice_creams(self):
            for _ in range(2):
                self._click(self.ICE_CREAM_PLUS)

            return self._find(self.ICE_CREAM_VALUE).text

        def order_taxi_and_wait_search_modal(self):
            print("Pedindo táxi...")

            order_button = self.wait.until(
                lambda driver: next(
                    (
                        btn for btn in driver.find_elements(By.TAG_NAME, "button")
                        if btn.is_displayed()
                           and btn.is_enabled()
                           and "Pedir" in btn.text
                    ),
                    None
                )
            )

            self.driver.execute_script("arguments[0].click();", order_button)

            modal = self.wait.until(
                lambda driver: next(
                    (
                        el for el in
                    driver.find_elements(By.XPATH, '//*[contains(text(),"Buscar") or contains(text(),"Procurando")]')
                        if el.is_displayed()
                    ),
                    None
                )
            )

            print("Modal de busca apareceu")

            return modal


















      









    


