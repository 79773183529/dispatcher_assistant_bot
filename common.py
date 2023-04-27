import emoji
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from with_file import start_registration


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    start_registration(message)
    await message.answer(emoji.emojize(":woman_raising_hand:"))
    await message.answer("Привет\nЯ ваш новый мобильный ассистент!!",
                         parse_mode=types.ParseMode.HTML
                         )


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(emoji.emojize(":woman_frowning:"))


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start", state="*")
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
