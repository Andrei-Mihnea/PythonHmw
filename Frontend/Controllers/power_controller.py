from Utils.decorators import login_required
import os

class PowerController:
    @login_required
    def index(self):
        current_dir = os.path.dirname(__file__)
        template_path = os.path.join(current_dir, '..', 'Templates', 'power.html')
        template_path = os.path.abspath(template_path)

        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        return html

    @login_required
    def status(self):
        return "Power Status: All systems operational"