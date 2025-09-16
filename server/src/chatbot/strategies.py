from typing import Tuple


class PreferenceDiscoveryStrategy:
    """Strategic preference discovery for luxury online jewelry consultation."""

    DISCOVERY_SEQUENCE = [
        'purchase_type',
        'gender',
        'category',
        'metal_type',
        'stone_type',
        'budget_range'
    ]

    QUESTION_TEMPLATES = {
        'purchase_type': "Will you be the lucky wearer, or are you selecting a gift to delight someone dear to you?",

        'gender': {
            'self': "To ensure I show you our most suitable collections, do you prefer pieces from our women's or men's lines?",
            'gift': "So thoughtful of you! Are you shopping for a lady or a gentleman?"
        },

        'category': "Now for the exciting part - what type of piece speaks to you? Perhaps elegant earrings, a stunning necklace, a meaningful ring, or something else from our collections?",

        'metal_type': "Our pieces come in precious metals that each have their own character. Do you have a preference for the cool elegance of platinum, the warmth of yellow gold, or the romantic glow of rose gold?",

        'stone_type': "Are you drawn to any particular gemstone? We have exquisite diamonds, vibrant rubies and emeralds, or the serene beauty of pink, blue or yellow sapphires and aquamarines.",

        'budget_range': "To ensure I present pieces that align with your vision, are you thinking of this as a significant investment piece, or would you prefer to explore a specific range?",
    }

    @classmethod
    def get_next_question(cls, preferences) -> Tuple[str, str]:
        """
        Returns the next question to ask based on discovery sequence and context.
        Returns (field_name, question_text)
        """

        for field_name in cls.DISCOVERY_SEQUENCE:
            field_value = preferences.get(field_name)

            # Skip fields that are already filled
            if field_value:
                continue

            # Get appropriate question
            question = cls._select_question(field_name, preferences)
            return question

        return None

    @classmethod
    def _select_question(cls, field_name: str, preferences) -> str:
        """Select the most appropriate question variant."""

        question = cls.QUESTION_TEMPLATES.get(field_name)

        if isinstance(question, dict):
            # Handle conditional question
            if field_name == 'gender':
                variant = 'self' if preferences['purchase_type'] == 'self_purchase' else 'gift'
                return question[variant]

        return question
