import asyncio
from aiogram import Bot, F, Dispatcher
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
import asyncpg
import pytz
from datetime import datetime


async def cr():
    conn = await asyncpg.connect(user='postgres', password='8967824ib', host='localhost', database='deposit') 
    return conn 

async def cr_deposit():
    conn = await cr()
    await conn.execute('''create table menu (
    id BIGSERIAL PRIMARY KEY,
    user_id bigint unique,
	username text,
	data_start text,
	income_sum bigint,
	second_sum bigint,
	balance float,
	deposits float,
	income_trade float,
	trade_plan bigint,
	trade_ref_program float,
	conclusion float,
	referrals bigint,
	count_deposits bigint,
	sum_deposits float,
    your_income float,
	referrer bigint
)
''') 
    await conn.close() 

async def cr_menu_c():
    conn = await cr()
    await conn.execute('''create table menu_c (
    id BIGSERIAL PRIMARY KEY,
    user_id bigint unique,
	second_c bigint,
	application boolean
)
''') 
    await conn.close() 

async def cr_bot():
    conn = await cr()
    await conn.execute('''create table bot (
    id BIGSERIAL PRIMARY KEY,
    users_h bigint unique,
	second_h bigint,
	bot_h bigint
)
''') 
    await conn.close() 

bot = Bot(token='7409696935:AAF-9MKFI0hRjxwVdZASQdaPOAP8iLq6VcA')

dp = Dispatcher(storage=MemoryStorage())

async def data_start():
    moscow = pytz.timezone('Europe/Moscow')
    time = datetime.now(moscow)
    t = time.strftime('%Y-%m-%d')
    return t

async def user_f(message: Message):
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM menu WHERE user_id=$1''', message.from_user.id)
    return user

async def NACH():
    while True:
        await asyncio.sleep(1)
        conn = await cr()
        result = await conn.fetch("SELECT * FROM menu")
        for i in result:
            if i[5] <= 86400:
                await conn.execute(f'''UPDATE menu SET second_sum = second_sum + 1 WHERE user_id=$1''', i[1])
            else:
                await conn.execute(f'''UPDATE menu SET second_sum = 0 WHERE user_id=$1''', i[1])
                await conn.execute(f'''UPDATE menu SET balance = balance + {i[8]} WHERE user_id=$1''', i[1])
                if i[-1]:
                    a = i[8]*20/100
                    await conn.execute(f'''UPDATE menu SET balance = balance + {a} WHERE user_id=$1''', i[-1])
                    await conn.execute(f'''UPDATE menu SET your_income = your_income + {a} WHERE user_id=$1''', i[-1])
        result_c = await conn.fetch("SELECT * FROM menu_c")
        for j in result_c:
            await conn.execute(f'''UPDATE menu_c SET second_c = second_c + 1 WHERE user_id=$1''', j[1])
            if j[2] >= 86400:
                if j[3]:
                    await conn.execute(f'''UPDATE menu_c SET application = False WHERE user_id=$1''', j[1])
        result_h = await conn.fetchrow("SELECT * FROM bot")
        if result_h[2] >= 86400:
            await conn.execute(f'''UPDATE bot SET second_h = 0''')
            await conn.execute(f'''UPDATE bot SET users_h = 0''')
        else:
            await conn.execute(f'''UPDATE bot SET second_h = second_h + 1''')


@dp.message(Command('start'))
async def start(message: Message):
    global referrer_id_user_id
    referrer_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    referrer_id_user_id = {message.from_user.id: referrer_id}
    await start1(message)

async def start1(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status != 'member':
        a_button = InlineKeyboardButton(text=f'Проверить', callback_data='member_verify')
        button = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
        await bot.send_message(call.from_user.id, text="👉 Для продолжения работы с ботом Smart 🔑 System необходимо\n<a href='https://t.me/SmartSystem_channel'>🔔 подписаться на наш канал 🔔</a>", reply_markup=button, parse_mode='HTML')
    else:
        await start2(call)

@dp.callback_query(F.data == 'member_verify')
async def member_verify(call: CallbackQuery):
    await start1(call)

async def start2(message: Message):
    try:
        referrer_id = referrer_id_user_id[message.from_user.id]
    except:
        pass
    try:
        print(referrer_id)
    except:
        referrer_id = None
    conn = await cr()
    user = await user_f(message)
    if user:
        await menu(message)
    else:
        await message.answer('Добро пожаловать в наш бот!')
        if referrer_id and int(referrer_id) != int(message.from_user.id):
            a_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
            button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
            await bot.send_message(int(referrer_id), text=f"Вы пригласили нового<a href='tg://user?id={message.from_user.id}'> реферала! </a>", parse_mode='HTML', reply_markup=button)
            await conn.execute('''UPDATE menu SET referrals = referrals + 1 WHERE user_id=$1''', int(referrer_id)) 
            await conn.execute('''INSERT INTO menu (user_id, username, data_start, income_sum, second_sum, balance, deposits, income_trade, trade_plan, trade_ref_program, conclusion, referrals, count_deposits, sum_deposits, your_income, referrer) VALUES 
                               ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)''', 
                               message.from_user.id, message.from_user.username, await data_start(), 0, 0, 0.0, 0.0, 0.0, None, 0.0, 0.0, 0, 0, 0.0, 0.0, int(referrer_id)) 
        else:
            await conn.execute('''INSERT INTO menu (user_id, username, data_start, income_sum, second_sum, balance, deposits, income_trade, trade_plan, trade_ref_program, conclusion, referrals, count_deposits, sum_deposits, your_income, referrer) VALUES 
                               ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)''', 
                               message.from_user.id, message.from_user.username, await data_start(), 0, 0, 0.0, 0.0, 0.0, None, 0.0, 0.0, 0, 0, 0.0, 0.0, 0.0) 
        await menu(message)
        await conn.execute('''INSERT INTO menu_c (user_id, second_c, application) VALUES 
                               ($1, $2, $3)''', 
                               message.from_user.id, 0, False)
        await conn.execute(f'''UPDATE bot SET users_h = users_h + 1''')
        
    try:
        del referrer_id_user_id[message.from_user.id]
    except:
        pass

@dp.callback_query(F.data == 'Перейти в начало')
async def Перейти_в_начало(call: CallbackQuery, state: FSMContext):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        await state.clear()
        await menu(call)
        try:
            del mailing2[call.from_user.id]
        except:
            pass
    else:
        await start1(call)

async def menu(message: Message):
    a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
    b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
    c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
    d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
    e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
    f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button], [e_button], [f_button]])
    await bot.send_message(message.from_user.id, text='<b>Приветствую Вас в Smart 🔑 System!</b>\n\n'
'Наш бот основан на алгоритмах и искусственном интеллекте, что позволяет ему анализировать множество данных, принимать решения и осуществлять сделки самостоятельно.\n\n'
'Он работает намного быстрее и точнее, чем человек, способен анализировать большие объемы данных и реагировать на изменения рынка мгновенно. Кроме того, может работать круглосуточно, что позволяет получать доход в любое время суток.', parse_mode='HTML', reply_markup=button)

@dp.callback_query(F.data == 'Начать торговлю')
async def Начать_торговлю(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        user = await user_f(call)
        a_button = InlineKeyboardButton(text='50$: 3% в день', callback_data='50$: 3% в день')
        b_button = InlineKeyboardButton(text='100$: 4% в день', callback_data='100$: 4% в день')
        c_button = InlineKeyboardButton(text='500$: 5% в день', callback_data='500$: 5% в день')
        d_button = InlineKeyboardButton(text='1 000$: 6% в день', callback_data='1 000$: 6% в день')
        e_button = InlineKeyboardButton(text='🌀 3 000$: 7% в день 🌀', callback_data='3 000$: 7% в день')
        f_button = InlineKeyboardButton(text='5 000$: 7% в день', callback_data='5 000$: 7% в день')
        g_button = InlineKeyboardButton(text='10 000$: 8% в день', callback_data='10 000$: 8% в день')
        h_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button], [e_button], [f_button, g_button], [h_button]])
        await call.message.edit_text('Smart 🔑 System работает полностью автоматически и не требует Вашего прямого участия.\n\n'
'Вы можете выбрать удобный для вас план, который будет формировать выделенный торговый пул для работы Smart 🔑 System.\n\n'
f'Текущий план: {user[9] if user[9] is not None else "<b>Не определен (Сумма депозитов недостаточна для активации минимального тарифного плана)</b>"}\n\n'
'Стоит отметить, что чем выше сумма инвестиции, тем быстрее и больше инвестор будет получать доход.\n'
'Такая корреляция объясняется тем, что торговля идет на достаточно волатильных криптовалютных активах и более крупные суммы обеспечивают страховки от проскальзываний и преждевременных исполнения ордеров.'
'Обеспечивая тем самым надежность работы конкретного торгового пула, инвесторы с более крупными инвестициями получают скорейшую отдачу вложенных средств.\n\n'
'Взвесьте все ЗА и ПРОТИВ и выберите для себя оптимальный вариант.', reply_markup=button, parse_mode='HTML')
    else:
        await start1(call)

@dp.callback_query(F.data == 'Мой доход')
async def Начать_торговлю(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        user = await user_f(call)
        g_button = InlineKeyboardButton(text='💸 Вывод средств', callback_data='Вывод средств')
        a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
        b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
        c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
        d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
        e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
        f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[g_button], [a_button, b_button], [c_button, d_button], [e_button], [f_button]])
        await call.message.edit_text(f'Дата регистрации: <b>{user[3]}</b>\n'
f'Баланс: <b>{user[6]}$</b>\n\n'
f'Депозиты: <b>{user[7]}$</b>\n'
f'Доход от торговли: <b>{user[8]}$</b>\n'
f'Торговый план: <b>{user[9] if user[9] is not None else "Не определен"}</b>\n'
f'Доход от реф. программы: <b>{user[-2]}$</b>\n'
f'Выводы средств: <b>{user[11]}$</b>\n\nВывод средств доступен при достижении на балансе суммы, минимум в 1.5 раза больше разницы сумм всех депозитов и сумм всех выводов, но не менее 50$ и не менее 1.5 суммы всех депозитов, сделанных после последнего вывода.\n'
'Чем больше инвестиция, тем быстрее достигается минимальная для вывода сумма. Это обусловлено необходимостью обеспечивать ликвидность средств в торговом пуле.', reply_markup=button, parse_mode='HTML')
    else:
        await start1(call)

@dp.callback_query(F.data == 'Подробнее о боте')
async def Подробнее_о_боте(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
        b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
        c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
        d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
        e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
        f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button], [e_button], [f_button]])
        conn = await cr()
        result_h = await conn.fetchrow("SELECT * FROM bot")
        result = await conn.fetch("SELECT * FROM menu")
        count = 0
        for i in result:
            count += 1
        await call.message.edit_text(f'<b>Smart 🔑 System</b> работает на основе алгоритмов и стратегий торговли, заданных в программное обеспечение бота. <b>Он использует данные с биржи</b>, анализирует их и принимает решения о покупке или продаже криптовалюты в соответствии с заданными параметрами, поставленными профессионалами.\n\n'
'<b>В работе торгового бота используется API</b> (Application Programming Interface) – программный интерфейс для взаимодействия с биржей. <b>С помощью API бот получает доступ к данным</b> о ценах на криптовалюту и может осуществлять сделки на бирже.\n\n'
'<b>Бот работает в режиме автоматической торговли</b>, когда все операции осуществляются без участия пользователя.\n\n'
'<b>Smart 🔑 System</b> может использовать различные стратегии торговли, например, основные <b>индикаторы технического анализа, анализ свечей, отслеживание изменений объемов торгов</b> и др.\n\n'
'Кроме того, бот может <b>учитывать изменения цен на различных биржах и автоматически переносить средства между биржами</b> для получения наиболее выгодной цены.', reply_markup=button, parse_mode='HTML')
        if call.from_user.id == 7032079647:
            a_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
            button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
            await call.answer(f'Бот работает дней: {result_h[3]}\nВсего пользователей: {count}\nВсего пользователей за 24 часа: {result_h[1]}', reply_markup=button, show_alert=True)
    else:
        await start1(call)


def invite(event: Message, obot) -> str:
    user_id: int = event.from_user.id
    botname = obot.username
    text = f"Зарабатывай деньги, не прилагая усилий! Надежный и стабильный пассивный доход уже ждет тебя. Не упусти свой шанс!\n\nhttps://t.me/{botname}?start={user_id}"
    return text



@dp.callback_query(F.data == 'Реферальная программа')
async def Реферальная_программа(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        obot = await bot.get_me()
        botname = obot.username
        user = await user_f(call)
        ref_button = InlineKeyboardButton(text='Отправить ссылку', switch_inline_query=invite(call.message, obot))
        a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
        b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
        c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
        d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
        e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
        f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[ref_button], [a_button, b_button], [c_button, d_button], [e_button], [f_button]])
        obot = await bot.get_me()
        botname = obot.username
        await call.message.edit_text(f'Ваша реферальная ссылка:\n<code>https://t.me/{botname}?start={call.from_user.id}</code>\n\n'
'Распространяйте свою реферальную ссылку, привлекайте инвесторов в проект и получайте за это дополнительный доход - <b>20% от каждой инвестиции Вашего партнёра.</b>\n\n'
'Статистика:\n'
f'Количество рефералов: <b>{user[-5]}</b>\n'
f'Количество депозитов: <b>{user[-4]}</b>\n'
f'Сумма депозитов: <b>{user[-3]}$</b>\n'
f'Ваш доход: <b>{user[-2]}$</b>', reply_markup=button, parse_mode='HTML')
    else:
        await start1(call)
    
@dp.callback_query(F.data.endswith('в день'))
async def replenish(call: CallbackQuery):
    global replenish_sum_user
    import re
    number = re.search(r'\d+', str(call.data)).group()
    if 1 <= int(number) <= 10:
        number = int(number) * 1000
    replenish_sum_user = {call.from_user.id: [number, call.data]}
    a_button = InlineKeyboardButton(text='Tether USDT TRC20', callback_data='Tether USDT TRC20')
    b_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
    await call.message.edit_text(f'Вы выбрали "<b>{call.data}</b>"\n\nДля оплаты мы используем один удобный и единый способ оплаты.', reply_markup=button, parse_mode='HTML')

@dp.callback_query(F.data == 'Tether USDT TRC20')
async def Only1(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        a_button = InlineKeyboardButton(text='Я оплатил(а)', callback_data='Я оплатил(а)')
        b_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
        conn = await cr()
        result = await conn.fetchrow("SELECT * FROM bot")
        await call.message.edit_text(f'Вы выбрали план "<b>{replenish_sum_user.get(call.from_user.id, 0)[1]}</b>" и способ оплаты "<b>Tether USDT TRC20</b>".\n\n'
f'Для активации плана в течение 30 минут оплатите заказ <b>D/DGZFCV</b>, переведя РОВНО {replenish_sum_user.get(call.from_user.id, 0)[0]} USDT TRC20 (Tether в сети Tron) на указанный ниже адрес, после чего нажмите кнопку "Я оплатил(а)"\n\n'
'Будьте внимательны!!! 👇'
f'Если по какой-то причине, переведенная сумма окажется меньше указанной, применятся условия меньшего тарифного плана. <b>Суммы менее {replenish_sum_user.get(call.from_user.id, 0)[0]} USDT системой не засчитываются.</b>\n\n'
f'Адрес для перевода:\n<code>{result[4]}</code>', reply_markup=button, parse_mode='HTML')
    else:
        await start1(call)
    

@dp.callback_query(F.data == 'Я оплатил(а)') 
async def Я_оплатил(call: CallbackQuery) -> None:
    sum = replenish_sum_user.get(call.from_user.id, 0)
    a_button = InlineKeyboardButton(text='Принять от пополнения', callback_data=f'{call.from_user.id}_p1')
    b_button = InlineKeyboardButton(text='Отказаться от пополнения', callback_data=f'{call.from_user.id}_o1')
    button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
    await bot.send_message(7032079647, text=f"<a href='tg://user?id={call.from_user.id}'>Пользователь</a> пополнил вам и ожидает {sum[1]}", parse_mode='HTML', reply_markup=button)
    
    a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
    b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
    c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
    d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
    e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
    f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button], [e_button], [f_button]])
    await bot.send_message(call.from_user.id, text='В настоящий момент мы проверяем оплату. '
'При поступлении оплаты средства зачислятся Вам на счет и активируется торговый план согласно выбранного тарифа. Об этом Вы получите соответствующее уведомление.\n\n'
'Для отслеживания платежей и статуса активации торгового плана перейдите в раздел <b>"Мой доход"</b>', reply_markup=button, parse_mode='HTML')

@dp.callback_query(F.data.endswith("_p1") | F.data.endswith("_o1"))
async def po(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[0])
    if callback.data[-3:] == '_p1':
        await callback.message.edit_text('Принято')
        await bot.send_message(user_id, text=f'Ваша заявка на пополнение принята!', reply_markup=None)
        conn = await cr()
        await conn.execute(f'''UPDATE menu_c SET second_c = 0 WHERE user_id=$1''', int(user_id))
        await conn.execute(f'''UPDATE menu SET deposits = deposits + {replenish_sum_user.get(user_id, 0)[0]} WHERE user_id=$1''', int(user_id))
        await conn.execute(
    '''
    UPDATE menu
    SET trade_plan = $1
    WHERE user_id = $2
    ''',
    replenish_sum_user.get(user_id, 0)[1],
    int(user_id)
)
        user = await conn.fetchrow('''SELECT * FROM menu WHERE user_id=$1''', int(user_id))
        sum_p = None
        n = int(replenish_sum_user.get(user_id, 0)[0])
        if n == 50:
            sum_p = 3
        else:
            if n == 100:
                sum_p = 4
            else:
                if n == 500:
                    sum_p = 5
                else:
                    if n == 1000:
                        sum_p = 6
                    else:
                        if n == 3000 or replenish_sum_user.get(user_id, 0)[0] == 5000:
                            sum_p = 7
                        else:
                            if n == 10000:
                                sum_p = 8
                            else:
                                print(100*'no\n')
                                print(sum_p)
        num = replenish_sum_user.get(user_id, 0)[0]
        a = float(num) * float(sum_p) / 100
        if user[-1]:
            await conn.execute(f'''UPDATE menu SET sum_deposits = sum_deposits + {replenish_sum_user.get(user_id, 0)[0]} WHERE user_id=$1''', user[-1])
            await conn.execute(f'''UPDATE menu SET count_deposits = count_deposits + 1 WHERE user_id=$1''', user[-1])
            try:
                await conn.execute(f'''UPDATE menu SET your_income = your_income + {a} WHERE user_id=$1''', user[-1])
            except:
                await conn.execute(f'''UPDATE menu SET your_income = {a} WHERE user_id=$1''', user[-1])
        await conn.execute(f'''UPDATE menu SET income_trade = {a} WHERE user_id=$1''', int(user_id))
    elif callback.data[-3:] == '_o1':
        await callback.message.edit_text('Отказано', reply_markup=None)
        await bot.send_message(user_id, text='Ваша заявка на пополнение отказана!')
    del replenish_sum_user[user_id]

@dp.callback_query(F.data == 'Вывод средств')
async def Вывод_средств(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        await Вывод_средств00(call)
    else:
        await start1(call)

async def Вывод_средств00(call: CallbackQuery):
    a_button0 = InlineKeyboardButton(text='Вывести', callback_data='Вывести')
    a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
    b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
    c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
    d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
    e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
    f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button], [e_button], [f_button]])
    button1   = InlineKeyboardMarkup(inline_keyboard=[[a_button0], [f_button]])
    conn = await cr()
    user1 = await conn.fetchrow('''SELECT * FROM menu_c WHERE user_id=$1''', call.from_user.id)
    user = await user_f(call)
    if user[6] == 0:
        await call.message.edit_text(
f'Доступно к выводу: <b>{user[6]}$</b>\n\n'
'----------------------------------------------------------------\n'
'<u>Запросы на вывод:</u>\n\n'
f'{"Заявок на вывод еще не было." if not user1[3] else "Заявка на вывод была создана, ожидайте!"}\n\nНету кнопка "вывести", потому что у вас на балансе <b>{user[6]}$</b>.', parse_mode='HTML', reply_markup=button)
    else:
        if not user1[3]:
            if user1[2] >= 7776000:
                b = (user[7] + user[11]) * 1.5
                if b <= user[6]:
                    await call.message.answer(
f'Доступно к выводу: <b>{user[6]}$</b>\n\n'
'----------------------------------------------------------------\n'
'Нажмите на "Вывести" чтобы вывести.', parse_mode='HTML', reply_markup=button1)
                else:
                    await call.message.answer(f'Минимальная сумма вывода <b>{b}$</b>!\nНа вашем балансе <b>{user[6]}$</b>', reply_markup=button, parse_mode='HTML')
            else:
                a = user[7] * 30 / 100
                await call.message.answer(f'Не прошло 3 месяца прибылей!\nЕсли вы хотите вывести раньше чем 3 месяца, то вам необходимо пополнить еще <b>{a}$</b>!', reply_markup=button, parse_mode='HTML')
        else:
            await call.message.answer('У вас уже была создана заявка! Ожидайте ответа.', reply_markup=button)
                
@dp.callback_query(F.data == 'Вывести')
async def Вывести(call: CallbackQuery):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        a_button = InlineKeyboardButton(text='Tether USDT TRC20', callback_data='Tether USDT TRC20v')
        b_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
        await call.message.edit_text('Для вывода мы используем один удобный и единый способ вывода.', reply_markup=button)
    else:
        await start1(call)

class con(StatesGroup):
    score = State()

@dp.callback_query(F.data == 'Tether USDT TRC20v')
async def conclusion1(call: CallbackQuery, state: FSMContext):
    user_chat_member = await bot.get_chat_member(-1001613934290, call.from_user.id)
    if user_chat_member.status == 'member':
        a_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
        await call.message.edit_text('Введите ваш адрес кошелька:', reply_markup=button)
        await state.set_state(con.score)
    else:
        await start1(call)

@dp.message(StateFilter(con.score))
async def conclusion2(message: Message, state: FSMContext):
    if message.text:
        global replenish_sum_user1
        user = await user_f(message)
        replenish_sum_user1 = {message.from_user.id: [message.text, user[6]]}
        conn = await cr()
        await conn.execute(f'''UPDATE menu_c SET application = True WHERE user_id=$1''', message.from_user.id)
        sum = replenish_sum_user1.get(message.from_user.id, 0)
        a_button = InlineKeyboardButton(text='Принять от пополнения', callback_data=f'{message.from_user.id}_p2')
        b_button = InlineKeyboardButton(text='Отказаться от пополнения', callback_data=f'{message.from_user.id}_o2')
        button = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
        await bot.send_message(7032079647, text=f"<a href='tg://user?id={message.from_user.id}'>Пользователь</a> создал заявку на вывод.\nАдрес кошелька:\n<code>{sum[0]}</code>\n\nСумма: <b>{sum[1]}</b>", parse_mode='HTML', reply_markup=button)
    
        a_button = InlineKeyboardButton(text='🎯 Начать торговлю', callback_data='Начать торговлю')
        b_button = InlineKeyboardButton(text='💰 Мой доход', callback_data='Мой доход')
        c_button = InlineKeyboardButton(text='ℹ Подробнее о боте', callback_data='Подробнее о боте')
        d_button = InlineKeyboardButton(text='❔ Задать вопрос', url='tg://user?id=7032079647')
        e_button = InlineKeyboardButton(text='🤝 Реферальная программа', callback_data='Реферальная программа')
        f_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button, b_button], [c_button, d_button], [e_button], [f_button]])
        await message.edit_text('<b>Заявка</b> успешно отправлена! Ожидайте.', reply_markup=button, parse_mode='HTML')
    else:
        await message.edit_text('Нужно вводить адрес кошелька!')
        await menu(message)
    await state.clear()

@dp.callback_query(F.data.endswith("_p2") | F.data.endswith("_o2"))
async def po(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[0])
    if callback.data[-3:] == '_p2':
        await callback.message.edit_text('Принято')
        await bot.send_message(user_id, text=f'Ваша заявка на вывод принята!', reply_markup=None)
        conn = await cr()
        await conn.execute(f'''UPDATE menu SET second_c = 0 WHERE user_id=$1''', int(user_id))
        await conn.execute(f'''UPDATE menu_c SET application = False WHERE user_id=$1''', int(user_id))
        await conn.execute(f'''UPDATE menu SET balance = 0 WHERE user_id=$1''', int(user_id))
        await conn.execute(f'''UPDATE menu SET conclusion = conclusion + {replenish_sum_user1.get(int(user_id), 0)[1]} WHERE user_id=$1''', int(user_id))
    elif callback.data[-3:] == '_o2':
        await callback.message.edit_text('Отказано', reply_markup=None)
        await bot.send_message(user_id, text='Ваша заявка на вывод отказана!')
    del replenish_sum_user1[user_id]

@dp.message(F.text == '/users')
async def users_bot(call: CallbackQuery):
    if call.from_user.id == 7032079647:
        await users_bot99(call)

async def users_bot99(call: CallbackQuery):
    arr = []
    j = 100
    conn = await cr()
    result = await conn.fetch("SELECT * FROM menu")
    for i, row in enumerate(result):
        arr.append([InlineKeyboardButton(text=f'ID: {row[1]}', callback_data=f'ref.users_{row[1]}')])
        if i == j - 1 or i == len(result) - 1:
            keyboard = InlineKeyboardMarkup(inline_keyboard=arr)
            await call.bot.send_message(call.from_user.id, text="Ваши users:", reply_markup=keyboard)
            arr = []
            j += 100
    if len(arr) > 0:
        keyboard = InlineKeyboardMarkup(inline_keyboard=arr)
        await call.bot.send_message(call.from_user.id, text="Ваши users:", reply_markup=keyboard)
    count = 0
    for i in result:
        count += 1
    await call.bot.send_message(call.from_user.id, text=f'Всего пользователей {count}')

    
@dp.callback_query(F.data.startswith('ref.users_'))
async def users(call: CallbackQuery):
    global ref_user
    user_id = int(call.data[10:])
    ref_user = {call.from_user.id: user_id}
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM menu WHERE user_id=$1''', user_id)
    a_button = InlineKeyboardButton(text='Профиль', url=f'tg://user?id={user[1]}')
    b_button = InlineKeyboardButton(text='Изменения баланса', callback_data='ref_change_balance')
    c_button = InlineKeyboardButton(text='Удалить', callback_data='ref_delete_user')
    d_button = InlineKeyboardButton(text='В меню', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button], [c_button], [d_button]])
    await call.bot.send_message(call.from_user.id, text=f'''Дата регистрации: {user[3]}\n
ID: {user[1]}\nUsername: @{user[2]}\n
Баланс: {user[6]}₽\nРеферер: <code>{user[-1] if user[-1] else "нету"}</code>\n
Рефералов: {user[-5]}''', reply_markup=button, parse_mode='HTML')


@dp.callback_query(F.data == 'ref_delete_user')
async def ref_delete_user(call: CallbackQuery):
    a_button = InlineKeyboardButton(text='Подтвердить', callback_data='ref_delete_user_p')
    b_button = InlineKeyboardButton(text='Отменить', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
    await call.message.edit_text('Удалить пользователя из вашего бота, в таком случае у пользователя всё обнулится. Хотите удалить?', reply_markup=button)
        
@dp.callback_query(F.data == 'ref_delete_user_p')
async def ref_delete_user_p(callback: CallbackQuery):
    conn = await cr()
    await conn.execute('DELETE FROM menu WHERE user_id=$1', ref_user[callback.from_user.id])
    await conn.execute('DELETE FROM menu_c WHERE user_id=$1', ref_user[callback.from_user.id])
    await callback.message.edit_text(f'Пользователь с ID {ref_user[callback.from_user.id]} успешно удален.')
    await bot.send_message(ref_user[callback.from_user.id], 'Вы были удалены из базы данных!\nПерезапустите бота для начала работы /start')
    await menu(callback)


@dp.callback_query(F.data == 'ref_change_balance')
async def ref_change_balance(call: CallbackQuery):
    conn = await cr()
    user = await conn.fetchrow('''SELECT * FROM menu WHERE user_id=$1''', ref_user[call.from_user.id])
    a_button = InlineKeyboardButton(text='Прибавить', callback_data='ref_p_sum')
    b_button = InlineKeyboardButton(text='Вычислить', callback_data='ref_v_sum')
    c_button = InlineKeyboardButton(text='Изменить сумму', callback_data='ref_change_sum')
    d_button = InlineKeyboardButton(text='В меню', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button],[b_button], [c_button], [d_button]])
    await call.message.answer(f'Баланс пользователя: {user[3]}₽\nВыберите:', reply_markup=button)

class ref_sum(StatesGroup):
    p = State()
    v = State()
    change = State()

@dp.callback_query(F.data == 'ref_p_sum')
async def ref_p_sum(call: CallbackQuery, state: FSMContext):
    try:
        if ref_user[call.from_user.id]:
            a_button = KeyboardButton(text='Отменить')
            button   = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True)
            await call.message.answer('Введите сумму:')
            await state.set_state(ref_sum.p)
        else:
            pass
    except:
        pass

@dp.message(StateFilter(ref_sum.p))
async def ref_p_sum1(message: Message, state: FSMContext):
    if message.text.isdigit():
        conn = await cr()
        await conn.execute(f'''UPDATE menu SET balance = balance + {int(message.text)} WHERE user_id=$1''', ref_user[message.from_user.id])
        await state.clear()
        await message.answer('Сумма успешна прибавлена пользователю.', reply_markup=None)
        await menu(message)
    else:
        if message.text == 'Отменить':
            await message.answer('Отменено', reply_markup=None)
            await state.clear()
        else:
            await message.answer('Введите целое число!')

@dp.callback_query(F.data == 'ref_v_sum')
async def ref_v_sum(call: CallbackQuery, state: FSMContext):
    try:
        if ref_user[call.from_user.id]:
            a_button = KeyboardButton(text='Отменить')
            button   = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True)
            await call.message.answer('Введите сумму:')
            await state.set_state(ref_sum.v)
        else:
            pass
    except:
        pass

@dp.message(StateFilter(ref_sum.v))
async def ref_v_sum1(message: Message, state: FSMContext):
    if message.text.isdigit():
        conn = await cr()
        await conn.execute(f'''UPDATE menu SET balance = balance - {int(message.text)} WHERE user_id=$1''', ref_user[message.from_user.id])
        await state.clear()
        await message.answer('Сумма успешна вычислена пользователю.', reply_markup=None)
        await menu(message)
    else:
        if message.text == 'Отменить':
            await message.answer('Отменено', reply_markup=None)
            await state.clear()
        else:
            await message.answer('Введите целое число!')

@dp.callback_query(F.data == 'ref_change_sum')
async def ref_change_sum(call: CallbackQuery, state: FSMContext):
    try:
        if ref_user[call.from_user.id]:
            a_button = KeyboardButton(text='Отменить')
            button   = ReplyKeyboardMarkup(keyboard=[[a_button]], resize_keyboard=True)
            await call.message.answer('Введите сумму:')
            await state.set_state(ref_sum.change)
        else:
            pass
    except:
        pass


@dp.message(StateFilter(ref_sum.change))
async def ref_change_sum1(message: Message, state: FSMContext):
    if message.text.isdigit():
        conn = await cr()
        await conn.execute(f'''UPDATE menu SET balance = {int(message.text)} WHERE user_id=$1''', ref_user[message.from_user.id])
        await state.clear()
        await message.answer('Сумма успешна изменена пользователю.', reply_markup=None)
        await menu(message)
    else:
        if message.text == 'Отменить':
            await message.answer('Отменено', reply_markup=None)
            await state.clear()
        else:
            await message.answer('Введите целое число!')

class maili(StatesGroup):
    text = State()

@dp.message(F.text == '/mailing')
async def mailing(msg: Message, state: FSMContext):
    if msg.from_user.id == 7032079647:
        await msg.answer('Введите текст:')
        await state.set_state(maili.text)


@dp.message(StateFilter(maili.text))
async def mailing1(msg: Message, state: FSMContext):
    global mailing2
    mailing2 = {msg.from_user.id: msg.text}
    await msg.answer('Текст:')
    await msg.answer(msg.text)
    a_button = InlineKeyboardButton(text='Отправить', callback_data='Отправить текст')
    b_button = InlineKeyboardButton(text='Отменить', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
    await msg.answer('Хотите отправить этот текст всем пользователям?', reply_markup=button)
    await state.clear()

@dp.callback_query(F.data == 'Отправить текст')
async def Отправить_текст(call: CallbackQuery):
    conn = await cr()
    result = await conn.fetch("SELECT * FROM menu")
    for i in result:
        await bot.send_message(i[1], text=mailing2.get(call.from_user.id, 0))
    await call.message.answer('Текст успешно отправлен всем пользователям.')
    del mailing2[call.from_user.id]
    await menu(call)

@dp.message(F.text == '/score')
async def score_t(msg: Message):
    if msg.from_user.id == 7032079647:
        conn = await cr()
        result = await conn.fetchrow("SELECT * FROM bot")
        a_button = InlineKeyboardButton(text='Изменить', callback_data='change_score')
        b_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
        button   = InlineKeyboardMarkup(inline_keyboard=[[a_button], [b_button]])
        await msg.answer(f'Адрес кошелька <code>{result[4]}</code>', reply_markup=button, parse_mode='HTML')

class c_s(StatesGroup):
    score = State()

@dp.callback_query(F.data == 'change_score')
async def change_score(call: CallbackQuery, state: FSMContext):
    a_button = InlineKeyboardButton(text='🏠 Перейти в начало', callback_data='Перейти в начало')
    button   = InlineKeyboardMarkup(inline_keyboard=[[a_button]])
    await call.message.answer('Введите адрес кошелька:', reply_markup=button)
    await state.set_state(c_s.score)

@dp.message(StateFilter(c_s.score))
async def change_score1(msg: Message):
    if msg.text:
        conn = await cr()
        await conn.execute(f"UPDATE bot SET score = '{msg.text}'")
        await msg.answer('Адрес на пополнение успешно изменено!')
    else:
        await msg.answer('Ошибка! Нужно вводить, а не фото и тд.')
    await menu(msg)



async def main():
    task = asyncio.create_task(NACH())
    while True:
        try:
            await dp.start_polling(bot)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            await asyncio.sleep(3)
            continue

if __name__ == '__main__':
    asyncio.run(main())