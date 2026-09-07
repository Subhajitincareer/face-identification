import os
import speech_recognition as sr

# Bengali triggers (including common variations)
TRIGGERS = ["কম্পিউটার বন্ধ করো", "কম্পিউটার বন্ধ কর", "কম্পিউটার অফ করো", "পিসি বন্ধ করো", "computer bondho koro"]

recognizer = sr.Recognizer()

with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=1)

    recognizer.dynamic_energy_threshold = True  # Helps detect voice accurately in varying background noise

    print("Voice shutdown is running... (Say 'কম্পিউটার বন্ধ করো')")

    while True:
        try:
            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=5
            )

            # language="bn-BD" detects Bengali speech (Use "bn-IN" if you are in India)
            text = recognizer.recognize_google(audio, language="bn-BD").lower().strip()

            print("Heard:", text)

            if any(trigger in text for trigger in TRIGGERS):
                print("Shutdown command detected.")
                os.system("shutdown /s /t 5")
                break

        except sr.UnknownValueError:
            pass

        except sr.RequestError as e:
            print("Speech recognition error:", e)

        except Exception as e:
            print("Error:", e)
