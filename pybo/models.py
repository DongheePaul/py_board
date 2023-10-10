from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    author 필드는 User모델을 외래키로 적용. User모델은 django.contrib.auth 앱이 제공하는 사용자 모델.
    on_delete=models.CASCADE 뜻은 계정이 삭제되면 이 계정이 작성한 질문을 모두 삭제하라는 의미.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    def __str__(self):
        return self.subject

class Answer(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    #다른 모델과 연결하기 위한 외래키. ondelete 옵션 사용해 연결된 질문 삭제 시 답변 모두 삭제.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()