# Copyright 2020 by John A Kline <john@johnkline.com>
# Copyright 2022 Dirk Husemann
# Distributed under the terms of the GNU Public License (GPLv3)
# See LICENSE for your rights.

import sys
import weewx

from setup import ExtensionInstaller


def loader():
    if sys.version_info[0] < 3 or (sys.version_info[0] == 3
                                   and sys.version_info[1] < 9):
        sys.exit("weewx-mastodon requires python 3.9 or later, found %s.%s" % (
            sys.version_info[0], sys.version_info[1]))

    if weewx.__version__ < "4":
        sys.exit("weewx-mastodon requires WeeWX 4, found %s" %
                 weewx.__version__)
    return MastodonReporterInstaller()


class MastodonReporterInstaller(ExtensionInstaller):
    def __init__(self):
        super(MastodonReporterInstaller, self).__init__(
            version='1.0.1',
            name='mastodon',
            description='Skin for the mastodon reporter',
            author='Dirk Husemann',
            author_email='dr_who@d2h.net',
            config={
                'StdReport': {
                    'mastodon': {
                        'skin': 'mastodon',
                        'enable': 'true',
                        'HTML_ROOT': 'replace with mastodon destination path',
                        'access_token': 'insert access token from mastodon here',
                        'api_base_url': 'base URL of your mastodon instance',
                    }
                }
            },
            files=[('skins/mastodon',
                    ['skins/mastodon/toot.tmpl',
                     'skins/mastodon/skin.conf']),
                   ('bin/user', ['bin/user/mastodonreporter.py'])
                   ]
        )
