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
from wcc.churches.source import ObjectProvidesPathSourceBinder

from wcc.churches import MessageFactory as _
from plone.app.dexterity.behaviors.metadata import IBasic
from wcc.churches.backref import back_references
from wcc.churches.churchmember import IChurchMember

# Interface class; used to define content-type schema.
from collective import dexteritytextindexer

class IChurchBody(form.Schema, IBasic, IImageScaleTraversable):
    """
    Church Body
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/churchbody.xml to define the content type
    # and add directives here as necessary.

    title = schema.TextLine(
        title = _(u'label_short_title', default=u'Short Name / Abbreviation'),
        required = True
    )

    full_title = schema.TextLine(
        title=_(u'label_full_title', u'Full Name'),
        required=True
    )

    dexteritytextindexer.searchable('text')
    form.widget(text="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    text = schema.Text(
        title=_(u'label_body_text', u"Body Text"),
        description=u'',
        required=False,
    )

    
    member_of = RelationChoice(
            title=_(u'label_member_of', u"Member Of"),
            source=ObjectProvidesPathSourceBinder(object_provides=[
                'wcc.churches.churchfamily.IChurchFamily',
                'wcc.churches.churchbody.IChurchBody'
            ]),
            required=False
    )

    assoc_member_of = RelationChoice(
            title=_(u'label_assoc_member_of', u'Associate Member Of'),
            source=ObjectProvidesPathSourceBinder(
                object_provides=[
                    'wcc.churches.churchfamily.IChurchFamily',
                    'wcc.churches.churchbody.IChurchBody',
                ]
            ),
            required=False
    )

    form.widget(other_members="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    other_members = schema.Text(
        title=_(u'label_other_members', u'Other Members'),
        required=False
    )

    form.widget(other_assoc_members="plone.app.z3cform.wysiwyg.WysiwygFieldWidget")
    other_assoc_members = schema.Text(
        title=_(u'label_other_assoc_members', u'Other Associate Members'),
        required=False
    )

    remoteUrl = schema.TextLine(
        title=_(u"Website"),
        default=u'http://',
        description=u"",
        required=False,
    )


    form.order_before(full_title = '*')
    form.order_before(title = '*')


class IChurchBodyDataProvider(Interface):
    pass

class ChurchBodyDataProvider(grok.Adapter):
    grok.context(IChurchBody)
    grok.implements(IChurchBodyDataProvider)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        return self.context.title

    @property
    def full_title(self):
        return self.context.full_title

    @property
    def text(self):
        return self.context.text

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
    def members(self):
        result = []
        for i in back_references(self.context, 'member_of'):
            if IChurchMember.providedBy(i):
                result.append(i)
        return result


    @property
    def organizations(self):
        result = []
        for i in back_references(self.context, 'member_of'):
            if IChurchBody.providedBy(i):
                result.append(i)
        return result

    @property
    def assoc_members(self):
        result = []
        for i in back_references(self.context, 'assoc_member_of'):
            if IChurchMember.providedBy(i):
                result.append(i)
        return result

    @property
    def assoc_organizations(self):
        result = []
        for i in back_references(self.context, 'assoc_member_of'):
            if IChurchBody.providedBy(i):
                result.append(i)
        return result

    @property
    def other_members(self):
        return self.context.other_members

    @property
    def other_assoc_members(self):
        return self.context.other_assoc_members

    @property
    def remoteUrl(self):
        url =  self.context.remoteUrl
        if url == 'http://':
            return ''
        return url



# View class
# The view will automatically use a similarly named template in
# churchbody_templates.
# Template filenames should be all lower case.

class Index(dexterity.DisplayForm):
    grok.context(IChurchBody)
    grok.require('zope2.View')
    grok.name('view')

    def provider(self):
        return IChurchBodyDataProvider(self.context)
