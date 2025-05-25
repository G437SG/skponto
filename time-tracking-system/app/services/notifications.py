from flask import current_app
from firebase_admin import messaging

class NotificationService:
    @staticmethod
    def send_notification_to_user(user_id, title, body):
        # Logic to send a notification to a specific user
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=user_id,  # Assuming user_id is the FCM token
        )
        response = messaging.send(message)
        return response

    @staticmethod
    def send_notification_to_group(group_id, title, body):
        # Logic to send a notification to a group of users
        # This would typically involve fetching user tokens from the database
        user_tokens = NotificationService.get_user_tokens_by_group(group_id)
        messages = [
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=token,
            ) for token in user_tokens
        ]
        response = messaging.send_all(messages)
        return response

    @staticmethod
    def send_global_notification(title, body):
        # Logic to send a global notification to all users
        # This would typically involve fetching all user tokens from the database
        user_tokens = NotificationService.get_all_user_tokens()
        messages = [
            messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=token,
            ) for token in user_tokens
        ]
        response = messaging.send_all(messages)
        return response

    @staticmethod
    def get_user_tokens_by_group(group_id):
        # Placeholder for fetching user tokens by group from the database
        return []

    @staticmethod
    def get_all_user_tokens():
        # Placeholder for fetching all user tokens from the database
        return []