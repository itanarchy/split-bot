
buttons-create_gift_code = 🎁 Новый подарочный код
buttons-set_gift_code_activations = ✏️ Кол-во активаций
buttons-set_gift_code_amount = ✏️ Сумма активации

messages-gift_codes-info =
    <b>🎁 Подарочный код на звёзды</b>

    ☑️ Всего активаций » <b>{ $activations ->
        [null] не установлено
        *[other] { $activations }
    }</b>
    ⭐️ Сумма активации » <b>{ $amount ->
        [null] не установлено
        *[other] { $amount } TON (~${ $usd_amount })
    }</b>

    <b>{ $status ->
        [not_ready] 🔘 Используйте кнопки ниже, чтобы настроить подарочный код
        [activations_limit] ❌ Допустимое кол-во активаций: от { $min_activations } до { $max_activations }
        [amount_limit] ❌ Допустимая сумма активации: от { $min_amount } до { $max_amount } TON
        *[other] 🟢 Готов к созданию
    }</b>


messages-gift_codes-enter_amount = ✏️ Введите сумму активации в TON ({ $min } - { $max })
messages-gift_codes-enter_activations = ✏️ Введите кол-во активаций ({ $min } - { $max })

messages-gift_codes-created =
    <b>🎁 Подарочный код создан</b>

    <b>🔗 Теперь любой может активировать его по ссылке снизу »</b>
    { $link }

    <blockquote>⚠️ Пожалуйста, убедитесь, что вы подтвердили транзакцию в кошельке перед использованием подарочного кода.</blockquote>

messages-gift_codes-expired = 🎁 Подарочный код истёк

messages-gift_codes-view =
    <b>🎁 Подарочный код на { $max_buy_amount } TON</b>

    <b>🚀 Осталось { $activations_left } из { $max_activations } активаций</b>

    <b>✏️ Введите юзернейм пользователя, на которого хотите принять подарок</b>

messages-gift_codes-use_requested =
    👛 Транзакция на получение звёзд на аккаунт @{ $username } была отправлена на подтверждение в ваш кошелёк
