last-lp-message =
    Вижу, что ты ко мне прямиком с прошлого Лимонад Пати! Давай забудем это недоразумение, ведь на этот раз я работаю!

    Наслаждайся мероприятием ❤️

    Мы можем притворится, что не знакомы, если ты дашь команду /start, или можешь просто продолжить пользоваться мной 😉
start-message =
    Хей, привет! 👋
    Ты пришёл на главное событие этой весны - Лимонад Пати!🍋 Тебя ждёт много интересных точек, море лимонада, веселья и куча классных призов!

    Сегодня с 17:00 до 19:00 у нас работают интерактивные точки. За прохождение каждой из них можно получить баллы. Зарабатывай баллы и повышай свои шансы на выигрыш в лотерее, которая пройдёт в 21:15

    А как же лимонад? За прохождение точек каждому мы подарим бутылочку освежающего напитка от Дона Лимона 🥤

    Номер твоего лотерейного билета - {$lottery}

    Веселись! Вот тебе карта активностей
infocard-message =
    Карта поможет тебе сориентироваться на Лимонад Пати ❤️
    Лови👇
infocard-button =🍋 Карта
wheretogo-message =
    В нашем квесте всё просто. Получаешь особый код за прохождение особой точки, даёшь его мне - и получаешь 1 балл

    Проходи все особые точки и получай гарантированный приз 🎁
wheretogo-button =🎯 Куда пойти?
statistics-message =
    Твои очки: {$points}. Номер лотерейного билета: {$lottery}
statistics-button = 🤩 Моя статистика
star-message =
    🥳 Ура! Ты прошёл все особые точки! Теперь ты можешь получить заслуженный приз - лимонад и стикерпак ✨
    Подходи на точку "Раздатка"!
superstar-message =
    Молодец! Ты прошёл все точки и набрал максимум баллов! Оставайся с нами и следи за результатами розыгрыша, не забудь номер своего лотерейного билета! 🎰
    Его узнать ты можешь, нажав кнопку "Моя статистика"!
unexpected-message =
    Я тебя не понимаю 😢 Воспользуйся кнопкой "Помощь", чтобы узнать, что я могу
help-message =
    Я квест-бот Лимонад Пати!

    📍 Проходи интерактивные точки и вводи мне числа, которые тебе скажут организаторы.

    🎯 Если не знаешь, куда сходить и какие точки ещё пройти, нажми на "Куда сходить?"

    🍋 Если не можешь найти какую-то точку, воспользуйся кнопкой "Карта"

    🤩 Если хочешь узнать набранные баллы или забыл номер лотерейного билета, жми "Моя статистика"

    🔥 Узнать программу Лимонад Пати ты можешь, нажав на кнопку "Программа мероприятия"

    🆘 Кнопка "Помощь" покажет тебе это сообщение

    Если есть вопросы, на которые я не смог ответить, обратить с организаторам. Это ребята с бейджиками!
help-button =🆘 Помощь
lottery-message =
    Номер твоего лотерейного билета {$lottery}, баллы: {$points}

    📌 Каждый, кто пройдёт все точки, гарантированно получает приз: бутылку лимонада.

    📌 Среди набравших максимальное количество баллов пройдёт розыгрыш призов от наших партнёров.

    📌 Три лучших фотографии нашего фестиваля получат персональный подарок от Дона Лимона.
    Открывай профиль, делай фото и выкладывай на свою страницу ВК с хэштегом #LemonadeParty2024
lottery-button =🥰 Розыгрыш
programma-message =
    Чтобы не пропустить всё самое интересное, лови расписание нашего дня:

    🕔 17:00-19:00
    Интерактивные точки, выдача лимонада и квест

    🕖 19:00
    Выступление музыкантов и певцов от творческих объединений ТПУ и не только!

    🕤 21:15
    Розыгрыш, розыгрыш, розыгрыш и ещё розыгрыш
programma-button =🔥 Программа мероприятия
doubled-station = Верный код! Но ты уже проходил "{$station_name}"...
station-arrangement =
    Ты посетил {$type ->
        [star] одну из особых точке
        *[unstar] одну из точек
    }: "{$station_name}"
    Ты получил {$station_points} балла. Теперь у тебя их: {$user_points}!
wrong-code-message = Это неверный код 🧐 Уточни его у организатора точки
start-command-request =
    Похоже ты уже пользовался этим ботом раньше.
    Но времена меняются, для корректной работы бота введи команду /start
station-header =
    {$type ->
        [star] Особые
        *[unstar] Обычные
    } точки:
undone-station =
    {$type ->
        [star] ⭐️
        *[unstar] 👉
    } {$station_name} - {$description}
done-station = ✅ {$station_name} - {$description}
station-name =
    {$station ->
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
    }
station-description =
    {$station ->
        [neigri] любишь играть? Тогда как на счёт понеиграть!
        [kubes] это кубики для умников! ТО ЕСТЬ ДЛЯ ТЕБЯ
        [melody] звенит ярская вьюга... Сможешь отгадать мелодию?
        [limbo] проверь себя на падкость... и на гибкость!
        [gadalka] ты право имеешь или перед сессией дрожишь?
        [rubius] IT квиз, задачки на логику и мерч от Rubius, заходи!
        [QR] как сказал его создатель: "Там будет про лимоны, Томск и Политех"
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
    }
