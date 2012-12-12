from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from wcc.churches.churchbody import IChurchBody

class RegionVocabularyFactory(object):
    def __call__(self, context):
        regions = context.portal_catalog(portal_type='wcc.churches.region')
        terms = [SimpleTerm(value=r.getId,
                    title=r.Title) for r in regions]
        return SimpleVocabulary(terms)

grok.global_utility(RegionVocabularyFactory, IVocabularyFactory,
            name='wcc.churches.region')


class SubRegionalChurchBodyVocabularyFactory(object):
    def __call__(self, context):
        churchbodies = context.portal_catalog(
            portal_type='wcc.churches.churchbody',
            regions=context.getId()
        )
        intids = getUtility(IIntIds)
        terms = []
        keys = []
        for brain in churchbodies:
            intid = intids.getId(brain.getObject())
            terms.append(SimpleTerm(value=intid, title=brain.Title))
            keys.append(intid)

        for obj in context.values():
            if IChurchBody.providedBy(obj):
                intid = intids.getId(obj)
                if intid not in keys:
                    terms.append(SimpleTerm(value=intid,
                                title=obj.Title()))
        return SimpleVocabulary(terms)

grok.global_utility(SubRegionalChurchBodyVocabularyFactory, IVocabularyFactory,
            name='wcc.churches.regional_churchbodies')
