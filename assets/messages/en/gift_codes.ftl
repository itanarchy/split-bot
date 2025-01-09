
buttons-create_gift_code = 🎁 Create Gift Code
buttons-set_gift_code_activations = ✏️ Activations
buttons-set_gift_code_amount = ✏️ Claim amount

messages-gift_codes-info =
    <b>🎁 Gift code for stars</b>

    ☑️ Total activations » <b>{ $activations ->
        [null] not set
        *[other] { $activations }
    }</b>
    ⭐️ Claim amount » <b>{ $amount ->
        [null] not set
        *[other] { $amount } TON (~${ $usd_amount })
    }</b>

    <b>{ $status ->
        [not_ready] 🔘 Use buttons below to edit gift code
        [activations_limit] ❌ Total activations must be between { $min_activations } and { $max_activations }
        [amount_limit] ❌ Claim amount must be between { $min_amount } and { $max_amount } TON
        *[other] 🟢 Ready to create
    }</b>


messages-gift_codes-enter_amount = ✏️ Enter claim amount in TON ({ $min } - { $max })
messages-gift_codes-enter_activations = ✏️ Enter total activations ({ $min } - { $max })

messages-gift_codes-created =
    <b>🎁 Gift code created</b>

    <b>🔗 Now anyone can activate it via link below »</b>
    { $link }

    <blockquote>⚠️ Please make sure that you have confirmed transaction before using gift code.</blockquote>

messages-gift_codes-expired = 🎁 Gift code expired

messages-gift_codes-view =
    <b>🎁 Gift code for { $max_buy_amount } TON</b>

    <b>🚀 { $activations_left } of { $max_activations } activations left</b>

    <b>✏️ Enter username below to claim stars</b>

messages-gift_codes-use_requested =
    👛 A transaction to receive stars for username @{ $username } has been requested from your wallet
