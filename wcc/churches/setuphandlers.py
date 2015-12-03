from collective.grok import gs
from wcc.churches import MessageFactory as _
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from wcc.churches.interfaces import IWccChurchSettings

@gs.importstep(
    name=u'wcc.churches', 
    title=_('wcc.churches import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.churches.marker.txt') is None:
        return
    portal = context.getSite()
    registry = getUtility(IRegistry)
    registry.registerInterface(IWccChurchSettings)

    # do anything here
