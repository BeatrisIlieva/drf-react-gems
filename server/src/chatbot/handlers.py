import json
from typing import Optional, Tuple

from src.chatbot.models import CategoryClassification, ColorClassification, StoneClassification, GenderClassification, MetalClassification, PurchaseClassification
from src.chatbot.utils import get_classification_json

class PreferenceHandler:
    @staticmethod
    def extract_customer_preferences(
        llm,
        conversation_summary: str, 
        classification_human_message: str, 
        classification_system_message: str
    ) -> Tuple[Optional[str], bool]:
        """Extract customer preferences and check if ready for recommendations."""
        
        # Define classifications to extract
        classifications = [
            (GenderClassification, 'gender'),
            (ColorClassification, 'color'),
            (CategoryClassification, 'category'),
            (StoneClassification, 'stone_type'),
            (MetalClassification, 'metal_type'),
            (PurchaseClassification, 'purchase_type')
        ]
        
        # Extract all values
        extracted = {}
        for classification_class, key in classifications:
            result = json.loads(get_classification_json(
                llm,
                conversation_summary, 
                classification_human_message, 
                classification_system_message, 
                classification_class,
            ))
            extracted[key] = result[key]
            
            # Also get recipient_relationship from purchase classification
            if classification_class == PurchaseClassification:
                extracted['recipient_relationship'] = result.get('recipient_relationship')
        
        # Check if all required fields are present
        required_fields = [key for _, key in classifications]
        if extracted['purchase_type'] == 'gift_purchase':
            required_fields.append('recipient_relationship')
        
        ready_to_transition = all(extracted[field] for field in required_fields)
        
        # Build preferences string
        preferences_items = [f"{field}: {extracted[field]}" for field in required_fields]
        customer_preferences = '\n'.join(preferences_items)
        
        return customer_preferences, ready_to_transition
    

    
        