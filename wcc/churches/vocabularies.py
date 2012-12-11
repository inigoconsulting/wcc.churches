from five import grok
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory
from zope.component import getUtility
from z3c.formwidget.query.interfaces import IQuerySource


class RegionVocabularyFactory(object):
    def __call__(self, context):
        regions = context.portal_catalog(portal_type='wcc.churches.region')
        terms = [SimpleTerm(value=r.getId,
                    title=r.Title) for r in regions]
        return SimpleVocabulary(terms)

grok.global_utility(RegionVocabularyFactory, IVocabularyFactory,
            name='wcc.churches.region')
