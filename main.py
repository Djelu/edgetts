import asyncio
import io
import itertools
import re
import time
from faker import Faker
import edge_tts

REPEAT_REQUEST_COUNT = 10


async def foo(buffer_size):
    text = get_text()
    # text = get_fake_text(111111)
    # start_time = time.time()
    splited = prepare_splited_text(text, buffer_size, 1000, 2000)
    # res = list(map(lambda str: {'len': len(str), 'text': str}, splited))
    # mp3 = await tts_one(0, text)

    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(f"time = {execution_time}")

    # mp3 = mp3[0]
    # with open("testText.mp3", "wb") as f:
    #     f.write(mp3)
    # all_sentences = re.split('[.!?]', text)
    array_of_sentences = get_splited_sentences(splited, buffer_size)
    all_mp3_parts = await run_it_with_buffer(array_of_sentences, buffer_size)
    write_to_file(all_mp3_parts)
    i = 0


async def run_it_with_buffer(sentences, buffer_size):
    result = []
    sum_time = 0
    for buffer_index, buffered_sentences in enumerate(sentences):
        start_time = time.time()

        ext_num = buffer_index * buffer_size
        mp3_parts = await tts_all(buffered_sentences, ext_num)
        result.append(mp3_parts)


        with open(f"test/test_{buffer_index+1}.mp3", "wb") as f:
            for mp3_index, mp3_part in enumerate(mp3_parts):
                for key, val in mp3_part.items():
                    f.write(val)

        end_time = time.time()
        execution_time = end_time - start_time
        sum_time = sum_time + execution_time
        print(f"{buffer_index + 1}/{len(sentences)} completed by {execution_time}")
    print(f"all converted by {sum_time}")
    return result


def get_splited_sentences(sentences, count):
    return [sentences[i:i + count] for i in range(0, len(sentences), count)]


def prepare_splited_text(text, buffer_size, first_strings_len, last_strings_len):
    words = text.split(" ")
    first_part = strip_strings(words, first_strings_len, buffer_size)
    last_part = strip_strings(words[first_part['last_word_index'] + 1:], last_strings_len)
    return [*first_part['result'], *last_part['result']]


def strip_strings(words, strings_len, buffer_size=None):
    result = []
    s = ""
    last_word_index = 0
    for index, word in enumerate(words):
        s += word + " "
        if len(s) > strings_len:
            result.append(s.strip())
            if buffer_size is None or len(result) < buffer_size:
                s = ""
            else:
                last_word_index = index
                break
    return {'result': result, 'last_word_index': last_word_index}


async def tts_all(sentences, ext_num):
    tasks = [tts_one(index + ext_num, sentence) for index, sentence in enumerate(sentences)]
    return await asyncio.gather(*tasks)


async def tts_one(index, text):
    print(f"th{index + 1} started")
    audio_bytes = None
    for repeat_num in range(0, REPEAT_REQUEST_COUNT):
        repeat_str = f"repeat{repeat_num} "
        try:
            communicate = edge_tts.Communicate(text, 'ru-RU-SvetlanaNeural', rate="+100%")
            bytes_io = io.BytesIO()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    bytes_io.write(chunk["data"])
            audio_bytes = bytes_io.getvalue()
            # with open(f"test/test_{index+1}.mp3", "wb") as f:
            #     f.write(audio_bytes)
            # with open(f"test/test_{index + 1}.txt", "wb") as f:
            #     f.write(text.encode("utf-8"))
            print(f"{repeat_str}th{index + 1} completed")
            break
        except Exception as ex:
            print(f"{repeat_str}th{index + 1}={ex}")
            if repeat_num+1 == REPEAT_REQUEST_COUNT:
                raise ex
            time.sleep(1)
    return {index: audio_bytes}


def write_to_file(mp3_parts):
    mp3_parts = list(itertools.chain.from_iterable(mp3_parts))
    result_data = dict(item for dict_ in mp3_parts for item in dict_.items())
    with open("testFull.mp3", "wb") as f:
        for index in range(0, len(mp3_parts)):
            f.write(result_data[index])


def get_text():
    with open('textFull.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    return text


def get_fake_text(length):
    faker = Faker('ru_RU')
    return faker.text(max_nb_chars=length)


async def test_it(text):
    communicate = edge_tts.Communicate(text, 'ru-RU-SvetlanaNeural', rate="+100%")
    bytes_io = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            bytes_io.write(chunk["data"])
    audio_bytes = bytes_io.getvalue()
    return audio_bytes


if __name__ == '__main__':
    asyncio.run(foo(20))
    # asyncio.run(test_it(get_text()))
    i = 0
