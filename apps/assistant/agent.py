from . import tools
from .llm import request_tool_call, generate_response


class AssistantAgent:
    # def detect_intent(self, message):
    #     message = message.lower()

    #     if "وظیفه جدید" in message or "ایجاد وظیفه" in message:
    #         return "create_task"

    #     if "گزارش روزانه" in message or "گزارش امروز" in message:
    #         return "daily_report"

    #     if any(
    #         word in message
    #         for word in [
    #             "وظایف عقب‌افتاده",
    #             "کارهای عقب‌افتاده",
    #             "کارهایی که عقب افتاده",
    #             "چه کارهایی از من عقب افتاده",
    #         ]
    #     ):
    #         return "overdue_tasks"

    #     if "وظایف مهم" in message or "کارهای مهم" in message:
    #         return "prioritized_tasks"

    #     return "unknown"

    def process(self, user, message):
        return request_tool_call(user, message)

    #     intent = self.detect_intent(message)

    #     if intent == "create_task":
    #         entities = self.extract_entities(message)

    #         title = entities.get("title")

    #         if not title:
    #             return {"success": False, "message": "عنوان وظیفه مشخص نشده است."}

    #         task = tools.create_task(
    #             user=user, title=title, priority=entities["priority"]
    #         )

    #         return {
    #             "success": True,
    #             "message": "وظیفه با موفقیت ایجاد شد.",
    #             "task": {
    #                 "id": str(task.id),
    #                 "title": task.title,
    #                 "priority": task.priority,
    #             },
    #         }

    #     if intent == "daily_report":
    #         return tools.get_daily_report_tool(user)

    #     elif intent == "overdue_tasks":
    #         return tools.get_overdue_tasks_tool(user)

    #     elif intent == "prioritized_tasks":
    #         return tools.get_prioritized_tasks_tool(user)

    #     # اگر درخواست با قوانین فعلی شناسایی نشد
    #     return generate_response(message)

    # def extract_entities(self, message):
    #     entities = {}
    #     message = message.strip()

    #     # Extract priority
    #     priority_keywords = {
    #         "اولویت فوری": "urgent",
    #         "اولویت بالا": "high",
    #         "اولویت متوسط": "medium",
    #         "اولویت پایین": "low",
    #     }

    #     for keyword, priority in priority_keywords.items():
    #         if keyword in message:
    #             entities["priority"] = priority
    #             message = message.replace(keyword, "", 1)
    #             break

    #     entities.setdefault("priority", "medium")

    #     # Extract title
    #     title_keywords = [
    #         "یک وظیفه جدید با عنوان",
    #         "وظیفه جدید با عنوان",
    #         "با عنوان",
    #     ]

    #     for keyword in title_keywords:
    #         if keyword in message:
    #             title = message.split(keyword, 1)[1]

    #             title = title.replace("ایجاد کن", "")
    #             title = title.strip().removesuffix("و").strip()

    #             entities["title"] = title
    #             break

    #     return entities
