import asyncio
import logging

from loader import bot
from utils  import send_all_admin
from utils.db_api.sqlite import get_userx, update_userx, add_invoice, del_invoice, get_all_invoice
from keyboards.default   import check_user_out_func

from typing   import Callable
from asyncio  import Event
from aiocryptopay import AioCryptoPay, Networks



class Crypto:
    @staticmethod
    async def paid(
        invoice_id: int, 
        user_id:    int, 
        username:   str | None, 
        first_name: str,
    ) -> bool:

        Executor.invoices[invoice_id] = [
            user_id,
            username,
            first_name
        ]
        await add_invoice(invoice_id, user_id, username, first_name)



class Executor:
    crypto: AioCryptoPay = None
    defult_delay: float = 0.300

    event = Event() 
    invoices: dict[int, tuple[Event, Callable]] = {}


    def __init__(self, token: str, network: Networks = Networks.MAIN_NET):
        Executor.crypto = AioCryptoPay(
            token   = token, 
            network = network
        )

    @staticmethod
    def get_crypto() -> AioCryptoPay:
        return Executor.crypto


    def start_polling(self) -> None:
        asyncio.create_task(Executor.polling())


    @staticmethod
    async def polling() -> None:
        for (
            invoice_id, 
            user_id, 
            username, 
            first_name
        ) in await get_all_invoice():
            if invoice_id in Executor.invoices:
                continue
            
            Executor.invoices[invoice_id] = [
                user_id,
                username,
                first_name
            ]

        while True:
            if not Executor.invoices:
                await Executor.event.wait()
                Executor.event = Event()
            
            try:
                invoices = await Executor.crypto.get_invoices(
                    invoice_ids = [
                        *Executor.invoices.keys()
                    ]
                )
            except BaseException as ex:
                logging.error(f"{ex.__class__.__name__}: {ex}")
                await asyncio.sleep(Executor.defult_delay)
                continue

            for invoice in invoices:
                if invoice.status == "paid" and invoice.invoice_id in Executor.invoices:
                    [
                        user_id,
                        username,
                        first_name
                    ] = Executor.invoices[invoice.invoice_id]

                    Executor.invoices.pop(invoice.invoice_id)

                    asyncio.create_task(
                        refill(
                            user_id, 
                            username, 
                            first_name, 
                            invoice.amount,
                            invoice.invoice_id
                        )
                    )

            await asyncio.sleep(Executor.defult_delay)

async def refill(
    user_id: int, 
    username: str | None, 
    first_name: str, 
    pay_amount: int, 
    invoice_id: int
):
    get_user_info = await get_userx(user_id = user_id)
    
    await update_userx(
        user_id,
        balance    = int(get_user_info[4]) + pay_amount,
        all_refill = int(get_user_info[5]) + pay_amount
    )

    await bot.send_message(
        user_id,
        f"<b>✅ Вы успешно пополнили баланс на сумму {pay_amount}$. Удачи ❤</b>\n",
        reply_markup = check_user_out_func(user_id)
    )

    await send_all_admin(
        f"<b>💰 Пользователь</b> "
        f"(@{username}|<a href='tg://user?id={user_id}'>{first_name}</a>"
        f"|<code>{user_id}</code>) "
        f"<b>пополнил баланс на сумму</b> <code>{pay_amount}$</code> 🤖\n"
        f"📃 <b>invoice id:</b> <code>+{invoice_id}</code>"
    )

    await del_invoice(invoice_id)
