# -*- coding: utf-8 -*-
"""
EPUB Workflow Plugin for Calibre
Plugin d'automatisation pour le traitement d'EPUB avec menu interactif, traitement batch et balayage récursif
"""

__license__ = 'GPL v3'
__copyright__ = '2025'
__version__ = (1, 0, 0)
__docformat__ = 'restructuredtext en'

# The class that all Interface Action plugin wrappers must inherit from
from calibre.customize import InterfaceActionBase

# pulls in translation files for _() strings
try:
    load_translations()
except NameError:
    pass  # load_translations() added in calibre 1.9

## Apparently the name for this class doesn't matter.
class EPUBWorkflowBase(InterfaceActionBase):
    '''
    This class is a simple wrapper that provides information about the
    actual plugin class. The actual interface plugin class is called
    EPUBWorkflowPlugin and is defined in the plugin.py file, as
    specified in the actual_plugin field below.

    The reason for having two classes is that it allows the command line
    calibre utilities to run without needing to load the GUI libraries.
    '''
    name                = 'EPUB Workflow'
    description         = 'EPUB automation plugin with interactive menu, batch processing and recursive scanning. Author: u/iamkxrz on Reddit'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Florent Bertiaux (u/iamkxrz)'
    version             = (1, 0, 0)
    minimum_calibre_version = (6, 0, 0)

    #: This field defines the GUI plugin class that contains all the code
    #: that actually does something. Its format is module_path:class_name
    #: The specified class must be defined in the specified module.
    actual_plugin       = 'calibre_plugins.epub_workflow.plugin:EPUBWorkflowPlugin'

    def is_customizable(self):
        '''
        This method must return True to enable customization via
        Preferences->Plugins
        '''
        return False  # Pas de configuration pour l'instant

# Point d'entrée pour Calibre
load_plugin = EPUBWorkflowBase

