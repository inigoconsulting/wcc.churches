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

from z3c.relationfield.schema import RelationList, RelationChoice, Relation
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.churches import MessageFactory as _
from plone.indexer.decorator import indexer

# Interface class; used to define content-type schema.

class IChurchMember(form.Schema, IImageScaleTraversable):
    """
    Church Member
    """

    church_image = NamedBlobImage(
            title=_(u'Image'),
            required=False,
            )

    church_family = RelationChoice(
            title=_(u'Church Family'),
            source=ObjPathSourceBinder(object_provides='wcc.churches.churchfamily.IChurchFamily'),
            required=False
            )

    based_in = schema.Choice(
            title=_(u'Based in'),
            vocabulary='wcc.vocabulary.country',
            description=_(u''),
            required=False,
            )

    present_in = schema.List(
            title=_(u'Present in'),
            value_type=schema.Choice(vocabulary='wcc.vocabulary.country'),
            description=_(u''),
            required=False,
            )

    membership = schema.Int(
            title=_(u'Membership'),
            description=_(u''),
            required=False,
            )

    pastors = schema.Int(
            title=_(u'Pastors'),
            description=_(u''),
            required=False
            )

    congregations = schema.Int(
            title=_(u'Congregations'),
            description=_(u''),
            required=False
            )

    member_of = RelationList(
            title=_(u'label_member_of', u"Member Of"),
            default=[],
            value_type=RelationChoice(
                source=ObjPathSourceBinder(object_provides='wcc.churches.churchbody.IChurchBody')
                ),
            required=False
            )

    assoc_member_of = RelationList(
            title=_(u'label_assoc_member_of', u'Associate Member Of'),
            default=[],
            value_type=RelationChoice(
                source=ObjPathSourceBinder(object_provides='wcc.churches.churchbody.IChurchBody'),
            ),
            required=False
            )

    wcc_member_since = schema.Date(
            title=u'WCC Member Since',
            required=False
            )


    remoteUrl = schema.TextLine(
            title=_(u"Website"),
            default=u'http://',
            description=u"",
            required=False,
            )

class IChurchMemberDataProvider(Interface):
        pass


class ChurchMemberDataProvider(grok.Adapter):
    grok.context(IChurchMember)
    grok.implements(IChurchMemberDataProvider)

    def __init__(self, context):
        self.context = context

    @property
    def church_family(self):
        if self.context.church_family:
            return self.context.church_family.to_object
        return None

    @property
    def based_in(self):
        return self.context.based_in

    @property
    def present_in(self):
        return self.context.present_in

    @property
    def membership(self):
        return self.context.membership

    @property
    def pastors(self):
        return self.context.pastors

    @property
    def congregations(self):
        return self.context.congregations

    @property
    def member_of(self):
        if self.context.member_of:
            return self.context.member_of.to_object
        return None

    @property
    def assoc_member_of(self):
        if self.context.assoc_member_of:
            return self.context.assoc_member_of.to_object
        return None

    @property
    def remoteUrl(self):
        url =  self.context.remoteUrl
        if url == 'http://':
            return ''
        return url

class Index(dexterity.DisplayForm):
    grok.context(IChurchMember)
    grok.require('zope2.View')
    grok.name('view')

    def provider(self):
        return IChurchMemberDataProvider(self.context)
