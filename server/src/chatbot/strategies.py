from typing import Tuple

from src.chatbot.models import PurchaseType, WearerGender, CategoryType, MetalType, StoneType, BudgetRange


class PreferenceDiscoveryStrategy:
    """Strategic preference discovery for luxury online jewelry consultation."""

    DISCOVERY_SEQUENCE = {
        'purchase_type': {
            'question': 'Will you be the lucky wearer, or are you selecting a gift to delight someone dear to you?',
            'model': PurchaseType,
        },
        'gender': {
            'question': {
                'self': "To ensure I show you our most suitable collections, do you prefer pieces from our women's or men's lines?",
                'gift': "So thoughtful of you! Are you shopping for a lady or a gentleman?"
            },
            'model': WearerGender,
        },
        'category': {
            'question': 'Now for the exciting part - what type of piece speaks to you? Perhaps elegant earrings, a stunning necklace, a meaningful ring, or something else from our collections?',
            'model': CategoryType,
        },
        'metal_type': {
            'question': 'Our pieces come in precious metals that each have their own character. Do you have a preference for the cool elegance of platinum, the warmth of yellow gold, or the romantic glow of rose gold?',
            'model': MetalType,
        },
        'stone_type': {
            'question': 'Are you drawn to any particular gemstone? We have exquisite diamonds, vibrant rubies and emeralds, or the serene beauty of pink, blue or yellow sapphires and aquamarines.',
            'model': StoneType,
        },
        'budget_range': {
            'question': 'To ensure I present pieces that align with your vision, are you thinking of this as a significant investment piece, or would you prefer to explore a specific range?',
            'model': BudgetRange,
        },
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

            if key == 'gender':
                variant = 'self' if preferences['purchase_type'] == 'self_purchase' else 'gift'
                
                return value['question'][variant]

            return value['question']
