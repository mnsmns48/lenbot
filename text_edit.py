import asyncio
import re


async def replacer(text: str) -> str:
    pattern_dict = {
        'нашей районной газете "Репортер Восточного Крыма"': 'нашему телеграм каналу',
        'нашей районной газете Репортер Восточного Крыма': 'нашему телеграм каналу',
        'Газета #РепортерВосточногоКрыма': 'Наш телеграм канал',
        'газете #РепортерВосточногоКрыма': 'нашему телеграм каналу',
        'газете РепортерВосточногоКрыма': 'нашему телеграм каналу',
        'а газета #РепортерВосточногоКрыма': ' наш телеграм канал',
        'газета #РепортерВосточногоКрыма': 'наш телеграм канал',
        'нашей районной газете': 'нашему телеграм каналу',
        'нашей газете': 'нашему телеграм каналу',
        'Репортер': '',
        '>': ' ',
        '<': ' ',
    }

    pattern = re.compile("|".join(re.escape(key) for key in pattern_dict))
    replaced_text = pattern.sub(lambda match: pattern_dict[match.group(0)], text).strip()

    vk_link_pattern_ = re.compile(r'\[{1}\w{10,20}\|{1}.+]{1}')
    find_vk_link = re.search(vk_link_pattern_, replaced_text)
    if find_vk_link:
        split_link_ = find_vk_link.group().split('|')
        replaced_text = re.sub(pattern=vk_link_pattern_,
                               repl=f"<a href='https://vk.com/{split_link_[0][1:]}'>{split_link_[1][:-1]}</a>",
                               string=replaced_text)

    pattern_1 = re.findall(r"([кКkK][аАaA@][кКkK])[\s]*(.+[КкkK][рРpP][ы][MMМм][aAАа@])", replaced_text)
    if pattern_1:
        pattern = re.compile(str(pattern_1[0][0]) + '.*?' + str(pattern_1[0][1]))
        response = re.search(pattern, replaced_text)
        replace_string = 'По информации, которую передали нашему телеграм каналу'
        replaced_text = replaced_text.replace(response.group(), replace_string)

    pattern_2 = re.findall(r"(печатной версии)", replaced_text)
    if pattern_2:
        pattern_index = text.index(pattern_2[-1])
        for i in range(pattern_index, 0, -1):
            if ((replaced_text[i] == 'П' or replaced_text[i] == 'О')
                    and (replaced_text[i - 1] == '\n' or replaced_text[i - 1] == ' ')):
                replaced_text = replaced_text[:i]
                break
    await asyncio.sleep(0.1)
    return replaced_text.replace(' ""', ' ')
