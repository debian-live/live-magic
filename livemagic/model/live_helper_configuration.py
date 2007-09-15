import commands
import tempfile
import yaml

from os.path import join, dirname

from key_var_config_file import KeyVarConfigFile
from folder_of_files import FolderOfFiles

spec_str = """
key_value:
    common:
        LH_APT                  : string
        LH_APT_FTPPROXY         : string
        LH_APT_HTTPPROXY        : string
        LH_APT_PDIFFS           : boolean
        LH_APT_PIPELINE         : int
        LH_APT_RECOMMENDS       : boolean
        LH_APT_SECURE           : boolean
        LH_BOOTSTRAP            : string
        LH_CACHE_INDICES        : boolean
        LH_CACHE_PACKAGES       : boolean
        LH_CACHE_STAGES         : list
        LH_DEBCONF_FRONTEND     : string
        LH_DEBCONF_NOWARNINGS   : boolean
        LH_DEBCONF_PRIORITY     : string
        LH_GENISOIMAGE          : string
        LH_INITRAMFS            : string
        LH_LOSETUP              : string
        LH_MODE                 : string
        LH_ROOT_COMMAND         : string
        LH_TASKSEL              : string
        LIVE_ROOT               : string
        LIVE_INCLUDES           : string
        LIVE_TEMPLATES          : string
        LH_BREAKPOINTS          : boolean
        LH_DEBUG                : boolean
        LH_FORCE                : boolean
        LH_QUIET                : boolean
        LH_VERBOSE              : boolean

    bootstrap:
        LIVE_ARCHITECTURE                       : list
        LIVE_BOOTSTRAP_CONFIG                   : string
        LIVE_BOOTSTRAP_FLAVOUR                  : string
        LIVE_BOOTSTRAP_KEYRING                  : string
        LIVE_DISTRIBUTION                       : string
        LIVE_MIRROR_BOOTSTRAP                   : string
        LIVE_MIRROR_BOOTSTRAP_SECURITY          : string
        LIVE_MIRROR_BINARY                      : string
        LIVE_MIRROR_BINARY_SECURITY             : string
        LIVE_SECTIONS                           : list

    chroot:
        LIVE_CHROOT_FILESYSTEM  : string
        LIVE_UNION_FILESYSTEM   : string
        LIVE_HOOKS              : list
        LIVE_INTERACTIVE        : boolean
        LIVE_KEYRING_PACKAGES   : list
        LIVE_LANGUAGE           : string
        LIVE_LINUX_FLAVOURS     : list
        LIVE_LINUX_PACKAGES     : list
        LIVE_PACKAGES           : list
        LIVE_PACKAGES_LISTS     : string
        LIVE_PRESEED            : string
        LIVE_TASKS              : list
        LIVE_SECURITY           : boolean
        LIVE_SYMLINKS           : boolean
        LIVE_SYSVINIT           : boolean

    binary:
        LIVE_BINARY_IMAGES      : string
        LIVE_BINARY_INDICES     : boolean
        LIVE_BOOTAPPEND         : string
        LIVE_BOOTLOADER         : string
        LIVE_DEBIAN_INSTALLER   : boolean
        LIVE_ENCRYPTION         : string
        LIVE_GRUB_SPLASH        : string
        LIVE_HOSTNAME           : string
        LIVE_ISO_APPLICATION    : string
        LIVE_ISO_PREPARER       : string
        LIVE_ISO_PUBLISHER      : string
        LIVE_ISO_VOLUME         : string
        LIVE_MEMTEST            : string
        LIVE_NET_PATH           : string
        LIVE_NET_SERVER         : string
        LIVE_SYSLINUX_SPLASH    : string
        LIVE_USERNAME           : string

    source:
        LIVE_SOURCE             : boolean
        LIVE_SOURCE_IMAGES      : list

folder_of_files:
    chroot_local-hooks
"""

class LiveHelperConfiguration(object):
    """
    Represents a configuration for a Debian Live system.
    """

    def __init__(self, confdir=None):
        self._load_observers = []
        self.first_load = True

        self.spec = yaml.load(spec_str)

        if confdir is None:
            self.new()
        else:
            self.open(dir)

    def new(self):
        """
        Creates and initialises a new configuration in a temporary folder.
        """
        self.dir = tempfile.mkdtemp('live-magic')
        res, out = commands.getstatusoutput('cd %s; lh_config' % self.dir)
        if res != 0: raise IOError, out
        self._load()

    def open(self, dir):
        """
        Discards the current configuration, and then loads and initialises
        the configuration from the specified directory.
        """
        self.dir = dir
        self._load()

    def reload(self):
        """
        Reloads the current configuration.
        """
        self._load()

    def save(self):
        """
        Saves the current configuration.
        """
        for conf in self.children:
            conf.save()

    def altered(self):
        """
        Returns True if the state of the configuration has changed since last save.
        """
        for conf in self.children:
            if conf.altered() == True:
                return True
        return False

    def _load(self):
        self.children = []
        for filename, spec in self.spec['key_value'].iteritems():
            kv = KeyVarConfigFile(join(self.dir, 'config', filename), spec)
            self.children.append(kv)
            setattr(self, filename, kv)

        # chroot_local-hooks
        fof_hooks = FolderOfFiles(join(self.dir, 'config', 'chroot_local-hooks'))
        setattr(self, 'hooks', fof_hooks)
        self.children.append(fof_hooks)

        # Notify all the observers, but avoid double load when the view is ready
        if not self.first_load:
            self.notify_load_observers()
        self.first_load = False

    def notify_load_observers(self):
        """
        Notify all the registered observers that we have reloaded.
        """
        map(apply, self._load_observers)

    def attach_load_observer(self, fn):
        self._load_observers.append(fn)
