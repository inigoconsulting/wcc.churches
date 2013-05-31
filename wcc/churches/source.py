from plone.formwidget.contenttree.utils import closest_content
from plone.formwidget.contenttree import ObjPathSourceBinder

class ObjectProvidesPathSourceBinder(ObjPathSourceBinder):

    def __init__(self, object_provides=None,
                navigation_tree_query=None, **kw):
        self._object_provides = object_provides or []

        if object_provides:
            kw['object_provides'] = object_provides

        super(ObjectProvidesPathSourceBinder, self).__init__(
                navigation_tree_query, **kw
        )

    def __call__(self, context):
        source = self.path_source(
            closest_content(context),
            selectable_filter=self.selectable_filter,
        )
        del source.navigation_tree_query['portal_type']

        object_provides = [
            'plone.dexterity.interfaces.IDexterityContainer',
            'Products.ATContentTypes.interfaces.folder.IATFolder'
        ] + self._object_provides

        source.navigation_tree_query['object_provides'] = object_provides
        return source

