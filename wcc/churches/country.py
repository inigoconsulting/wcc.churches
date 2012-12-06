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
from wcc.vocabularies.countries import lookup_capital
from geopy import geocoders
from collective.geo.mapwidget.browser.widget import MapWidget

# Interface class; used to define content-type schema.

class IReligionPercentage(Interface):

    religion = schema.Choice(
        title=_(u'Religion'),
        vocabulary='wcc.vocabulary.religionfollower'
    )

    percentage = schema.Float(
        title=_(u'Percentage')
    )

class IDenominationCount(Interface):

    denomination = schema.Choice(
        title=_(u'Denomination'),
        vocabulary='wcc.vocabulary.denomination'
    )

    count = schema.Int(
        title=_(u'Count')
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

    gni_percapita = schema.TextLine(
        title=_(u'GNI per capita'),
        required=False
    )

    classification = schema.Choice(
        title=_(u'Classification'),
        required=False,
        vocabulary='wcc.vocabulary.classification'
    )

    languages = schema.List(
        title=_(u'Languages'),
        value_type=schema.TextLine(),
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

    def table_widgets(self):
        result = []
        for i in ['population', 'surface_area']:
            widget = self.w[i]
            result.append({
                'label': widget.label,
                'render': widget.render()
            })
        result.append({
            'label': _(u'Capital'),
            'render': lookup_capital(self.context.country_code)
        })
        for i in ['gni_percapita',
                  'classification',
                  'languages']:
            widget = self.w[i]
            result.append({
                'label': widget.label,
                'render': widget.render(),
            })

        # religion
        religions = getattr(self.context, 'religions', [])
        rows = ['<tr><th>%s</th><td>%s</td></li>' % (i['religion'],
            i['percentage']) for i in religions]
        result.append({
            'label': _(u'Religions'),
            'render': 
            '<table id="country-religions-table">%s</table>' % ''.join(rows)
        })

        denominations = getattr(self.context, 'denominations', [])
        rows = ['<tr><th>%s</th><td></td></li>' % (i['denomination'],
            i['count']) for i in denominations]
        result.append({
            'label': _(u'Denominations'),
            'render': 
            '<table id="country-denominations-table">%s</table>' % ''.join(rows)
        })
        return result

    def map_state(self):
        country = self.context.title
        geo = geocoders.GeoNames()  
        location = geo.geocode(country, False)
        
        if not location:
            return ''

        place, (lat, lng) = location[0]
        return '''
        cgmap.state['country-cgmap'] = {
            lon : %(lon)s,
            lat : %(lat)s,
            zoom : 4
        }
        ''' % {'lon': lng, 'lat': lat}

    def cgmap(self):
        cgmap = MapWidget(self, self.request, self.context)
        cgmap.mapid = 'country-cgmap'
        return cgmap
