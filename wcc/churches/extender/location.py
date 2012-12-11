from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes.public import (LinesField, InAndOutWidget)
from five import grok
from archetypes.schemaextender.interfaces import ISchemaExtender
from plone.app.collection.interfaces import ICollection
from Products.Archetypes.atapi import AttributeStorage
from Products.Archetypes.atapi import RichWidget
from Products.ATContentTypes.configuration import zconf
from Products.ATContentTypes.interfaces.news import IATNewsItem
from Products.ATContentTypes.interfaces.event import IATEvent

from wcc.churches import MessageFactory as _

class ExtensionLinesField(ExtensionField, LinesField):
    pass


class LocationTagsExtender(grok.Adapter):
    grok.implements(ISchemaExtender)
    grok.baseclass()

    fields = [
        ExtensionLinesField('regions',
            vocabulary_factory='wcc.churches.region',
            storage=AttributeStorage(),
            widget=InAndOutWidget(title=_(u'Related Regions'))
        ),
        ExtensionLinesField('countries',
            vocabulary_factory='wcc.vocabulary.country',
            storage=AttributeStorage(),
            widget=InAndOutWidget(title=_(u'Related Countries'))
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields


class NewsLocationTagsExtender(LocationTagsExtender):
    grok.context(IATNewsItem)

class EventLocationTagsExtender(LocationTagsExtender):
    grok.context(IATEvent)
