from datetime import date
import uuid

from postgrest import APIResponse
from pydantic import ValidationError

from config.supabase_config import createDatabaseClient
from supabase import SupabaseException
from supabase_auth import AuthResponse, UserResponse
from fastapi import UploadFile


from models.budgets import BudgetsModel
from models.categories import CategoriesModel
from models.goals import GoalsModel
from models.mpesa_drafts import MpesaDraftModel
from models.profiles import ProfilesModel
from models.recurring_rules import RecurringRulesModel
from models.transactions import TransactionModel


class SupabaseDatabase:

    def __init__(self) -> None:
        self.client = createDatabaseClient()

    # _________________________________PROFILES_________________________________________________

    # create user
    def signUpUSer(
        self,
        passwd: str,
        email: str,
        name: str | None,
        currency: str = "KES",
        timezone: str = "Africa/Nairobi",
    ):
        try:
            res: AuthResponse = self.client.auth.sign_up(
                {
                    "email": email,
                    "password": passwd,
                }
            )
            if res.user:
                user = res.user
                self.client.from_("profiles").insert(
                    {
                        "user_id": user.id,
                        "name": name,
                        "currency": currency,
                        "timezone": timezone,
                        "email": user.email,
                    }
                ).execute()
                return True
            raise Exception("Sign up failed")
        except (
            SupabaseException,
            ValidationError,
            TypeError,
            ValueError,
            Exception,
        ) as e:
            print(e.args)
            raise

    def loginUser(self, email: str, passwd: str):
        try:
            res: AuthResponse = self.client.auth.sign_in_with_password(
                {"email": email, "password": passwd}
            )
            return res.session
        except (SupabaseException, ValidationError, TypeError, ValueError, Exception):
            raise

    # retrieve user
    def getUser(self, access_token: str):
        try:
            res: UserResponse | None = self.client.auth.get_user(access_token)
            if not res:
                raise Exception("User not found")
            user_profile = (
                self.client.from_("profiles")
                .select("*")
                .eq("user_id", res.user.id)
                .single()
                .execute()
            )
            return ProfilesModel.model_validate(user_profile.data)
        except (
            SupabaseException,
            ValidationError,
            TypeError,
            ValueError,
        ):
            raise

    # ___________________________________________TRANSACTIONS_________________________________

    # add transaction
    def addTransaction(self, t: TransactionModel):
        try:
            (
                self.client.from_("transactions")
                .insert(
                    TransactionModel.model_dump(
                        t, exclude_none=True, exclude={"id", "deleted_at"}
                    )
                )
                .eq("user_id", t.user_id)
                .execute()
            )

            return t
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # get all transactions
    def getAllTransactions(self, user_id: uuid.UUID):
        try:
            res: list = (
                self.client.from_("transactions")
                .select("*")
                .eq("user_id", user_id)
                .execute()
                .data
            )
            return [TransactionModel.model_validate(t) for t in res]
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # fetch one transaction
    def getsingleTransaction(self, t_id: int, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("transactions")
                .select("*")
                .eq("user_id", user_id)
                .eq("id", t_id)
                .maybe_single()
                .execute()
            )
            if not res:
                return "Transaction not found."

            return TransactionModel.model_validate(res.data)
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # edit a transaction
    def editTransaction(
        self,
        t_id: int,
        c_id: int,
        user_id: uuid.UUID,
        amt: int | None,
        date: date | None,
        note: str | None,
        t_type: str | None,
    ):
        try:
            payload = {}
            if amt and date and note and t_type and c_id:
                payload = {
                    "transaction_amount": amt,
                    "transaction_type": t_type,
                    "category_id": c_id,
                    "transaction_date": date,
                    "transaction_note": note,
                }
            elif amt and date and t_type and note:
                payload = {
                    "transaction_amount": amt,
                    "transaction_type": t_type,
                    "category_id": c_id,
                    "transaction_date": date,
                    "transaction_note": note,
                }
            elif amt and date and t_type:
                payload = {
                    "transaction_amount": amt,
                    "transaction_date": date,
                    "transaction_type": t_type,
                    "category_id": c_id,
                }
            elif amt and date:
                payload = {
                    "transaction_amount": amt,
                    "transaction_date": date,
                    "category_id": c_id,
                }
            elif amt:
                payload = {
                    "transaction_amount": amt,
                    "category_id": c_id,
                }

            res: APIResponse = (
                self.client.from_("transactions")
                .update(payload)
                .eq("id", t_id)
                .eq("user_id", user_id)
                .execute()
            )

            if not res.count:
                return "Transaction NOT updated"

            return "Transaction updated"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # delete a transaction
    def deleteTransaction(self, t_id: int, user_id: uuid.UUID):
        try:
            (
                self.client.from_("transactions")
                .delete()
                .eq("id", t_id)
                .eq("user_id", user_id)
                .execute()
            )

            return "Transaction deleted"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # ____________________________________________CATEGORIES_________________________________________

    # get all categories
    def getAllCategories(
        self,
        user_id: uuid.UUID,
    ):
        try:
            res = (
                self.client.from_("categories")
                .select("*")
                .eq("user_id", user_id)
                .execute()
                .data
            )
            if not res:
                return "No categories found"
            return [CategoriesModel.model_validate(c) for c in res]
        except SupabaseException as se:
            raise
        except ValidationError as se:
            raise
        except ValueError as se:
            raise
        except TypeError as se:
            raise

    # create custom categories
    def createCustomCategory(
        self,
        c: CategoriesModel,
    ):
        try:

            (
                self.client.from_("categories")
                .insert(
                    json=CategoriesModel.model_dump(
                        c, exclude_none=True, exclude={"id", "deleted_at"}
                    )
                )
                .execute()
            )
            return "Category created"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # edit custom categories
    def editCategory(
        self,
        c_id: int,
        colour: str | None,
        icon: str | None,
        name: str | None,
        type: str | None,
        user_id: uuid.UUID,
    ):
        try:

            (
                self.client.from_("categories")
                .update(
                    {
                        "category_name": name,
                        "category_type": type,
                        "category_icon": icon,
                        "category_color": colour,
                    }
                )
                .eq("user_id", user_id)
                .eq("id", c_id)
                .execute()
            )

            return "Category updated"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # delete custom category
    def deleteCategory(self, c_id: int, user_id: uuid.UUID):
        try:
            self.client.from_("categories").delete().eq("id", c_id).eq(
                "user_id", user_id
            ).execute()
            return "Category deleted"
        except (SupabaseException, ValidationError, ValueError, TypeError, Exception):
            raise

    # __________________________________________________________BUDGETS____________________________________________________________________

    # get all budgets
    def getAllBudgets(self, user_id: uuid.UUID):
        try:
            response = (
                self.client.from_("budgets")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            if not response.data:
                return "No budgets recorded."

            return [BudgetsModel.model_validate(b) for b in response.data]
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # create new budget
    def createBudget(self, b: BudgetsModel):
        try:
            res = (
                self.client.from_("budgets")
                .insert(BudgetsModel.model_dump(b, exclude_none=True, exclude={"id"}))
                .execute()
            )

            return "Budget set"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # update existing budget
    def updateBudget(
        self, b_id: int | None, amount: int, c_id: int, user_id: uuid.UUID
    ):
        try:
            res = (
                self.client.from_("budgets")
                .update(
                    {
                        "limit_amount": amount,
                        "category_id": c_id,
                    }
                )
                .eq("id", b_id)
                .eq("user_id", user_id)
                .execute()
            )

            return "Budget updated."

        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    def deleteBudget(self, user_id: uuid.UUID, b_id: int):
        try:
            res = (
                self.client.from_("budgets")
                .delete()
                .eq("user_id", user_id)
                .eq("id", b_id)
                .execute()
            )

            return "Budget deleted"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # _____________________________________________GOALS___________________________________________________

    # create goal
    def createGoal(self, g: GoalsModel):
        try:
            res = (
                self.client.from_("goals")
                .insert(GoalsModel.model_dump(g, exclude={"id"}))
                .execute()
            )

            return "Goal has been set and saved"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # get all goals
    def getAllGoals(self, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("goals").select("*").eq("user_id", user_id).execute()
            )
            if not res.data:
                return "No goals found"
            return [GoalsModel.model_validate(g) for g in res.data]
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # contribute money to a goal
    def contributeToGoal(
        self, g_id: int, amount: int, user_id: uuid.UUID, update_date: date
    ):
        try:
            res = (
                self.client.from_("goal_contributions")
                .insert(
                    {
                        "goal_id": g_id,
                        "amount": amount,
                        "user_id": user_id,
                        "updated_at": update_date,
                    }
                )
                .execute()
            )

            return "Contribution Saved"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # delete goal
    def deleteGoal(self, g_id: int, user_id: uuid.UUID):
        try:
            (
                self.client.from_("goals")
                .delete()
                .eq("id", g_id)
                .eq("user_id", user_id)
                .execute()
            )

            return "Goal deleted"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # ______________________________________________MPESA_______________________________________________
    # save an mpesa draft
    def createDraft(self, d: MpesaDraftModel):
        try:
            res = (
                self.client.from_("mpesa_drafts")
                .insert(MpesaDraftModel.model_dump(d, exclude={"id"}))
                .execute()
            )

            return "Draft saved"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # retrieve drafts not confirmed
    def getAllDrafts(self, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("mpesa_drafts")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
            if not res.data:
                return "No drafts found."

            return [MpesaDraftModel.model_validate(m) for m in res.data]
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # confirm a pending draft
    def confirmPendingDraft(self, d_id: int, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("mpesa_drafts")
                .update({"status": "confirmed"})
                .eq("id", d_id)
                .eq("user_id", user_id)
                .execute()
            )

            if not res.count:
                return "Draft NOT confirmed."
            return "Draft confirmed"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # delete draft
    def deleteDraft(self, d_id: int, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("mpesa_drafts")
                .delete()
                .eq("user_id", user_id)
                .eq("id", d_id)
                .execute()
            )

            return "Draft deleted"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # _______________________________________RECURRING RULES________________________________________________

    # create a recurring rule
    def createRecurringRule(self, r: RecurringRulesModel):
        try:
            res = self.client.from_("recurring_rules").insert(r.model_dump()).execute()

            return "Rule saved"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # get all recurring rules
    def getAllRecurringRules(self, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("recurring_rules")
                .select("*")
                .eq("user_id", user_id)
                .execute()
                .data
            )

            return [RecurringRulesModel.model_validate(r) for r in res]
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # delete a rule
    def deleteRecurringRule(self, user_id: uuid.UUID, r_id: int):
        try:
            res = (
                self.client.from_("recurring_rule")
                .delete()
                .eq("user_id", user_id)
                .eq("id", id)
                .execute()
            )

            return "Rule deleted"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # ___________________________________RECEIPTS________________________________________

    # upload receipt image to storage
    async def uploadReceipt(self, img: UploadFile, t_id: int, user_id: uuid.UUID):
        try:
            file_bytes = await img.read()
            path = (
                self.client.storage.from_("transaction_receipts")
                .upload(
                    path=f"transaction_receipts/{user_id}/{img.filename}",
                    file=file_bytes,
                )
                .fullPath
            )
            if not path:
                return "Could not upload receipt"
            response = (
                self.client.from_("transactions")
                .update(
                    {
                        "transaction_receipt_url": path,
                    }
                )
                .eq("id", t_id)
                .eq("user_id", user_id)
                .execute()
            )
            if not response.count:
                return "Receipt url NOT updated "
            return "Receipt url updated"
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise

    # view receipt image
    def getReceiptUrl(self, t_id: int, user_id: uuid.UUID):
        try:
            res = (
                self.client.from_("transactions")
                .select("transaction_receipt_url")
                .eq("id", t_id)
                .eq("user_id", user_id)
                .single()
                .execute()
                .data
            )
            if not res:
                return "Could not find the receipt of that transaction"

            path_to_receipt: str = res["transaction_receipt_url"]  # type: ignore

            response = self.client.storage.from_(
                "transaction_receipts"
            ).create_signed_url(path=path_to_receipt, expires_in=300)
            return response
        except SupabaseException:
            raise
        except ValidationError:
            raise
        except ValueError:
            raise
        except Exception:
            raise


def get_db():
    try:
        sup = SupabaseDatabase()
        yield sup
    except Exception:
        raise
