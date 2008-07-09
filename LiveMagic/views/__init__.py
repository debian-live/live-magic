from build import BuildView as Build
from main import MainView as Main
from wizard import WizardView as Wizard

from LiveMagic.utils import find_resource

import gtk.glade

class View(Main, Build, Wizard):
    def __init__(self, controller):
        self.controller = controller

        self.xml = gtk.glade.XML(find_resource('live-magic.glade'))
        self.xml.signal_autoconnect(self.controller)

        Main.__init__(self)
        Build.__init__(self)
        Wizard.__init__(self)
