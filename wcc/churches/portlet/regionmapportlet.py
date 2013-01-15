from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from AccessControl import getSecurityManager

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from wcc.churches import MessageFactory as _
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from wcc.churches.country import ICountry

class IRegionMapPortlet(IPortletDataProvider):
    """
    Define your portlet schema here
    """
    africa = schema.Choice(
        title=_(u"Africa"),
        description=_(u'Region content to link the Africa region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    north_america = schema.Choice(
        title=_(u"North America"),
        description=_(u'Region content to link the North America region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    south_america = schema.Choice(
        title=_(u"South America"),
        description=_(u'Region content to link the South America region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    pacific = schema.Choice(
        title=_(u"Pacific"),
        description=_(u'Region content to link the Pacific region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    caribbean = schema.Choice(
        title=_(u"Caribbean"),
        description=_(u'Region content to link the Caribbean region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    asia = schema.Choice(
        title=_(u"Asia"),
        description=_(u'Region content to link the Asia region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    europe = schema.Choice(
        title=_(u"Europe"),
        description=_(u'Region content to link the Europe region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

    middle_east = schema.Choice(
        title=_(u"Middle East"),
        description=_(u'Region content to link the Middle East region to'),
        source=SearchableTextSourceBinder({'portal_type': 'wcc.churches.region'}, default_query='path:'),
        required=False
    )

class Assignment(base.Assignment):
    implements(IRegionMapPortlet)

    africa = None
    north_america = None
    south_america = None
    pacific = None
    caribbean = None
    asia = None
    europe = None
    middle_east = None

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def title(self):
        return _('Region Map Portlet')

class Renderer(base.Renderer):
    
    render = ViewPageTemplateFile('templates/regionmapportlet.pt')

    @property
    def available(self):
        return True

    def obj_map(self):
        result = {}
        for k in ['africa', 'north_america', 'south_america', 'pacific',
                'caribbean', 'asia', 'europe', 'middle_east']:
            value = getattr(self.data, k, None)
            result[k] = self._obj_from_path(value)
        return result

    def _obj_from_path(self, path):
        if path and path.startswith('/'):
            path = path[1:]

        if not path:
            return None

        portal_state = getMultiAdapter((self.context, self.request),
                             name=u'plone_portal_state')
        portal = portal_state.portal()

        if isinstance(path, unicode):
            path = str(path)

        result = portal.unrestrictedTraverse(path, default=None)
        if result is not None:
            sm = getSecurityManager()
            if not sm.checkPermission('View', result):
                result = None
        return result

    def get_countries(self, region):
        result = [i for i in region.values() if ICountry.providedBy(i)]
        return sorted(result, key=lambda x: x.Title())


class AddForm(base.AddForm):
    form_fields = form.Fields(IRegionMapPortlet)
    label = _(u"Add Region Map Portlet")
    description = _(u"Portlet showing the region map")

    form_fields['africa'].custom_widget = UberSelectionWidget
    form_fields['north_america'].custom_widget = UberSelectionWidget
    form_fields['south_america'].custom_widget = UberSelectionWidget
    form_fields['pacific'].custom_widget = UberSelectionWidget
    form_fields['caribbean'].custom_widget = UberSelectionWidget
    form_fields['asia'].custom_widget = UberSelectionWidget
    form_fields['europe'].custom_widget = UberSelectionWidget
    form_fields['middle_east'].custom_widget = UberSelectionWidget

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    form_fields = form.Fields(IRegionMapPortlet)
    label = _(u"Edit Region Map Portlet")
    description = _(u"Portlet showing the region map")

    form_fields['africa'].custom_widget = UberSelectionWidget
    form_fields['north_america'].custom_widget = UberSelectionWidget
    form_fields['south_america'].custom_widget = UberSelectionWidget
    form_fields['pacific'].custom_widget = UberSelectionWidget
    form_fields['caribbean'].custom_widget = UberSelectionWidget
    form_fields['asia'].custom_widget = UberSelectionWidget
    form_fields['europe'].custom_widget = UberSelectionWidget
    form_fields['middle_east'].custom_widget = UberSelectionWidget


