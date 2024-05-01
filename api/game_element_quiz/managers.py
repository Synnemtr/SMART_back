from rest_framework import exceptions
from django.db import models
from app.utils import unique

class GameQuizManager(models.Manager):
    use_in_migrations = True

    def create_game_quiz(self, **data):
        try:
            question = data.pop('question')
            option_one = data.pop('option_one')
            option_two = data.pop('option_two')
            option_three = data.pop('option_three')
            option_four = data.pop('option_four')
            correct_answer = data.pop('correct_answer')
        except KeyError:
            raise exceptions.ValidationError("Question, options and correct_answer are required")
        game_quiz = self.model(
            question=question,
            option_one=option_one,
            option_two=option_two,
            option_three=option_three,
            option_four=option_four,
            correct_answer=correct_answer
        )
        game_quiz.save(using=self._db)
        return game_quiz

    def update_game_quiz(self, game_quiz, **data):
        game_quiz.question = data.get('question', game_quiz.question)
        game_quiz.option_one = data.get('option_one', game_quiz.option_one)
        game_quiz.option_two = data.get('option_two', game_quiz.option_two)
        game_quiz.option_three = data.get('option_three', game_quiz.option_three)
        game_quiz.option_four = data.get('option_four', game_quiz.option_four)
        game_quiz.correct_answer = data.get('correct_answer', game_quiz.correct_answer)
        game_quiz.save()
        return game_quiz

    def delete_game_quiz(self, game_quiz):
        game_quiz.delete()
        return game_quiz

    def get_quiz_by_id(self, quiz_id):
        if not self.filter(id=quiz_id).exists():
            raise exceptions.ValidationError("Quiz with id {} does not exist".format(quiz_id))
        quiz = self.get(id=quiz_id)
        return quiz

    def validate_quiz_answer(self, list_answers):
        list_quiz_number = [answer['quiz_id'] for answer in list_answers]
        list_quiz_number = unique(list_quiz_number)
        if len(list_quiz_number) != 1:
            raise exceptions.ValidationError("You must answer the question")
        list_answer_type = []
        for answer in list_answers:
            quiz_id = answer['quiz_id']
            quiz = self.get_quiz_by_id(quiz_id)
            type_quiz_id = quiz.correct_answer.id
            score = answer['score']
            if not isinstance(score, int):
                raise exceptions.ValidationError("Score must be an integer")
            if score < 1 or score > 4:
                raise exceptions.ValidationError("Score must be between 1 and 4")
            list_answer_type.append({'type_quiz_id': type_quiz_id, 'score': score})
        return list_answer_type