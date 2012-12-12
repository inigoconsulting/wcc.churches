from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid, Interface

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.churches import MessageFactory as _
from wcc.churches.churchbody import IChurchBody
from wcc.churches.country import ICountry
from zope.intid.interfaces import IIntIds
from zope.component import getUtility
from zope.security import checkPermission

# Interface class; used to define content-type schema.

class IRegion(form.Schema, IImageScaleTraversable):
    """
    Region Information
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/region.xml to define the content type
    # and add directives here as necessary.

    subregional_churchbodies = schema.List(
        title=_(u'Subregional Bodies'),
        value_type=schema.Choice(vocabulary='wcc.churches.regional_churchbodies'),
        required=False
    )

# View class
# The view will automatically use a similarly named template in
# region_templates.
# Template filenames should be all lower case.

class IRegionDataProvider(Interface):
    pass

class RegionDataProvider(grok.Adapter):
    grok.context(IRegion)
    grok.implements(IRegionDataProvider)

    def __init__(self, context):
        self.context = context

    def churchbodies(self):
        result = []
        for brain in self.context.portal_catalog(
                    portal_type='wcc.churches.churchbody',
                    regions=self.context.getId()
                ):
                result.append(brain.getObject())
        for obj in self.context.values():
            if IChurchBody.providedBy(obj) and obj not in result:
                result.append(obj)
        return result

    def regional_churchbodies(self):
        intids = getUtility(IIntIds)
        return [cb for cb in self.churchbodies() if (
                    intids.getId(cb) not in
                    self.context.subregional_churchbodies)
                ]

    def subregional_churchbodies(self):
        intids = getUtility(IIntIds)
        result = []
        for i in self.context.subregional_churchbodies:
            obj = intids.queryObject(i)
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result

    def countries(self):
        result = []
        for obj in self.context.values():
            if ICountry.providedBy(obj):
                result.append(obj)
        return result


class Index(dexterity.DisplayForm):
    grok.context(IRegion)
    grok.require('zope2.View')
    grok.name('view')

    def provider(self):
        return IRegionDataProvider(self.context)
