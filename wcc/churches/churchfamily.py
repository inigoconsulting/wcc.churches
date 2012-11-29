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
from wcc.churches.backref import back_references

# Interface class; used to define content-type schema.

class IChurchFamily(form.Schema, IImageScaleTraversable):
    """
    Church Family
    """
    
    websites = schema.List(
        title=_(u'label_websites', u'Websites'),
        value_type=schema.TextLine(),
        required=False,
    )


class IChurchFamilyDataProvider(Interface):
    pass

class ChurchFamilyDataProvider(grok.Adapter):
    grok.context(IChurchFamily)
    grok.implements(IChurchFamilyDataProvider)

    @property
    def text(self):
        return self.context.text

    @property
    def websites(self):
        return self.context.websites

    @property
    def churchbodies(self):
        return back_references(self.context, 'member_of')

    @property
    def churchmembers(self):
        return back_references(self.context, 'church_family')

class Index(dexterity.DisplayForm):
    grok.context(IChurchFamily)
    grok.require('zope2.View')
    grok.name('view')

    def provider(self):
        return IChurchFamilyDataProvider(self.context)
