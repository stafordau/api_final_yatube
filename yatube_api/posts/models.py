from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',)

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Подписан',)

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follower'
            )
        ]


class Group(models.Model):
    """Модель сообщества"""

    title = models.TextField(verbose_name='Название')

    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True,
    )
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'Сообщества'
        ordering = ('title',)

    def __str__(self):
        return self.title


class Post(models.Model):
    """Модель поста"""

    text = models.TextField(verbose_name='Текст')

    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор')

    image = models.ImageField(
        upload_to='posts/',
        null=True,
        blank=True,
        verbose_name='Изображение')

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='posts',
        verbose_name='Сообщество'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост'
    )

    text = models.TextField(verbose_name='Текст')

    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарий'
