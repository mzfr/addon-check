"""
    Copyright (C) 2018 Team Kodi
    This file is part of Kodi - kodi.tv

    SPDX-License-Identifier: GPL-3.0-only
    See LICENSES/README.md for more information.
"""

import gzip
import xml.etree.ElementTree as ET
from io import BytesIO

import requests

from .Addon import Addon


class Repository():
    """Get information of all the addons
    """
    def __init__(self, version, path):
        super().__init__()
        self.version = version
        self.path = path

        # Recover from unreliable mirrors
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=5)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        content = session.get(path, timeout=(30, 30)).content

        if path.endswith('.gz'):
            with gzip.open(BytesIO(content), 'rb') as xml_file:
                content = xml_file.read()

        tree = ET.fromstring(content)
        self.addons = []
        for addon in tree.findall("addon"):
            self.addons.append(Addon(addon))

    def __contains__(self, addonId):
        """Check if addon is present in the list or not

        Arguments:
            addonId {str} -- Id of addon that is to be looked for
        """
        for addon in self.addons:
            if addon.id == addonId:
                return True
        return False

    def find(self, addonId):
        """If the addon exists in the list then return it

        Arguments:
            addonId {str} -- Id of addon that is to be looked for
        """
        for addon in self.addons:
            if addon.id == addonId:
                return addon
        return None

    def rdepends(self, addonId):
        """Check if addon is dependent on any other addon.

        Arguments:
            addonId {str} -- Id of addon whose dependencies
                             are to be looked
        """
        rdepends = []
        for addon in self.addons:
            if addon.dependsOn(addonId):
                rdepends.append(addon)
        return rdepends
