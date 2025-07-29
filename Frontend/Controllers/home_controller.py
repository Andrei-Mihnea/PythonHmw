# Controllers/home_controller.py
from Utils.decorators import login_required
class HomeController:
    @login_required
    def index(self):
        return "Welcome to Home!"

    @login_required
    def about(self):
        return "This is the about page."
