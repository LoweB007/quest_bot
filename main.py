import logging
from aiogram import Bot, Dispatcher, executor, types
from quest1 import Location, read_quest, Path, quests_list
from aiogram.types import Message, InputFile, InputMediaPhoto, InputMediaVideo

# Объект бота
bot = Bot(token="1682510407:AAGqeOlhiO_qWmPCUFc90Lr7CLllTh5Vh6Q")
# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
txt, path_texts = "", []
loc = ""
pathes = []
quest = False


# Хэндлер на команду /test1
@dp.message_handler(commands="test1")
async def cmd_test1(message: types.Message):
    await message.reply("Test 1")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard_quest = types.ReplyKeyboardMarkup()
    quests = quests_list()
    for n, txt in quests:
        button_1 = types.KeyboardButton(text=f"{n}. {txt}")
        keyboard_quest .add(button_1)
    await message.answer("выберите квест", reply_markup=keyboard_quest)


@dp.message_handler(lambda message: message.text[:1].isdigit())
async def run_to_path(message: types.Message):
    global pathes, quest
    if quest:
        ans = int(message.text[:1])
        path = Path(pathes[ans - 1][0], pathes[ans - 1][1], pathes[ans - 1][2],
                    [pathes[ans - 1][3], pathes[ans - 1][4]])
        actloc = path.activate()
        loc = Location(actloc)
        text, pathes = loc.activate()
        keyboard = types.ReplyKeyboardMarkup()
        for n, txt in enumerate(pathes):
            button_1 = types.KeyboardButton(text=f"{n + 1}. {txt[1]}")
            keyboard.add(button_1)
        await message.answer(text, reply_markup=keyboard)
        if pathes == []:
            await message.reply("квест завершен", reply_markup=types.ReplyKeyboardRemove())
            return
    else:
        actloc = read_quest(int(message.text[:1]))
        quest = True
        loc = Location(actloc)
        text_loc, pathes = loc.activate()
        keyboard = types.ReplyKeyboardMarkup()
        if "/" in text_loc:
            text, image = text_loc.split("/")
            photo = InputFile(f"./images/{image}")
            print(photo)
            await bot.send_photo(chat_id=message.chat.id, photo=photo)
        else:
            text = text_loc
        for n, txt in enumerate(pathes):
            button_1 = types.KeyboardButton(text=f"{n + 1}. {txt[1]}")
            keyboard.add(button_1)

        await message.answer(text, reply_markup=keyboard)
if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
