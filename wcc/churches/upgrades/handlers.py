from collective.grok import gs
from Products.CMFCore.utils import getToolByName
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.churches to 1003',
                description=u'Upgrade wcc.churches to 1003',
                source='1002', destination='1003',
                sortkey=1, profile='wcc.churches:default')
def to1003(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.churches.upgrades:to1003')


@gs.upgradestep(title=u'Upgrade wcc.churches to 1002',
                description=u'Upgrade wcc.churches to 1002',
                source='1', destination='1002',
                sortkey=1, profile='wcc.churches:default')
def to1002(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.churches.upgrades:to1002')
    catalog = getToolByName(context, 'portal_catalog')
    catalog.clearFindAndRebuild()
    intids = getUtility(IIntIds)

    for brain in catalog(Language='all'):
        try:
            obj = brain.getObject()
            intids.register(obj)
        except (AttributeError, KeyError):
            pass
