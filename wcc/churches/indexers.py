from wcc.churches.churchmember import IChurchMember
from wcc.churches.behavior.location import ILocationTags
from plone.indexer.decorator import indexer

@indexer(IChurchMember)
def churchmember_countries(context, **kw):
    result = []
    if context.based_in:
        result.append(context.based_in)
    if context.present_in:
        result.append(context.present_in)
    return result
