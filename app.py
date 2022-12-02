from flask import Flask, send_from_directory, jsonify
import logging
from main.views import main_blueprint
from utils import get_posts_all, get_posts_by_user, get_comments_by_post_id, get_post_by_pk, search_for_posts



app = Flask(__name__)
# Чтобы заработала кириллица
app.config['JSON_AS_ASCII'] = False

# регистрируем блюпринты
app.register_blueprint(main_blueprint)


@app.errorhandler(404)
def page_error_404(error):
    return 'Такой страницы не существует', 404


@app.errorhandler(500)
def page_error_500(error):
    return f'На сервере произошла ошибка - {error}', 500


@app.errorhandler(ValueError)
def page_value_error(error):
    return "Таких постов не существует"


# Вьюшка, которая обрабатывает запрос GET /api/posts и возвращает полный список постов в виде JSON-списка.
@app.route('/api/posts')
def api_posts_page():
    posts = get_posts_all()
    return jsonify(posts)


# Вьюшка, которая обрабатывает запрос GET /api/posts/<post_id> и возвращает один пост в виде JSON-словаря."""
@app.route('/api/posts/<int:post_id>')
def api_post_page(post_id):
    data = get_post_by_pk(post_id)
    return jsonify(data)


# Создаем или получаем новый логгер
logger = logging.getLogger()

# Cоздаем ему обработчик для вывода в консоль и в файл
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("logs/api.log")

# Создаем форматирование (объект класса Formatter)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
# Применяем форматирование к обработчику
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Добавляем обработчик к журналу
logger.addHandler(console_handler)
logger.addHandler(file_handler)

logger.warning("Логгер работает")

app.run()
