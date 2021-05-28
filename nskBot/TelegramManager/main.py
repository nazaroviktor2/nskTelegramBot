import logging
import re
import os
from aiogram import Bot, Dispatcher, executor, types
from exceptions import NotFoundTransfer, NotFoundUser, NotFound, NotFoundTool, NotFoundLocation, NotEnoughTools, \
    HaveNewLocation
from db import *

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
CREATOR_ID = os.getenv("CREATOR_ID")
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

WORKER_COMMANDS = ["/"]

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply(f"Привет, я бот NSK.\n"
                        f"Если Вы новый работник, обратись к персанулу и назовите им Ваш id!\n"
                        f"Ваш id - {message.from_user.id} ")


@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    answer = [f"Ваш id - {message.from_user.id}"]

    try:
        statuses = get_user_status(message.from_user.id)
        if statuses[0]:  # worker
            answer.append("/me - узнать информацию о себе")
            answer.append("/me_id - узнать свой id")
            answer.append("/get_tools - список интсрументов")
            answer.append("/get_locations - список адресов")
            answer.append("/get_transfers - список запросов")
            answer.append(
                "/create_transfer [id_tool] [id_new_location] [count] - создать запрос на перемещение инстуремента ")

        if statuses[1]:  # staff
            answer.append("/add_tool [id_location] [count] [name_of_tool] - добавить новый инсрумент")
            answer.append("/delete_tool [id_of_tool] - удалить инсрумент")
            answer.append("/accept_transfer [id] - принять запрос на перемещение")
            answer.append("/accept_all_transfers - принять все запросы на перемещение")
            answer.append("/reject_transfer [id]  - отклонить запрос на перемещение")
            answer.append("/reject_all_transfers  - отклонить все запросы на перемещение")
            answer.append("/add_worker [id_user] [name_user] - повысыть пользователя до рабочего")
            answer.append("/delete_worker [id_user]  - забрать у пользователя роль рабочего")
            answer.append("/get_workers  - получить список всех рабочих")

        if statuses[2]:  # admin
            answer.append("/add_location [name_of_location] - добавить новый адрес")
            answer.append("/delete_location [id_of_location] - удалить адрес")
            answer.append("/add_staff [id_user] [name_user] - повысть пользователя до сотрудника")
            answer.append("/delete_staff [id_user]  - забрать у пользователя роль сотрудника")
            answer.append("/get_staff - получить список всех сотрудников")
            answer.append("/get_admins - получить список всех администраторов")

        if statuses[3]:  # creator
            answer.append("/add_admin [id_user] [name_user] - повысить пользователя до администратора")
            answer.append("/delete_admin [id_user]  - забрать у пользователя роль администратора")
            answer.append("/add_creator [id_user] [name_user] - повысить пользователя до создателя")
            answer.append("get_creators - получить список всех создателей")
            answer.append("/get_users - получить список всех пользователей")
            answer.append("/delete_user [id_user] - удалить пользователя из системы (удаляются все его упоминания)")

        await message.reply("\n".join(answer))
    except (NotFoundUser, TypeError):
        await message.reply(f"Вас нет в базе, обратись к персаналу и назовите им ваш id\n"
                            f"Ваш id - {message.from_user.id} ")


@dp.message_handler(commands=['me_id'])
async def send_id(message: types.Message):
    await message.reply(f"Ваш id - {message.from_user.id}")


@dp.message_handler(commands=['add_location', 'add_loc', 'al'])
async def send_add_location(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=1)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        try:
            add_location(s[1])
            await message.reply(f"Локация с именем  - {s[1]} - добавлена ")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить локацию используете /add_location [name_of_location]")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['delete_location', 'del_loc', 'dl'])
async def send_delete_location(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)

    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        try:
            delete_location(s[1])

            await message.reply(f"Локация с id - {s[1]} - удалена ")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы удалить локацию используете /delete_location [id_of_location]")
        except NotFound:
            await message.reply(f"Локация с id - {s[1]} - не найдена ")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_locations', 'get_loc', 'gl'])
async def send_get_locations(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if worker or staff or admin or creator:
        answer = get_locations()
        if not answer:
            await message.reply(f"У вас нет не одной локации!\n"
                                f"Чтобы добавить локацию используете /add_location [name_of_location]")
        else:

            answer.insert(0, "ID   Локация")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['add_tool', 'atool', "at"])
async def send_add_tool(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=4)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:
            add_tool(s[1], s[2], s[3])
            await message.reply(f"Инструмент с именем  - {s[3]} - добавлен")
        except (IndexError, psycopg2.errors.SyntaxError, psycopg2.errors.InvalidTextRepresentation):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить локацию используете /add_tool [id_location] [count] [name_of_tool]")
        except NotFoundLocation:

            await message.reply(f"Локация с id - {s[1]} - не найден ")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['delete_tool', 'del_tool', 'dtool'])
async def send_delete_tool(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:
            delete_tool(s[1])
            await message.reply(f"Инструмент с id - {s[1]} - удален")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы удалить интрумент используете /delete_tool [id_of_tool]")
        except NotFound:
            await message.reply(f"Инструмент с id - {s[1]} - не найден ")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_tools', 'gt'])
async def send_get_tools(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if worker or staff or admin or creator:
        answer = get_tools()
        if not answer:
            await message.reply(f"У вас нет не одного инстумента!\n"
                                f"Чтобы добавить инструмент используете /add_tools [name_of_tool]")
        else:

            answer.insert(0, "ID IDЛокации  Кол-во Название")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['create_transfer', 'create_tr', "ctr"])
async def send_create_transfer(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=4)

    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if worker and not (staff or admin or creator):
        try:
            create_transfer(message.from_user.id, s[1], s[2], int(s[3]))
            await message.reply(f"Запрос на перемещение добавлен, ожидайте когда его одобрят")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить добавить запрос на перемещение используете\n"
                                f"/create_transfer [id_tool] [id_new_location] [count]")
        except NotFoundLocation:
            await message.reply(f"Локация с id - {s[1]} - не найден ")
        except NotFoundTool:
            await message.reply(f"Инструмент с id - {s[1]} - не найден ")
        except NotEnoughTools as e:
            await message.reply(f"Инструмент с id - {s[1]} - не имеет такого количества")
            await message.reply(e.txt)
    elif staff or admin or creator:
        try:
            create_transfer_with_accept(message.from_user.id, s[1], s[2], int(s[3]))
            await message.reply(f"Запрос на перемещение добавлен и одобрен")

        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить добавить запрос на перемещение используете\n"
                                f"/add_transfer [id_tool] [id_new_location] [count]")
        except NotFoundLocation:
            await message.reply(f"Локация с id - {s[1]} - не найден ")
        except NotFoundTool:
            await message.reply(f"Инструмент с id - {s[1]} - не найден ")
        except NotEnoughTools as e:
            await message.reply(f"Инструмент с id - {s[1]} - не имеет такого количества")
            await message.reply(e.txt)

    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['accept_all_transfers', 'accept_all_tr', "a_all_tr", "atr_all"])
async def send_accept_all_transfers(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:

            answer = accept_all_transfers()
            if not answer:
                await message.reply(f"У вас нет не одного запроса")
            else:
                await message.reply("\n".join(answer))
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы принять все запросы на перемещение\n"
                                f"/accept_all_transfers")
        except NotFoundLocation:
            await message.reply(f"Локация с id - {s[1]} - не найден ")
        except NotFoundTool:
            await message.reply(f"Инструмент с id - {s[1]} - не найден ")
        except NotEnoughTools as e:
            await message.reply(f"Инструмент с id - {s[1]} - не имеет такого количества")
            await message.reply(e.txt)
        except NotFoundTransfer:
            await message.reply(f"Запрос с id - {s[1]} не найден")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['accept_transfer', 'accept_tr', "atr"])
async def send_accept_transfer(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:
            accept_transfer(int(s[1]))
            await message.reply(f"Запрос на перемещение с id - {s[1]} одобрен")
        except (IndexError, psycopg2.errors.SyntaxError, ValueError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы принять запрос на перемещение используете\n"
                                f"/accept_transfer [id]")
        except NotFoundLocation:
            await message.reply(f"Локация с id - {s[1]} - не найден ")
        except NotFoundTool:
            await message.reply(f"Инструмент с id - {s[1]} - не найден ")
        except NotEnoughTools as e:
            await message.reply(f"Инструмент с id - {s[1]} - не имеет такого количества")
            await message.reply(e.txt)
        except NotFoundTransfer:
            await message.reply(f"Запрос с id - {s[1]} не найден")

    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['reject_transfer', 'reject_tr', "rtr"])
async def send_reject_transfer(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:
            delete_transfer(int(s[1]))
            await message.reply(f"Запрос на перемещение с id - {s[1]} отклонен")
        except (IndexError, psycopg2.errors.SyntaxError, ValueError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы принять запрос на перемещение используете\n"
                                f"/reject_transfer [id]")
        except NotFoundTransfer:
            await message.reply(f"Запрос с id - {s[1]} не найден")

    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['reject_all_transfers', 'reject_all_tr', "r_all_tr", "rtr_all"])
async def send_accept_all_transfers(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:

            answer = reject_all_transfers()
            if not answer:
                await message.reply(f"У вас нет не одного запроса")
            else:
                await message.reply("\n".join(answer))
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы принять все запросы на перемещение\n"
                                f"/reject_all_transfers")
        except NotFoundTransfer:
            await message.reply(f"Запрос с не найден")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_transfers', 'gtr'])
async def send_get_transfers(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if worker or staff or admin or creator:
        answer = get_transfers()
        if not answer:
            await message.reply(f"У вас нет не одного запроса")
        else:

            answer.insert(0, "ID User  Last   New Tool number ")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['me'])
async def send_welcome(message: types.Message):
    answer = [f"Ваш id - {message.from_user.id}"]
    try:
        statuses = get_user_status(message.from_user.id)
        if statuses[3]:
            answer.append(f"Вы - создатель")
            answer.append(f"Вы можете удалять и добавлять новых создателей, администраторов, сотрудников, рабочих")
        elif statuses[2]:
            answer.append(f"Вы - администратор")
            answer.append(f"Вы можете удалять и добавлять новых сотрудников и рабочих")

        elif statuses[2]:
            answer.append(f"Вы - сотрудник")
            answer.append(f"Вы можете потверждать добавление и перемещение интрументов")
            answer.append(f"Вам для пеермещение не требуется второй сотрудник")

        elif statuses[0]:
            answer.append(f"Вы - работник")
            answer.append(f"Вы можете перемещать и добавлять инструменты только с потверждением старшего сотрудника")

        answer.append(f"Напишить /help чтобы получить список команд доступных вам")
        await message.reply("\n".join(answer))
    except (NotFoundUser, TypeError) as e:
        await message.reply(f"Вас нет в базе, обратись к персанулу и назовите им ваш id\n"
                            f"Ваш id - {message.from_user.id} ")


@dp.message_handler(commands=['add_creator'])
async def send_add_creator(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if creator:
        try:
            add_creator(int(s[1]), s[2])
            await message.reply(f"Creator with id - {s[1]} - added")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить создателя используете /add_creator [id_user] [name_user]")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['add_admin'])
async def send_add_admin(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if creator:
        try:
            add_admin(int(s[1]), s[2])
            await message.reply(f"Admin with id - {s[1]} - added")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить администратора используете /add_admin [id_user] [name_user]")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['add_staff'])
async def send_add_staff(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        try:
            add_staff(int(s[1]), s[2])
            await message.reply(f"Staff with id - {s[1]} - added")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить персонал используете /add_staff [id_user] [name_user]")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['add_worker'])
async def send_add_worker(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:
            add_worker(int(s[1]), s[2])
            await message.reply(f"Worker with id - {s[1]} - added")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить работника используете /add_worker [id_user] [name_user]")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['delete_admin'])
async def send_delete_admin(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if creator:
        try:
            delete_admin(int(s[1]))
            await message.reply(f"Admin with id - {s[1]} - deleted")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы удалить администратора используете /delete_admin [id_user] ")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['delete_staff'])
async def send_delete_staff(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        try:
            delete_staff(int(s[1]))
            await message.reply(f"Staff with id - {s[1]} - deleted")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы удалить персонал используете /delete_staff [id_user] ")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['delete_worker'])
async def send_delete_worker(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        try:
            delete_worker(int(s[1]))
            await message.reply(f"Worker with id - {s[1]} - deleted")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы удалить рабочего используете /delete_worker [id_user] ")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['delete_user'])
async def send_delete_user(message: types.Message):
    s = re.split(r' ', message.text, maxsplit=2)
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if creator:
        try:
            delete_user(int(s[1]))
            await message.reply(f"User with id - {s[1]} - delete")
        except (IndexError, psycopg2.errors.SyntaxError):
            await message.reply(f"Не верная форма записи!\n"
                                f"Чтобы добавить локацию используете /delete_user [id_user]")
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_users'])
async def send_get_users(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if creator:
        answer = get_all_users()
        if not answer:
            await message.reply("Не найдено не одного пользователя")
        else:

            answer.insert(0, "ID   Name")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_workers'])
async def send_get_workers(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if staff or admin or creator:
        answer = get_all_worker()
        if not answer:
            await message.reply("Не найдено не одного пользователя")
        else:

            answer.insert(0, "ID   Name")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_staff'])
async def send_get_staff(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        answer = get_all_staff()
        if not answer:
            await message.reply("Не найдено не одного пользователя")
        else:

            answer.insert(0, "ID   Name")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_admins'])
async def send_get_admins(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        answer = get_all_admin()
        if not answer:
            await message.reply("Не найдено не одного пользователя")
        else:

            answer.insert(0, "ID   Name")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


@dp.message_handler(commands=['get_creators'])
async def send_get_creators(message: types.Message):
    worker, staff, admin, creator = get_user_status(message.from_user.id)
    if admin or creator:
        answer = get_all_creators()
        if not answer:
            await message.reply("Не найдено не одного пользователя")
        else:

            answer.insert(0, "ID   Name")
            await message.reply("\n".join(answer))
    else:
        await message.reply("У вас нет прав на использование этой команды")


if __name__ == '__main__':
    print("Main!")
    init_database()
    add_creator(CREATOR_ID, "Creator")
    executor.start_polling(dp, skip_updates=True)
