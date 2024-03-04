from datetime import datetime, timedelta
import requests

TIME_TO_WRITE = 60#SECONDS
ENDPOINT_URL = "https://random-word-api.herokuapp.com/word"

class TypeTest:
    def __init__(self) -> None:
        self.text_data: list = []
        self.written_words = []
        self.incorrect_words = {}
        self.end_time:datetime = None
        self.start_time:datetime = None
        self.test_is_on: bool = False
    
    def fetch_texts(self):
        req_params = {
            "number": 100,
            "lang": "en"
        }
        req = requests.get(ENDPOINT_URL, params=req_params)
        req.raise_for_status()
        self.text_data = req.json()
    
    def check_word(self, word:str, correct_word:str):
        if word == correct_word:
            self.written_words.append(word)
        else:
            self.incorrect_words[correct_word] = word
        
    def start_timer(self):
        self.test_is_on = True
        self.start_time = datetime.now()
        self.end_time = self.start_time + timedelta(seconds=TIME_TO_WRITE)
        
    def time_left(self) -> bool:
        left = self.end_time - datetime.now()
        return left.total_seconds() > 0
    
    def get_results(self):
        test_length = datetime.now() - self.start_time
        characters:int = 0
        for word in self.written_words:
            characters += len(word)
        cpm = characters / test_length.total_seconds() * 60
        
        return {"cpm": cpm, "incorrect_words": self.incorrect_words, "characters": characters }
    
    def reset_test(self):
        self.written_words = []
        self.incorrect_words = {}
        self.fetch_texts()

