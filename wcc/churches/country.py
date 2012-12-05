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
from collective.z3cform.datagridfield import DataGridFieldFactory, DictRow

# Interface class; used to define content-type schema.

class IReligionPercentage(Interface):

    religion = schema.Choice(
        title=u'Religion',
        vocabulary='wcc.vocabulary.religionfollower'
    )

    percentage = schema.Float(
        title=u'Percentage'
    )

class IDenominationCount(Interface):

    denomination = schema.Choice(
        title=u'Denomination',
        vocabulary='wcc.vocabulary.denomination'
    )

    count = schema.Int(
        title=u'Count'
    )

class ICountry(form.Schema, IImageScaleTraversable):
    """
    Country Information
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/country.xml to define the content type
    # and add directives here as necessary.

    country_code = schema.Choice(
        title=_(u'Country Code'),
        description=_(u'ISO 3166-1 alpha-2 code for this country'),
        required=True,
        vocabulary='wcc.vocabulary.country'
    )

    population = schema.Int(
        title=_(u'Population'),
        required=False
    )

    surface_area = schema.Int(
        title=_(u'Surface area (square KM)'),
        required=False,
    )

    gpi_percapita = schema.TextLine(
        title=_(u'GNI per capita'),
        required=False
    )

    languages = schema.List(
        title=_(u'Languages'),
        value_type=schema.Choice(vocabulary='wcc.vocabulary.language'),
        required=False,
    )

    form.widget(religions=DataGridFieldFactory)
    religions = schema.List(
        title=_(u'Religions'),
        value_type=DictRow(schema=IReligionPercentage)
    )

    form.widget(christianity_denominations=DataGridFieldFactory)
    christianity_denominations = schema.List(
        title=_(u'Christianity'),
        value_type=DictRow(schema=IDenominationCount)
    )

# View class
# The view will automatically use a similarly named template in
# country_templates.
# Template filenames should be all lower case.

class Index(dexterity.DisplayForm):
    grok.context(ICountry)
    grok.require('zope2.View')
    grok.name('view')
