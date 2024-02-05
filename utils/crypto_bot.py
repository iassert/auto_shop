import asyncio

from aiocryptopay import AioCryptoPay, Networks

from asyncio import Event

from typing import Callable


class Crypto:
    @staticmethod
    async def paid(invoice_id: int, wait: bool = False, func: Callable = None) -> bool:
        Executor.event.set()
        event = Event()

        Executor.invoices[invoice_id] = [
            event,
            func
        ]

        if wait:
            return await event.wait()


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
        while True:
            if not Executor.invoices:
                await Executor.event.wait()
                Executor.event = Event()

            invoices = await Executor.crypto.get_invoices(
                invoice_ids = [
                    *Executor.invoices.keys()
                ]
            )

            for invoice in invoices:
                if invoice.status == "paid" and invoice.invoice_id in Executor.invoices:
                    event, func = Executor.invoices[invoice.invoice_id]
                    event.set()
                    Executor.invoices.pop(invoice.invoice_id)

                    if func is not None:
                        asyncio.create_task(func())

            await asyncio.sleep(Executor.defult_delay)
