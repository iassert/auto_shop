from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboardBuilder(InlineKeyboardMarkup):
    def row(self, *buttons):
        super().row(*[
            (
                InlineKeyboardButton(i, callback_data = i) if isinstance(i, str)
                else i
            ) for i in buttons
        ])