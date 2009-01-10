# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from DebianLive.elements import FolderOfFiles
from DebianLive.elements import KeyVar

spec = {
    'chroot_hooks': (FolderOfFiles, 'chroot_local-hooks'),
    'binary_hooks': (FolderOfFiles, 'binary_local-hooks'),

    'binary': (KeyVar, {
        'LH_BINARY_FILESYSTEM': str,
        'LH_BINARY_IMAGES': list,
        'LH_BINARY_INDICES': bool,
        'LH_BOOTAPPEND_LIVE': str,
        'LH_BOOTAPPEND_INSTALL': str,
        'LH_BOOTLOADER': str,
        'LH_CHECKSUMS': bool,
        'LH_CHROOT_BUILD': bool,
        'LH_DEBIAN_INSTALLER': bool,
        'LH_DEBIAN_INSTALLER_DISTRIBUTION': str,
        'LH_DEBIAN_INSTALLER_PRESEEDFILE': str,
        'LH_ENCRYPTION': str,
        'LH_GRUB_SPLASH': str,
        'LH_HOSTNAME': str,
        'LH_ISO_APPLICATION': str,
        'LH_ISO_PREPARER': str,
        'LH_ISO_PUBLISHER': str,
        'LH_ISO_VOLUME': str,
        'LH_JFFS2_ERASEBLOCK': str,
        'LH_MEMTEST': str,
        'LH_WIN32_LOADER': bool,
        'LH_NET_ROOT_FILESYSTEM': str,
        'LH_NET_ROOT_MOUNTOPTIONS': str,
        'LH_NET_ROOT_PATH': str,
        'LH_NET_ROOT_SERVER': str,
        'LH_NET_COW_FILESYSTEM': str,
        'LH_NET_COW_MOUNTOPTIONS': str,
        'LH_NET_COW_PATH': str,
        'LH_NET_COW_SERVER': str,
        'LH_NET_TARBALL': str,
        'LH_SYSLINUX_SPLASH': str,
        'LH_SYSLINUX_TIMEOUT': int,
        'LH_SYSLINUX_CFG': str,
        'LH_SYSLINUX_MENU': bool,
        'LH_SYSLINUX_MENU_LIVE_ENTRY': str,
        'LH_SYSLINUX_MENU_LIVE_FAILSAFE_ENTRY': str,
        'LH_SYSLINUX_MENU_MEMTEST_ENTRY': str,
        'LH_USERNAME': str,
    }),

    'bootstrap': (KeyVar, {
        'LH_ARCHITECTURE': str,
        'LH_BOOTSTRAP_CONFIG': str,
        'LH_BOOTSTRAP_INCLUDE': str,
        'LH_BOOTSTRAP_EXCLUDE': str,
        'LH_BOOTSTRAP_FLAVOUR': str,
        'LH_BOOTSTRAP_KEYRING': str,
        'LH_DISTRIBUTION': str,
        'LH_MIRROR_BOOTSTRAP': str,
        'LH_MIRROR_CHROOT': str,
        'LH_MIRROR_CHROOT_SECURITY': str,
        'LH_MIRROR_BINARY': str,
        'LH_MIRROR_BINARY_SECURITY': str,
        'LH_CATEGORIES': list,
    }),

    'chroot': (KeyVar, {
        'LH_CHROOT_FILESYSTEM': str,
        'LH_UNION_FILESYSTEM': str,
        'LH_EXPOSED_ROOT': bool,
        'LH_HOOKS': list,
        'LH_INTERACTIVE': bool,
        'LH_KEYRING_PACKAGES': list,
        'LH_LANGUAGE': str,
        'LH_LINUX_FLAVOURS': list,
        'LH_LINUX_PACKAGES': list,
        'LH_PACKAGES': list,
        'LH_PACKAGES_LISTS': list,
        'LH_TASKS': str,
        'LH_SECURITY': bool,
        'LH_SYMLINKS': bool,
        'LH_SYSVINIT': bool,
    }),

    'common': (KeyVar, {
        'LH_APT': str,
        'LH_APT_FTP_PROXY': str,
        'LH_APT_HTTP_PROXY': str,
        'LH_APT_PDIFFS': bool,
        'LH_APT_PIPELINE': int,
        'LH_APT_RECOMMENDS': bool,
        'LH_APT_SECURE': bool,
        'LH_BOOTSTRAP': str,
        'LH_CACHE': bool,
        'LH_CACHE_INDICES': bool,
        'LH_CACHE_PACKAGES': bool,
        'LH_CACHE_STAGES': list,
        'LH_DEBCONF_FRONTEND': str,
        'LH_DEBCONF_NOWARNINGS': bool,
        'LH_DEBCONF_PRIORITY': str,
        'LH_INITRAMFS': str,
        'LH_FDISK': str,
        'LH_LOSETUP': str,
        'LH_MODE': str,
        'LH_USE_FAKEROOT': str,
        'LH_TASKSEL': str,
        'LH_INCLUDES': str,
        'LH_TEMPLATES': str,

        'LH_BREAKPOINTS': bool,
        'LH_DEBUG': bool,
        'LH_FORCE': bool,
        'LH_VERBOSE': bool,
        'LH_QUIET': bool,
    }),

   'source': (KeyVar, {
       'LH_SOURCE': bool,
       'LH_SOURCE_IMAGES': list,
    }),
}

constructor_args = ('apt', 'apt-ftp-proxy', 'apt-http-proxy', 'apt-pdiffs',
    'apt-options', 'aptitude-options', 'apt-pipeline', 'apt-recommends',
    'apt-secure', 'architecture', 'binary-images', 'binary-filesystem',
    'binary-indices', 'bootappend-install', 'bootappend-live', 'bootloader',
    'bootstrap', 'bootstrap-config', 'bootstrap-flavour', 'bootstrap-keyring',
    'breakpoints', 'cache', 'cache-indices', 'cache-packages', 'cache-stages',
    'checksums', 'chroot-build', 'chroot-filesystem', 'color', 'conffile', 'debconf-frontend',
    'debconf-nowarnings', 'debconf-priority', 'debian-installer',
    'debian-installer-distribution', 'debian-installer-preseedfile',
    'distribution', 'encryption', 'fdisk', 'genisoimage',
    'grub-splash', 'hooks', 'hostname', 'ignore-system-defaults', 'includes', 'initramfs', 'interactive',
    'iso-application', 'iso-preparer', 'iso-publisher', 'iso-volume',
    'jffs2-eraseblock', 'keyring-packages', 'language', 'linux-flavours',
    'linux-packages', 'losetup', 'memtest', 'mirror', 'mirror-binary-security',
    'mirror-binary', 'mirror-bootstrap-security', 'mirror-bootstrap',
    'mirror-chroot', 'mirror-chroot-security', 'mode',
    'net-root-filesystem', 'net-root-mountoptions', 'net-root-path',
    'net-root-server', 'net-cow-filesystem', 'net-cow-mountoptions',
    'net-cow-path', 'net-cow-server', 'net-tarball', 'packages-lists', 'packages',
    'root-command', 'use-fakeroot', 'categories', 'security', 'source',
    'source-images', 'symlinks', 'syslinux-splash', 'syslinux-timeout',
    'syslinux-menu', 'sysvinit', 'tasksel', 'tasks', 'templates',
    'union-filesystem', 'exposed-root', 'username', 'win32-loader')
