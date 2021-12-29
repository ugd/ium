import speech_recognition as sr

r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        print('say something')
        audio = r.listen(source)
        print('sample width ',audio.sample_width)
        print('frame data type ',type(audio.frame_data))    #type = bytes. need convert bytes-to-idk...list? FML
        print('sample rate ',audio.sample_rate)
        try:
            voice_data = r.recognize_google(audio, language="en-US", show_all=False)
        except:
            print("except")
            continue    #to avoid stopping the program if the voice data has not been recognized as a valid utterance
        print(voice_data)