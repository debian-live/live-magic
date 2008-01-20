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
        LH_ROOT               : string
        LH_INCLUDES           : string
        LH_TEMPLATES          : string
        LH_BREAKPOINTS          : boolean
        LH_DEBUG                : boolean
        LH_FORCE                : boolean
        LH_QUIET                : boolean
        LH_VERBOSE              : boolean

    bootstrap:
        LH_ARCHITECTURE                       : list
        LH_BOOTSTRAP_CONFIG                   : string
        LH_BOOTSTRAP_FLAVOUR                  : string
        LH_BOOTSTRAP_KEYRING                  : string
        LH_DISTRIBUTION                       : string
        LH_MIRROR_BOOTSTRAP                   : string
        LH_MIRROR_BOOTSTRAP_SECURITY          : string
        LH_MIRROR_BINARY                      : string
        LH_MIRROR_BINARY_SECURITY             : string
        LH_SECTIONS                           : list

    chroot:
        LH_CHROOT_FILESYSTEM  : string
        LH_UNION_FILESYSTEM   : string
        LH_HOOKS              : list
        LH_INTERACTIVE        : boolean
        LH_KEYRING_PACKAGES   : list
        LH_LANGUAGE           : string
        LH_LINUX_FLAVOURS     : list
        LH_LINUX_PACKAGES     : list
        LH_PACKAGES           : list
        LH_PACKAGES_LISTS     : string
        LH_PRESEED            : string
        LH_TASKS              : list
        LH_SECURITY           : boolean
        LH_SYMLINKS           : boolean
        LH_SYSVINIT           : boolean

    binary:
        LH_BINARY_IMAGES      : string
        LH_BINARY_INDICES     : boolean
        LH_BOOTAPPEND         : string
        LH_BOOTLOADER         : string
        LH_DEBIAN_INSTALLER   : boolean
        LH_ENCRYPTION         : string
        LH_GRUB_SPLASH        : string
        LH_HOSTNAME           : string
        LH_ISO_APPLICATION    : string
        LH_ISO_PREPARER       : string
        LH_ISO_PUBLISHER      : string
        LH_ISO_VOLUME         : string
        LH_MEMTEST            : string
        LH_NET_PATH           : string
        LH_NET_SERVER         : string
        LH_SYSLINUX_SPLASH    : string
        LH_USERNAME           : string

    source:
        LH_SOURCE             : boolean
        LH_SOURCE_IMAGES      : list

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
