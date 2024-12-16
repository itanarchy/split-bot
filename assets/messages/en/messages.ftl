messages-hello =
    <b>👋 Hello, { $name }!</b>

    <b>🤩 Ready to buy some stars?</b>

    <b>⚡️ Powered by <a href="https://t.me/SplitTg">Split.tg</a></b>

messages-choose_wallet = 👛 Choose wallet to connect
messages-ton_connect = 👇 Click the button below or scan QR code to connect your TON wallet
messages-wallet_connected = 👛 You have successfuly linked your TON wallet { $address }
messages-wallet_not_connected = 👛 Connect your TON wallet to continue
messages-connection_cancelled = ☑️ Connection cancelled
messages-connection_timeout = ⏳ Connection expired
messages-something_went_wrong = Oops! Something went wrong...
messages-language = 🌎 Select your preferred language by clicking button below:

extra-language = 🇬🇧 🇬English
extra-selectable = { $selected ->
    [true] [ {$value} ]
    *[other] { $value }
}

messages-purchase-enter_username = ✏️ Enter username
messages-purchase-enter_count = ⭐️ Enter stars count
messages-purchase-wrong_count =
    <b>❌ Wrong stars count!</b>

    <b>↘️ Minimum »</b> <code>{ $minimum }</code> ⭐️
    <b>↗️ Maximum »</b> <code>{ $maximum }</code> ⭐️

    <b>🔢 Entered »</b> <code>{ $entered }</code> ⭐️

messages-purchase-stars = { $count } ⭐️
messages-purchase-subscription_period = { $period ->
    [1] 1 month
    [12] 1 year
    *[other] { $period } months
}

messages-purchase-error = { $error ->
    [already_premium] 😴 @{ $username } already has a premium subscription
    [username_not_assigned] ⛓️‍💥 Username @{ $username } is not assigned to a user
    [username_not_found] 🫗 No users found with username @{ $username }
    *[other] { $error }
}

messages-purchase-currency_not_available = 🫗 Currency is no longer available
messages-purchase-subscription_not_available = 🫗 Subscription is no longer available
messages-purchase-premium = Telegram Premium for { messages-purchase-subscription_period }
messages-purchase-select_period = 📅 Select the subscription period
messages-purchase-select_currency = 💱 Select the currency
messages-purchase-confirm =
    <b>👤 Receiver »</b> @{ $username }
    <b>🛒 Product »</b> { $product }
    <b>💸 Price »</b> ${ $price }

messages-confirm_transaction = 👛 Confirm transaction in your wallet app to proceed
messages-transaction_canceled = ❌ Transaction canceled

messages-referral-info =
    🌟 Invite friends with your referral link and get 40% of their commissions!

    👇 Click button below to copy your referral link

messages-referral-invite =
    ⭐️ Buy Stars without KYC via Split ❤️

    🚀 { $link }

buttons-menu = 📚 Menu
buttons-premium = 💠 Premium
buttons-stars = ⭐️ Stars
buttons-select_username = 👤 @{ $username } (Me)
buttons-app = 📱 Open in App
buttons-referral_program = 🚀 Referral Program
buttons-language = 🌎 Language
buttons-copy_link = 🔗 Copy Link
buttons-share = 👥 Share
buttons-join_bot = 💝️ Buy Stars via Split.tg
buttons-disconnect = ⛓️‍💥 Disconnect Wallet
buttons-connect = 🔌 Connect Wallet
buttons-back = 🔙 Back
buttons-cancel = ❌ Cancel
buttons-ton_connect_url = 📱 Go to the app
buttons-confirm = ✅ Everything is correct
