from . import tools


class AssistantAgent:

    def process(self, user, message):
        message = message.lower()

        if "گزارش روزانه" in message or "گزارش امروز" in message:
            return tools.get_daily_report_tool(user)

        elif "وظایف عقب‌افتاده" in message:
            return tools.get_overdue_tasks_tool(user)

        elif "وظایف مهم" in message:
            return tools.get_prioritized_tasks_tool(user)

        return "I couldn't understand your request."