#!/usr/bin/env python

from distutils.core import setup

setup(
    name='live-magic',
    version='0.4',
    maintainer = "Chris Lamb",
    maintainer_email = "chris@chris-lamb.co.uk",
    description = "GTK+ frontend for configuring Debian Live systems",
    license = "GNU GPL v3",
    scripts = ['live-magic'],
    packages= [
        'LiveMagic',
        'LiveMagic.views',
        'LiveMagic.controllers',
        'DebianLive',
        'DebianLive.elements',
        'DebianLive.utils',
    ],
    data_files = [
        ('share/live-magic', [
            'misc/live-magic-builder',
            'misc/live-magic.glade',
            'misc/debian_openlogo-nd-100.png',
            'misc/debian_sm.png',
            'misc/gnome-logo-icon-transparent.png',
            'misc/kde.png',
            'misc/xfce.png',
            ]),
        ('share/applications', [
            'misc/live-magic.desktop'
        ]),
    ]
)
