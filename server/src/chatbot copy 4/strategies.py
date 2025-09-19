# from typing import Tuple

# from src.chatbot.models import PurchaseType, WearerGender, CategoryType, MetalType, StoneType


# class PreferenceDiscoveryStrategy:
#     """Strategic preference discovery for luxury online jewelry consultation."""

#     DISCOVERY_SEQUENCE = {
#         'purchase_type': {
#             'question': 'Formulate a question to determine whether the purchase is for oneself or as a gift. The question must be thoughtful and aligned with luxury jewelry standards. Bold the keywords so I can easily detect what you are asking.',
#             'model': PurchaseType,
#         },
#         'gender': {
#             'question': 'Formulate a question to determine the gender of the person who will be wearing the jewelry. The question must be thoughtful and aligned with luxury jewelry standards. Use the keywords lady or gentleman and bold them so I can easily detect what you are asking.',
#             'model': WearerGender,
#         },
#         'category': {
#             'question': 'Formulate a question to determine what jewelry category I am interested in. Guide me to select one of the jewelry categories that exist into the AVAILABLE PRODUCTS. The question must be thoughtful and aligned with luxury jewelry standards. Bold the jewelry categories so I can easily detect what you are asking. Only suggest characteristics that exist in products that completely match all aspects of my stated PREFERENCES, not from products that only partially match. Do not invite me to explore options that do not exist.',
#             'model': CategoryType,
#         },
#         'metal_type': {
#             'question': 'Formulate a question to determine what metal type I am interested in. Guide me to select one of the metal types that exist into the AVAILABLE PRODUCTS. The question must be thoughtful and aligned with luxury jewelry standards. Bold metal types so I can easily detect what you are asking. Only suggest characteristics that exist in products that completely match all aspects of my stated PREFERENCES, not from products that only partially match. Do not invite me to explore options that do not exist.',
#             'model': MetalType,
#         },
#         'stone_type': {
#             'question': 'Formulate a question to determine what stone type I am interested in. Guide me to select one of the stone types that exist into the AVAILABLE PRODUCTS. The question must be thoughtful and aligned with luxury jewelry standards. Bold the stone types so I can easily detect what you are asking. Only suggest characteristics that exist in products that completely match all aspects of my stated PREFERENCES, not from products that only partially match. Do not invite me to explore options that do not exist.',
#             'model': StoneType,
#         }
#     }

#     @classmethod
#     def get_next_question(cls, preferences) -> Tuple[str, str]:
#         """
#         Returns the next question to ask based on discovery sequence and context.
#         Returns (field_name, question_text)
#         """
#         for key, value in cls.DISCOVERY_SEQUENCE.items():
#             customer_preference = preferences.get(key)

#             if customer_preference:
#                 continue

#             return value['question']





# strategies.py - Async Strategies (unchanged, but imported)
from typing import Tuple
from src.chatbot.models import PurchaseType, WearerGender, CategoryType, MetalType, StoneType


class PreferenceDiscoveryStrategy:
    """Strategic preference discovery for luxury online jewelry consultation."""

    DISCOVERY_SEQUENCE = {
        'purchase_type': {
            'question': 'Formulate a question to determine whether the purchase is for oneself or as a gift. The question must be thoughtful and aligned with luxury jewelry standards. Bold the keywords so I can easily detect what you are asking.',
            'model': PurchaseType,
        },
        'gender': {
            'question': 'Formulate a question to determine the gender of the person who will be wearing the jewelry. The question must be thoughtful and aligned with luxury jewelry standards. Use the keywords lady or gentleman and bold them so I can easily detect what you are asking.',
            'model': WearerGender,
        },
        'category': {
            'question': 'Formulate a question to determine what jewelry category I am interested in. Guide me to select one of the jewelry categories that exist into the AVAILABLE PRODUCTS. The question must be thoughtful and aligned with luxury jewelry standards. Bold the jewelry categories so I can easily detect what you are asking. Only suggest characteristics that exist in products that completely match all aspects of my stated PREFERENCES, not from products that only partially match. Do not invite me to explore options that do not exist.',
            'model': CategoryType,
        },
        'metal_type': {
            'question': 'Formulate a question to determine what metal type I am interested in. Guide me to select one of the metal types that exist into the AVAILABLE PRODUCTS. The question must be thoughtful and aligned with luxury jewelry standards. Bold metal types so I can easily detect what you are asking. Only suggest characteristics that exist in products that completely match all aspects of my stated PREFERENCES, not from products that only partially match. Do not invite me to explore options that do not exist.',
            'model': MetalType,
        },
        'stone_type': {
            'question': 'Formulate a question to determine what stone type I am interested in. Guide me to select one of the stone types that exist into the AVAILABLE PRODUCTS. The question must be thoughtful and aligned with luxury jewelry standards. Bold the stone types so I can easily detect what you are asking. Only suggest characteristics that exist in products that completely match all aspects of my stated PREFERENCES, not from products that only partially match. Do not invite me to explore options that do not exist.',
            'model': StoneType,
        }
    }

    @classmethod
    def get_next_question(cls, preferences) -> Tuple[str, str]:
        """
        Returns the next question to ask based on discovery sequence and context.
        Returns (field_name, question_text)
        """
        for key, value in cls.DISCOVERY_SEQUENCE.items():
            customer_preference = preferences.get(key)

            if customer_preference:
                continue

            return value['question']