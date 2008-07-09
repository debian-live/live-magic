from build import BuildController as Build
from main import MainController as Main
from hooks import HooksController as Hooks
from wizard import WizardController as Wizard

class Controller(Main, Build, Hooks, Wizard):
    def __init__(self):
        self.model = None

        Main.__init__(self)
        Build.__init__(self)
        Hooks.__init__(self)
        Wizard.__init__(self)
