# -*- coding: utf-8 -*-
#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the streaming API.

NOTE: This module requires the additional dependency `pyaudio`. To install
using pip:

    pip install pyaudio

Example usage:
    python transcribe_streaming_mic.py
"""

# [START import_libraries]
from __future__ import division

import re
import sys

from google.cloud import speech

import pyaudio
from six.moves import queue
import win32com.client

# [END import_libraries]

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms
text = win32com.client.Dispatch('SAPI.SpVoice')

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,

            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]

cmdLists = [
        #명령어    대답    종료 리턴값
        [u'잘가',     '안녕히가세요',       0],
        [u'안녕 포스텍',       '무엇이 궁금하신가요',        1],
        [u'커피 어디 있어',     '커피는 A4 구역에 있습니다',   1],
        [u'커피 어디 있니',     '커피는 A4 구역에 있습니다',   1],
        [u'커피 어디 있는지 궁금해',     '커피는 A4 구역에 있습니다',   1],
        [u'고래밥 어디 있어',     '고래밥은 C1 구역에 있습니다',   1],
        [u'고래밥 어디 있니',     '고래밥은 C1 구역에 있습니다',   1],
        [u'고래밥 어디 있는지 궁금해',     '고래밥은 C1 구역에 있습니다',   1]]



"""
리턴이 0이면 종료
"""
def CommandProc(stt):
    # 문자 양쪽 공백 제거
    cmd = stt.strip()
    # 입력 받은 문자 화면에 표시
    print('나 : ' + str(cmd))

    for cmdList in cmdLists:
        if str(cmd) == cmdList[0]:
            #명령 리스트와 비교
            print ('포리 : ' + cmdList[1])
            text.Speak(cmdList[1])
            # 종료 명령 리턴 0이면 종료
            # 1이면 계속
            return cmdList[2]
        # 계속            
    print ('포리 : 다시 말씀해주세요')
    return 1
    
def listen_print_loop(responses):

    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # There could be multiple results in each response.
        result = response.results[0]
        if not result.alternatives:
            continue

        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            #### 추가 ### 화면에 인식 되는 동안 표시되는 부분.
            sys.stdout.write('나 : ')
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()
            num_chars_printed = len(transcript)

        else:
            #### 추가 ### 
            if CommandProc(transcript) == 0:
                break

            num_chars_printed = 0


def main():

    language_code = 'ko-KR'  # 한국어로 변경

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code)
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True)

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        # Now, put the transcription responses to use.
        listen_print_loop(responses)


if __name__ == '__main__':
    main()