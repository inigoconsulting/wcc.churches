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
from wcc.churches import MessageFactory as _
from wcc.churches.source import ObjectProvidesPathSourceBinder
from plone.indexer.decorator import indexer
from zope.component.hooks import getSite
from datetime import date
from plone.multilingualbehavior.directives import languageindependent
from plone.api.portal import get_tool

# Interface class; used to define content-type schema.

class IChurchMember(form.Schema, IImageScaleTraversable):
    """
    Church Member
    """

    languageindependent('church_image')
    church_image = NamedBlobImage(
        title=_(u'Image'),
        required=False,
    )

    languageindependent('church_family')
    church_family = RelationChoice(
            title=_(u'Church Family'),
            source=ObjectProvidesPathSourceBinder(
                object_provides='wcc.churches.churchfamily.IChurchFamily'),
            required=False
    )

    languageindependent('based_in')
    based_in = schema.Choice(
            title=_(u'Based in'),
            vocabulary='wcc.vocabulary.country',
            description=_(u''),
            required=False,
            )

    languageindependent('present_in')
    present_in = schema.List(
            title=_(u'Present in'),
            value_type=schema.Choice(vocabulary='wcc.vocabulary.country'),
            description=_(u''),
            required=False,
            )

    languageindependent('membership')
    membership = schema.Int(
            title=_(u'Membership'),
            description=_(u''),
            required=False,
            )

    languageindependent('pastors')
    pastors = schema.Int(
            title=_(u'Pastors'),
            description=_(u''),
            required=False
            )

    languageindependent('congregations')
    congregations = schema.Int(
            title=_(u'Congregations'),
            description=_(u''),
            required=False
            )

    languageindependent('member_of')
    member_of = RelationList(
            title=_(u'label_member_of', u"Member Of"),
            default=[],
            value_type=RelationChoice(
                source=ObjectProvidesPathSourceBinder(
                    object_provides='wcc.churches.churchbody.IChurchBody'
                )
            ),
            required=False
            )

    languageindependent('assoc_member_of')
    assoc_member_of = RelationList(
            title=_(u'label_assoc_member_of', u'Associate Member Of'),
            default=[],
            value_type=RelationChoice(
                source=ObjectProvidesPathSourceBinder(
                    object_provides='wcc.churches.churchbody.IChurchBody'),
            ),
            required=False
            )

    languageindependent('wcc_member_since')
    wcc_member_since = schema.Date(
            title=u'WCC Member Since',
            min = date(1900, 1, 1),
            max = date.today(),
            required=False
            )

    languageindependent('remoteUrl')
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
        url = self.context.remoteUrl
        if url == 'http://':
            return ''
        return url


class Index(dexterity.DisplayForm):
    grok.context(IChurchMember)
    grok.require('zope2.View')
    grok.name('view')

    def provider(self):
        return IChurchMemberDataProvider(self.context)

    def get_country_info(self, country_code):
        catalog = get_tool('portal_catalog')
        return catalog(portal_type="wcc.churches.country",
                       countries=country_code)

    def get_valid_url(self):
        if self.context.remoteUrl.startswith('http'):
            return self.context.remoteUrl
        return 'http://' + self.context.remoteUrl
