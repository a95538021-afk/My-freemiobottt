from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client

from config import SUPABASE_URL, SUPABASE_KEY


app = FastAPI()


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)



class WithdrawRequest(BaseModel):

    user_id: int

    target_username: str



# ================= BALANCE =================


@app.get("/balance/{user_id}")
def get_balance(user_id:int):

    result = (
        supabase
        .table("users")
        .select("balance")
        .eq("user_id", user_id)
        .execute()
    )


    if result.data:

        return {
            "balance":
            result.data[0]["balance"]
        }


    return {
        "balance":0
    }



# ================= WITHDRAW =================


@app.post("/withdraw")
def withdraw(data:WithdrawRequest):


    user = (
        supabase
        .table("users")
        .select("balance")
        .eq(
            "user_id",
            data.user_id
        )
        .execute()
    )


    if not user.data:

        return {
            "message":
            "کاربر پیدا نشد"
        }



    balance = user.data[0]["balance"]



    if balance <= 0:

        return {
            "message":
            "موجودی شما صفر است"
        }



    supabase.table(
        "withdraw_queue"
    ).insert({

        "user_id":
        data.user_id,

        "target_username":
        data.target_username,

        "amount":
        balance,

        "withdraw_type":
        "id",

        "status":
        0,

    }).execute()



    return {

        "message":
        "✅ درخواست برداشت ثبت شد"

    }
