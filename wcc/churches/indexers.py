from wcc.churches.churchmember import IChurchMember
from wcc.churches.country import ICountry
from wcc.churches.behavior.location import ILocationTags
from plone.indexer.decorator import indexer

@indexer(IChurchMember)
def churchmember_countries(context, **kw):
    result = []
    if context.based_in:
        result.append(context.based_in)
    if context.present_in:
        for country in context.present_in:
            result.append(country)
    return result

@indexer(ICountry)
def country_countries(context, **kw):
    if context.country_code:
        return [context.country_code]
    return []
