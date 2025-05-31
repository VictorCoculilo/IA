import chainlit as cl

commands = [
    {"id": "Picture", "icon": "image", "description": "Use DALL-E"},
    {"id": "Search", "icon": "globe", "description": "Find on the web"},
    {
        "id": "Canvas",
        "icon": "pen-line",
        "description": "Collaborate on writing and code",
    },
]

@cl.on_chat_start
async def start():
    await cl.context.emitter.set_commands(commands)

@cl.on_message
async def message(msg: cl.Message):
    print(msg)
    if msg.command == "Picture":
        print("User is using the Picture command")
    elif msg.command == "Search":
        print("User is using the Search command")