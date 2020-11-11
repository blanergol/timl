import re


def break_lines(html_data_site):
    text_data_site = []

    for elem in html_data_site:
        text = elem.get("text")
        text = re.split("[.!?\n]", text)
        text_data_site.append({"url": elem.get("url"), "text": text})

    return text_data_site


def get_size_stat(text_data_site):
    stat_index = {}
    for index_text, text in enumerate(text_data_site):
        text = text.get("text")
        stat_index.update({index_text: {}})
        for index_sentence, sentence in enumerate(text):
            stat_index.get(index_text).update({index_sentence: 0})
    return stat_index


def find_query(text_data_site, main_par):
    query = main_par.get("query").split(" ")
    for i, elem_query in enumerate(query):
        if len(elem_query) < 3:
            query.pop(i)

    stat_index = get_size_stat(text_data_site)

    for index_text, text in enumerate(text_data_site):
        text = text.get("text")
        for index_sentence, sentence in enumerate(text):
            for q in query:
                q = re.compile(q)
                result = q.findall(sentence)
                if len(result) > 0:
                    count = len(result)
                    weight = stat_index.get(index_text)
                    weight = weight.get(index_sentence)
                    weight = weight + count
                    stat_index[index_text][index_sentence] = weight

    return stat_index


def research_find_query(stat_index):

    stat_index_result = {}

    for index_text in stat_index:
        stat_index_result.update({index_text: {}})
        tmp_text = stat_index.get(index_text)
        for index_sentence in tmp_text:
            tmp_sentence = tmp_text.get(index_sentence)
            if tmp_sentence != 0:
                stat_index_result[index_text].update(
                    {index_sentence: tmp_text[index_sentence]}
                )

    return stat_index_result


def sort_find_query(stat_index_result):

    sort_stat_index = {}

    for index_text in stat_index_result:
        tmp = sorted(
            stat_index_result[index_text].items(), key=lambda x: x[1], reverse=True
        )
        sort_stat_index.update({index_text: tmp})

    return sort_stat_index


def depth_find_query(sort_stat_index, main_par):

    sort_stat_index_result = {}

    for index_text in sort_stat_index:
        sort_stat_index_result.update({index_text: {}})
        tmp = sort_stat_index[index_text]
        for index_sentence in tmp:
            sort_stat_index_result[index_text].update(
                {index_sentence[0]: index_sentence[1]}
            )
            if index_sentence[1] < 2:
                break

    return sort_stat_index_result


def get_text_index(sort_stat_index_result, lines_text):

    result_text = []
    text_tmp = ""

    for index_text, elem in enumerate(lines_text):
        index_sentence = sort_stat_index_result[index_text]
        for index in index_sentence:
            for index_elem_tmp, elem_tmp in enumerate(elem.get("text")):
                if index == index_elem_tmp:
                    text_tmp = text_tmp + elem_tmp
        result_text.append({"url": elem.get("url"), "text": text_tmp})
        text_tmp = ""

    return result_text
