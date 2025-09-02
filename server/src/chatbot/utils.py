def build_conversation_history(conversation_state, user_query):
    conversation_history = []
    messages = conversation_state['channel_values']['messages']
    user_messages = [msg.content.split('INPUT:')[-1].strip()
                     for msg in messages if msg.__class__.__name__ == 'HumanMessage']
    assistant_messages = [msg.content.strip()
                          for msg in messages if msg.__class__.__name__ == 'AIMessage']

    for i in range(len(user_messages)):
        conversation_history.append(
            f'{i + 1}. user: {user_messages[i]}, assistant: {assistant_messages[i]};')

    conversation_history.append(
        f'{len(user_messages) + 1}. user: {user_query};')

    return conversation_history
