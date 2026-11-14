import json

from django.conf import settings
from groq import Groq

from . import tools


client = Groq(api_key=settings.GROQ_API_KEY)


def generate_response(message):
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful AI personal assistant."},
            {"role": "user", "content": message},
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


available_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_overdue_tasks_tool",
            "description": "Get the user's overdue tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_daily_report_tool",
            "description": "Get the user's daily task report.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_prioritized_tasks_tool",
            "description": "Get the user's prioritized tasks.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_task_tool",
            "description": "Create a new task for the user.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Task title",
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "urgent"],
                    },
                },
                "required": ["title", "priority"],
            },
        },
    },
]


def request_tool_call(user, message):
    messages = [
        {
            "role": "system",
            "content": """
    You are Mindra, an AI personal assistant.
    Always respond in Persian.

    Response formatting rules:
    - Use clear and organized Persian.
    - Keep responses concise and readable.
    - Use bullet points instead of Markdown tables.
    - For task lists, show each task separately.
    - Display task title, priority, and due date.
    - Translate priority values:
    low = پایین
    medium = متوسط
    high = بالا
    urgent = فوری
    - Display dates in a readable format.
    - If there are no tasks, clearly say so.
    - Avoid unnecessary introductions and conclusions.
    - Never invent task information.
    """,
        },
        {"role": "user", "content": message},
    ]

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=available_tools,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        return assistant_message.content

    messages.append(assistant_message)

    for tool_call in assistant_message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name == "get_overdue_tasks_tool":
            result = tools.get_overdue_tasks_tool(user)

        elif function_name == "get_daily_report_tool":
            result = tools.get_daily_report_tool(user)

        elif function_name == "get_prioritized_tasks_tool":
            result = tools.get_prioritized_tasks_tool(user)

        elif function_name == "create_task_tool":
            task = tools.create_task(
                user=user,
                title=arguments["title"],
                priority=arguments["priority"],
            )

            result = {
                "id": str(task.id),
                "title": task.title,
                "priority": task.priority,
            }

        else:
            result = {"error": "Unknown tool"}

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, default=str),
            }
        )

    final_response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
    )

    return final_response.choices[0].message.content
