from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice, Relation
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.churches import MessageFactory as _


# Interface class; used to define content-type schema.

class IChurchMember(form.Schema, IImageScaleTraversable):
    """
    Church Member
    """

    church_family = RelationChoice(
        title=_(u'Church Family'),
        source=ObjPathSourceBinder(object_provides='wcc.churches.churchfamily.IChurchFamily'),
        required=False
    )

    based_in = schema.Choice(
                title=_(u'Based in'),
                vocabulary='wcc.vocabulary.country',
                description=_(u''),
                )

    present_in = schema.List(
                title=_(u'Present in'),
                value_type=schema.Choice(vocabulary='wcc.vocabulary.country'),
                description=_(u''),
                )
    membership = schema.Int(
                title=_(u'Membership'),
                description=_(u''),
                )

    pastors = schema.Int(
                title=_(u'Pastors'),
                description=_(u''),
                )

    congregations = schema.Int(
                title=_(u'Congregations'),
                description=_(u''),
                )

    member_of = RelationList(
            title=_(u'label_member_of', u"Member Of"),
            default=[],
            value_type=RelationChoice(
                source=ObjPathSourceBinder(object_provides='wcc.churches.churchbody.IChurchBody')
                ),
            required=False
    )

    assoc_member_of = RelationChoice(
            title=_(u'label_assoc_member_of', u'Associate Member Of'),
            source=ObjPathSourceBinder(object_provides='wcc.churches.churchbody.IChurchBody'),
            required=False
    )


    website = schema.URI(
            title=_(u'URL'),
            description=_(u''),
            )

    form.widget(text='plone.app.z3cform.wysiwyg.WysiwygFieldWidget')
    text = schema.Text(
            title=_(u'Text'),
            description=_(u''),
            )


class Index(dexterity.DisplayForm):
    grok.context(IChurchMember)
    grok.require('zope2.View')
    grok.name('view')
