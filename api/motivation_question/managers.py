from rest_framework import exceptions
from django.db import models
import datetime


class MotivationQuestionManager(models.Manager):
    use_in_migrations = True

    def create_motivation_question(self, **data):
        try:
            question = data.pop('question')
            motivation = data.pop('motivation')
        except KeyError:
            raise exceptions.ValidationError("Question and motivation is required")

        motivation_question = self.filter(question=question).first()
        if motivation_question:
            raise exceptions.ValidationError("Question is already taken")

        motivation_question = self.model(question=question, motivation=motivation)
        motivation_question.save(using=self._db)
        return motivation_question

    def update_motivation_question(self, motivation_question, **data):
        motivation_question.question = data.get('question', motivation_question.question)
        motivation_question.updated_at = datetime.datetime.now()
        motivation_question.save()
        return motivation_question

    def delete_motivation_question(self, motivation_question):
        motivation_question.delete()
        return True

    def get_motivation_question_by_id(self, question_id):
        if not self.filter(id=question_id).exists():
            raise exceptions.ValidationError("Question with id {} does not exist".format(question_id))
        question = self.get(id=question_id)
        return question

    def validate_form_answer(self, list_answers):
        list_question_number = [answer['question_id'] for answer in list_answers]
        if len(list_question_number) != 24:
            raise exceptions.ValidationError("You must answer all the questions")
        list_answer_type = []
        for answer in list_answers:
            question_id = answer['question_id']
            question = self.get_motivation_question_by_id(question_id)
            motivation_id = question.motivation.id
            score = answer['score']
            if not isinstance(score, int):
                raise exceptions.ValidationError("Score must be an integer")
            if score < 1 or score > 7:
                raise exceptions.ValidationError("Score must be between 1 and 7")
            list_answer_type.append({'motivation_id': motivation_id, 'score': score})
        return list_answer_type
