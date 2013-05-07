from collective.grok import gs
from Products.CMFCore.utils import getToolByName
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from zc.relation.interfaces import ICatalog
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from z3c.relationfield.event import _relations, updateRelations
from zope.globalrequest import getRequest

# -*- extra stuff goes here -*- 


@gs.upgradestep(title=u'Upgrade wcc.churches to 1006',
                description=u'Upgrade wcc.churches to 1006',
                source='1005', destination='1006',
                sortkey=1, profile='wcc.churches:default')
def to1006(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.churches.upgrades:to1006')

    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexIndex('countries', getRequest())

@gs.upgradestep(title=u'Upgrade wcc.churches to 1005',
                description=u'Upgrade wcc.churches to 1005',
                source='1004', destination='1005',
                sortkey=1, profile='wcc.churches:default')
def to1005(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.churches.upgrades:to1005')

    portal_catalog = getToolByName(context, 'portal_catalog')

    catalog = getUtility(ICatalog)
    intids = getUtility(IIntIds)

    for b in portal_catalog(
            portal_type=[
                'wcc.churches.churchmember',
                'wcc.churches.churchfamily',
                'wcc.churches.churchbody'],
            Language='all'):
        obj = b.getObject()
        for name, relation in _relations(obj):
            try:
                relation.to_id = intids.getId(relation.to_object)
            except KeyError:
                continue
        updateRelations(obj, None)


@gs.upgradestep(title=u'Upgrade wcc.churches to 1004',
                description=u'Upgrade wcc.churches to 1004',
                source='1003', destination='1004',
                sortkey=1, profile='wcc.churches:default')
def to1004(context):
    setup = getToolByName(context, 'portal_setup')
    setup.runAllImportStepsFromProfile('profile-wcc.churches.upgrades:to1004')

    catalog = getToolByName(context, 'portal_catalog')

    for brain in catalog(portal_type=['wcc.churches.churchmember',
                                    'wcc.churches.churchfamily',
                                    'wcc.churches.churchbody'],
                                    Language='all'):
        obj = brain.getObject()
        obj.reindexObject()
        adapted = IExcludeFromNavigation(obj)
        adapted.exclude_from_nav = False
        obj.reindexObject()


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

#from five.intid.site import del_intids
#from plone.app.intid.setuphandlers import add_intids, registerContent
#from Products.CMFCore.interfaces import IDynamicType
#from zope.component import getUtility
#from zope.app.intid.interfaces import IIntIds
#from z3c.relationfield.interfaces import IHasRelations
#from zc.relation.interfaces import ICatalog
#from zope.component.hooks import setSite
#def rebuild(site):
#    setSite(site)
#    del_intids(site)
#    add_intids(site)
#    catalog = site.portal_catalog
#    print "Rebuild catalog"
#    catalog.clearFindAndRebuild()
#    intids = getUtility(IIntIds)
#    print "Rebuild intid"
#    brains = catalog(object_provides=IDynamicType.__identifier__, Language='all')
#    for brain in brains:
#        intids.register(brain.getObject())
#    print "Rebuild relations"
#    rcatalog = getUtility(ICatalog)
#    rcatalog.clear()
#    brains = catalog.searchResults(
#            object_provides=IHasRelations.__identifier__,
#            Language='all')
#    for brain in brains:
#        obj = brain.getObject()
#        updateRelations(obj, None)
#
