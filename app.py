import string

from flask import Flask, render_template, request, redirect

app = Flask(__name__)


class ArchiveResult:
    def __init__(self, input_text, output_text):
        self.input_bytes_count = len(input_text)
        self.output_text = output_text
        self.output_bytes_count = len(output_text)


def lzw_archive(text):
    strings = [chr(i) for i in range(128)]
    output_code = []
    x = text[0]
    for y in text[1:]:
        if x + y in strings:
            x = x + y
        else:
            output_code.append(strings.index(x))
            strings.append(x + y)
            x = y
    output_code.append(strings.index(x))
    output_str = "".join([chr(n) for n in output_code])
    return ArchiveResult(text, output_str)


def lzw_unarchive(text):
    strings = [chr(i) for i in range(128)]
    input_code = [ord(c) for c in text]
    output_str = ""
    last = input_code[0]
    output_str += strings[last]
    for current in input_code[1:]:
        string = strings[current]
        output_str += string
        strings.append(strings[last] + string[0])
        last = current
    return output_str


@app.errorhandler(404)
def page_not_found(e):
    return redirect('index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text'].replace("\r", "")
        initial = lzw_unarchive(text)
        return render_template('index.html', initial=initial, available=string.printable[:-6])
    return render_template('index.html', available=string.printable[:-6])


@app.route('/archive', methods=['POST'])
def archive():
    text = request.form['text'].replace("\r", "")
    result = lzw_archive(text)
    return render_template('archive.html', result=result)


if __name__ == '__main__':
    app.run()
