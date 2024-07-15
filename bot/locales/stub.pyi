from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    last: Last
    start: Start
    infocard: Infocard
    wheretogo: Wheretogo
    statistics: Statistics
    star: Star
    superstar: Superstar
    unexpected: Unexpected
    help: Help
    top: Top
    lottery: Lottery
    programma: Programma
    doubled: Doubled
    station: Station
    wrong: Wrong
    undone: Undone
    done: Done


class Last:
    lp: LastLp


class LastLp:
    @staticmethod
    def message() -> Literal["""Вижу, что ты ко мне прямиком с прошлого Лимонад Пати! Давай забудем это недоразумение, ведь на этот раз я работаю!

Наслаждайся мероприятием ❤️

Мы можем притворится, что не знакомы, если ты дашь команду /start, или можешь просто продолжить пользоваться мной 😉"""]: ...


class Start:
    command: StartCommand

    @staticmethod
    def message(*, lottery) -> Literal["""Хей, привет! 👋
Ты пришёл на главное событие этой весны - Лимонад Пати!🍋 Тебя ждёт много интересных точек, море лимонада, веселья и куча классных призов!

Сегодня с 17:00 до 19:00 у нас работают интерактивные точки. За прохождение каждой из них можно получить баллы. Зарабатывай баллы и повышай свои шансы на выигрыш в лотерее, которая пройдёт в 21:15

А как же лимонад? За прохождение точек каждому мы подарим бутылочку освежающего напитка от Дона Лимона 🥤

Номер твоего лотерейного билета - { $lottery }

Веселись! Вот тебе карта активностей"""]: ...


class Infocard:
    @staticmethod
    def message() -> Literal["""Карта поможет тебе сориентироваться на Лимонад Пати ❤️
Лови👇"""]: ...

    @staticmethod
    def button() -> Literal["""🍋 Карта"""]: ...


class Wheretogo:
    @staticmethod
    def message() -> Literal["""В нашем квесте всё просто. Получаешь особый код за прохождение особой точки, даёшь его мне - и получаешь 1 балл

Проходи все особые точки и получай гарантированный приз 🎁"""]: ...

    @staticmethod
    def button() -> Literal["""🎯 Куда пойти?"""]: ...


class Statistics:
    @staticmethod
    def message(*, points, lottery) -> Literal["""Твои очки: { $points }. Номер лотерейного билета: { $lottery }"""]: ...

    @staticmethod
    def button() -> Literal["""🤩 Моя статистика"""]: ...


class Star:
    @staticmethod
    def message() -> Literal["""🥳 Ура! Ты прошёл все особые точки! Теперь ты можешь получить заслуженный приз - лимонад и стикерпак ✨
Подходи на точку &#34;Раздатка&#34;!"""]: ...


class Superstar:
    @staticmethod
    def message() -> Literal["""Молодец! Ты прошёл все точки и набрал максимум баллов! Оставайся с нами и следи за результатами розыгрыша, не забудь номер своего лотерейного билета! 🎰
Его узнать ты можешь, нажав кнопку &#34;Моя статистика&#34;!"""]: ...


class Unexpected:
    @staticmethod
    def message() -> Literal["""Я тебя не понимаю 😢 Воспользуйся кнопкой &#34;Помощь&#34;, чтобы узнать, что я могу"""]: ...


class Help:
    @staticmethod
    def message() -> Literal["""Я квест-бот Лимонад Пати!

📍 Проходи интерактивные точки и вводи мне числа, которые тебе скажут организаторы.

🎯 Если не знаешь, куда сходить и какие точки ещё пройти, нажми на &#34;Куда сходить?&#34;

🍋 Если не можешь найти какую-то точку, воспользуйся кнопкой &#34;Карта&#34;

🤩 Если хочешь узнать набранные баллы или забыл номер лотерейного билета, жми &#34;Моя статистика&#34;

🔥 Узнать программу Лимонад Пати ты можешь, нажав на кнопку &#34;Программа мероприятия&#34;

🆘 Кнопка &#34;Помощь&#34; покажет тебе это сообщение

Если есть вопросы, на которые я не смог ответить, обратить с организаторам. Это ребята с бейджиками!"""]: ...

    @staticmethod
    def button() -> Literal["""🆘 Помощь"""]: ...


class Top:
    user: TopUser


class TopUser:
    @staticmethod
    def template(*, user_name, points, lottery, quest_time) -> Literal["""Имя: { $user_name }
Очки: { $points }
Лоттерейный билет: { $lottery }
Время прохождения точкек: { $quest_time }\n\n"""]: ...


class Lottery:
    @staticmethod
    def message(*, lottery, points) -> Literal["""Номер твоего лотерейного билета { $lottery }, баллы: { $points }

📌 Каждый, кто пройдёт все особые точки, гарантированно получает приз: бутылку лимонада.

📌 Среди набравших максимальное количество баллов пройдёт розыгрыш призов от наших партнёров.

📌 Три лучших фотографии нашего фестиваля получат персональный подарок от Дона Лимона.
Открывай профиль, делай фото и выкладывай на свою страницу ВК с хэштегом #LemonadeParty2024"""]: ...

    @staticmethod
    def button() -> Literal["""🥰 Розыгрыш"""]: ...


class Programma:
    @staticmethod
    def message() -> Literal["""Чтобы не пропустить всё самое интересное, лови расписание нашего дня:

🕔 17:00-19:00
Интерактивные точки, выдача лимонада и квест

🕖 19:00
Выступление музыкантов и певцов от творческих объединений ТПУ и не только!

🕤 21:15
Розыгрыш, розыгрыш, розыгрыш и ещё розыгрыш"""]: ...

    @staticmethod
    def button() -> Literal["""🔥 Программа мероприятия"""]: ...


class Doubled:
    @staticmethod
    def station(*, station_name) -> Literal["""Верный код! Но ты уже проходил &#34;{ $station_name }&#34;..."""]: ...


class Station:
    @staticmethod
    def arrangement(*, type, station_name, station_points, user_points) -> Literal["""Ты посетил { $type -&gt;
[star] одну из особых точке
*[unstar] одну из точек
}: &#34;{ $station_name }&#34;
Ты получил { $station_points } балла. Теперь у тебя их: { $user_points }!"""]: ...

    @staticmethod
    def header(*, type) -> Literal["""{ $type -&gt;
[star] Особые
*[unstar] Обычные
} точки:"""]: ...

    @staticmethod
    def name(*, station) -> Literal["""{ $station -&gt;
[neigri] Неигры
[kubes] Кубики для умников
[melody] Угадай мелодию
[limbo] Лимбо
[gadalka] Гадалка
[QR] Лимонный квиз
[KKO] ККО
[rubius] Rubius
[jenga] Дженга
[sport] Спорт
[twister] Твистер
[PS] PS5
[grim] Аквагрим
[kicker] Киккер
[drawing] Мелки
[lemonade_pong] Лимонад-понг
[ball] Мяч в клетке
[photozone] Фотозона
[biser] Бисер
[tatoo] Тату от STK Tattoo studio
[vr] Вирутальная реальность
[quiz] Квиз, плиз! от ККО
[electrosheme] Электроcхемы
[djaing] Диджеинг
*[other] этого не должно тут быть...
}"""]: ...

    @staticmethod
    def description(*, station) -> Literal["""{ $station -&gt;
[neigri] любишь играть? Тогда как на счёт понеиграть!
[kubes] это кубики для умников! ТО ЕСТЬ ДЛЯ ТЕБЯ
[melody] звенит ярская вьюга... Сможешь отгадать мелодию?
[limbo] проверь себя на падкость... и на гибкость!
[gadalka] ты право имеешь или перед сессией дрожишь?
[rubius] IT квиз, задачки на логику и мерч от Rubius, заходи!
[QR] как сказал его создатель: &#34;Там будет про лимоны, Томск и Политех&#34;
[KKO] проверь себя на головоломках, ребусах и вопросах на эрудицию
[ball] покажи умения работать в команде и достань мяч!
[jenga] попробуй сыграть в большую дженгу, будет весело!
[sport] покажи всем свою физическую подготовку!
[twister] покажи всем самые эксроординарные позы!
[PS] признаяся, что сразу захотел пойти именно сюда
[grim] все мы когда-то хотели выглядеть как супергерои
[kicker] сразись в настольный футбол!
[melki] вспомни детсво и разукрась весь асфальт мелками!
[lemonade_pong] такая знакомая игра... Проверь свою точность!
[photozone] сделай топовые фото для соцсетей прямо на нашем фестивале и участвуй в конкурсе!
[biser] сплети себе брелок с лимоном на память!
[tatoo] всегда хотелось сделать тату, но было страшно? Попробуй на лимоне!
[vr] хочешь побывать по ту сторону экрана?
[quiz] как хорошо ты помнишь школьную программу?
[electrosheme] узнай, как работают электросхемы!
[djaing] почувствуй себя в роли диджея, тебе понравится!
*[other] этого тут быть не должно...
}"""]: ...


class Wrong:
    code: WrongCode


class WrongCode:
    @staticmethod
    def message() -> Literal["""Это неверный код 🧐 Уточни его у организатора точки"""]: ...


class StartCommand:
    @staticmethod
    def request() -> Literal["""Похоже ты уже пользовался этим ботом раньше.
Но времена меняются, для корректной работы бота введи команду /start"""]: ...


class Undone:
    @staticmethod
    def station(*, type, station_name, description) -> Literal["""{ $type -&gt;
[star] ⭐️
*[unstar] 👉
} { $station_name } - { $description }"""]: ...


class Done:
    @staticmethod
    def station(*, station_name, description) -> Literal["""✅ { $station_name } - { $description }"""]: ...

