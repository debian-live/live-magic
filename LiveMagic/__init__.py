
import gtk
import pygtk
pygtk.require('2.0')

import optparse

from LiveMagic import views, controllers

__version__ = '0.4'

class LiveMagic(object):

    def __init__(self, args):
        try:
            gtk.init_check()
        except RuntimeError, e:
            sys.exit('E: %s. Exiting.' % e)

        optparser = optparse.OptionParser(version=__version__)
        _, args = optparser.parse_args()

        c = controllers.Controller(args)
        v = views.View(c)

        c.ready()

        gtk.gdk.threads_init()
        gtk.main()
