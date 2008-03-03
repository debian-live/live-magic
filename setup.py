#!/usr/bin/env python

from distutils.core import setup

setup(
    name='live-magic',
    version='0.3',
    maintainer = "Chris Lamb",
    maintainer_email = "chris@chris-lamb.co.uk",
    description = "GTK+ frontend for configuring Debian Live systems",
    license = "GNU GPL v3",
    scripts = ['live-magic'],
    packages= [
        'LiveMagic',
        'LiveMagic.controllers',
        'LiveMagic.models',
        'LiveMagic.views',
    ],
    data_files = [
        ('share/live-magic', [
            'glade/main.glade',
            'glade/debian_openlogo-nd-100.png',
            'glade/debian_sm.png',
            'glade/gnome-logo-icon-transparent.png',
            'glade/kde.png',
            'glade/world_map-960.png',
            'glade/xfce.png',
            ]),
        ('share/applications', [
            'misc/live-magic.desktop'
        ]),
    ]
)
