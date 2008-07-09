from build import BuildController as Build
from main import MainController as Main
from wizard import WizardController as Wizard

class Controller(Main, Build, Wizard):
    def __init__(self):
        self.model = None

        Main.__init__(self)
        Build.__init__(self)
        Wizard.__init__(self)
