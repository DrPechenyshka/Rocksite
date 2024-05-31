from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

thing = Flask(__name__)

# Получаем путь к текущему каталогу
basedir = os.path.abspath(os.path.dirname(__file__))
# Создаем путь к файлу базы данных
db_path = os.path.join(basedir, 'rocksite.db')

# Устанавливаем путь к базе данных
thing.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
# Указываем SQLAlchemy, что не хотим отслеживать изменения в базе данных
thing.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализируем объект SQLAlchemy
db = SQLAlchemy(thing)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    
    def __repr__(self):
        return '<Article %r>' % self.id

@thing.route('/')
@thing.route('/home')
def index():
    return render_template("index.html")

@thing.route('/groups')
def groups():
    return render_template("about.html")

@thing.route('/songs')
def songs():
    return render_template("Tracks.html")

@thing.route('/history')
def history():
    return render_template("history.html")

@thing.route('/posts')
def posts():
    articles = Article.query.order_by(Article.id).all()
    return render_template("posts.html", articles = articles)

@thing.route('/posts/<int:id>')
def posts_delete(id):
    articles = Article.query.get(id)
    return render_template("posts_detail.html", articles = articles)

@thing.route('/posts/<int:id>/del')
def posts_detail(id):
    articles = Article.query.get_or_404(id)
    try:
        db.session.delete(articles)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Произошла непредвиденная ошибка"
    
@thing.route('/posts/<int:id>/up', methods = ['POST', 'GET'])
def posts_up(id):
    articles = Article.query.get(id)
    if request.method == "POST":
        articles.title = request.form['title']
        articles.intro = request.form['intro']
        articles.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Произошла непредвиденная ошибка"

    else:
        return render_template("post_update.html", articles=articles)

@thing.route('/faq', methods = ['POST', 'GET'])
def faq():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title = title, intro = intro, text = text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Произошла непредвиденная ошибка"

    else:
        return render_template("feedback.html")

if __name__ == '__main__':
    # Создаем папку для хранения базы данных, если ее нет
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    # Создаем все таблицы, определенные в моделях SQLAlchemy
    with thing.app_context():
        db.create_all()
    # Запускаем приложение Flask
    thing.run(debug=True)