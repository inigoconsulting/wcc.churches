from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import wcc.churches


WCC_CHURCHES = PloneWithPackageLayer(
    zcml_package=wcc.churches,
    zcml_filename='testing.zcml',
    gs_profile_id='wcc.churches:testing',
    name="WCC_CHURCHES")

WCC_CHURCHES_INTEGRATION = IntegrationTesting(
    bases=(WCC_CHURCHES, ),
    name="WCC_CHURCHES_INTEGRATION")

WCC_CHURCHES_FUNCTIONAL = FunctionalTesting(
    bases=(WCC_CHURCHES, ),
    name="WCC_CHURCHES_FUNCTIONAL")
