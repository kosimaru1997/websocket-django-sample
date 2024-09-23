from ninja import Schema


class Scout(Schema):
    company_id: int
    displayed_name: str
    scout_message: str


class ScoutResponse(Schema):
    scout: list[Scout]
