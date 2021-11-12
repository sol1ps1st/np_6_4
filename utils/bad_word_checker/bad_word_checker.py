import re

from utils.bad_word_checker.bad_words import bad_words as b_words


class BadWordChecker:
    def __init__(self, bad_words=b_words):
        """
        :param bad_words: словарик плохих слов
        """
        self._bad_words = bad_words

    @staticmethod
    def _distance(a, b):
        "Levenshtein distance between a and b"
        n, m = len(a), len(b)
        if n > m:
            # Make sure n <= m, to use O(min(n, m)) space
            a, b = b, a
            n, m = m, n

        current_row = range(n + 1)  # Keep current and previous row, not entire matrix
        for i in range(1, m + 1):
            previous_row, current_row = current_row, [i] + [0] * n
            for j in range(1, n + 1):
                add, delete, change = previous_row[j] + 1, current_row[j - 1] + 1, previous_row[j - 1]
                if a[j - 1] != b[i - 1]:
                    change += 1
                current_row[j] = min(add, delete, change)

        return current_row[n]

    def is_bad(self, word):
        prepare_word = re.compile('\w+').findall(word.lower())  # Возвращается либо список из одного слова, либо пустой
        if len(prepare_word) != 1:
            return False  # Это всякие символы по типу '-'
        for bad_word in self._bad_words:
            if BadWordChecker._distance(bad_word, prepare_word[0]) <= len(bad_word) * 0.25:
                return True
