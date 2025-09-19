# import re

# from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch

# from src.chatbot.handlers import HANDLERS_MAPPER
# from src.chatbot.strategies import PreferenceDiscoveryStrategy


# class GeneralInfoMixin:
#     """Mixin for general information handling."""
#     PRODUCT_TO_RECOMMEND = None

#     def _build_general_info_chain(self):
#         """Build chain for general information responses."""
#         return RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER[inputs['customer_intent']](
#                 self.llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#             )
#         )


# class JewelryConsultationMixin:
#     """Mixin for building conditional chains."""

#     def _build_jewelry_consultation_chain(self):
#         """Build the complete jewelry consultation process chain."""
#         return (
#             self._build_preference_extraction_chain()
#             | RunnablePassthrough.assign(
#                 product_match_status=RunnableLambda(
#                     lambda inputs: self._check_products_individually(
#                         inputs
#                     )
#                 )
#             )

#             | RunnableBranch(
#                 (
#                     lambda x: x['product_match_status'].startswith('FOUND'),
#                     self._build_discovery_or_recommend_chain()
#                 ),
#                 self._build_available_options_navigator_chain()
#             )
#         )

#     def _build_preference_extraction_chain(self):
#         """Build chain for extracting customer preferences."""
#         preference_assignments = {
#             preference_key: RunnableLambda(
#                 lambda inputs, model=config['model']: HANDLERS_MAPPER['extract_customer_preferences'](
#                     self.llm,
#                     model,
#                     optimized_query=inputs['optimized_query_for_search']
#                 )
#             )
#             for preference_key, config in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.items()
#         }

#         return RunnablePassthrough.assign(**preference_assignments)

#     def _build_discovery_or_recommend_chain(self):
#         """Build conditional chain for discovery vs recommendation."""
#         return RunnableBranch(
#             (
#                 # If all preferences are collected, recommend products
#                 lambda x: self._all_preferences_collected(x),
#                 self._build_recommend_product_chain()
#             ),
#             # Otherwise, continue discovery
#             self._build_continue_discovery_chain()
#         )

#     @classmethod
#     def _all_preferences_collected(cls, inputs):
#         """Check if all required preferences have been collected"""
#         return all(
#             inputs.get(key, {}).get(key, "") not in ("", None)
#             for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
#         )

#     def _build_recommend_product_chain(self):
#         """Build chain for product recommendations."""
#         return RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['recommend_product'](
#                 self.llm,
#                 product_to_recommend=JewelryConsultationMixin.PRODUCT_TO_RECOMMEND,
#                 customer_query=inputs["customer_query"],
#                 # customer_query=inputs["optimized_query_for_search"],
#                 **self._extract_preferences(inputs),
#                 conversation_history=inputs["conversation_history"]
#             )
#         )

#     def _build_continue_discovery_chain(self):
#         """Build chain for continuing preference discovery."""
#         return (
#             RunnablePassthrough.assign(
#                 next_discovery_question=RunnableLambda(
#                     lambda inputs: PreferenceDiscoveryStrategy.get_next_question(
#                         self._extract_safe_preferences(inputs)
#                     )
#                 )
#             )
#             | RunnableLambda(
#                 lambda inputs: HANDLERS_MAPPER['discover_customer_preferences'](
#                     self.llm,
#                     context=inputs["context"],
#                     customer_query=inputs["customer_query"],
#                     # customer_query=inputs["optimized_query_for_search"],
#                     next_discovery_question=inputs['next_discovery_question'],
#                     **self._extract_safe_preferences(inputs),
#                     conversation_history=inputs["conversation_history"]
#                 )
#             )
#         )

#     def _build_available_options_navigator_chain(self):
#         """Build chain for navigating available options."""
#         return RunnableLambda(
#             lambda inputs: HANDLERS_MAPPER['navigate_towards_available_options'](
#                 self.llm,
#                 context=inputs["context"],
#                 customer_query=inputs["customer_query"],
#                 # customer_query=inputs["optimized_query_for_search"],
#                 mismatch_reason=inputs['product_match_status'],
#                 **self._extract_safe_preferences(inputs),
#                 conversation_history=inputs["conversation_history"]
#             )
#         )

#     def _extract_preferences(self, inputs):
#         """Extract preferences assuming they're all present."""
#         return {
#             key: inputs[key][key]
#             for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.keys()
#         }

#     def _extract_safe_preferences(self, inputs):
#         """Extract preferences with safe dictionary access."""
#         return {
#             key: inputs.get(key, {}).get(key, "")
#             for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.keys()
#         }

#     def _extract_individual_products(self, context):
#         """Extract individual products from context using regex."""
#         # Find all products matching the pattern
#         return re.findall(r"Collection:.*?stars;", context, re.DOTALL)

#     def _check_products_individually(self, inputs):
#         """Check each product individually until a match is found."""
#         context = inputs["context"]
#         preferences = {k: v for k, v in self._extract_safe_preferences(
#             inputs
#         ).items() if k != 'purchase_type'}

#         # Extract individual products
#         individual_products = self._extract_individual_products(context)
#         print('preferences', preferences)

#         if not individual_products:
#             return "NOT_FOUND: No products found in context"

#         last_reason = None
#         # Check each product individually
#         for i, product in enumerate(individual_products, 1):
#             try:
#                 result = HANDLERS_MAPPER['check_for_products_matching_customer_preferences'](
#                     self.llm,
#                     context=product,  # Single product context
#                     **preferences
#                 )

#                 # If this product matches, return success immediately
#                 if result and not result.startswith('NOT_FOUND'):
#                     JewelryConsultationMixin.PRODUCT_TO_RECOMMEND = product
#                     return f"FOUND: Match found in product {i}"

#                 # If we get a specific reason why this product doesn't match,
#                 # store it but continue checking other products
#                 if result and result.startswith('NOT_FOUND'):

#                     last_reason = result

#             except Exception as e:
#                 # Log error and continue with next product
#                 print(f"Error checking product {i}: {e}")
#                 continue

#         # No matches found in any product
#         # Return the last specific reason or a general message
#         return last_reason





# mixins.py - Async Mixins
import re
import asyncio
from typing import AsyncGenerator, Dict, Any
from asgiref.sync import sync_to_async

from langchain.schema.runnable import RunnablePassthrough, RunnableLambda, RunnableBranch
from src.chatbot.strategies import PreferenceDiscoveryStrategy
from src.chatbot.handlers import ASYNC_HANDLERS_MAPPER


class AsyncRunnableLambda:
    """Async wrapper for lambda functions"""
    
    def __init__(self, func):
        self.func = func
    
    async def ainvoke(self, inputs):
        return await self.func(inputs)


class AsyncGeneralInfoMixin:
    """Async mixin for general information handling."""
    PRODUCT_TO_RECOMMEND = None

    async def _build_general_info_chain(self):
        """Build chain for general information responses."""
        async def handle_general_info(inputs):
            return await ASYNC_HANDLERS_MAPPER[inputs['customer_intent']](
                self.llm,
                context=inputs["context"],
                customer_query=inputs["customer_query"],
            )
        
        return AsyncRunnableLambda(handle_general_info)


class AsyncJewelryConsultationMixin:
    """Async mixin for building conditional chains."""

    async def _build_jewelry_consultation_chain(self):
        """Build the complete jewelry consultation process chain."""
        async def process_jewelry_consultation(inputs):
            # Extract preferences
            inputs_with_prefs = await self._extract_all_preferences(inputs)
            
            # Check product match status
            product_match_status = await self._check_products_individually(inputs_with_prefs)
            inputs_with_prefs['product_match_status'] = product_match_status
            
            # Branch based on match status
            if product_match_status.startswith('FOUND'):
                if await self._all_preferences_collected(inputs_with_prefs):
                    return await self._handle_recommend_product(inputs_with_prefs)
                else:
                    return await self._handle_continue_discovery(inputs_with_prefs)
            else:
                return await self._handle_available_options_navigator(inputs_with_prefs)
        
        return AsyncRunnableLambda(process_jewelry_consultation)

    async def _extract_all_preferences(self, inputs):
        """Extract all preferences concurrently"""
        result = dict(inputs)
        
        # Extract preferences concurrently
        tasks = []
        for preference_key, config in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE.items():
            task = ASYNC_HANDLERS_MAPPER['extract_customer_preferences'](
                self.llm,
                config['model'],
                optimized_query=inputs['optimized_query_for_search']
            )
            tasks.append((preference_key, task))
        
        # Wait for all preference extractions
        for preference_key, task in tasks:
            result[preference_key] = await task
            
        return result

    async def _all_preferences_collected(self, inputs):
        """Check if all required preferences have been collected"""
        return all(
            inputs.get(key, {}).get(key, "") not in ("", None)
            for key in PreferenceDiscoveryStrategy.DISCOVERY_SEQUENCE
        )

    async def _handle_recommend_product(self, inputs):
        """Handle product recommendation"""
        return await ASYNC_HANDLERS_MAPPER['recommend_product'](
            self.llm,
            product_to_recommend=AsyncJewelryConsultationMixin.PRODUCT_TO_RECOMMEND,
            customer_query=inputs["customer_query"],
            **self._extract_preferences(inputs),
            conversation_history=inputs["conversation_history"]
        )

    async def _handle_continue_discovery(self, inputs):
        """Handle continuing preference discovery"""
        next_discovery_question = await sync_to_async(PreferenceDiscoveryStrategy.get_next_question)(
            self._extract_safe_preferences(inputs)
        )
        
        return await ASYNC_HANDLERS_MAPPER['discover_customer_preferences'](
            self.llm,
            context=inputs["context"],
            customer_query=inputs["customer_query"],
            next_discovery_question=next_discovery_question,
            **self._extract_safe_preferences(inputs),
            conversation_history=inputs["conversation_history"]
        )

    async def _handle_available_options_navigator(self, inputs):
        """Handle navigating available options"""
        return await ASYNC_HANDLERS_MAPPER['navigate_towards_available_options'](
            self.llm,
            context=inputs["context"],
            customer_query=inputs["customer_query"],
            mismatch_reason=inputs['product_match_status'],
            **self._extract_safe_preferences(inputs),
            conversation_history=inputs["conversation_history"]
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

    async def _extract_individual_products(self, context):
        """Extract individual products from context using regex."""
        return await sync_to_async(self._extract_individual_products_sync)(context)

    def _extract_individual_products_sync(self, context):
        """Sync version of product extraction"""
        return re.findall(r"Collection:.*?stars;", context, re.DOTALL)

    async def _check_products_individually(self, inputs):
        """Check each product individually until a match is found."""
        context = inputs["context"]
        preferences = {k: v for k, v in self._extract_safe_preferences(inputs).items() 
                      if k != 'purchase_type'}

        # Extract individual products
        individual_products = await self._extract_individual_products(context)
        print('preferences', preferences)

        if not individual_products:
            return "NOT_FOUND: No products found in context"

        # Use semaphore to limit concurrent API calls
        semaphore = asyncio.Semaphore(3)
        
        async def check_single_product(i, product):
            async with semaphore:
                try:
                    result = await ASYNC_HANDLERS_MAPPER['check_for_products_matching_customer_preferences'](
                        self.llm,
                        context=product,
                        **preferences
                    )
                    return i, product, result
                except Exception as e:
                    print(f"Error checking product {i}: {e}")
                    return i, product, None

        # Create tasks for all products
        tasks = [
            check_single_product(i, product) 
            for i, product in enumerate(individual_products, 1)
        ]
        
        # Process results as they complete
        last_reason = None
        for task in asyncio.as_completed(tasks):
            i, product, result = await task
            
            if result and not result.startswith('NOT_FOUND'):
                AsyncJewelryConsultationMixin.PRODUCT_TO_RECOMMEND = product
                return f"FOUND: Match found in product {i}"
            
            if result and result.startswith('NOT_FOUND'):
                last_reason = result

        # No matches found in any product
        return last_reason if last_reason else "NOT_FOUND: No matching products found"
