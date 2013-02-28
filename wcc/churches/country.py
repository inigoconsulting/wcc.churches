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
from wcc.churches.backref import back_references
# Interface class; used to define content-type schema.


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

# View class
# The view will automatically use a similarly named template in
# country_templates.
# Template filenames should be all lower case.

class ICountryDataProvider(Interface):
    pass

class CountryDataProvider(grok.Adapter):
    grok.implements(ICountryDataProvider)
    grok.context(ICountry)

    def churchbodies(self):
        result = []
        for brain in self.context.portal_catalog(
                portal_type='wcc.churches.churchbody',
                countries=self.context.country_code
                ):
            result.append(brain.getObject())
        return result

    def ecumenical_orgs(self):
        return self.churchbodies()

    def churchmembers(self):
        result = []
        for brain in self.context.portal_catalog(
                portal_type="wcc.churches.churchmember",
                countries=self.context.country_code
            ):
            result.append(brain.getObject())
        return result

    def based_churchmembers(self):
        churchmembers = self.churchmembers()
        return [c for c in churchmembers if (
            self.context.country_code == c.based_in)]

    def present_churchmembers(self):
        churchmembers = self.churchmembers()
        return [c for c in churchmembers if (
            self.context.country_code in c.present_in)]




class Index(dexterity.DisplayForm):
    grok.context(ICountry)
    grok.require('zope2.View')
    grok.name('view')

    def provider(self):
        return ICountryDataProvider(self.context)

    def table_widgets(self):
        result = []
        provider = self.provider

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
        rows = ['<tr><th>%s :</th><td>%s%%</td></tr>' % (i['religion'],
            i['percentage']) for i in religions]
        result.append({
            'label': _(u'Religions'),
            'render': 
            '<table id="country-religions-table">%s</table>' % ''.join(rows)
        })

        denominations = getattr(self.context, 'christianity_denominations', [])
        rows = ['<tr><th>%s :</th><td>%s</td></tr>' % (i['denomination'],
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
        import ipdb; ipdb.set_trace()
        
        if not location:
            return ''
        
        #additional condition to fix problem with congo
        if not location[0]:
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
