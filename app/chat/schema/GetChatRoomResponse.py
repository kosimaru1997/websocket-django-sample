from typing import Optional

from ninja import Schema


class ChatRoom(Schema):
    user_id: str
    room_id: str
    last_message: Optional[str]
    unchecked_count: int
    updated_at: int


class GetChatRoomResponse(Schema):
    room_list: list[ChatRoom]
