from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    start: Start
    infocard: Infocard
    wheretogo: Wheretogo
    statistics: Statistics
    star: Star
    superstar: Superstar
    unexpected: Unexpected
    help: Help
    lottery: Lottery
    programma: Programma
    doubled: Doubled
    station: Station
    wrong: Wrong
    undone: Undone
    done: Done


class Start:
    command: StartCommand

    @staticmethod
    def message(*, lottery) -> Literal["""Хей, привет! 👋
Ты пришёл на главное событие этой весны - Лимонад Пати!🍋 Тебя ждёт много интересных точек, море лимонада, веселья и куча классных призов!

Сегодня с 17:00 до 19:00 у нас работают интерактивные точки. За прохождение каждой из них можно получить баллы. Зарабатывай баллы и повышай свои шансы на выигрыш в лотерее, которая пройдёт в 19:00

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
    def message() -> Literal["""Точки в нашем квесте деляться на 2 категории:
⭐️ особые  -&gt; получаешь 3 балла
👉 обычные -&gt; получаешь 1 балл

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
Проходи интерактивные точки и вводи мне числа, которые тебе скажут организаторы.

Если не знаешь, куда сходить и какие точки ещё пройти, нажми на &#34;Куда сходить?&#34;

Если не можешь найти какую-то точку, воспользуйся кнопкой &#34;Карта&#34;

Если хочешь узнать набранные баллы или забыл номер лотерейного билета, жми &#34;Моя статистика&#34;

Узнать программу Лимонад Пати ты можешь, нажав на кнопку &#34;Программа мероприятия&#34;

Кнопка &#34;Помощь&#34; покажет тебе это сообщение
Если есть вопросы, на которые я не смог ответить, обратить с организаторам. Это ребята с бейджиками!"""]: ...

    @staticmethod
    def button() -> Literal["""🆘 Помощь"""]: ...


class Lottery:
    @staticmethod
    def message(*, lottery, points) -> Literal["""Номер твоего лотерейного билета { $lottery }, баллы: { $points }

Каждый, кто пройдёт все точки, гарантированно получает приз: бутылку лимонада.
Среди набравших максимальное количество баллов пройдёт розыгрыш лучшего набора мерча ТПУ.
В завершение нашей тусовки пройдёт розыгрыш среди всех участников QR-квеста через Лототрон
Три лучших фотографии нашего фестиваля получат персональный подарок от Дона Лимона. Открывай профиль, делай фото и выкладывай на свою страницу ВК с хэштегом #ЛимонадПати2023"""]: ...

    @staticmethod
    def button() -> Literal["""🥰 Розыгрыш"""]: ...


class Programma:
    @staticmethod
    def message() -> Literal["""Чтобы не пропустить всё самое интересное, лови расписание нашего дня: ⏰

🕔 17:00-19:00
Интерактивные точки, выдача лимонада и квест

🕖 19:00
Выступление музыкантов и певцов от творческих объединений МКЦ

🕗 20:00
Зажигательный сет от нашего ди-джея и розыгрыши от ведущих

🕤 21:40
Розыгрыш &#34;Лототрон&#34;"""]: ...

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
Ты получил { $station_points } балла. Итого у тебя их: { $user_points }!"""]: ...

    @staticmethod
    def header(*, type) -> Literal["""{ $type -&gt;
[star] Особые
*[unstar] Обычные
} точки:"""]: ...

    @staticmethod
    def name(*, station) -> Literal["""{ $station -&gt;
[rubius] Rubius
[jenga] Дженга
[sport] Спорт
[kicker] Киккер
[drawing] Мелки
[lemonade_pong] Лимонад-понг
[ball] Мяч в клетке
[photozone] Фотозона
[biser] Бисер
[tatoo] Тату от STK Tattoo studio
[virtual_reality] Вирутальная реальность
[quiz] Квиз, плиз! от ККО
[electrosheme] Электроcхемы
[djaing] Диджеинг
*[other] этого не должно тут быть...
}"""]: ...

    @staticmethod
    def description(*, station) -> Literal["""{ $station -&gt;
[rubius] IT квиз, задачки на логику и мерч от Rubius, заходи!
[ball] покажи умения работать в команде и достань мяч!
[jenga] попробуй сыграть в большую дженгу, будет весело!
[sport] покажи всем свою физическую подготовку!
[kicker] сразись в настольный футбол!
[drawing] вспомни детсво и разукрась весь асфальт мелками!
[lemonade_pong] такая знакомая игра... Проверь свою точность!
[photozone] сделай топовые фото для соцсетей прямо на нашем фестивале и участвуй в конкурсе!
[biser] сплети себе брелок с лимоном на память!
[tatoo] всегда хотелось сделать тату, но было страшно? Попробуй на лимоне!
[virtual_reality] хочешь побывать по ту сторону экрана?
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

