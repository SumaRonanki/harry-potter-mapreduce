import re
from mrjob.job import MRJob
from mrjob.step import MRStep
from spellchecker import SpellChecker

# My date of birth is 31st March 2004

WORD_RE = re.compile(r"[A-Za-z']+")

class MRNonEnglishCount(MRJob):

    def mapper_init(self):
        self.spell = SpellChecker()

    def steps(self):
        return [MRStep(mapper_init=self.mapper_init,
                       mapper=self.mapper_non_english,
                       combiner=self.combiner_sum,
                       reducer=self.reducer_sum)]

    def mapper_non_english(self, _, line):
        for w in WORD_RE.findall(line):
            if not self.spell.known([w.lower()]):
                yield w, 1

    def combiner_sum(self, word, counts):
        yield word, sum(counts)

    def reducer_sum(self, word, counts):
        yield word, sum(counts)

if __name__ == "__main__":
    MRNonEnglishCount.run()