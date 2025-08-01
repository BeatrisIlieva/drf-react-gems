from django.urls import reverse_lazy
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    'SITE_URL': 'https://drf-react-gems.web.app',
    'SITE_DROPDOWN': [
        {
            'icon': 'diamond',
            'title': _('DRF-React-TS Gems'),
            'link': 'https://drf-react-gems.web.app',
        },
    ],
    'THEME': 'light',
    'STYLES': [
        lambda request: static('css/style.css'),
    ],
    'SCRIPTS': [
        lambda request: static('js/script.js'),
    ],
    'SIDEBAR': {
        'navigation': [
            {
                'title': _('Users & Groups'),
                'icon': 'people',
                'collapsible': True,
                'separator': True,
                'items': [
                    {
                        'title': _('Users'),
                        'icon': 'person',
                        'link': reverse_lazy(
                            'admin:accounts_usercredential_changelist'
                        ),
                        'permission': lambda request: request.user.is_superuser,
                    },
                    {
                        'title': _('Groups'),
                        'icon': 'group',
                        'link': reverse_lazy('admin:auth_group_changelist'),
                        'permission': lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                'title': _('Products'),
                'collapsible': True,
                'separator': True,
                'permission': lambda request: request.user.has_perm(
                    'products.view_earwear'
                ),
                'items': [
                    {
                        'title': _('Earwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy(
                            'admin:products_earwear_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_earwear'
                        ),
                    },
                    {
                        'title': _('Fingerwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy(
                            'admin:products_fingerwear_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_fingerwear'
                        ),
                    },
                    {
                        'title': _('Neckwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy(
                            'admin:products_neckwear_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_neckwear'
                        ),
                    },
                    {
                        'title': _('Wristwear'),
                        'icon': 'inventory',
                        'link': reverse_lazy(
                            'admin:products_wristwear_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_wristwear'
                        ),
                    },
                ],
            },
            {
                'title': _('Product Attributes'),
                'separator': True,
                'collapsible': True,
                'permission': lambda request: request.user.has_perm(
                    'products.view_color'
                ),
                'items': [
                    {
                        'title': _('Colors'),
                        'icon': 'Palette',
                        'link': reverse_lazy(
                            'admin:products_color_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_color'
                        ),
                    },
                    {
                        'title': _('Metals'),
                        'icon': 'Texture',
                        'link': reverse_lazy(
                            'admin:products_metal_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_metal'
                        ),
                    },
                    {
                        'title': _('Stone'),
                        'icon': 'Diamond',
                        'link': reverse_lazy(
                            'admin:products_stone_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_stone'
                        ),
                    },
                    {
                        'title': _('Collections'),
                        'icon': 'Bookmarks',
                        'link': reverse_lazy(
                            'admin:products_collection_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_collection'
                        ),
                    },
                    {
                        'title': _('Size'),
                        'icon': 'crop',
                        'link': reverse_lazy('admin:products_size_changelist'),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_size'
                        ),
                    },
                ],
            },
            {
                'separator': True,
                'permission': lambda request: request.user.has_perm(
                    'products.view_review'
                ),
                'items': [
                    {
                        'title': _('Product Reviews'),
                        'icon': 'star',
                        'link': reverse_lazy(
                            'admin:products_review_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'products.view_review'
                        ),
                    },
                    {
                        'title': _('Shopping Bags'),
                        'icon': 'shopping_bag',
                        'link': reverse_lazy(
                            'admin:shopping_bags_shoppingbag_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'shopping_bags.view_shoppingbag'
                        ),
                    },
                    {
                        'title': _('Orders'),
                        'icon': 'shopping_cart',
                        'link': reverse_lazy('admin:orders_order_changelist'),
                        'permission': lambda request: request.user.has_perm(
                            'orders.view_order'
                        ),
                    },
                    {
                        'title': _('Wishlists'),
                        'icon': 'favorite',
                        'link': reverse_lazy(
                            'admin:wishlists_wishlist_changelist'
                        ),
                        'permission': lambda request: request.user.has_perm(
                            'wishlists.view_wishlist'
                        ),
                    },
                ],
            },
        ],
    },
}
