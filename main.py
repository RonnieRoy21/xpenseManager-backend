from fastapi import FastAPI, APIRouter
from routers.alerts import alerts_router
from routers.analytics import analytics_router
from routers.budgets import budgets_router
from routers.categories import categories_router
from routers.goals import goals_router
from routers.insights import insights_router
from routers.mpesa import mpesa_router
from routers.receipts import receipts_router
from routers.recurring import recurring_router
from routers.transactions import transaction_router
from routers.me import me_router

app = FastAPI(
    title="XpenseManager API",
)

main_router = APIRouter(prefix="/api/v1")
main_router.include_router(alerts_router)
main_router.include_router(analytics_router)
main_router.include_router(budgets_router)
main_router.include_router(categories_router)
main_router.include_router(goals_router)
main_router.include_router(insights_router)
main_router.include_router(me_router)
main_router.include_router(mpesa_router)
main_router.include_router(receipts_router)
main_router.include_router(recurring_router)
main_router.include_router(transaction_router)


app.include_router(main_router)


@main_router.get("/health")
def health_check():
    return {"status": "OK"}
