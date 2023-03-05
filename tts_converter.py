import asyncio
import io
import itertools
import re
import time

import edge_tts


class TtsConverter:
    REPEAT_REQUEST_COUNT = 100
    BUFFER_SIZE = 20
    FIRST_STRINGS_LENGTH = 500
    LAST_STRINGS_LENGTH = 2000
    VOICE = 'ru-RU-SvetlanaNeural'
    VOICE_RATE = "+0%"
    VOICE_VOLUME = "+0%"
    TEXT = None

    def __init__(self, data):
        if not data['text']:
            raise Exception("Text parameter is important!")
        self.TEXT = data['text']
        if data['repeat_request_count']:
            self.REPEAT_REQUEST_COUNT = data['repeat_request_count']
        if data['buffer_size']:
            self.BUFFER_SIZE = data['buffer_size']
        if data['first_strings_len']:
            self.FIRST_STRINGS_LENGTH = data['first_strings_len']
        if data['last_strings_len']:
            self.LAST_STRINGS_LENGTH = data['last_strings_len']
        if data['voice']:
            self.VOICE = data['voice']
        if data['voice_rate']:
            self.VOICE_RATE = data['voice_rate']
        if data['voice_volume']:
            self.VOICE_VOLUME = data['voice_volume']

    async def foo(self):
        # text = self.get_text()
        splited = self.prepare_splited_text(self.TEXT)
        array_of_sentences = self.get_splited_sentences(splited, self.BUFFER_SIZE)
        all_mp3_parts = await self.run_it_with_buffer(array_of_sentences)
        # self.write_to_file(all_mp3_parts)
        return self.prepare_mp3_data(all_mp3_parts)

    def split_text(self, text):
        substrings = re.split(r'([:;\-,.!?])(?:\s+|\n)', text)
        return ["".join(substrings[i:i + 2]) for i in range(0, len(substrings), 2)]

    async def run_it_with_buffer(self, sentences):
        result = []
        sum_time = 0
        for buffer_index, buffered_sentences in enumerate(sentences):
            start_time = time.time()

            ext_num = buffer_index * self.BUFFER_SIZE
            mp3_parts = await self.tts_all(buffered_sentences, ext_num)
            result.append(mp3_parts)

            with open(f"test/test_{buffer_index + 1}.mp3", "wb") as f:
                for mp3_index, mp3_part in enumerate(mp3_parts):
                    for key, val in mp3_part.items():
                        f.write(val)

            end_time = time.time()
            execution_time = end_time - start_time
            sum_time = sum_time + execution_time
            print(f"{buffer_index + 1}/{len(sentences)} completed by {execution_time}")
        print(f"all converted by {sum_time}")
        return result

    def get_splited_sentences(self, sentences, count):
        return [sentences[i:i + count] for i in range(0, len(sentences), count)]

    def prepare_splited_text(self, text):
        if len(text) < self.FIRST_STRINGS_LENGTH:
            return [text]
        parts = self.split_text(text)
        first_part = self.strip_strings(parts, self.FIRST_STRINGS_LENGTH, self.BUFFER_SIZE)
        last_part = self.strip_strings(parts[first_part['last_word_index'] + 1:], self.LAST_STRINGS_LENGTH)
        return [*first_part['result'], *last_part['result']]

    def strip_strings(self, words, strings_len, buffer_size=None):
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

    async def tts_all(self, sentences, ext_num):
        tasks = [self.tts_one(index + ext_num, sentence) for index, sentence in enumerate(sentences)]
        return await asyncio.gather(*tasks)

    async def tts_one(self, index, text):
        print(f"th{index + 1} started")
        audio_bytes = None
        for repeat_num in range(0, self.REPEAT_REQUEST_COUNT):
            repeat_str = f"repeat{repeat_num} "
            try:
                communicate = edge_tts.Communicate(text, voice=self.VOICE, rate=self.VOICE_RATE, volume=self.VOICE_VOLUME)
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
                if repeat_num + 1 == self.REPEAT_REQUEST_COUNT:
                    raise ex
                time.sleep(1)
        return {index: audio_bytes}

    def write_to_file(self, mp3_parts):
        mp3_parts = list(itertools.chain.from_iterable(mp3_parts))
        result_data = dict(item for dict_ in mp3_parts for item in dict_.items())
        with open("testFull.mp3", "wb") as f:
            for index in range(0, len(mp3_parts)):
                f.write(result_data[index])

    def prepare_mp3_data(self, mp3_parts):
        mp3_parts = list(itertools.chain.from_iterable(mp3_parts))
        result_data = dict(item for dict_ in mp3_parts for item in dict_.items())
        return b"".join(result_data.values())

    def get_text(self):
        with open('text.txt', 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    async def test_it(self, text):
        communicate = edge_tts.Communicate(text, voice=self.VOICE, rate=self.VOICE_RATE, volume=self.VOICE_VOLUME)
        bytes_io = io.BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                bytes_io.write(chunk["data"])
        audio_bytes = bytes_io.getvalue()
        return audio_bytes

    def convert(self):
        return asyncio.run(self.foo())
