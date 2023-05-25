from django.db import models

from accounts.models import User


class Post(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50,  default='',blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.author.username} - {self.title}'

    @property
    def avg_mark(self):
        try:
            mark_dict = PostMark.objects.filter(post=self)
            mark_list = []
            if len(mark_dict) >= 1:
                for mark in mark_dict:
                    mark_list.append(getattr(mark, 'mark'))
                avg_mark = round(sum(mark_list)/len(mark_list), 2)
            if len(mark_dict) < 1:
                avg_mark = 'Нет оценок'
        except ZeroDivisionError:
            return 'Проверьте ввод данных'
        else:
            return avg_mark


class PostMark(models.Model):
    mark = models.IntegerField(choices=[
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    ], max_length=10)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'post']

    def __str__(self):
        return f'{self.user} - {self.mark}'


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=20, null=True, blank=True)



