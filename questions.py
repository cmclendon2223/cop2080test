## A question with a text and an answer.
#
class Question:
    ## Constructs a question with empty question and answer strings.
    #
    def __init__(self):
        self._text = ""
        self._answer = ""

    ##  Sets the question text.
    #   @param questionText the text of this question
    #
    def setText(self, questionText):
        self._text = questionText

    ## Sets the answer for this question.
    #  @param correctResponse the answer
    #
    def setAnswer(self, correctResponse):
        self._answer = correctResponse

    ## Checks a given response for correctness.
    #  @param response the response to check
    #  @return True if the response was correct, False otherwise
    #
    def checkAnswer(self, response):
        return response == self._answer

    ## Displays this question.
    #
    def display(self):
        print(self._text)

        ## Generate a string representation of the object.

    #  @return a string representing the object
    #
    def __repr__(self):
        return self._text


## A question with multiple choices.
#
class ChoiceQuestion(Question):
    # Constructs a choice question with no choices.
    def __init__(self):
        super().__init__()
        self._choices = []

    ## Adds an answer choice to this question.
    #  @param choice the choice to add
    #  @param correct True if this is the correct choice, False otherwise
    #
    def addChoice(self, choice, correct):
        self._choices.append(choice)
        if correct:
            # Convert len(choices) to string.
            choiceString = str(len(self._choices))
            self.setAnswer(choiceString)

    # Override Question.display().
    def display(self):
        # Display the question text.
        super().display()

        # Display the answer choices.
        for i in range(len(self._choices)):
            choiceNumber = i + 1
            print("%d: %s" % (choiceNumber, self._choices[i]))

    ## Generate a string representation of the object.
    #  @return a string representing the object
    #
    def __repr__(self):
        result = self._text
        for i in range(len(self._choices)):
            result = result + "\n%d: %s" % (i + 1, self._choices[i])
        return result 

