from flask import Blueprint, request, render_template
from utils import get_comments_by_post_id, get_post_by_pk, get_posts_all, search_for_posts, comments_counter, \
    get_posts_by_user

# Блюпринт main для вывода постов
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates')


# Вьюшка главной страницы
@main_blueprint.route('/')
def main_page():
    posts = get_posts_all()
    for post in posts:
        post['content'] = post['content'][:50] + '...'
        post_comments = get_comments_by_post_id(post['pk'])
        post['comments_count'] = comments_counter(post_comments)
    return render_template('index.html', posts=posts)


# Вьюшка страницы поста с комментариями
@main_blueprint.route('/posts/<int:postid>')
def post_page(postid):
    post = get_post_by_pk(postid)
    comments = get_comments_by_post_id(postid)
    comments_count = comments_counter(comments)
    return render_template('post.html', post=post, comments=comments, comments_count=comments_count)


# Вьюшка страницы поиска по ключу
@main_blueprint.route('/search/')
def search_page():
    query = request.args['s']
    posts = search_for_posts(query)[:10]
    posts_count = len(posts)

    for post in posts:
        post['content'] = post['content'][:50] + '...'
        post_comments = get_comments_by_post_id(post['pk'])
        post['comments_count'] = comments_counter(post_comments)

    return render_template('search.html', posts=posts, posts_count=posts_count, query=query)


# Вьюшка постов пользователя
@main_blueprint.route('/users/<username>')
def user_page(username):
    posts = get_posts_by_user(username)
    for post in posts:
        post['content'] = post['content'][:50] + '...'
        post_comments = get_comments_by_post_id(post['pk'])
        post['comments_count'] = comments_counter(post_comments)
    return render_template('user-feed.html', posts=posts)
