import re


def build_conversation_history(conversation_state, user_query, max_messages=20):
    """
    Build conversation history with the last max_messages user-AI message pairs.

    Args:
        conversation_state: Dictionary containing the conversation state with messages.
        user_query: The current user query to append.
        max_messages: Maximum number of previous message pairs to include (default: 3).

    Returns:
        List of strings representing the conversation history.

    Raises:
        ValueError: If the number of user and AI messages is not equal.
    """
    conversation_history = []
    messages = conversation_state['channel_values']['messages']

    # Extract user and assistant messages
    user_messages = [msg.content.split('INPUT:')[-1].strip()
                     for msg in messages if msg.__class__.__name__ == 'HumanMessage']
    assistant_messages = [msg.content.strip()
                          for msg in messages if msg.__class__.__name__ == 'AIMessage']

    # Validate that user and assistant messages are paired (equal counts)
    if len(user_messages) != len(assistant_messages):
        raise ValueError(
            f"Mismatched message counts: {len(user_messages)} user messages, "
            f"{len(assistant_messages)} assistant messages. Expected equal counts."
        )

    # Take the last max_messages pairs (or fewer if not enough pairs)
    num_pairs = len(user_messages)
    start_index = max(0, num_pairs - max_messages)

    # Build history with the most recent message pairs
    for i in range(start_index, num_pairs):
        conversation_history.append(
            f'{i + 1}. user: {user_messages[i]}, assistant: {assistant_messages[i]};')

    # Append the current user query
    conversation_history.append(
        f'{num_pairs + 1}. user: {user_query};')

    return conversation_history


def filter_chunk_with_most_keywords(keywords, relevant_chunks, k=10):
    if not relevant_chunks:
        return None

    # Split keywords into list
    keyword_list = keywords.split()

    # For each chunk, count exact keyword occurrences (case-insensitive whole word match)
    chunk_scores = []
    for chunk in relevant_chunks:
        chunk_text_lower = chunk.page_content.lower()
        score = sum(1 for keyword in keyword_list if re.search(r'\b{}\b'.format(
            re.escape(keyword.lower())), chunk_text_lower, re.IGNORECASE))
        chunk_scores.append((chunk, score))

    # Filter chunks with at least one keyword match
    valid_chunks = [(chunk, score)
                    for chunk, score in chunk_scores if score > 0]

    # If no chunks have any matches, return None
    if not valid_chunks:
        return None

    # Find the chunk with the maximum score
    max_chunk = max(valid_chunks, key=lambda x: x[1])[0]

    return max_chunk
