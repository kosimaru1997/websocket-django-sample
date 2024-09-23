from ninja import Schema


class CreateChatRequest(Schema):
    user_id: str
    message: str
    message_id: str
    