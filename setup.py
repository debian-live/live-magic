#!/usr/bin/env python

from distutils.core import setup

setup(
    name='live-magic',
    version='0.1',
    maintainer = "Chris Lamb",
    maintainer_email = "chris@chris-lamb.co.uk",
    description = "GTK+ frontend for configuring Debian Live systems",
    license = "GNU GPL v2",
    scripts = ['live-magic'],
    packages= [
        'livemagic',
        'livemagic.controllers',
        'livemagic.model',
        'livemagic.views',
    ],
    data_files = [
        ('share/live-magic', [
            'glade/main.glade',
            'glade/debian_openlogo-nd-100.png',
            ])
        ]
)
