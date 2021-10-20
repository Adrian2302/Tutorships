from django.test import LiveServerTestCase
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium import webdriver


class IndexTest(LiveServerTestCase):

    @staticmethod
    def test_homePage() -> None:
        driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())
        driver.get('http://127.0.0.1:8000/')
        assert "P-I" in driver.title
