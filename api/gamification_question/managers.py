from rest_framework import exceptions
from django.db import models
from app.utils import unique


class GamificationQuestionManager(models.Manager):
    use_in_migrations = True

    def create_gamification_question(self, **data):
        try:
            question = data.pop('question')
            gamification_type = data.pop('gamification_type')
        except KeyError:
            raise exceptions.ValidationError("Question and gamification_type are required")
        gamification_question = self.model(
            question=question,
            gamification_type=gamification_type
        )
        gamification_question.save(using=self._db)
        return gamification_question

    def update_gamification_question(self, gamification_question, **data):
        gamification_question.question = data.get('question', gamification_question.question)
        gamification_question.save()
        return gamification_question

    def delete_gamification_question(self, gamification_question):
        gamification_question.delete()
        return gamification_question

    def get_question_by_id(self, question_id):
        if not self.filter(id=question_id).exists():
            raise exceptions.ValidationError("Question with id {} does not exist".format(question_id))
        question = self.get(id=question_id)
        return question

    def validate_form_answer(self, list_answers):
        list_question_number = [answer['question_id'] for answer in list_answers]
        list_question_number = unique(list_question_number)
        if len(list_question_number) != 12:
            raise exceptions.ValidationError("You must answer all the questions")
        list_answer_type = []
        for answer in list_answers:
            question_id = answer['question_id']
            question = self.get_question_by_id(question_id)
            type_question_id = question.gamification_type.id
            score = answer['score']
            if not isinstance(score, int):
                raise exceptions.ValidationError("Score must be an integer")
            if score < 1 or score > 7:
                raise exceptions.ValidationError("Score must be between 1 and 7")
            list_answer_type.append({'type_question_id': type_question_id, 'score': score})
        return list_answer_type
