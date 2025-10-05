from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=200,
        help_text="User's message to the chatbot",
    )

    def validate_message(self, value):
        """Validate the message field"""
        if not value.strip():
            raise serializers.ValidationError(
                "Message cannot be empty",
            )

        return value.strip()


class ChatResponseSerializer(serializers.Serializer):
    response = serializers.CharField(
        help_text="Chatbot's response",
    )
    success = serializers.BooleanField(
        help_text='Whether the request was successful',
    )
    error = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text='Error message if any',
    )
