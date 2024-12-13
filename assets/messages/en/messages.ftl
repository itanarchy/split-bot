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

messages-purchase-enter_username = Enter username
messages-purchase-enter_count = Enter stars count
messages-purchase-wrong_count =
    Wrong stars count!

    Minimum: { $minimum }
    Maximum: { $maximum }

    You've entered: { $entered }

messages-purchase-stars = { $count } stars
messages-purchase-subscription_period = { $period ->
    [1] 1 month
    [12] 1 year
    *[other] { $period } months
}

messages-purchase-currency_not_available = Currency is not available
messages-purchase-subscription_not_available = Subscription is not available
messages-purchase-premium = Telegram Premium for { messages-purchase-subscription_period }
messages-purchase-select_period = Select the subscription period
messages-purchase-select_currency = Select the currency
messages-purchase-confirm =
    Username: { $username }
    Product: { $product }
    Price: ${ $price }

messages-confirm_transaction = Confirm transaction in your wallet app to proceed
messages-transaction_canceled = Transaction canceled

messages-referral-info =
    🌟 Invite friends with your referral link and get 40% of their commissions!

    👇 Click button below to copy your referral link

messages-referral-invite =
    ⭐️ Buy Stars without KYC via Split ❤️

    🚀 { $link }

buttons-menu = 📚 Menu
buttons-premium = 💠 Premium
buttons-stars = ⭐️ Stars
buttons-app = 📱 Open in App
buttons-referral_program = 🚀 Referral Program
buttons-language = 🌎 Language
buttons-copy_link = 🔗 Copy Link
buttons-disconnect = ⛓️‍💥 Disconnect Wallet
buttons-connect = 🔌 Connect Wallet
buttons-back = 🔙 Back
buttons-cancel = ❌ Cancel
buttons-ton_connect_url = 📱 Go to the app
buttons-confirm = ✅ Everything is correct
