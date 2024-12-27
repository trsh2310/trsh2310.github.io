from flask import Flask, render_template, request, session, url_for, redirect

app = Flask(__name__)
app.secret_key = "super_secret_key"


@app.route("/", methods=['GET'])
def main():
    dark = session.get("dark", False)
    lang = session.get("lang", "en")# Переводим строку вручную
    return render_template("index.html", dark=dark, lang = lang)


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
    return "Ничего не нашлось! Вот неудача, отправляйтесь на главную!"

@app.errorhandler(500)
def render_server_error(error):
    return "Что-то не так, но мы все починим"



if __name__ == '__main__':
    app.run(port=5002, debug=True)
