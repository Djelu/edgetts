import asyncio
import io
import re
import numpy as np
import math
import time
import edge_tts
import itertools
import proxy_service


async def foo(buffer_size):
    text = get_text()
    all_sentences = re.split('[.!?]', text)
    array_of_sentences = get_splited_sentences(all_sentences, buffer_size)
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

        end_time = time.time()
        execution_time = end_time - start_time
        sum_time = sum_time + execution_time
        print(f"{buffer_index+1}/{len(sentences)} completed by {execution_time}")
    print(f"all converted by {sum_time}")
    return result


def get_splited_sentences(sentences, count):
    # counts_in_one_part = math.ceil(len(sentences) / count)
    return [sentences[i:i + count] for i in range(0, len(sentences), count)]


async def tts_all(sentences, ext_num):
    tasks = [tts_one(index+ext_num, sentence) for index, sentence in enumerate(sentences)]
    return await asyncio.gather(*tasks)


async def tts_one(index, sentences):
    print(f"th{index+1} started")
    text = " ".join(sentences)
    communicate = edge_tts.Communicate(text, 'ru-RU-SvetlanaNeural')
    bytes_io = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            bytes_io.write(chunk["data"])
    audio_bytes = bytes_io.getvalue()
    with open(f"test/test_{index+1}.mp3", "wb") as f:
        f.write(audio_bytes)
    with open(f"test/test_{index + 1}.txt", "wb") as f:
        f.write(text.encode("utf-8"))
    print(f"th{index + 1} completed")
    return {index: audio_bytes}


def write_to_file(mp3_parts):
    mp3_parts = list(itertools.chain.from_iterable(mp3_parts))
    result_data = dict(item for dict_ in mp3_parts for item in dict_.items())
    with open("testFull.mp3", "wb") as f:
        for index in range(0, len(mp3_parts)):
            f.write(result_data[index])


def get_text():
    with open('text.txt', 'r', encoding='utf-8') as file:
        text = file.read()
    return text


if __name__ == '__main__':
    # asyncio.run(foo(20))
    proxies = proxy_service.get_proxy_info(100)
    i = 0
