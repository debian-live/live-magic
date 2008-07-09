
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

        parser = optparse.OptionParser(version=__version__)
        parser.add_option('--build-for', dest='build_for',
            metavar='owner:group', help="Perform build on behalf of owner:group. "
            "This option is used internally.")
        parser.add_option('--kde-full-session', dest='kde_full_session',
            metavar='', help="Value of KDE_FULL_SESSION. "
            "This option is used internally.")
        parser.add_option('--gnome-desktop-session-id', dest='gnome_desktop_session_id',
            metavar='', help="Value of GNOME_DESKTOP_SESSION_ID. "
            "This option is used internally.")
        options, args = parser.parse_args()

        c = controllers.Controller()
        v = views.View(c)

        c.ready(options, args)

        gtk.gdk.threads_init()
        gtk.main()
