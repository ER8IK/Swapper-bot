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
        "quote_failed": "❌ <b>Не удалось получить котировку.</b>",
        "confirm": "📋 <b>Подтверди обмен:</b>\n\nОтдаёшь: <b>{amount} {from_label}</b>\nПолучаешь: <b>≈{amount_to} {to_label}</b>\nАдрес: <code>{address}</code>\n\nВсё верно?",
        "creating": "⏳ Создаю обмен...",
        "created": "✅ <b>Обмен создан!</b>\n\nID: <code>{id}</code>\nОтправь <b>{amount} {from_label}</b> на адрес:\n<code>{address_from}</code>",
        "create_failed": "❌ Не удалось создать обмен.",
        "cancelled": "❌ Отменено.",
        "no_active": "Нет активного действия.",
        "invalid_amount": "⚠️ Введи корректную сумму",
        "address_short": "⚠️ Адрес слишком короткий для <b>{label}</b>.",
        "choose_language": "🌐 Выбери язык:",
        "language_set": "✅ Язык изменён на Русский",
        "fiat_choose": "💳 <b>Купить крипту картой</b>\n\nВыбери валюту оплаты:",
        "fiat_enter_amount": "Введите сумму:",
        "fiat_created": "✅ <b>Заказ создан!</b>\n\nОплати здесь:\n{url}",
        "fiat_created_no_url": "✅ <b>Заказ создан!</b>",
    },

    "en": {
        "welcome": "👋 Hello! I'm a crypto exchange bot powered by SimpleSwap.",
        "how_it_works": "📖 <b>How it works:</b>",
        "btn_swap": "🔄 Swap",
        "btn_buy_card": "💳 Buy with card",
        "btn_how": "ℹ️ How it works?",
        "btn_back": "🔙 Back",
        "btn_cancel": "❌ Cancel",
        "btn_confirm": "✅ Confirm",
        "btn_language": "🌐 Language",
        "choose_from": "Choose asset to send:",
        "choose_to": "Choose asset to receive:",
        "enter_amount": "Enter amount:",
        "fetching_quote": "⏳ Fetching quote...",
        "quote": "💱 <b>Quote</b>",
        "amount_too_small": "⚠️ Amount too small",
        "quote_failed": "❌ Could not get quote",
        "confirm": "📋 Confirm swap",
        "creating": "⏳ Creating exchange...",
        "created": "✅ Exchange created",
        "create_failed": "❌ Failed to create exchange",
        "cancelled": "❌ Cancelled",
        "no_active": "No active action",
        "invalid_amount": "⚠️ Invalid amount",
        "address_short": "⚠️ Address too short",
        "choose_language": "🌐 Choose language:",
        "language_set": "✅ Language set to English",
        "fiat_choose": "💳 Buy crypto with card",
        "fiat_enter_amount": "Enter amount:",
        "fiat_created": "✅ Order created\n{url}",
        "fiat_created_no_url": "✅ Order created",
    },

    "de": {
        "welcome": "👋 Hallo! Ich bin ein Krypto-Tauschbot.",
        "how_it_works": "📖 <b>So funktioniert es</b>",
        "btn_swap": "🔄 Tauschen",
        "btn_buy_card": "💳 Mit Karte kaufen",
        "btn_how": "ℹ️ Wie funktioniert es?",
        "btn_back": "🔙 Zurück",
        "btn_cancel": "❌ Abbrechen",
        "btn_confirm": "✅ Bestätigen",
        "btn_language": "🌐 Sprache",
        "choose_from": "Wähle Sendewährung:",
        "choose_to": "Wähle Empfangswährung:",
        "enter_amount": "Betrag eingeben:",
        "fetching_quote": "⏳ Kurs wird geladen...",
        "quote": "💱 Kurs",
        "amount_too_small": "⚠️ Betrag zu klein",
        "quote_failed": "❌ Kurs nicht verfügbar",
        "confirm": "📋 Tausch bestätigen",
        "creating": "⏳ Erstelle Tausch...",
        "created": "✅ Tausch erstellt",
        "create_failed": "❌ Fehler",
        "cancelled": "❌ Abgebrochen",
        "no_active": "Keine aktive Aktion",
        "invalid_amount": "⚠️ Ungültiger Betrag",
        "address_short": "⚠️ Adresse zu kurz",
        "choose_language": "🌐 Sprache wählen:",
        "language_set": "✅ Deutsch gesetzt",
        "fiat_choose": "💳 Krypto mit Karte kaufen",
        "fiat_enter_amount": "Betrag eingeben:",
        "fiat_created": "✅ Bestellung erstellt\n{url}",
        "fiat_created_no_url": "✅ Bestellung erstellt",
    },

    "fr": {
        "welcome": "👋 Bonjour! Bot d'échange crypto.",
        "how_it_works": "📖 Fonctionnement",
        "btn_swap": "🔄 Échanger",
        "btn_buy_card": "💳 Acheter",
        "btn_how": "ℹ️ Aide",
        "btn_back": "🔙 Retour",
        "btn_cancel": "❌ Annuler",
        "btn_confirm": "✅ Confirmer",
        "btn_language": "🌐 Langue",
        "choose_from": "Choisir devise d’envoi:",
        "choose_to": "Choisir devise de réception:",
        "enter_amount": "Entrer montant:",
        "fetching_quote": "⏳ Chargement...",
        "quote": "💱 Taux",
        "amount_too_small": "⚠️ Montant trop faible",
        "quote_failed": "❌ Erreur taux",
        "confirm": "📋 Confirmer échange",
        "creating": "⏳ Création...",
        "created": "✅ Échange créé",
        "create_failed": "❌ Échec",
        "cancelled": "❌ Annulé",
        "no_active": "Aucune action",
        "invalid_amount": "⚠️ Montant invalide",
        "address_short": "⚠️ Adresse trop courte",
        "choose_language": "🌐 Choisir langue:",
        "language_set": "✅ Français activé",
        "fiat_choose": "💳 Acheter crypto",
        "fiat_enter_amount": "Entrer montant:",
        "fiat_created": "✅ Commande créée\n{url}",
        "fiat_created_no_url": "✅ Commande créée",
    },

    # =========================
    # FARSI
    # =========================

    "fa": {
        "welcome": (
            "👋 سلام! من ربات تبدیل ارز دیجیتال با SimpleSwap هستم.\n\n"
            "⚡ سریع، بدون ثبت‌نام، بدون KYC.\n\n"
            "یک گزینه انتخاب کنید:"
        ),
        "how_it_works": (
            "📖 <b>نحوه کار:</b>\n\n"
            "1. ارز و مقدار را انتخاب کنید\n"
            "2. نرخ تبدیل را بگیرید\n"
            "3. تأیید کنید\n"
            "4. ارز را ارسال کنید\n"
            "5. کوین دریافت کنید 🎉"
        ),
        "btn_swap": "🔄 تبدیل",
        "btn_buy_card": "💳 خرید با کارت",
        "btn_how": "ℹ️ چگونه کار می‌کند؟",
        "btn_back": "🔙 بازگشت",
        "btn_cancel": "❌ لغو",
        "btn_confirm": "✅ تأیید",
        "btn_language": "🌐 زبان",
        "choose_from": "ارز ارسالی را انتخاب کنید:",
        "choose_to": "ارز دریافتی را انتخاب کنید:",
        "enter_amount": "مقدار را وارد کنید:",
        "fetching_quote": "⏳ دریافت نرخ...",
        "quote": "💱 نرخ تبدیل",
        "amount_too_small": "⚠️ مقدار خیلی کم است",
        "quote_failed": "❌ دریافت نرخ ممکن نشد",
        "confirm": "📋 تأیید تبدیل",
        "creating": "⏳ در حال ایجاد سفارش...",
        "created": "✅ سفارش ایجاد شد",
        "create_failed": "❌ خطا در ایجاد سفارش",
        "cancelled": "❌ لغو شد",
        "no_active": "عملیاتی فعال نیست",
        "invalid_amount": "⚠️ مقدار نامعتبر",
        "address_short": "⚠️ آدرس خیلی کوتاه است",
        "choose_language": "🌐 زبان را انتخاب کنید:",
        "language_set": "✅ زبان فارسی فعال شد",
        "fiat_choose": "💳 خرید کریپتو با کارت",
        "fiat_enter_amount": "مبلغ را وارد کنید:",
        "fiat_created": "✅ سفارش ایجاد شد\n{url}",
        "fiat_created_no_url": "✅ سفارش ایجاد شد",
    },

    # =========================
    # ARABIC
    # =========================

    "ar": {
        "welcome": (
            "👋 أهلاً! أنا بوت تبادل العملات عبر SimpleSwap.\n\n"
            "⚡ سريع، بدون تسجيل، بدون KYC.\n\n"
            "اختر إجراء:"
        ),
        "how_it_works": (
            "📖 <b>كيف يعمل:</b>\n\n"
            "1. اختر العملة والمبلغ\n"
            "2. احصل على السعر\n"
            "3. أكد العملية\n"
            "4. أرسل العملات\n"
            "5. استلم عملاتك 🎉"
        ),
        "btn_swap": "🔄 تبديل",
        "btn_buy_card": "💳 شراء بالبطاقة",
        "btn_how": "ℹ️ كيف يعمل؟",
        "btn_back": "🔙 رجوع",
        "btn_cancel": "❌ إلغاء",
        "btn_confirm": "✅ تأكيد",
        "btn_language": "🌐 اللغة",
        "choose_from": "اختر العملة المرسلة:",
        "choose_to": "اختر العملة المستلمة:",
        "enter_amount": "أدخل المبلغ:",
        "fetching_quote": "⏳ جاري جلب السعر...",
        "quote": "💱 السعر",
        "amount_too_small": "⚠️ المبلغ صغير جداً",
        "quote_failed": "❌ تعذر الحصول على السعر",
        "confirm": "📋 تأكيد التبديل",
        "creating": "⏳ إنشاء الطلب...",
        "created": "✅ تم إنشاء الطلب",
        "create_failed": "❌ فشل الإنشاء",
        "cancelled": "❌ تم الإلغاء",
        "no_active": "لا يوجد إجراء نشط",
        "invalid_amount": "⚠️ مبلغ غير صالح",
        "address_short": "⚠️ العنوان قصير جداً",
        "choose_language": "🌐 اختر اللغة:",
        "language_set": "✅ تم تفعيل العربية",
        "fiat_choose": "💳 شراء كريبتو بالبطاقة",
        "fiat_enter_amount": "أدخل المبلغ:",
        "fiat_created": "✅ تم إنشاء الطلب\n{url}",
        "fiat_created_no_url": "✅ تم إنشاء الطلب",
    }
}

DEFAULT_LANG = "en"


def t(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS[DEFAULT_LANG]).get(key)
    if text is None:
        text = TEXTS[DEFAULT_LANG].get(key, key)
    if kwargs:
        text = text.format(**kwargs)
    return text