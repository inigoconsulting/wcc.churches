from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable
from five import grok
from collective.grok import gs
from zope.i18nmessageid import MessageFactory
from plone.registry.interfaces import IRegistry
from wcc.churches.interfaces import IWccChurchSettings
from zope.component import getUtility

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('wcc.churches')

_ = MessageFactory

class HiddenProducts(grok.GlobalUtility):
    """This hides the upgrade profiles from the quick installer tool."""
    implements(INonInstallable)
    grok.name('wcc.churches.upgrades')

    def getNonInstallableProducts(self):
        return [
            'wcc.churches.upgrades',
        ]

gs.profile(name=u'default',
           title=u'wcc.churches',
           description=_(u''),
           directory='profiles/default')

def getSettings():
    registry = getUtility(IRegistry)
    try:
        return registry.forInterface(IWccChurchSettings)
    except:
        registry.registerInterface(IWccChurchSettings)
    return registry.forInterface(IWccChurchSettings)

