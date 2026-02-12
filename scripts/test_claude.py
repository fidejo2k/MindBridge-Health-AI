import anthropic
import os

# Get API key from environment variable
api_key = os.environ.get("ANTHROPIC_API_KEY")

# Create the client
client = anthropic.Anthropic(api_key=api_key)

# Call Claude!
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Hello! Please respond with: 'MindBridge Health CLI is working!'"}
    ]
)

# Print the response
print(message.content[0].text)