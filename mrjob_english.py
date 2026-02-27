import re
from mrjob.job import MRJob
from mrjob.step import MRStep

# My date of birth is 31st March 2004

WORD_RE = re.compile(r"[A-Za-z']+")

class MRWordCount(MRJob):
    def steps(self):
        return [MRStep(mapper=self.mapper_words,
                       combiner=self.combiner_sum,
                       reducer=self.reducer_sum)]

    def mapper_words(self, _, line):
        for w in WORD_RE.findall(line.lower()):
            yield w, 1

    def combiner_sum(self, word, counts):
        yield word, sum(counts)

    def reducer_sum(self, word, counts):
        yield word, sum(counts)

if __name__ == "__main__":
    MRWordCount.run()