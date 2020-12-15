#!/usr/bin/python3
# Isaac Bordfeld
import numpy as np
class Subject:
    def __init__(self):
        # Basic information for storing
        self.first = ""
        self.last = ""
        self.age = ""
        self.sex = ""

        # Data being collected by user's response during experiment
        self.timeStart = 0
        self.timeEnd = 0
        self.responseTime = 0
        self.isCorrect = 0
        self.conditionType = None
        self.sentence = None
        self.answer = None

        # Sentences used during experiment
        self.experimentSentences = [
                                    "we can walk by the river", 
                                    "come pet my puppy when you come over", 
                                    "there is ice cream in the freezer", 
                                    "the virus had powers none of us knew existed", 
                                    "can i go to the mall with my friends", 
                                    "i bet you can read this sentence"
                                    ]

        # Data for overall results at the end
        self.totalRight = 0
        self.totalResponseTime = 0
        self.originalSentences = self.experimentSentences

        self.isScrambled = 3 # Number of sentences that will be shown that look "Scrambled"
        self.isNormal = 3 # Number of sentences that will be shown that look "Normal"

        # This attribute was used for storing whether the new sentence was 
        # picked. Otherwise, it would render a new one before I could check the answer
        self.pickedSentence = False

        self.trial = 1

    def runExperiment(self):
        if len(self.experimentSentences) == 6:
            self.experimentSentences = self.experiment(self.experimentSentences)

        np.random.shuffle(self.experimentSentences)

        next_sentence = self.experimentSentences.pop()

        self.chooseCondition()

        if self.conditionType == "Scrambled":
            next_sentence[0] = self.scramble_sentence(next_sentence[0])
        
        return next_sentence

    # Scrambles the words in a sentence and concatenates back into a sentence
    def experiment(self, original_sentence):
        final_scramble = list()
        for sentence in original_sentence:
            storedSentence = sentence
            scramble_sentence = list()
            sentence = sentence.split(" ")
            for word in sentence:
                if len(word) > 3:
                    scramble_sentence.append(word[0] + self.scramble(word[1:-1]) + word[-1])
                else:
                    scramble_sentence.append(word)
            
            scramble_sentence = " ".join(scramble_sentence)
            final_scramble.append([scramble_sentence, storedSentence])

        """
        x number sentences in an np array
        One will be randomly chosen for task
            - Sentence will be split into a list and each word will be scrambled
                - first and last letter in each word are fixed
                - Once randomized, concatenate the words together
                    - We will need the original list of words unscrambled and scrambled words for comparing
        """

        return final_scramble

    # Scrambles a word
    def scramble(self, word):
        original_word = word
        while word == original_word:
            word = list(word)
            np.random.shuffle(word)
            word = "".join(word)
        return word

    # Scrambles sentence for one condition
    def scramble_sentence(self, sentence):
        original_sentence = sentence
        sentence = sentence.split(" ")
        np.random.shuffle(sentence)
        sentence = " ".join(sentence)

        if sentence == original_sentence:
            self.scramble_sentence(original_sentence)

        return sentence

    def chooseCondition(self):
        if self.isScrambled == 0:
            self.conditionType = "Normal"
            self.isNormal -= 1
        elif self.isNormal == 0:
            self.conditionType = "Scrambled"
            self.isScrambled -= 1
        else:
            self.conditionType = np.random.choice(["Normal", "Scrambled"])
            if self.conditionType == "Normal":
                self.isNormal -= 1
            else:
                self.isScrambled -= 1

    def checkAnswer(self, correctAnswer, userAnswer):
        correctAnswer = correctAnswer.split(" ")
        correctAnswer = [word.lower() for word in correctAnswer]

        userAnswer = userAnswer.split(" ")
        userAnswer = [word.lower() for word in userAnswer]

        if len(correctAnswer) == len(userAnswer):
            for word in userAnswer:
                if word not in correctAnswer:
                    return 0
        else:
            return 0
        return 1

    def results(self):
        """
        Calculate Results:
            - Average Response Time
            - % correct
        """
        averageResponseTime = self.totalResponseTime  / 6

        return averageResponseTime

    def reset(self):
        self.totalRight += self.isCorrect
        self.responseTime = 0
        self.isCorrect = 0
        self.conditionType = None
        self.sentence = None
        self.pickedSentence = False
        self.answer = None
        self.trial += 1
    
    def updateInformation(self, first, last, age, sex):
        self.first = first
        self.last = last
        self.age = age
        self.sex = sex

    def done(self):
        return self.isScrambled == 0 and self.isNormal == 0

    def showData(self):
        fptr = open('data.csv', 'a')

        if self.sex == "1":
            sex = "Male"
        else:
            sex = "Female"

        fptr.write(f"{self.first},{self.last},{self.age},{sex},{self.responseTime},{self.isCorrect}," +
            f"{self.conditionType},{self.sentence[0]},{self.sentence[1]},{self.answer}\n")
        fptr.close()
