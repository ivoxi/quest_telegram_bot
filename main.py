from game_functions import check_file_in_directory
from user import User, load_user
from endings import load_endings
from stages_map import create_stages, find_stage_by_number
import telebot

TOKEN = 'Token_here'
users_started = {}
quest_chosen = {}
users_named = {}
users_in_game = {}

# Create the bot
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    if not check_file_in_directory('users', f'{user_id}.json') and user_id not in users_started:
        bot.send_message(user_id, "Выберите квест из предложенного списка\n*1. The Inside. Акт-1*",
                         parse_mode="Markdown")
        users_started[user_id] = True
        print(f'User {user_id} started the bot')
    elif check_file_in_directory('users', f'{user_id}.json') and user_id not in users_started:
        last_save(message)
    else:
        bot.send_message(user_id, "Эта команда уже недоступна")


@bot.message_handler(commands=['inventory'])
def character_sheet_message(message):
    user_id = message.from_user.id
    if user_id in users_in_game:
        user = users_in_game[user_id]
        bot.send_message(user_id, user, parse_mode="Markdown")
    else:
        bot.send_message(user_id, "Вы не начали прохождение квеста", parse_mode="Markdown")


@bot.message_handler(commands=['start_game'])
def start_game_message(message):
    user_id = message.from_user.id
    if user_id in users_named and user_id not in users_in_game:
        print(f'User {user_id} started the game')
        users_in_game[user_id] = User(user_id, users_named[user_id])
        user = users_in_game[user_id]
        user.save_user()
        bot.send_message(user_id, "Для того, чтобы посмотреть текущее состояние инвентаря напишите команду /inventory")
        stages = create_stages(user)
        current_stage = find_stage_by_number(stages, user.current_stage)
        current_choices = current_stage.get_choices(user)
        buts_len = len(current_choices)
        out_text = current_stage.get_description() + '\n' + '\n'.join(
            f'{i + 1} - {current_choices[i]['text']}' for i in range(len(current_choices)))
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[f'{i + 1}' for i in range(buts_len)])
        if current_stage.image is not None:
            with open(current_stage.image, "rb") as photo:
                bot.send_photo(user_id, photo, caption=out_text, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(user_id, out_text, parse_mode="Markdown", reply_markup=markup)
    elif user_id not in users_started:
        bot.send_message(user_id, "Напишите команду /start, чтобы начать новую игру")
    elif user_id not in quest_chosen:
        bot.send_message(user_id, "Выберите квест")
    elif user_id not in users_named:
        bot.send_message(user_id, "Укажите имя")
    elif user_id in users_in_game:
        bot.send_message(user_id, "Вы уже начали прохождение квеста")


@bot.message_handler(commands=['last_save'])
def last_save(message):
    user_id = message.from_user.id
    try:
        user = load_user(user_id)
        users_started[user_id] = True
        users_named[user_id] = user.name
        users_in_game[user_id] = user
        quest_chosen[user_id] = 'The Inside. Акт-1'
        bot.send_message(user_id, "Загружаемся с последнего сохранения...")
        stages = create_stages(user)
        current_stage = find_stage_by_number(stages, user.current_stage)
        current_choices = current_stage.get_choices(user)
        buts_len = len(current_choices)
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[f'{i + 1}' for i in range(buts_len)])
        out_text = current_stage.get_description() + '\n' + '\n'.join(
            f'{i + 1} - {current_choices[i]['text']}' for i in range(len(current_choices)))
        if current_stage.image is not None:
            photo = open(current_stage.image, 'rb')
            bot.send_photo(user_id, photo, caption=out_text, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(user_id, out_text, parse_mode="Markdown", reply_markup=markup)

    except FileNotFoundError:
        bot.send_message(user_id, "Последнее сохранение отсутствует")


@bot.message_handler(commands=['my_endings'])
def endings(message):
    user_id = message.from_user.id
    try:
        cur_endings = load_endings(user_id)
        bot.send_message(user_id, cur_endings, parse_mode="Markdown")
    except FileNotFoundError:
        bot.send_message(user_id, "Эта команда пока Вам недоступна")


@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_id = message.from_user.id
    if not check_file_in_directory('users', f'{user_id}.json') and user_id not in users_started:
        bot.send_message(user_id, "Напишите команду /start")
    elif check_file_in_directory('users', f'{user_id}.json') and user_id not in users_started:
        last_save(message)
    elif user_id not in quest_chosen and user_id not in users_in_game and user_id in users_started:
        if message.text == '1':
            quest_chosen[user_id] = 'The Inside. Акт-1'
            bot.send_message(user_id, 'Вы выбрали The Inside. Акт-1. Введите ваше имя:')
        else:
            bot.send_message(user_id, "Такого квеста нет")
    elif user_id not in users_in_game and user_id in quest_chosen and user_id not in users_named:
        users_named[user_id] = message.text
        bot.send_message(user_id, f'Ваше имя: {message.text}\nДоступные команды:\n'
                                  f'/start_game - Начать игру\n/my_endings - Ваши концовки\n')
    elif user_id in users_in_game:
        user = users_in_game[user_id]
        stages = create_stages(user)
        current_stage = find_stage_by_number(stages, user.current_stage)
        current_choices = current_stage.get_choices(user)
        try:
            choice_key = int(message.text)
        except Exception:
            bot.send_message(user_id, "Нет такого выбора!")
            return
        if 0 < choice_key <= len(current_choices):
            current_stage.apply_choice(user, choice_key)
            user.save_counter += 1
            if user.save_counter % 5 == 0:
                user.save_user()
        else:
            bot.send_message(user_id, f'Неправильный выбор. Выберите цифру в диапазоне (1 - {len(current_choices)})')
        stages = create_stages(user)
        current_stage = find_stage_by_number(stages, user.current_stage)
        if current_stage.is_ending:
            bot.send_message(user_id, current_stage.get_description(), parse_mode="Markdown")
            cur_endings = load_endings(user_id)
            cur_endings.update_endings(current_stage.ending_name)
            cur_endings.save_endings()
            del users_in_game[user_id]
            del quest_chosen[user_id]
            del users_started[user_id]
            del users_named[user_id]
            user.delete_user()
            print(f'User {user_id} finished the game')
            delete_markup = telebot.types.ReplyKeyboardRemove()
            bot.send_message(user_id,
                             "\nСписок команд:\n/start - Начать новую игру\n/my_endings - Список ваших концовок",
                             reply_markup=delete_markup)

        else:
            current_choices = current_stage.get_choices(user)
            buts_len = len(current_choices)
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(*[f'{i + 1}' for i in range(buts_len)])
            out_text = current_stage.get_description() + '\n' + '\n'.join(
                f'{i + 1} - {current_choices[i]['text']}' for i in range(len(current_choices)))
            if current_stage.image is not None:
                photo = open(current_stage.image, 'rb')
                bot.send_photo(user_id, photo, caption=out_text, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.send_message(user_id, out_text, parse_mode="Markdown", reply_markup=markup)
    elif user_id in users_named:
        bot.send_message(user_id, f'Доступные команды:\n'
                                  f'/start_game - Начать игру\n/inventory - Инвентарь персонажа')
    else:
        bot.send_message(user_id, "Напишите команду /start чтобы начать")


if __name__ == '__main__':
    bot.polling(none_stop=True)
