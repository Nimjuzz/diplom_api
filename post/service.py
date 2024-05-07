from openai import OpenAI

def preprocess_text(text):
    # Приведение текста к нижнему регистру
    text = text.lower()
    # Удаление знаков препинания
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for char in punctuation:
        text = text.replace(char, ' ')
    return text

def tokenize_text(text):
    # Разбиение текста на токены (слова)
    words = text.split()
    return words

def count_word_frequencies(words):
    # Подсчет частоты встречаемости каждого слова
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts

def compute_word_scores(word_counts, max_freq):
    # Вычисление веса слов на основе их частоты встречаемости
    word_scores = {}
    for word, freq in word_counts.items():
        # Простой способ нормализации частоты
        word_scores[word] = freq / max_freq
    return word_scores

def score_sentences(sentences, word_scores):
    # Оценка предложений на основе весов ключевых слов
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        sentence_scores[i] = 0
        for word in sentence:
            if word in word_scores:
                sentence_scores[i] += word_scores[word]
    return sentence_scores

def find_keywords(text, top_n=5):
    # Предобработка текста
    processed_text = preprocess_text(text)
    # Токенизация текста
    words = tokenize_text(processed_text)
    # Подсчет частоты встречаемости слов
    word_counts = count_word_frequencies(words)
    # Определение максимальной частоты слова
    max_freq = max(word_counts.values())
    # Вычисление весов слов
    word_scores = compute_word_scores(word_counts, max_freq)
    # Разбиение текста на предложения
    sentences = processed_text.split('.')
    # Токенизация предложений
    tokenized_sentences = [tokenize_text(sentence) for sentence in sentences]
    # Оценка предложений
    sentence_scores = score_sentences(tokenized_sentences, word_scores)
    # Сортировка предложений по оценке
    sorted_sentence_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    # Получение ключевых предложений
    top_sentences_indices = [index for index, _ in sorted_sentence_scores[:top_n]]
    # Сбор ключевых слов из ключевых предложений
    top_keywords = set()
    for index in top_sentences_indices:
        top_keywords.update(tokenized_sentences[index])
    return list(top_keywords)



def get_keywords(text):
    client = OpenAI(api_key='sk-proj-T2Q2Ru23L2XpeZUqertzT3BlbkFJBH258BZxRjOvA0yIe7vD')

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": """
            Ответ на вопрос используя ниже указанные данные.
            Что такое FX?
            Оценка "FX" - выставляется, когда итоговая оценка по дисциплине
            находится в пределах 25-49. Обучающийся, получивший оценку ""FX"",
            имеет право на повторную пересдачу.

            Чтобы сдать экзамен FX вы можете нажимать кнопку FX order на портале, где портал попросит деньги.

            Сдача FX стоит 1 ECTS

            Если вы пропустите FX, вы повторно будете изучать данный предмет в
            летнем семестре.

            Если портал закрылся, а преподаваетель забыл поставить FX, то преподаватель пишет заявление в деканат. Вопрос рассматривается на
            собрании, после чего портал снова откроется для преподавателя.

            Что такое пререквизиты?
            Пререквизиты - это дисциплины, предшествующие изучению данной дисциплины.
            В какой период можно сделать drop?
            Drop (отказ от тех или иных дисциплин с вашего расписания) дисциплин при регистрации на портале - бесплатна. На 5-10 неделе вы платите
            50% от полной стоимости предмета, на 10-15 неделе 100% сумму.
            Ретейк мы считаем по кредитам или же по ects?
            По современной кредитной технологии расчет за ретейк рассчитывается по ECTS.
            Летний семестр по академическому календарю начинается в начале июня. Студент
            учится 5 недель, экзамен сдает на 6-7 неделе.
            Формат экзамена решается деканатом, онлайн либо оффлайн формат.
            Все курсы летнего семестра платные.
            По внутренним правилам нашего вуза скидки на пересдачу предметов не
            предусмотрены. Деньги за ретейк должны быть оплачены до открытия регистрации на портале.
            Если нужный вам предмет не открыли на летний семестр, вы можете закрыть его в течении следующего учебного года.
            Если вы пропустили сдачу , заплатив за Ретейк, ваши деньги
            сгорят. В течение учебного года вы можете получить
            повторный предмет.

            Если у студента есть деньги на счету, он может взять ретейк курсы. Оплату делает
            так же как и за обучение. В СДУ есть возможность оплатить ретейк в рассрочку.

            Диплом можно защитить по окончании зимнего экзамена на 5 и более курсе. В летнем семестре, если вы закрываете ретейки, а диссертация не готова, студент обращается в деканат.

            В нашем университете можно ли сдать Upgrade
            предмета? Если да сколько он будет стоит?
            Upgrade - это услуга по повторному изучению дисциплин, производится
            только при условии, что повторный предмет не превышает установленной доли
            (квоты) в текущем семестре и в случае отсутствия противоречий в расписании
            занятий и при наличии разрешения заведующего кафедрой, на которую обучается
            абитуриент.
            При Upgrade выставляется последняя оценка, даже если это ремейк.
            Если вы берете Upgrade необходимо будет полностью проходить весь курс.

            Оплату вы определяете в отделе бухгалтерии.

            Чтобы взять Upgrade (услуга по повторному изучению дисциплин) вы можете написать заявление на
            почту ssc@sdu.edu.kz
            Если восстановил стипендию в этом семестре, с какого месяца она
            начнет поступать?
            Распределение стипендий производится по результатам сессии. Для 1 курса IBAN счет
            открывается со стороны университета и необходимо дождаться информацию для
            получения банковской карты.
            Обучающийся может восстановить стипендию, закрыв последующий семестр (весенний/осенниий) или летний
            семестры на 70 баллов и выше.
            Если вы восстановили стипендию в осеннем семестре, то выплаты будут поступать с февраля.
            если восстановили в весеннем семестре, то выплаты будут поступать с сентября.

            Назначение государственных стипендий прекращается в следующем случае:
            1. В конце семестра если ваш балл ниже С+, ваша стипендия будет потеряна;
            2. В случае отчисления (исключения) обучающегося из организации образования,
            независимо от причин отчисления (исключения);
            3. В случае смерти обучающегося;
            4. После завершения учебы обучающимся со дня выхода приказа о выпуске.

            Для получения повышенной государственной стипендии необходимо закрыть все предметы на "отлично" (90 и более баллов), вы автоматически будете добавлены в список студентов, получающих повышенную стипендию из базы данных.

            Ежегодно ВУЗ запрашивает необходимые данные студентов для самостоятельного
            открытия счета совместно с Народным Банком.

            что такое дорожка?
            Дорожные выплаты - это компенсация на проезд, студентам, учащимся по государственному образовательному заказу: студентам организаций высшего и послевузовского образования, магистрантам два раза в год, в период зимних и летних каникул в размере 4-х кратного месячного расчетного показателя (МРП);учащимся льготы на проезды на транспорте (проездные). Дорожная выплата производится независимо от результатов сессии. То есть даже если вы лишились стипендии, дорожные выплаты вам все равно будут поступать.

            Какие требования чтобы получить красный диплом?
            Требования для получения красного диплома:
             - Оценка «отлично»: А-(90-95 баллов), А (95-100 баллов) за все государственные экзамены и дипломную работу/проект.
            - Студенту, сдавшему экзамены и дифференцированные зачеты с оценками А, А- «отлично», В-, В, В+ «хорошо» и имеющему средний балл успеваемости (GPA) за весь период обучения не ниже 3.5, а также сдавшему все государственные экзамены и защитившему дипломную работу (проект) с оценками А, А- «отлично».

            Где посмотреть программу обучения?
            Чтобы посмотреть программу обучения зайдите во внутреннюю систему программ университета PMS портальная система – > Curriculum.
            Все изменения связанные с программой обучения будут сразу отображены в портале.
            На факультете студент не участвует в разработке ОП, заместитель декана по административным делам выступает от имени студентов.

            Куда обращаться если вовремя регистрационной недели не могу составить расписание из-за пересечения нужных уроков,а адвайзер не знает ответа?
            Регистрация на курс в любом семестре осуществляется на усмотрение студента по кредитной технологии. Только у студента не должна быть накладка в расписаний.
            Если во время регистрационной недели вы не можете составить расписание из-за пересечения нужных уроков, нехватки мест на определенную дисциплину (квот), то попробуйте обратиться к вашему куратору(эдвайзеру).

            Если вы нажали на конфирм, и только потом узнал о смене расписания, то обратитесь в деканат. Учебные вопросы рассматриваются деканатом. Студент пишет заявление на имя декана, после чего формируется комиссия для рассмотрения. Затем ознакомят решением студента.

            По внутренним правилам университета студент не может закрыть предмет, участвуя в Олимпиаде. Только в тот период времени, когда вы отправитесь на Олимпиаду, вас освободят из деканата.

            Как взять академический отпуск? Кому он дается? Кому нужно обратиться и какие документы нужны? Можно ли брать платникам?
            Студент грантник может получить академический отпуск по состоянию здоровья, по рождению ребенка или же с призывом в армию. Студент обучающиеся на платной основе может получить академический перерыв. В обеих случаях нужно написать заявление в студенческом отделе.

            Что можно сделать если я не согласен с поставленной оценкой преподавателя?
            Если вы не согласны с поставленной оценкой преподавателя, вы можете падать на аппеляцию. Комиссия формируется факультетом.

            Если между студентом и преподавателем произошел конфликт или недопонимание, студент может написать заявление на преподавателя в деканате. Заявление декан рассматривает на собрании.

            Если преподаватель навязывает свою точку зрения вне рамок академической границы студент имеет право написать заявление декану.

            Если вы хотите написать заявление в деканат, вы можете получить образец заявления от секретаря деканата и описать возникшую проблему.

            Можно ли сменить профессию и остаться на гранте?
            Если вы хотите сменить специальность и остаться на государственном гранте, то обе специальности должны быть одной квалификации. Перевод можно сделать во время летних и зимних каникул.

            Если я хочу отчислиться какие документы нужны? Куда мне обратиться?
            Для того чтобы отчислиться вам необходимо заполнить QR форму «Оқудан шығу», прикрепленную на сайте.
            Процесс идет онлайн. После выхода приказа, студент может забрать документы в студенческом отделе.


            """
        },
        {
          "role": "user",
          "content": text
        }
      ],
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    result = ''
    if response and response.choices:
        first_choice = response.choices[0]

        if first_choice.message and first_choice.message.content:
            result = first_choice.message.content
    return result



def get_keyword_val(text):
    client = OpenAI(api_key='sk-proj-T2Q2Ru23L2XpeZUqertzT3BlbkFJBH258BZxRjOvA0yIe7vD')

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": "Сөздің мағынасын, қысқаша түсіндір, Hyunday авто көлігі негізінде"
        },
        {
          "role": "user",
          "content": text
        }
      ],
      temperature=1,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    result = ''
    if response and response.choices:
        first_choice = response.choices[0]

        if first_choice.message and first_choice.message.content:
            result = first_choice.message.content

    return result


def extract_sentences(text):
    # Разбиение текста на предложения
    sentences = text.split('.')
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def get_context_words(sentence, keyword, window_size=2):
    # Получение контекстных слов вокруг ключевого слова в предложении
    words = sentence.split()
    keyword_index = words.index(keyword)
    start_index = max(0, keyword_index - window_size)
    end_index = min(len(words), keyword_index + window_size + 1)
    context_words = words[start_index:end_index]
    return context_words

def expand_keywords(keywords, text, window_size=2):
    # Расширение списка ключевых слов с учетом контекста
    expanded_keywords = set()
    sentences = extract_sentences(text)
    for keyword in keywords:
        for sentence in sentences:
            if keyword in sentence:
                context_words = get_context_words(sentence, keyword, window_size)
                expanded_keywords.update(context_words)
    return list(expanded_keywords)

def find_keywords(text, top_n=5, window_size=2):
    # Предобработка текста
    processed_text = preprocess_text(text)
    # Токенизация текста
    words = tokenize_text(processed_text)
    # Подсчет частоты встречаемости слов
    word_counts = count_word_frequencies(words)
    # Определение максимальной частоты слова
    max_freq = max(word_counts.values())
    # Вычисление весов слов
    word_scores = compute_word_scores(word_counts, max_freq)
    # Разбиение текста на предложения
    sentences = extract_sentences(processed_text)
    # Оценка предложений
    sentence_scores = score_sentences(sentences, word_scores)
    # Сортировка предложений по оценке
    sorted_sentence_scores = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)
    # Получение ключевых предложений
    top_sentences_indices = [index for index, _ in sorted_sentence_scores[:top_n]]
    # Извлечение ключевых слов из ключевых предложений с учетом контекста
    keywords = []
    for index in top_sentences_indices:
        sentence = sentences[index]
        sentence_keywords = [word for word in sentence.split() if word in word_scores]
        expanded_keywords = expand_keywords(sentence_keywords, text, window_size)
        keywords.extend(expanded_keywords)
    return list(set(keywords))[:top_n]









