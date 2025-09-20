import re

from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch

from src.chatbot.handlers import HANDLERS_MAPPER
from src.chatbot.strategies import PreferenceDiscoveryStrategy


class GeneralInfoMixin:
    """Mixin for general information handling."""
    PRODUCT_TO_RECOMMEND = None

    def _build_general_info_chain(self):
        """Build chain for general information responses."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER[inputs['customer_intent']](
                self.streaming_llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
            )
        )


class JewelryConsultationMixin:
    """Mixin for building conditional chains."""

    def _build_jewelry_consultation_chain(self):
        """Build the complete jewelry consultation process chain."""
        return (
            self._build_preference_extraction_chain()
            | RunnablePassthrough.assign(
                product_match_status=RunnableLambda(
                    lambda inputs: self._check_products_individually(
                        inputs
                    )
                )
            )

            | RunnableBranch(
                (
                    lambda x: x['product_match_status'].startswith('FOUND'),
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
                    optimized_query=inputs['optimized_query_for_search']
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
                self.streaming_llm,
                product_to_recommend=JewelryConsultationMixin.PRODUCT_TO_RECOMMEND,
                customer_query=inputs["customer_query"],
                **self._extract_preferences(inputs),
                conversation_history=inputs["conversation_history"]
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
                    self.streaming_llm,
                    context=inputs["context"],
                    customer_query=inputs["customer_query"],
                    next_discovery_question=inputs['next_discovery_question'],
                    **self._extract_safe_preferences(inputs),
                    conversation_history=inputs["conversation_history"]
                )
            )
        )

    def _build_available_options_navigator_chain(self):
        """Build chain for navigating available options."""
        return RunnableLambda(
            lambda inputs: HANDLERS_MAPPER['navigate_towards_available_options'](
                self.streaming_llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
                mismatch_reason=inputs['product_match_status'],
                **self._extract_safe_preferences(inputs),
                conversation_history=inputs["conversation_history"]
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

    def _extract_individual_products(self, context):
        """Extract individual products from context using regex."""
        # Find all products matching the pattern
        return re.findall(r"Stone:.*?stars;", context, re.DOTALL)

    def _check_products_individually(self, inputs):
        """Check each product individually until a match is found."""
        context = inputs["context"]
        preferences = {k: v for k, v in self._extract_safe_preferences(
            inputs
        ).items() if k != 'purchase_type'}

        # Extract individual products
        individual_products = self._extract_individual_products(context)
        print('preferences', preferences)

        if not individual_products:
            return "NOT_FOUND: No products found in context"

        last_reason = None
        # Check each product individually
        for i, product in enumerate(individual_products, 1):
            try:
                result = HANDLERS_MAPPER['check_for_products_matching_customer_preferences'](
                    self.llm,
                    context=product,  # Single product context
                    **preferences
                )

                # If this product matches, return success immediately
                if result and not result.startswith('NOT_FOUND'):
                    JewelryConsultationMixin.PRODUCT_TO_RECOMMEND = product
                    return f"FOUND: Match found in product {i}"

                # If we get a specific reason why this product doesn't match,
                # store it but continue checking other products
                if result and result.startswith('NOT_FOUND'):

                    last_reason = result

            except Exception as e:
                # Log error and continue with next product
                print(f"Error checking product {i}: {e}")
                continue

        # No matches found in any product
        # Return the last specific reason or a general message
        return last_reason
