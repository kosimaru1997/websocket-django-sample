from ninja import Schema


class CreateChatRoomRequest(Schema):
    name: str
    description: str