def voicebot():
    import os

    import google.generativeai as genai
    import speech_recognition as sr
    from gtts import gTTS
    import pyttsx3

    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for i, voice in enumerate(voices):
            print(f"Voice {i}: {voice.name} ({voice.id})")
        engine.setProperty('rate', 140)
        engine.setProperty('volume', 1.0)
        for voice in voices:
            engine.setProperty('voice', voice.id)
            print(f"Testing voice: {voice.name}")
            engine.say(text)
            engine.runAndWait()
            break

    def voice():

        # Initialize recognizer
        r = sr.Recognizer()

        # Capture audio from the microphone
        with sr.Microphone() as source:
            print("Please wait. Calibrating microphone...")
            # Listen for 5 seconds and create ambient noise energy level
            r.adjust_for_ambient_noise(source, duration=5)
            print("Microphone calibrated")
            
            print("-------- !!  Speak to me Now !! --------")
            audio = r.listen(source)

            try:
                # Recognize speech using Google Web Speech API
                print("Recognizing...")
                text = r.recognize_google(audio)
                print("You said: " + text)
                return text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

    genai.configure(api_key="AIzaSyDr73S6bNcCQbeCToZtSzmF2rfMOziTp-I") # replace with your actual API key

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        safety_settings=safety_settings,
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[
        ]
    )

    print('Voice bot Starting')

    while True:
        print("-- Speak Now -- ")
        prompt = voice()
        if "exit" in prompt or "quit" in prompt:
            break

        if prompt:  # Only send request if prompt is not empty
            response = chat_session.send_message(prompt)
            print(response.text)
            print(chat_session.history)
            speak(response.text)  # Speak the response

voicebot()

"""
lw Tech sprint @summerprogram made engineering students from across india ...
"""