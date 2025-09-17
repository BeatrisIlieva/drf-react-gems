from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch

from src.chatbot.handlers import HANDLERS_MAPPER
from src.chatbot.models import BudgetRange, CategoryType,  MetalType, PurchaseType, StoneType, WearerGender
from src.chatbot.strategies import PreferenceDiscoveryStrategy


# class PreferenceExtractionMixin:
#     """Mixin for extracting customer preferences."""

#     def _build_preference_extraction_chain(self):
#         """Build chain for extracting customer preferences."""
#         return (
#             RunnablePassthrough.assign(
#                 purchase_type=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         self.llm,
#                         PurchaseType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 gender=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         self.llm,
#                         WearerGender,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 category=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         self.llm,
#                         CategoryType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 metal_type=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         self.llm,
#                         MetalType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 stone_type=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         self.llm,
#                         StoneType,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#             | RunnablePassthrough.assign(
#                 budget_range=RunnableLambda(
#                     lambda inputs: HANDLERS_MAPPER['customer_preferences'](
#                         self.llm,
#                         BudgetRange,
#                         conversation_history=inputs["conversation_history"]
#                     )
#                 )
#             )
#         )


# class ProductDiscoveryMixin:
#     """Mixin for product discovery functionality."""

#     def _build_continue_discovery_chain(self):
#         """Build chain for continuing preference discovery."""
#         return (
#             RunnablePassthrough.assign(
#                 next_discovery_question=RunnableLambda(
#                     lambda inputs: PreferenceDiscoveryStrategy.get_next_question(
#                         {k: v for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
#                          for k, v in inputs.get(key, {}).items()}
#                     )
#                 )
#             )
#             | RunnableLambda(
#                 lambda inputs: HANDLERS_MAPPER['investigate'](
#                     self.llm,
#                     context=inputs["context"],
#                     customer_query=inputs["customer_query"],
#                     next_discovery_question=inputs['next_discovery_question'],
#                     **self._extract_safe_preferences(inputs),
#                     conversation_memory=inputs["conversation_memory"]
#                 )
#             )
#         )

#     def _build_recommend_product_chain(self):
#         """Build chain for product recommendations."""
#         return RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['recommend_product'](
#                 self.llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#                 **self._extract_preferences(inputs),
#                 conversation_memory=inputs["conversation_memory"]
#             )
#         )

#     def _build_available_options_navigator_chain(self):
#         """Build chain for navigating available options."""
#         return RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['available_options_navigator'](
#                 self.llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#                 **self._extract_safe_preferences(inputs),
#                 conversation_memory=inputs["conversation_memory"]
#             )
#         )

#     def _extract_preferences(self, inputs):
#         """Extract preferences assuming they're all present."""
#         return {
#             key: inputs[key][key]
#             for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
#         }

#     def _extract_safe_preferences(self, inputs):
#         """Extract preferences with safe dictionary access."""
#         return {
#             key: inputs.get(key, {}).get(key, "")
#             for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
#         }


class GeneralInfoMixin:
    """Mixin for general information handling."""

    def _build_general_info_chain(self):
        """Build chain for general information responses."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER[inputs['customer_intent']](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                conversation_memory=inputs["conversation_memory"]
            )
        )


class JewelryConsultationMixin:
    """Mixin for building conditional chains."""

    def _build_jewelry_consultation_chain(self):
        """Build the complete jewelry consultation process chain."""
        return (
            self._build_preference_extraction_chain()
            | RunnablePassthrough.assign(
                found_products=RunnableLambda(
                    lambda inputs: HANDLERS_MAPPER['check_for_products_matching_customer_preferences'](
                        self.llm,
                        context=inputs["context"],
                        **self._extract_safe_preferences(inputs),
                    )
                )
            )
            | RunnableBranch(
                (
                    # lambda x: x['found_products'] == 'FOUND',
                    lambda x: (print("found_products:", x.get('found_products')) or True) and x['found_products'] == 'FOUND',
                    self._build_discovery_or_recommend_chain()
                ),
                self._build_available_options_navigator_chain()
            )
        )

    def _build_preference_extraction_chain(self):
        """Build chain for extracting customer preferences."""
        preference_assignments = {
            preference_key: RunnableLambda(
                lambda inputs, model=config['model']: HANDLERS_MAPPER['extract_customer_preferences'](
                    self.llm,
                    model,
                    conversation_history=inputs["conversation_history"]
                )
            )
            for preference_key, config in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.items()
        }

        return RunnablePassthrough.assign(**preference_assignments)

    def _build_discovery_or_recommend_chain(self):
        """Build conditional chain for discovery vs recommendation."""
        return RunnableBranch(
            (
                # If all preferences are collected, recommend products
                lambda x: self._all_preferences_collected(x),
                self._build_recommend_product_chain()
            ),
            # Otherwise, continue discovery
            self._build_continue_discovery_chain()
        )

    @classmethod
    def _all_preferences_collected(cls, inputs):
        """Check if all required preferences have been collected"""
        return all(
            inputs.get(key, {}).get(key, "") not in ("", None)
            for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
        )

    def _build_recommend_product_chain(self):
        """Build chain for product recommendations."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['recommend_product'](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                **self._extract_preferences(inputs),
                conversation_memory=inputs["conversation_memory"]
            )
        )

    def _build_continue_discovery_chain(self):
        """Build chain for continuing preference discovery."""
        return (
            RunnablePassthrough.assign(
                next_discovery_question=RunnableLambda(
                    lambda inputs: PreferenceDiscoveryStrategy.get_next_question(
                        self._extract_safe_preferences(inputs) 
                    )
                )
            )
            | RunnableLambda(
                lambda inputs: HANDLERS_MAPPER['discover_customer_preferences'](
                    self.llm,
                    context=inputs["context"],
                    customer_query=inputs["customer_query"],
                    next_discovery_question=inputs['next_discovery_question'],
                    **self._extract_safe_preferences(inputs),
                    conversation_memory=inputs["conversation_memory"]
                )
            )
        )

    def _build_available_options_navigator_chain(self):
        """Build chain for navigating available options."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['navigate_towards_available_options'](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                **self._extract_safe_preferences(inputs),
                conversation_memory=inputs["conversation_memory"]
            )
        )

    def _extract_preferences(self, inputs):
        """Extract preferences assuming they're all present."""
        return {
            key: inputs[key][key]
            for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.keys()  
        }

    def _extract_safe_preferences(self, inputs):
        """Extract preferences with safe dictionary access."""
        return {
            key: inputs.get(key, {}).get(key, "")
            for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.keys()  
        }
