from flask import Flask, render_template, request, session, url_for, redirect
from flask_babel import Babel, _

app = Flask(__name__)
app.secret_key = "super_secret_key"
babel = Babel(app)

# Переводимые строки
translations = {
    'ru': {
        'greeting': 'Добро пожаловать!',
        'theme_switch': 'Переключить тему',
        'not_found': 'Ничего не нашлось! Вот неудача, отправляйтесь на главную!',
        'server_error': 'Что-то не так, но мы все починим'
    },
    'en': {
        'greeting': 'Welcome!',
        'theme_switch': 'Switch theme',
        'not_found': 'Nothing found! Oops, go back to the homepage!',
        'server_error': 'Something went wrong, but we will fix it'
    }
}

# Выбор языка на основе параметра в сессии
@babel.localeselector
def get_locale():
    return session.get('lang', 'en')  # Язык по умолчанию - английский

@app.route("/", methods=['GET'])
def main():
    dark = session.get("dark", False)
    greeting = _("greeting")  # Переводим строку
    return render_template("index.html", dark=dark, greeting=greeting)

@app.route("/switch_theme/", methods=["POST"])
def switch_theme():
    selected_theme = request.form.get("theme")
    session["dark"] = (selected_theme == "dark")
    return redirect(url_for("main"))

@app.route("/switch_language/", methods=["POST"])
def switch_language():
    selected_language = request.form.get("lang")
    session['lang'] = selected_language  # Сохраняем выбранный язык в сессии
    return redirect(url_for("main"))

@app.errorhandler(404)
def render_not_found(error):
    return translations[get_locale()]['not_found'], 404

@app.errorhandler(500)
def render_server_error(error):
    return translations[get_locale()]['server_error'], 500

if __name__ == '__main__':
    app.run(port=5002, debug=True)
