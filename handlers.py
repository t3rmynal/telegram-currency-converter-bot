# handlers.py
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from languages import MESSAGES
from utils import get_user, CRYPTO_IDS, convert_fiat, convert_crypto, convert_custom
from charts import generate_chart

router = Router()


class Form(StatesGroup):
    currency = State()
    crypto = State()
    custom = State()
    favorite = State()


@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user.get("language")
    if lang is None:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="English", callback_data="lang_en"),
                InlineKeyboardButton(text="Русский", callback_data="lang_ru")
            ]
        ])
        await message.answer(MESSAGES["en"]["choose_language"], reply_markup=keyboard)
        return
    text = MESSAGES[lang]["menu"]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=MESSAGES[lang]["fiat"], callback_data="platform_fiat"),
            InlineKeyboardButton(text=MESSAGES[lang]["crypto"], callback_data="platform_crypto")
        ],
        [
            InlineKeyboardButton(text=MESSAGES[lang]["custom"], callback_data="platform_custom"),
            InlineKeyboardButton(text=MESSAGES[lang]["favorites"], callback_data="platform_favorites")
        ],
        [
            InlineKeyboardButton(text=MESSAGES[lang]["change_language"], callback_data="change_language")
        ]
    ])
    await message.answer(text, reply_markup=keyboard)


@router.callback_query(F.data.startswith("lang_"))
async def set_language(callback: types.CallbackQuery):
    lang = callback.data.split("_")[1]
    user = get_user(callback.from_user.id)
    user["language"] = lang
    await callback.message.edit_text(MESSAGES[lang]["language_selected"])
    text = MESSAGES[lang]["menu"]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=MESSAGES[lang]["fiat"], callback_data="platform_fiat"),
            InlineKeyboardButton(text=MESSAGES[lang]["crypto"], callback_data="platform_crypto")
        ],
        [
            InlineKeyboardButton(text=MESSAGES[lang]["custom"], callback_data="platform_custom"),
            InlineKeyboardButton(text=MESSAGES[lang]["favorites"], callback_data="platform_favorites")
        ],
        [
            InlineKeyboardButton(text=MESSAGES[lang]["change_language"], callback_data="change_language")
        ]
    ])
    await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == "platform_fiat")
async def platform_fiat(callback: types.CallbackQuery, state: FSMContext):
    user = get_user(callback.from_user.id)
    lang = user["language"]
    await callback.message.answer(MESSAGES[lang]["enter_conversion_fiat"])
    await state.set_state(Form.currency)
    await callback.answer()


@router.callback_query(F.data == "platform_crypto")
async def platform_crypto(callback: types.CallbackQuery, state: FSMContext):
    user = get_user(callback.from_user.id)
    lang = user["language"]
    await callback.message.answer(MESSAGES[lang]["enter_conversion_crypto"])
    await state.set_state(Form.crypto)
    await callback.answer()


@router.callback_query(F.data == "platform_custom")
async def platform_custom(callback: types.CallbackQuery, state: FSMContext):
    user = get_user(callback.from_user.id)
    lang = user["language"]
    await callback.message.answer(MESSAGES[lang]["enter_conversion_custom"])
    await state.set_state(Form.custom)
    await callback.answer()


@router.callback_query(F.data == "platform_favorites")
async def platform_favorites(callback: types.CallbackQuery):
    user = get_user(callback.from_user.id)
    lang = user["language"]
    favs = user.get("favorites", [])
    if not favs:
        await callback.message.answer(MESSAGES[lang]["no_favorites"])
    else:
        text = MESSAGES[lang]["choose_favorite"]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"{pair[0]} -> {pair[1]}", callback_data=f"fav_{pair[0]}_{pair[1]}")]
            for pair in favs
        ])
        await callback.message.answer(text, reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data.startswith("fav_"))
async def favorite_selected(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split("_")
    from_curr = data[1]
    to_curr = data[2]
    user = get_user(callback.from_user.id)
    user["current_pair"] = (from_curr, to_curr)
    lang = user["language"]
    await callback.message.answer(MESSAGES[lang]["prompt_amount_for_favorite"].format(
        from_currency=from_curr, to_currency=to_curr))
    await state.set_state(Form.favorite)
    await callback.answer()


@router.callback_query(F.data.startswith("add_"))
async def add_to_favorite(callback: types.CallbackQuery):
    data = callback.data.split("_")
    from_curr = data[1]
    to_curr = data[2]
    user = get_user(callback.from_user.id)
    lang = user["language"]
    pair = (from_curr, to_curr)
    if pair not in user["favorites"]:
        user["favorites"].append(pair)
        await callback.message.answer(MESSAGES[lang]["added_favorite"])
    else:
        await callback.message.answer(MESSAGES[lang]["already_favorite"])
    await callback.answer()


@router.callback_query(F.data.startswith("chart_"))
async def show_chart(callback: types.CallbackQuery):
    data = callback.data.split("_")
    from_curr = data[1]
    to_curr = data[2]
    user = get_user(callback.from_user.id)
    lang = user["language"]
    chart = generate_chart(from_curr, to_curr)
    if chart:
        caption = MESSAGES[lang]["chart_generated"].format(
            from_currency=from_curr, to_currency=to_curr)
        photo = InputFile(chart, filename="chart.png")
        await callback.message.answer_photo(photo=photo, caption=caption)
    else:
        await callback.message.answer(MESSAGES[lang]["conversion_error"])
    await callback.answer()


@router.message(Form.currency)
async def process_fiat(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user["language"]
    parts = message.text.strip().split()
    if len(parts) != 4 or parts[2].lower() != "to":
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    try:
        amount = float(parts[0])
        from_curr = parts[1].upper()
        to_curr = parts[3].upper()
    except ValueError:
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    result = convert_fiat(amount, from_curr, to_curr)
    if result is None:
        await message.answer(MESSAGES[lang]["conversion_error"])
    else:
        text = MESSAGES[lang]["conversion_result"].format(
            amount=amount, from_currency=from_curr, result=result, to_currency=to_curr)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=MESSAGES[lang]["add_favorite_button"],
                                  callback_data=f"add_{from_curr}_{to_curr}")],
            [InlineKeyboardButton(text=MESSAGES[lang]["chart_button"],
                                  callback_data=f"chart_{from_curr}_{to_curr}")]
        ])
        await message.answer(text, reply_markup=keyboard)
    await state.clear()


@router.message(Form.crypto)
async def process_crypto(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user["language"]
    parts = message.text.strip().split()
    if len(parts) != 4 or parts[2].lower() != "to":
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    try:
        amount = float(parts[0])
        from_curr = parts[1].upper()
        to_curr = parts[3].upper()
    except ValueError:
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    result = convert_crypto(amount, from_curr, to_curr)
    if result is None:
        await message.answer(MESSAGES[lang]["conversion_error"])
    else:
        text = MESSAGES[lang]["conversion_result"].format(
            amount=amount, from_currency=from_curr, result=result, to_currency=to_curr)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=MESSAGES[lang]["add_favorite_button"],
                                  callback_data=f"add_{from_curr}_{to_curr}")],
            [InlineKeyboardButton(text=MESSAGES[lang]["chart_button"],
                                  callback_data=f"chart_{from_curr}_{to_curr}")]
        ])
        await message.answer(text, reply_markup=keyboard)
    await state.clear()


@router.message(Form.custom)
async def process_custom(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user["language"]
    parts = message.text.strip().split()
    if len(parts) != 4 or parts[2].lower() != "to":
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    try:
        amount = float(parts[0])
        from_curr = parts[1].upper()
        to_curr = parts[3].upper()
    except ValueError:
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    if from_curr != "FPI" and to_curr != "FPI":
        await message.answer(MESSAGES[lang]["unknown_currency"])
        await state.clear()
        return
    result = convert_custom(amount, from_curr, to_curr)
    if result is None:
        await message.answer(MESSAGES[lang]["conversion_error"])
    else:
        text = MESSAGES[lang]["conversion_result"].format(
            amount=amount, from_currency=from_curr, result=result, to_currency=to_curr)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=MESSAGES[lang]["add_favorite_button"],
                                  callback_data=f"add_{from_curr}_{to_curr}")]
        ])
        await message.answer(text, reply_markup=keyboard)
    await state.clear()


@router.message(Form.favorite)
async def process_favorite(message: types.Message, state: FSMContext):
    user = get_user(message.from_user.id)
    lang = user["language"]
    pair = user.get("current_pair")
    if not pair:
        await message.answer(MESSAGES[lang]["help"])
        await state.clear()
        return
    from_curr, to_curr = pair
    try:
        amount = float(message.text.strip())
    except ValueError:
        await message.answer(MESSAGES[lang]["invalid_format"])
        await state.clear()
        return
    if from_curr in CRYPTO_IDS or to_curr in CRYPTO_IDS:
        result = convert_crypto(amount, from_curr, to_curr)
    elif from_curr == "FPI" or to_curr == "FPI":
        result = convert_custom(amount, from_curr, to_curr)
    else:
        result = convert_fiat(amount, from_curr, to_curr)
    if result is None:
        await message.answer(MESSAGES[lang]["conversion_error"])
    else:
        text = MESSAGES[lang]["conversion_result"].format(
            amount=amount, from_currency=from_curr, result=result, to_currency=to_curr)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=MESSAGES[lang]["add_favorite_button"],
                                  callback_data=f"add_{from_curr}_{to_curr}")],
            [InlineKeyboardButton(text=MESSAGES[lang]["chart_button"],
                                  callback_data=f"chart_{from_curr}_{to_curr}")]
        ])
        await message.answer(text, reply_markup=keyboard)
    await state.clear()


@router.message()
async def default_handler(message: types.Message):
    user = get_user(message.from_user.id)
    lang = user.get("language", "en")
    await message.answer(MESSAGES[lang]["help"])
