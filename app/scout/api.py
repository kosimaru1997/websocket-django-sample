from ninja import Router

from app.scout.schema.scout_res import Scout, ScoutResponse

scout_router = Router(tags=["scout"])


@scout_router.get("/", response=ScoutResponse)
def get_scout(request):
    scout = Scout(company_id=1, displayed_name='株式会社HOGE', scout_message="messageです")
    scout_res = ScoutResponse(scout=[scout])
    return scout_res
