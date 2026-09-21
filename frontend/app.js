const tg = window.Telegram.WebApp;

tg.ready();

tg.expand();


const user = tg.initDataUnsafe.user;


let userId = null;


if(user){

    userId = user.id;

}


async function loadBalance(){

    if(!userId){

        document.getElementById("status").innerText =
        "خطا: تلگرام شناسایی نشد";

        return;

    }


    let response = await fetch(
        "https://YOUR-RENDER-URL.com/balance/" + userId
    );


    let data = await response.json();


    document.getElementById("balance").innerText =
    data.balance + " Mio";

}



async function withdraw(){

    let target = prompt(
        "آیدی مقصد را وارد کنید:"
    );


    if(!target)
        return;


    let response = await fetch(
        "https://YOUR-RENDER-URL.com/withdraw",
        {
            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                user_id:userId,

                target_username:target

            })
        }
    );


    let data = await response.json();


    document.getElementById("status").innerText =
    data.message;

}



async function invite(){

    document.getElementById("status").innerText =
    "لینک دعوت شما در حال ساخت است";

}



async function daily(){

    document.getElementById("status").innerText =
    "در حال بررسی میو روزانه";

}



loadBalance();
