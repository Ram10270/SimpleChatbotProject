from aiohttp import web
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

import os

# Define the bot adapter settings
adapter_settings = BotFrameworkAdapterSettings(
    app_id=os.getenv("MICROSOFT_APP_ID", ""),   # Set your app ID if required
    app_password=os.getenv("MICROSOFT_APP_PASSWORD", "")
)
adapter = BotFrameworkAdapter(adapter_settings)

# Simple dictionary-based response handler
RESPONSES = {
    "hello": "Hello! How can I assist you today?",
    "help": "I am a simple chatbot. You can say 'hello', 'help', or type any question!",
    "goodbye": "Goodbye! Have a great day!",
}

# Helper function to process user input and determine the response
def handle_user_input(user_input):
    """
    Process user input and return an appropriate response.
    Handles basic cases of 'hello', 'help', 'goodbye', or echoes back the input.
    """
    normalized_input = user_input.lower().strip()

    if normalized_input in RESPONSES:
        return RESPONSES[normalized_input]
    elif "?" in normalized_input:
        return "I'm still learning! Let me get back to you on that."
    else:
        return f"I heard you say: {user_input}"

# Main message handler function
async def messages(req: web.Request) -> web.Response:
    # Read the incoming message from the user
    body = await req.json()
    activity = Activity().deserialize(body)

    # Define the response handler for the TurnContext
    async def message_handler(turn_context: TurnContext):
        response_text = handle_user_input(turn_context.activity.text)
        await turn_context.send_activity(response_text)

    # Process the activity using process_activity, not send_activity
    await adapter.process_activity(activity, "", message_handler)
    return web.Response(status=200)

# Set up the web server and route
app = web.Application()
app.router.add_post("/api/messages", messages)

# Run the app on localhost port 3978
if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3978)
