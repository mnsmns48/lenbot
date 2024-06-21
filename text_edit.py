import asyncio
import re


async def replacer_v1(text: str) -> str:
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
        '>': ' ',
        '<': ' ',

    }
    pattern = re.compile("|".join(re.escape(key) for key in pattern_dict))
    replaced = pattern.sub(lambda match: pattern_dict[match.group(0)], text).strip()
    await asyncio.sleep(0.1)
    return replaced


async def replacer_v2(text: str) -> str:
    pattern_dict = {'>': ' ', '<': ' '}
    pattern = re.compile("|".join(re.escape(key) for key in pattern_dict))
    replaced_text = pattern.sub(lambda match: pattern_dict[match.group(0)], text).strip()

    pattern_1 = re.findall(r"([кКkK][аАaA@][кКkK])[\s]*(.+[КкkK][рРpP][ы][MMМм][aAАа@])", replaced_text)
    if pattern_1:
        print(pattern_1)
        pattern = re.compile(str(pattern_1[0][0]) + '.*?' + str(pattern_1[0][1]))
        response = re.search(pattern, replaced_text)
        replace_string = 'По информации, переданной нашему телеграм каналу'
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
    return replaced_text
