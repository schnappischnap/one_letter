from difflib import SequenceMatcher
from random import randrange
from string import ascii_lowercase


def lines_as_set(filename):
    with open(filename, 'r') as f:
        return set(f.read().lower().splitlines())


class Game:
    def __init__(self):
        self.matcher = SequenceMatcher()
        self.wordlist = lines_as_set("wordlist.txt")
        self.used = set()
        self.current_word = None

    def acceptable(self, word, skip_matcher=False):
        if word in self.used:          # word already used -> false
            return False
        if word not in self.wordlist:  # word is not valid -> false
            return False
        if self.current_word is None:  # first move -> true
            return True
        if skip_matcher:
            return True

        self.matcher.set_seqs(self.current_word, word)
        opcodes = self.matcher.get_opcodes()
        # more than one group changed -> false
        if sum(code[0] != 'equal' for code in opcodes) > 1:
            return False
        # more than one letter changed in at least one group -> false
        if any(code[0] != 'equal' and (
               code[4] - code[3] > 1 or
               code[2] - code[1] > 1) for code in opcodes):
            return False
        return True

    def get_possible_words(self):
        # first move -> yield entire word list
        if self.current_word is None:
            yield from self.wordlist
            return

        cur = self.current_word
        for i in range(len(cur)):
            word = cur[:i] + cur[i+1:]  # remove a letter
            if self.acceptable(word, skip_matcher=True):
                yield word
            for c in ascii_lowercase:
                word = cur[:i] + c + cur[i+1:]  # change a letter
                if self.acceptable(word, skip_matcher=True):
                    yield word
                word = cur[:i] + c + cur[i:]  # add a letter
                if self.acceptable(word, skip_matcher=True):
                    yield word

    def take_word(self, word):
        if not self.acceptable(word):
            return False
        self.current_word = word
        self.used.add(word)
        return True

    def get_word(self):
        words = list(self.get_possible_words())
        return words[randrange(0, len(words))] if len(words) > 0 else False

    def play(self, ai=True, hints=False):
        while True:
            if not any(True for _ in self.get_possible_words()):
                print("No more moves detected.")
                return

            inp = input("> ").lower()
            if inp == "?" and hints:
                print(list(self.get_possible_words()))
                continue
            elif not self.take_word(inp):
                print("Word is not acceptable!")
                continue

            if ai:
                reply = self.get_word()
                if reply:
                    print("> " + reply)
                    self.take_word(reply)
                else:
                    print("No more moves detected.")
                    return


if __name__ == '__main__':
    game = Game()
    game.play(False)
