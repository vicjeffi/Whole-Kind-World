import re

class ProfanityFilter:
    def __init__(self, word_files):
        self.replacement_characters = {'@', '*', '#', '!', '$', '%', '^', '&', '(', ')', '_', '+', '-', '='}
        self.unacceptable_words = {}
        for language, file_path in word_files.items():
            self.load_words(language, file_path)

    def load_words(self, language, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            words = [line.strip().upper() for line in file if line.strip()]
        self.unacceptable_words[language] = set(words)

    def add_word(self, language, word):
        if language not in self.unacceptable_words:
            self.unacceptable_words[language] = set()
        self.unacceptable_words[language].add(word.upper())

    def contains_unacceptable_words(self, text, language):
        if language not in self.unacceptable_words:
            return False
        words = text.upper().split()
        for word in words:
            for bad_word in self.unacceptable_words[language]:
                pattern = ''.join(f'[{re.escape(char)}{re.escape("".join(self.replacement_characters))}]' if char in self.replacement_characters else char for char in bad_word)
                if re.search(pattern, word):
                    return True
        return False