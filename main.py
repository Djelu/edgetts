import asyncio
import io
import re
import numpy as np
import math
import time
import edge_tts
import itertools
import proxy_service
import http.client


VOICE = 'ru-RU-SvetlanaNeural'

async def foo(buffer_size):
    text = get_text()
    all_sentences = re.split('[.!?]', text)
    array_of_sentences = get_splited_sentences(all_sentences, buffer_size)
    all_mp3_parts = await run_it_with_proxy(array_of_sentences, buffer_size)
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


async def run_it_with_proxy(sentences, buffer_size):
    # result = []
    proxies = proxy_service.get_proxy_info()
    proxies = await get_just_working_proxies(proxies, buffer_size)
    i = 0
    # tasks = [tts_all(buffered_sentences, buffer_index * buffer_size, proxies, buffer_index) for buffer_index, buffered_sentences in enumerate(sentences)]
    # return await asyncio.gather(*tasks)
    # sum_time = 0
    # for buffer_index, buffered_sentences in enumerate(sentences):
    #     start_time = time.time()
    #
    #     ext_num = buffer_index * buffer_size
    #     mp3_parts = await tts_all(buffered_sentences, ext_num)
    #     result.append(mp3_parts)
    #
    #     end_time = time.time()
    #     execution_time = end_time - start_time
    #     sum_time = sum_time + execution_time
    #     print(f"{buffer_index+1}/{len(sentences)} completed by {execution_time}")
    # print(f"all converted by {sum_time}")
    # return result


async def get_just_working_proxies(proxies, buffer_size):
    result = []

    proxies = get_splited_sentences(proxies, buffer_size)
    # tasks = [check_all_proxy(buffered_proxies) for buffered_proxies in proxies]
    # result = await asyncio.gather(*tasks)
    i = 0
    # all_sum_time = 0
    for buffer_index, buffered_proxies in enumerate(proxies):
        buff_result = await check_all_proxy(buffered_proxies)
        result.append(buff_result)
        i = 0
    return result
    #     # sum_time = 0
    #     # err = None
    #     for proxies in buffered_proxies:
    #         check_all_proxy(proxies)
        # print(f"whole buffer time={sum_time}")
        # all_sum_time = all_sum_time + sum_time
    # print(f"all time={all_sum_time}")


async def check_all_proxy(proxies):
    tasks = [check_one_proxy(proxy) for proxy in proxies]
    return await asyncio.gather(*tasks)


async def check_one_proxy(proxy):
    test_text = "Тестовое предложение для проверки работы через прокси"
    result = True
    start_time = time.time()

    bytes_io = io.BytesIO()
    err = None
    print(f"try {proxy['address']}:{proxy['port']}")
    communicate = edge_tts.Communicate(test_text, VOICE, proxy=f"http://{proxy['address']}:{proxy['port']}")
    try:
        async for chunk in communicate.stream():
            bytes_io.write(chunk["data"])
    except Exception as ex:
        err = ex
        result = False

    end_time = time.time()
    execution_time = end_time - start_time

    if err is not None:
        print(f"{proxy['address']}:{proxy['port']} = не ок, time={execution_time}, err={err}")
    else:
        print(f"{proxy['address']}:{proxy['port']} = ок, time={execution_time}")
    return {"proxy": proxy, "result": result}


def get_splited_sentences(sentences, count):
    # counts_in_one_part = math.ceil(len(sentences) / count)
    return [sentences[i:i + count] for i in range(0, len(sentences), count)]


async def tts_all(sentences, ext_num, proxies, proxy_index):
    tasks = [tts_one(index+ext_num, sentence, proxies, proxy_index) for index, sentence in enumerate(sentences)]
    return await asyncio.gather(*tasks)


async def tts_one(index, sentence, proxies, proxy_index):
    print(f"th{index+1} started")
    # text = " ".join(sentence)

    # conn = http.client.HTTPSConnection(proxy.address, proxy.port)
    # conn.set_tunnel('westus.tts.speech.microsoft.com', headers={
    #     'Ocp-Apim-Subscription-Key': 'your-subscription-key',
    # })

    global stream, bytes_io
    k = 0
    try_another_proxy = True
    while try_another_proxy:
        proxy = proxies[proxy_index+k]
        print(f"try proxy{proxy_index+k} = {proxy}")
        bytes_io = io.BytesIO()
        communicate = edge_tts.Communicate(sentence, VOICE, proxy=f"http://{proxy['address']}:{proxy['port']}")
        try:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    bytes_io.write(chunk["data"])
            print(f"good proxy{proxy_index + k} = {proxy}")
            try_another_proxy = False
        except Exception:
            print(f"Ошибка {k} с proxy={proxy}")
            k = k + 1
            try_another_proxy = k < len(proxies)
    audio_bytes = bytes_io.getvalue()
    # with open(f"test/test_{index+1}.mp3", "wb") as f:
    #     f.write(audio_bytes)
    # with open(f"test/test_{index + 1}.txt", "wb") as f:
    #     f.write(text.encode("utf-8"))
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
    asyncio.run(foo(20))
    # asyncio.get_event_loop().run_until_complete(foo(20))
    i = 0
