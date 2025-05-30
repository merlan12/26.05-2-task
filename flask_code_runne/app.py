from flask import Flask, request, render_template
from pygments import highlight
from pygments.lexers import PythonLexer, PythonTracebackLexer
from pygments.formatters import HtmlFormatter
import io
import contextlib
import traceback

app = Flask(__name__)

def run_code(code):
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
        return highlight(output.getvalue(), PythonLexer(), HtmlFormatter()), None
    except Exception:
        err = traceback.format_exc()
        return None, highlight(err, PythonTracebackLexer(), HtmlFormatter())

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    result_html = ""
    error_html = ""
    
    if request.method == "POST":
        code = request.form["code"]
        output, error = run_code(code)
        result_html = output or ""
        error_html = error or ""

    formatter = HtmlFormatter(style="monokai", linenos=True)
    style = f"<style>{formatter.get_style_defs('.highlight')}</style>"

    return render_template("index.html",
                           code=code,
                           result=result_html,
                           error=error_html,
                           style=style)

if __name__ == "__main__":
    app.run(debug=True)
