from collective.grok import gs
from wcc.churches import MessageFactory as _

@gs.importstep(
    name=u'wcc.churches', 
    title=_('wcc.churches import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('wcc.churches.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
