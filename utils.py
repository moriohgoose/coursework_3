import json
from pathlib import Path
from json import JSONDecodeError


def get_posts_all() -> list[dict]:
    """Возвращает посты"""
    path = Path('data/posts.json')
    try:
        with open('data/posts.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
    except (FileNotFoundError, JSONDecodeError):
        raise Exception(f'Не удается получить данные из файла {path}')
    return data


def get_posts_by_user(user_name) -> list[dict]:
    """возвращает посты определенного пользователя.
    Функция должна вызывать ошибку ValueError если такого пользователя нет."""
    result = []
    posts = get_posts_all()
    for post in posts:
        if post['poster_name'] == user_name:
            result.append(post)
    if not result:
        raise ValueError('Такого пользователя не существует')
    return result


def get_comments_by_post_id(post_id) -> list[dict]:
    """возвращает комментарии определенного поста.
    Функция должна вызывать ошибку ValueError если такого поста нет
    и пустой список, если у поста нет комментов. """
    with open('data/comments.json', 'r', encoding='utf-8') as file:
        comments = json.load(file)
    result = []
    user_name = ''
    for comment in comments:
        if comment['post_id'] == post_id:
            result.append(comment)

    for post in get_posts_all():
        if post_id == post['pk']:
            user_name = post['poster_name']
    if not user_name:
        raise ValueError('Такого поста не существует')

    return result


def search_for_posts(query) -> list[dict]:
    """возвращает список постов по ключевому слову"""
    result = []
    for post in get_posts_all():
        if query.lower() in post['content'].lower():
            result.append(post)
    if not result:
        raise ValueError('Нет таких постов')
    return result


def get_post_by_pk(pk) -> dict:
    """ возвращает один пост по его идентификатору"""
    result = {}
    for post in get_posts_all():
        if pk == post['pk']:
            result.update(post)
    if not result:
        raise ValueError('Такого поста не существует')
    return result


def comments_counter(comments: list) -> str:
    comments_count = len(comments)
    comments_amount = ''
    if comments_count == 1:
        comments_amount = '1 комментарий'
    elif 2 <= comments_count >= 4:
        comments_amount = f'{comments_count} комментария'
    elif 5 <= comments_count:
        comments_amount = f'{comments_count} комментариев'
    elif comments_count == 0:
        comments_amount = 'Нет комментариев'
    return comments_amount


print(get_post_by_pk(2))

"""Напишите к каждой функции юнит тесты, расположите тесты в отдельной папке `/tests`.

Организуйте тесты в виде классов или функций, на ваше усмотрение. """