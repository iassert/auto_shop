import logging
from aiogram.types import Update
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError, UserDeactivated,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter, CantParseEntities, MessageCantBeDeleted,
                                      TerminatedByOtherGetUpdates)

from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, CantDemoteChatCreator):
        logging.debug("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.debug('Message is not modified')
        return True

    if isinstance(exception, MessageCantBeDeleted):
        logging.debug('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.debug('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.debug('MessageTextIsEmpty')
        return True

    if isinstance(exception, UserDeactivated):
        return True

    if isinstance(exception, Unauthorized):
        logging.info(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        return True

    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TerminatedByOtherGetUpdates):
        print("You already have an active bot. Turn it off.")
        logging.exception(f'TerminatedByOtherGetUpdates: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        await Update.get_current().message.answer(f"❗ Ошибка HTML разметки\n"
                                                  f"▶ `{exception.args}`\n"
                                                  f"❕ Выполните заново действие с правильной разметкой тэгов.",
                                                  parse_mode="Markdown")
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True

    logging.exception(f'Update: {update} \n{exception}')
