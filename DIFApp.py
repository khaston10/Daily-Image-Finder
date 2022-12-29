from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from DatabaseFunctions import *
import mysql.connector


# Define all screens.
class StartScreen(Screen):

    def login(self):
        self.parent.current = "login"
        self.parent.transition.direction = "left"
        return True

    def create_account(self):
        self.parent.current = "credential"
        self.parent.transition.direction = "up"
        return True


class LoginScreen(Screen):

    def home(self):
        self.parent.current = "start"
        self.parent.transition.direction = "right"

        # Clear text inputs from the login in screen.
        main_screen = self.manager.get_screen('login')
        main_screen.ids.email.text = ""
        main_screen.ids.password.text = ""

        # Clear text inputs from the credential in screen.
        main_screen = self.manager.get_screen('credential')
        main_screen.ids.new_email.text = ""
        main_screen.ids.password.text = ""

        # Clear text inputs from the main in screen.
        main_screen = self.manager.get_screen('main')
        main_screen.ids.key_word.text = ""
        main_screen.ids.new_keyword.text = ""
        return True

    def login(self, email, password):

        if check_if_credentials_are_correct(email, password):
            self.parent.current = "main"
            self.parent.transition.direction = "up"

        else:
            self.parent.current = "start"
            self.parent.transition.direction = "down"

        # Clear the text boxes
        #self.ids.email.text = ''
        #self.ids.password.text = ''

        # Set the keyword
        # Update the keyword from the main_screen
        main_screen = self.manager.get_screen('main')
        main_screen.ids.key_word.text = get_key_word(email)

        return True


class CredentialScreen(Screen):

    def home(self):
        self.parent.current = "start"
        self.parent.transition.direction = "right"

        # Clear text inputs from the login in screen.
        main_screen = self.manager.get_screen('login')
        main_screen.ids.email.text = ""
        main_screen.ids.password.text = ""

        # Clear text inputs from the credential in screen.
        main_screen = self.manager.get_screen('credential')
        main_screen.ids.new_email.text = ""
        main_screen.ids.password.text = ""

        # Clear text inputs from the main in screen.
        main_screen = self.manager.get_screen('main')
        main_screen.ids.key_word.text = ""
        main_screen.ids.new_keyword.text = ""
        return True

    def create_account(self):
        if add_credentials(self.ids.new_email.text, self.ids.password.text):
            # Update the email address on the login screen so the
            login_screen = self.manager.get_screen('login')
            login_screen.ids.email.text = self.ids.new_email.text
            # Update the keyword from the main_screen
            main_screen = self.manager.get_screen('main')
            main_screen.ids.key_word.text = get_key_word(self.ids.new_email.text)
            self.parent.current = "main"
            self.parent.transition.direction = "up"
        else:
            self.parent.current = "start"
            self.parent.transition.direction = "down"
        return True


class MainScreen(Screen):

    def home(self):
        self.parent.current = "start"
        self.parent.transition.direction = "right"

        # Clear text inputs from the login in screen.
        main_screen = self.manager.get_screen('login')
        main_screen.ids.email.text = ""
        main_screen.ids.password.text = ""

        # Clear text inputs from the credential in screen.
        main_screen = self.manager.get_screen('credential')
        main_screen.ids.new_email.text = ""
        main_screen.ids.password.text = ""

        # Clear text inputs from the main in screen.
        main_screen = self.manager.get_screen('main')
        main_screen.ids.key_word.text = ""
        main_screen.ids.new_keyword.text = ""
        return True

    def update_key_word(self):
        main_screen = self.manager.get_screen('login')
        email = main_screen.ids.email.text
        if update_key_word(email, self.ids.new_keyword.text):
            self.ids.key_word.text = self.ids.new_keyword.text
            self.ids.new_keyword.text = ""
        else:
            self.ids.new_keyword.text = ""


class WindowManager(ScreenManager):
    pass


# Designate where the format of the app will come from.
kv = Builder.load_file('DIF.kv')


class DifApp(App):
    def build(self):
        return kv


if __name__ == '__main__':
    DifApp().run()