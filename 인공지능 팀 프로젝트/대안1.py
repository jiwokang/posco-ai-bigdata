#!/usr/bin/env python
# coding: utf-8

# # 1. text to speech

# In[53]:


import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound

#def speak(text):
#     tts = gTTS(text = text, lang = 'ko')
#     filename = 'voice1.mp3'
#     tts.save(filename)
#     playsound.playsound(filename)

# speak('물건을 구매 하시겠습니까?')


# # 2. speech to text

# ## 주스 찾는 문장

# In[1]:


import speech_recognition as sr
from gtts import gTTS
import os
import time
import playsound


# speech to text
def speak(text):
    tts = gTTS(text = text, lang = 'ko')
    filename = 'voice1.mp3'
    tts.save(filename)
    playsound.playsound(filename)

# text to speech

def listen():
    with sr.Microphone() as source:
        print('말씀하세요')
        audio_text = r.listen(source, phrase_time_limit = 3)
        
        try:
            recog_text = r.recognize_google(audio_text, language = 'ko-KR')
            #using google speech recognition
            print('Text'+recog_text)
            
            # 물건 위치 물어보는 문장
            find_word = ['커피 어디야', '커피 어디 있어', '커피 위치 알려줘', '커피 어디 있는지 알고 싶어']
            find_word2 = ['마스크 어디야', '마스크 어디 있어', '마스크 위치 알려줘', '마스크 어디 있는지 알고 싶어']
            
            
            if recog_text in find_word:
                speak('커피 위치는 A3 구역 입니다.')
            
            elif recog_text in find_word2:
                speak('마스크 위치는 A1 구역 입니다.')
            
            # 인식을 못했거나 지정되지 않은 물건을 물어볼 경우 '다시 말씀해 주세요'라고 말한 후 다시 들음
            else:
                speak('다시 말씀해주세요')
                listen()
                
        except:
            speak('말씀하지 않았습니다.')
            listen()

r = sr.Recognizer()
speak('말씀하세요.')
listen()

