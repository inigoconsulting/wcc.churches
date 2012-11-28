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

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from wcc.churches import MessageFactory as _


# Interface class; used to define content-type schema.

class IChurchBody(form.Schema, IImageScaleTraversable):
    """
    Church Body
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/churchbody.xml to define the content type
    # and add directives here as necessary.

    form.model("models/churchbody.xml")


# View class
# The view will automatically use a similarly named template in
# churchbody_templates.
# Template filenames should be all lower case.

class Index(dexterity.DisplayForm):
    grok.context(IChurchBody)
    grok.require('zope2.View')
    grok.name('view')
