from wcc.churches.churchmember import IChurchMember
from wcc.churches.behavior.location import ILocationTags
from plone.indexer.decorator import indexer

@indexer(IChurchMember)
def churchmember_countries(context, **kw):
    return [context.based_in] + context.present_in

