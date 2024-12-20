messages-hello =
    <b>👋 Привет, { $name }!</b>

    <b>🤩 Готов(-а) купить немного звёзд?</b>

    <b>⚡️ Сделано с ❤️ для <a href="https://t.me/SplitTg">Split.tg</a></b>

messages-choose_wallet = 👛 Выберите кошелёк для привязки
messages-ton_connect = 👇 Нажмите на кнопку ниже или отсканируйте QR-код, чтобы привязать ваш TON кошелёк
messages-wallet_connected = 👛 Вы успешно привязали свой кошелёк { $address }
messages-wallet_not_connected = 👛 Привяжите ваш TON кошелёк, чтобы продолжить
messages-session_expired = ⏳ Ваша сессия истекла. Пожалуйста, подключите ваш TON кошелёк снова
messages-connection_cancelled = ☑️ Подключение отменено
messages-connection_timeout = ⏳ Время подключения истекло
messages-something_went_wrong = Упс! Что-то пошло не так...
messages-language = 🌎 Выберите язык, нажав на кнопку ниже:
extra-language = 🇷🇺 Русский

messages-purchase-enter_username = ✏️ Введите юзернейм пользователя
messages-purchase-enter_count = ⭐️ Введите количество звёзд
messages-purchase-wrong_count =
    <b>❌ Неверное количество звёзд!</b>

    <b>↘️ Минимум »</b> <code>{ $minimum }</code> ⭐️
    <b>↗️ Максимум »</b> <code>{ $maximum }</code> ⭐️

    <b>🔢 Введено »</b> <code>{ $entered }</code> ⭐️

messages-purchase-stars = { $count } ⭐️
messages-purchase-subscription_period = { $period ->
    [one] { $period } месяц
    [few] { $period } месяца
    [12] 1 год
    *[other] { $period } месяцев
}

messages-purchase-error = { $error ->
    [already_premium] 😴 У @{ $username } уже есть подписка на Telegram Premium
    [username_not_assigned] ⛓️‍💥 Ссылка @{ $username } не привязана к пользователю
    [username_not_found] 🫗 Пользователь @{ $username } не найден
    *[other] { $error }
}

messages-purchase-currency_not_available = 🫗 Данная валюта больше не доступна
messages-purchase-subscription_not_available = 🫗 Данная опция недоступна
messages-purchase-premium = Telegram Premium на { messages-purchase-subscription_period }
messages-purchase-select_period = 📅 Выберите период подписки
messages-purchase-select_currency = 💱 Выберите валюту для оплаты
messages-purchase-confirm =
    <b>👤 Получатель »</b> @{ $username }
    <b>🛒 Товар »</b> { $product }
    <b>💸 Цена »</b> ${ $price }

messages-confirm_transaction =
    👛 Подтвердите транзакцию в приложении вашего кошелька, чтобы продолжить

messages-transaction_canceled = ❌ Транзакция отменена

messages-referral-info =
    🌟 Приглашай друзей по реферальной ссылке и получай 40% от их комиссий!

    👇 Нажми кнопку ниже, чтобы скопировать свою реферальную ссылку

messages-referral-invite =
    ⭐️ Покупай звёзды без KYC через Split ❤️

    🚀 { $link }

buttons-menu = 📚 Меню
buttons-premium = 💠 Premium
buttons-stars = ⭐️ Stars
buttons-select_username = 👤 @{ $username } (Я)
buttons-app = 📱 Открыть в приложении
buttons-referral_program = 🚀 Реферальная программа
buttons-language = 🌎 Язык
buttons-copy_link = 🔗 Скопировать ссылку
buttons-share = 👥 Поделиться
buttons-join_bot = 💝️ Покупай Stars через Split.tg
buttons-disconnect = ⛓️‍💥 Отключить кошелёк
buttons-connect = 🔌 Подключить кошелёк
buttons-back = 🔙 Назад
buttons-cancel = ❌ Отмена
buttons-ton_connect_url = 📱 Перейти к приложению
buttons-confirm = ✅ Всё верно
