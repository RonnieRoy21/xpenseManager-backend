from fastapi import APIRouter, HTTPException
from models.categories import CategoriesModel
from exceptions.handler import get_error_type
from dependency.all_dependencies import verified, db

categories_router = APIRouter(prefix="/categories")


# health check
@categories_router.get("/health")
def health_check():
    return {"status": "OK"}


# get all categories
@categories_router.get("/all")
def get_all_categories(
    v: verified,
    db: db,
):
    try:
        return db.getAllCategories(
            user_id=v.user_id,
        )
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# add new custom category
@categories_router.post("/new")
def add_new_custom_category(v: verified, db: db, category: CategoriesModel):
    try:
        category.user_id = v.user_id
        return db.createCustomCategory(c=category)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# rename or edit custom category
@categories_router.patch("/edit/{id}")
def edit_custom_category(
    v: verified,
    db: db,
    id: int,
    categoryName: str | None = "",
    categoryType: str | None = "",
    categoryIcon: str | None = "",
    categoryColor: str | None = "",
):
    try:
        return db.editCategory(
            c_id=id,
            name=categoryName,
            colour=categoryColor,
            icon=categoryIcon,
            type=categoryType,
            user_id=v.user_id,
        )

    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))


# delete custom category
@categories_router.delete("/delete/{id}")
def delete_custom_category(v: verified, db: db, id: int):
    try:
        return db.deleteCategory(c_id=id, user_id=v.user_id)
    except Exception as e:
        err = get_error_type(e=e)
        raise HTTPException(detail=err["message"], status_code=int(err["status"]))
