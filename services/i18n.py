TEXTS = {
    "ru": {
        "welcome": (
            "👋 Привет! Я бот для обмена криптовалют через SimpleSwap.\n\n"
            "⚡ Быстро, без регистрации, без KYC.\n\n"
            "Выбери действие:"
        ),
        "how_it_works": (
            "📖 <b>Как это работает:</b>\n\n"
            "1. Выбираешь валюту и сумму\n"
            "2. Получаешь курс обмена\n"
            "3. Подтверждаешь — я создаю обмен\n"
            "4. Отправляешь крипту на адрес\n"
            "5. Получаешь обмененные монеты 🎉\n\n"
            "<i>Powered by SimpleSwap</i>"
        ),
        "btn_swap": "🔄 Swap",
        "btn_buy_card": "💳 Buy with card",
        "btn_how": "ℹ️ Как это работает?",
        "btn_back": "🔙 Назад",
        "btn_cancel": "❌ Отмена",
        "btn_confirm": "✅ Подтвердить",
        "btn_language": "🌐 Язык / Language",
        "choose_from": "🔄 <b>Новый обмен</b>\n\nВыбери валюту, которую хочешь <b>отдать</b>:",
        "choose_to": "✅ Отдаёшь: <b>{from_label}</b>\n\nТеперь выбери валюту, которую хочешь <b>получить</b>:",
        "enter_amount": "✅ Получаешь: <b>{to_label}</b>\n\nВведи сумму в <b>{from_label}</b>:\n<i>Минимум: {min} {ticker}</i>\n\n<i>/cancel для отмены</i>",
        "fetching_quote": "⏳ Получаю котировку...",
        "quote": "💱 <b>Котировка:</b>\n\nОтдаёшь: <b>{amount} {from_label}</b>\nПолучаешь: <b>≈{amount_to} {to_label}</b>\n\nВведи адрес кошелька для получения <b>{to_label}</b>:\n\n<i>/cancel для отмены</i>",
        "amount_too_small": "⚠️ Сумма слишком маленькая.\n\nМинимум для <b>{from_label}</b>: <b>{min} {ticker}</b>\n\n<i>/cancel для отмены</i>",
        "quote_failed": "❌ <b>Не удалось получить котировку.</b>\n\nВозможные причины:\n• Сумма слишком маленькая\n• Пара временно недоступна\n• Проблемы с API\n\nПопробуй другую сумму.\n<i>/cancel для отмены</i>",
        "confirm": "📋 <b>Подтверди обмен:</b>\n\nОтдаёшь: <b>{amount} {from_label}</b>\nПолучаешь: <b>≈{amount_to} {to_label}</b>\nАдрес: <code>{address}</code>\n\nВсё верно?",
        "creating": "⏳ Создаю обмен...",
        "created": "✅ <b>Обмен создан!</b>\n\nID: <code>{id}</code>\nОтправь <b>{amount} {from_label}</b> на адрес:\n<code>{address_from}</code>\n\nСтатус: /status_{id}",
        "create_failed": "❌ Не удалось создать обмен. Попробуй позже.",
        "cancelled": "❌ Отменено.\n\nНапиши /start чтобы начать заново.",
        "no_active": "Нет активного действия. Напиши /start",
        "invalid_amount": "⚠️ Введи корректную сумму, например: <b>0.01</b>",
        "address_short": "⚠️ Адрес слишком короткий для <b>{label}</b>.\nМинимум {min} символов, у тебя {count}.\n\n<i>/cancel для отмены</i>",
        "choose_language": "🌐 Выбери язык:",
        "language_set": "✅ Язык изменён на Русский",
        "fiat_choose": "💳 <b>Купить крипту картой</b>\n\nВыбери валюту оплаты:",
        "fiat_enter_amount": "✅ Платишь: <b>{from_label}</b>\n\nВведи сумму:\n<i>Минимум: {min} {ticker}</i>\n\n<i>/cancel для отмены</i>",
        "fiat_created": "✅ <b>Заказ создан!</b>\n\nОплати здесь:\n{url}\n\nID: <code>{id}</code>\nСтатус: /status_{id}",
        "fiat_created_no_url": "✅ <b>Заказ создан!</b>\n\nID: <code>{id}</code>\nСтатус: /status_{id}",
    },
    "en": {
        "welcome": (
            "👋 Hello! I'm a crypto exchange bot powered by SimpleSwap.\n\n"
            "⚡ Fast, no registration, no KYC.\n\n"
            "Choose an action:"
        ),
        "how_it_works": (
            "📖 <b>How it works:</b>\n\n"
            "1. Choose currency and amount\n"
            "2. Get exchange rate\n"
            "3. Confirm — I create the exchange\n"
            "4. Send crypto to the address\n"
            "5. Receive your coins 🎉\n\n"
            "<i>Powered by SimpleSwap</i>"
        ),
        "btn_swap": "🔄 Swap",
        "btn_buy_card": "💳 Buy with card",
        "btn_how": "ℹ️ How it works?",
        "btn_back": "🔙 Back",
        "btn_cancel": "❌ Cancel",
        "btn_confirm": "✅ Confirm",
        "btn_language": "🌐 Language",
        "choose_from": "🔄 <b>New swap</b>\n\nChoose the currency you want to <b>send</b>:",
        "choose_to": "✅ Sending: <b>{from_label}</b>\n\nChoose the currency you want to <b>receive</b>:",
        "enter_amount": "✅ Receiving: <b>{to_label}</b>\n\nEnter amount in <b>{from_label}</b>:\n<i>Minimum: {min} {ticker}</i>\n\n<i>Type /cancel to abort</i>",
        "fetching_quote": "⏳ Fetching quote...",
        "quote": "💱 <b>Quote:</b>\n\nYou send: <b>{amount} {from_label}</b>\nYou receive: <b>≈{amount_to} {to_label}</b>\n\nEnter destination wallet address for <b>{to_label}</b>:\n\n<i>Type /cancel to abort</i>",
        "amount_too_small": "⚠️ Amount too small.\n\nMinimum for <b>{from_label}</b>: <b>{min} {ticker}</b>\n\n<i>Type /cancel to abort</i>",
        "quote_failed": "❌ <b>Could not get a quote.</b>\n\nPossible reasons:\n• Amount too small\n• Pair temporarily unavailable\n• API issue\n\nTry a different amount.\n<i>Type /cancel to abort</i>",
        "confirm": "📋 <b>Confirm swap:</b>\n\nYou send: <b>{amount} {from_label}</b>\nYou receive: <b>≈{amount_to} {to_label}</b>\nAddress: <code>{address}</code>\n\nEverything correct?",
        "creating": "⏳ Creating exchange...",
        "created": "✅ <b>Exchange created!</b>\n\nID: <code>{id}</code>\nSend <b>{amount} {from_label}</b> to:\n<code>{address_from}</code>\n\nCheck status: /status_{id}",
        "create_failed": "❌ Failed to create exchange. Please try again later.",
        "cancelled": "❌ Cancelled.\n\nType /start to begin again.",
        "no_active": "No active action. Type /start",
        "invalid_amount": "⚠️ Enter a valid amount, e.g. <b>0.01</b>",
        "address_short": "⚠️ Address too short for <b>{label}</b>.\nMinimum {min} characters, you entered {count}.\n\n<i>Type /cancel to abort</i>",
        "choose_language": "🌐 Choose language:",
        "language_set": "✅ Language set to English",
        "fiat_choose": "💳 <b>Buy crypto with card</b>\n\nChoose payment currency:",
        "fiat_enter_amount": "✅ Paying with: <b>{from_label}</b>\n\nEnter amount:\n<i>Minimum: {min} {ticker}</i>\n\n<i>Type /cancel to abort</i>",
        "fiat_created": "✅ <b>Order created!</b>\n\nComplete payment here:\n{url}\n\nID: <code>{id}</code>\nCheck status: /status_{id}",
        "fiat_created_no_url": "✅ <b>Order created!</b>\n\nID: <code>{id}</code>\nCheck status: /status_{id}",
    },
    "de": {
        "welcome": (
            "👋 Hallo! Ich bin ein Krypto-Tauschbot von SimpleSwap.\n\n"
            "⚡ Schnell, ohne Registrierung, ohne KYC.\n\n"
            "Wähle eine Aktion:"
        ),
        "how_it_works": (
            "📖 <b>So funktioniert es:</b>\n\n"
            "1. Währung und Betrag wählen\n"
            "2. Wechselkurs erhalten\n"
            "3. Bestätigen — ich erstelle den Tausch\n"
            "4. Krypto an die Adresse senden\n"
            "5. Coins erhalten 🎉\n\n"
            "<i>Powered by SimpleSwap</i>"
        ),
        "btn_swap": "🔄 Tauschen",
        "btn_buy_card": "💳 Mit Karte kaufen",
        "btn_how": "ℹ️ Wie funktioniert es?",
        "btn_back": "🔙 Zurück",
        "btn_cancel": "❌ Abbrechen",
        "btn_confirm": "✅ Bestätigen",
        "btn_language": "🌐 Sprache",
        "choose_from": "🔄 <b>Neuer Tausch</b>\n\nWähle die Währung zum <b>Senden</b>:",
        "choose_to": "✅ Senden: <b>{from_label}</b>\n\nWähle die Währung zum <b>Empfangen</b>:",
        "enter_amount": "✅ Empfangen: <b>{to_label}</b>\n\nBetrag in <b>{from_label}</b> eingeben:\n<i>Minimum: {min} {ticker}</i>\n\n<i>/cancel zum Abbrechen</i>",
        "fetching_quote": "⏳ Kurs wird abgerufen...",
        "quote": "💱 <b>Kurs:</b>\n\nSenden: <b>{amount} {from_label}</b>\nEmpfangen: <b>≈{amount_to} {to_label}</b>\n\nWallet-Adresse für <b>{to_label}</b> eingeben:\n\n<i>/cancel zum Abbrechen</i>",
        "amount_too_small": "⚠️ Betrag zu klein.\n\nMinimum für <b>{from_label}</b>: <b>{min} {ticker}</b>\n\n<i>/cancel zum Abbrechen</i>",
        "quote_failed": "❌ <b>Kurs konnte nicht abgerufen werden.</b>\n\nMögliche Gründe:\n• Betrag zu klein\n• Paar vorübergehend nicht verfügbar\n• API-Problem\n\nAnderen Betrag versuchen.\n<i>/cancel zum Abbrechen</i>",
        "confirm": "📋 <b>Tausch bestätigen:</b>\n\nSenden: <b>{amount} {from_label}</b>\nEmpfangen: <b>≈{amount_to} {to_label}</b>\nAdresse: <code>{address}</code>\n\nAlles korrekt?",
        "creating": "⏳ Tausch wird erstellt...",
        "created": "✅ <b>Tausch erstellt!</b>\n\nID: <code>{id}</code>\nSende <b>{amount} {from_label}</b> an:\n<code>{address_from}</code>\n\nStatus: /status_{id}",
        "create_failed": "❌ Tausch konnte nicht erstellt werden. Bitte später versuchen.",
        "cancelled": "❌ Abgebrochen.\n\n/start eingeben um neu zu beginnen.",
        "no_active": "Keine aktive Aktion. /start eingeben",
        "invalid_amount": "⚠️ Gültigen Betrag eingeben, z.B. <b>0.01</b>",
        "address_short": "⚠️ Adresse zu kurz für <b>{label}</b>.\nMindestens {min} Zeichen, du hast {count}.\n\n<i>/cancel zum Abbrechen</i>",
        "choose_language": "🌐 Sprache wählen:",
        "language_set": "✅ Sprache auf Deutsch gesetzt",
        "fiat_choose": "💳 <b>Krypto mit Karte kaufen</b>\n\nZahlungswährung wählen:",
        "fiat_enter_amount": "✅ Zahlung mit: <b>{from_label}</b>\n\nBetrag eingeben:\n<i>Minimum: {min} {ticker}</i>\n\n<i>/cancel zum Abbrechen</i>",
        "fiat_created": "✅ <b>Bestellung erstellt!</b>\n\nZahlung hier abschließen:\n{url}\n\nID: <code>{id}</code>\nStatus: /status_{id}",
        "fiat_created_no_url": "✅ <b>Bestellung erstellt!</b>\n\nID: <code>{id}</code>\nStatus: /status_{id}",
    },
    "fr": {
        "welcome": (
            "👋 Bonjour! Je suis un bot d'échange crypto via SimpleSwap.\n\n"
            "⚡ Rapide, sans inscription, sans KYC.\n\n"
            "Choisissez une action:"
        ),
        "how_it_works": (
            "📖 <b>Comment ça fonctionne:</b>\n\n"
            "1. Choisir la devise et le montant\n"
            "2. Obtenir le taux de change\n"
            "3. Confirmer — je crée l'échange\n"
            "4. Envoyer la crypto à l'adresse\n"
            "5. Recevoir vos coins 🎉\n\n"
            "<i>Powered by SimpleSwap</i>"
        ),
        "btn_swap": "🔄 Échanger",
        "btn_buy_card": "💳 Acheter par carte",
        "btn_how": "ℹ️ Comment ça marche?",
        "btn_back": "🔙 Retour",
        "btn_cancel": "❌ Annuler",
        "btn_confirm": "✅ Confirmer",
        "btn_language": "🌐 Langue",
        "choose_from": "🔄 <b>Nouvel échange</b>\n\nChoisissez la devise à <b>envoyer</b>:",
        "choose_to": "✅ Envoi: <b>{from_label}</b>\n\nChoisissez la devise à <b>recevoir</b>:",
        "enter_amount": "✅ Réception: <b>{to_label}</b>\n\nEntrez le montant en <b>{from_label}</b>:\n<i>Minimum: {min} {ticker}</i>\n\n<i>/cancel pour annuler</i>",
        "fetching_quote": "⏳ Récupération du taux...",
        "quote": "💱 <b>Taux:</b>\n\nVous envoyez: <b>{amount} {from_label}</b>\nVous recevez: <b>≈{amount_to} {to_label}</b>\n\nEntrez l'adresse du portefeuille pour <b>{to_label}</b>:\n\n<i>/cancel pour annuler</i>",
        "amount_too_small": "⚠️ Montant trop petit.\n\nMinimum pour <b>{from_label}</b>: <b>{min} {ticker}</b>\n\n<i>/cancel pour annuler</i>",
        "quote_failed": "❌ <b>Impossible d'obtenir un taux.</b>\n\nRaisons possibles:\n• Montant trop petit\n• Paire temporairement indisponible\n• Problème API\n\nEssayez un autre montant.\n<i>/cancel pour annuler</i>",
        "confirm": "📋 <b>Confirmer l'échange:</b>\n\nVous envoyez: <b>{amount} {from_label}</b>\nVous recevez: <b>≈{amount_to} {to_label}</b>\nAdresse: <code>{address}</code>\n\nTout est correct?",
        "creating": "⏳ Création de l'échange...",
        "created": "✅ <b>Échange créé!</b>\n\nID: <code>{id}</code>\nEnvoyez <b>{amount} {from_label}</b> à:\n<code>{address_from}</code>\n\nStatut: /status_{id}",
        "create_failed": "❌ Impossible de créer l'échange. Réessayez plus tard.",
        "cancelled": "❌ Annulé.\n\nTapez /start pour recommencer.",
        "no_active": "Aucune action active. Tapez /start",
        "invalid_amount": "⚠️ Entrez un montant valide, ex: <b>0.01</b>",
        "address_short": "⚠️ Adresse trop courte pour <b>{label}</b>.\nMinimum {min} caractères, vous avez {count}.\n\n<i>/cancel pour annuler</i>",
        "choose_language": "🌐 Choisir la langue:",
        "language_set": "✅ Langue définie en Français",
        "fiat_choose": "💳 <b>Acheter crypto par carte</b>\n\nChoisissez la devise de paiement:",
        "fiat_enter_amount": "✅ Paiement avec: <b>{from_label}</b>\n\nEntrez le montant:\n<i>Minimum: {min} {ticker}</i>\n\n<i>/cancel pour annuler</i>",
        "fiat_created": "✅ <b>Commande créée!</b>\n\nEffectuez le paiement ici:\n{url}\n\nID: <code>{id}</code>\nStatut: /status_{id}",
        "fiat_created_no_url": "✅ <b>Commande créée!</b>\n\nID: <code>{id}</code>\nStatut: /status_{id}",
    },
}

DEFAULT_LANG = "en"


def t(lang: str, key: str, **kwargs) -> str:
    """Get translated text."""
    text = TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key)
    if text is None:
        text = TEXTS[DEFAULT_LANG].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text