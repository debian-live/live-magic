# -*- coding: utf-8 -*-
#
#   live-magic - GUI frontend to create Debian LiveCDs, etc.
#   Copyright (C) 2007-2010 Chris Lamb <lamby@debian.org>
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
        'LB_BINARY_FILESYSTEM': str,
        'LB_BINARY_IMAGES': list,
        'LB_BINARY_INDICES': bool,
        'LB_BOOTAPPEND_LIVE': str,
        'LB_BOOTAPPEND_INSTALL': str,
        'LB_BOOTLOADER': str,
        'LB_CHECKSUMS': bool,
        'LB_CHROOT_BUILD': bool,
        'LB_DEBIAN_INSTALLER': bool,
        'LB_DEBIAN_INSTALLER_DISTRIBUTION': str,
        'LB_DEBIAN_INSTALLER_PRESEEDFILE': str,
        'LB_ENCRYPTION': str,
        'LB_GRUB_SPLASH': str,
        'LB_HOSTNAME': str,
        'LB_ISO_APPLICATION': str,
        'LB_ISO_PREPARER': str,
        'LB_ISO_PUBLISHER': str,
        'LB_ISO_VOLUME': str,
        'LB_JFFS2_ERASEBLOCK': str,
        'LB_MEMTEST': str,
        'LB_WIN32_LOADER': bool,
        'LB_NET_ROOT_FILESYSTEM': str,
        'LB_NET_ROOT_MOUNTOPTIONS': str,
        'LB_NET_ROOT_PATH': str,
        'LB_NET_ROOT_SERVER': str,
        'LB_NET_COW_FILESYSTEM': str,
        'LB_NET_COW_MOUNTOPTIONS': str,
        'LB_NET_COW_PATH': str,
        'LB_NET_COW_SERVER': str,
        'LB_NET_TARBALL': str,
        'LB_SYSLINUX_SPLASH': str,
        'LB_SYSLINUX_TIMEOUT': int,
        'LB_SYSLINUX_CFG': str,
        'LB_SYSLINUX_MENU': bool,
        'LB_SYSLINUX_MENU_LIVE_ENTRY': str,
        'LB_SYSLINUX_MENU_LIVE_FAILSAFE_ENTRY': str,
        'LB_SYSLINUX_MENU_MEMTEST_ENTRY': str,
        'LB_USERNAME': str,
    }),

    'bootstrap': (KeyVar, {
        'LB_ARCHITECTURE': str,
        'LB_BOOTSTRAP_CONFIG': str,
        'LB_BOOTSTRAP_INCLUDE': str,
        'LB_BOOTSTRAP_EXCLUDE': str,
        'LB_BOOTSTRAP_FLAVOUR': str,
        'LB_BOOTSTRAP_KEYRING': str,
        'LB_DISTRIBUTION': str,
        'LB_MIRROR_BOOTSTRAP': str,
        'LB_MIRROR_CHROOT': str,
        'LB_MIRROR_CHROOT_SECURITY': str,
        'LB_MIRROR_BINARY': str,
        'LB_MIRROR_BINARY_SECURITY': str,
        'LB_CATEGORIES': list,
    }),

    'chroot': (KeyVar, {
        'LB_CHROOT_FILESYSTEM': str,
        'LB_UNION_FILESYSTEM': str,
        'LB_EXPOSED_ROOT': bool,
        'LB_HOOKS': list,
        'LB_INTERACTIVE': bool,
        'LB_KEYRING_PACKAGES': list,
        'LB_LANGUAGE': str,
        'LB_LINUX_FLAVOURS': list,
        'LB_LINUX_PACKAGES': list,
        'LB_PACKAGES': list,
        'LB_PACKAGES_LISTS': list,
        'LB_TASKS': str,
        'LB_SECURITY': bool,
        'LB_SYMLINKS': bool,
        'LB_SYSVINIT': bool,
    }),

    'common': (KeyVar, {
        'LB_APT': str,
        'LB_APT_FTP_PROXY': str,
        'LB_APT_HTTP_PROXY': str,
        'LB_APT_PDIFFS': bool,
        'LB_APT_PIPELINE': int,
        'LB_APT_RECOMMENDS': bool,
        'LB_APT_SECURE': bool,
        'LB_BOOTSTRAP': str,
        'LB_CACHE': bool,
        'LB_CACHE_INDICES': bool,
        'LB_CACHE_PACKAGES': bool,
        'LB_CACHE_STAGES': list,
        'LB_DEBCONF_FRONTEND': str,
        'LB_DEBCONF_NOWARNINGS': bool,
        'LB_DEBCONF_PRIORITY': str,
        'LB_INITRAMFS': str,
        'LB_FDISK': str,
        'LB_LOSETUP': str,
        'LB_MODE': str,
        'LB_USE_FAKEROOT': str,
        'LB_TASKSEL': str,
        'LB_INCLUDES': str,
        'LB_TEMPLATES': str,

        'LB_BREAKPOINTS': bool,
        'LB_DEBUG': bool,
        'LB_FORCE': bool,
        'LB_VERBOSE': bool,
        'LB_QUIET': bool,
    }),

   'source': (KeyVar, {
       'LB_SOURCE': bool,
       'LB_SOURCE_IMAGES': list,
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
