from typing import TYPE_CHECKING

from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from bot.locales.stub import TranslatorRunner


def test_basics(i18n: TranslatorRunner):
    wheretogo_message = '''\
Точки в нашем квесте деляться на 2 категории:
⭐️ особые  -> получаешь 3 балла
👉 обычные -> получаешь 1 балл

Проходи все особые точки и получай гарантированный приз 🎁\
'''
    w = i18n.wheretogo.message()
    assert w == wheretogo_message

    wheretogo_button = "🎯 Куда пойти?"
    assert i18n.wheretogo.button() == wheretogo_button

    statistics_button = "🤩 Моя статистика"
    assert i18n.statistics.button() == statistics_button

    star_message = '''\
🥳 Ура! Ты прошёл все особые точки! Теперь ты можешь получить заслуженный приз - лимонад и стикерпак ✨
Подходи на точку "Раздатка"!\
'''
    assert i18n.star.message() == star_message
