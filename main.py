import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr

class AudioTranscriber:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def transcribe_audio_google(self, audio_file, language='en-US'):
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language=language)
                return text
        except sr.UnknownValueError:
            return "Failed to understand audio"
        except sr.RequestError as e:
            return f"Error in Google Speech Recognition request: {e}"

    def transcribe_audio_pocketsphinx(self, audio_file):
        try:
            with sr.AudioFile(audio_file) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_sphinx(audio_data)
                return text
        except sr.UnknownValueError:
            return "Failed to understand audio"
        except sr.RequestError as e:
            return f"Error in Pocketsphinx request: {e}"

    def transcribe_audio(self, audio_file, language='en-US'):
        google_result = self.transcribe_audio_google(audio_file, language)
        pocketsphinx_result = self.transcribe_audio_pocketsphinx(audio_file)
        return google_result, pocketsphinx_result

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav")])
    if filename:
        audio_file_entry.delete(0, tk.END)
        audio_file_entry.insert(0, filename)

def transcribe_audio():
    audio_file = audio_file_entry.get()
    if audio_file:
        google_transcription, pocketsphinx_transcription = transcriber.transcribe_audio(audio_file, language=language_var.get())
        google_text.delete(1.0, tk.END)
        google_text.insert(tk.END, google_transcription)
        pocketsphinx_text.delete(1.0, tk.END)
        pocketsphinx_text.insert(tk.END, pocketsphinx_transcription)
    else:
        status_label.config(text="Select an audio file first!")

if __name__ == "__main__":
    transcriber = AudioTranscriber()

    root = tk.Tk()
    root.title("Audio Transcriber")

    language_var = tk.StringVar(root, "en-US")

    audio_file_label = tk.Label(root, text="Audio File:")
    audio_file_label.grid(row=0, column=0, padx=5, pady=5)

    audio_file_entry = tk.Entry(root, width=50)
    audio_file_entry.grid(row=0, column=1, padx=5, pady=5)

    browse_button = tk.Button(root, text="Browse", command=browse_file)
    browse_button.grid(row=0, column=2, padx=5, pady=5)

    language_label = tk.Label(root, text="Language:")
    language_label.grid(row=1, column=0, padx=5, pady=5)

    language_menu = tk.OptionMenu(root, language_var, "en-US")
    language_menu.grid(row=1, column=1, padx=5, pady=5)

    transcribe_button = tk.Button(root, text="Transcribe", command=transcribe_audio)
    transcribe_button.grid(row=1, column=2, padx=5, pady=5)

    google_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
    google_text.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

    google_label = tk.Label(root, text="Transcription using Google Speech Recognition")
    google_label.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

    pocketsphinx_text = tk.Text(root, wrap=tk.WORD, width=50, height=10)
    pocketsphinx_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

    pocketsphinx_label = tk.Label(root, text="Transcription using Pocketsphinx")
    pocketsphinx_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    status_label = tk.Label(root, text="", fg="red")
    status_label.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

    root.mainloop()
