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
    client = OpenAI(api_key='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')

    response = client.chat.completions.create(
      model="gpt-4",
      messages=[
        {
          "role": "system",
          "content": "Жарнама сөздік синтезін жаса, Hyunday авто көлігі негізінде"
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
    client = OpenAI(api_key='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')

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









