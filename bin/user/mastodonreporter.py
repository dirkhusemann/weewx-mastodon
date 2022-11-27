#!/usr/bin/env python3

# System imports:
import logging
import os.path
import time

# WeeWX imports:
import weeutil.config
import weewx.defaults
import weewx.manager
import weewx.units
from weeutil.weeutil import to_bool, to_int
from weewx.reportengine import ReportGenerator

import mastodon

log = logging.getLogger(__name__)

VERSION = "1.0.1"

if weewx.__version__ < "4":
    raise weewx.UnsupportedFeature("weewx 4 is required, found %s" %
                                   weewx.__version__)


# Following the FtpGenerator class from weewx
#
class MastodonReporter(ReportGenerator):
    '''MastondonReporter class for reporting a generated weather report to the #fediverse.
    '''

    def run(self):
        try:
            report_root = os.path.join(self.config_dict['WEEWX_ROOT'],
                                       self.skin_dict.get('HTML_ROOT'))
            toot_path = os.path.join(report_root, self.skin_dict.get('toot', 'toot'))

            access_token = self.skin_dict.get('access_token')
            api_base_uri = self.skin_dict.get('api_base_url')
            max_attempts = to_int(self.skin_dict.get('max_attempts', 3))
            reattempt_wait = to_int(self.skin_dict.get('reattempt_wait', 10))

            dry_run = to_bool(self.skin_dict.get('dry_run', False))
        except KeyError as ke:
            log.error(f'missing key: {ke}')
            return

        if not os.path.exists(toot_path):
            log.error(f'toot report "{toot_path}" not found.')
            return
            
        with open(toot_path, 'rt', encoding='utf8') as toot_file:
            toot_text = toot_file.read()

        try:
            masto = mastodon.Mastodon(api_base_url=api_base_uri,
                                      access_token=access_token)
        except mastodon.MastodonUnauthorizedError as mue:
            log.error(f'Mastondon authorization failed: {mue}')
            return

        ntries = 0
        while ntries < max_attempts:
            ntries += 1
            try:
                if not dry_run:
                    masto.status_post(status=toot_text,
                                      idempotency_key=str(int(t1)))
                else:
                    log.info(f'dry_running: {toot_text}')
            except mastodon.MastodonUnauthorizedError as mue:
                log.error(f'Mastondon authorization failed: {mue}')
            except (mastodon.MastodonError, mastodon.MastodonRatelimitError) as me:
                log.error(f'Failed attempt {ntries} of {max_attempts}: {me}')
                log.debug(f'Waiting {reattempt_wait} seconds before retry')
                time.sleep(reattempt_wait)
            return
        else:
            log.info(f'Max attempts {max_attempts} exceeded')
