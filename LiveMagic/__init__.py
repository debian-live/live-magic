
import gtk
import pygtk
pygtk.require('2.0')

import sys

from LiveMagic import views, controllers

class LiveMagic(object):

    def __init__(self, args):
        c = controllers.Controller(sys.argv[1:])
        v = views.View(c)

        c.ready()

        gtk.gdk.threads_init()
        gtk.main()
