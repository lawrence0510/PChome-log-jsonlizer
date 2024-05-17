from flask import Flask, request, render_template_string

app = Flask(__name__)

html = """
<!DOCTYPE html>
<html>
<head>
    <title>Open URLs</title>
    <script>
    function openUrls() {
        var urls = document.getElementById('urlText').value.split('\\n');
        urls.forEach(function(url) {
            if(url.trim() !== '') {
                window.open(url.trim(), '_blank');
            }
        });
    }
    </script>
</head>
<body>
    <h1>Enter URLs</h1>
    <form action="#" onsubmit="openUrls(); return false;">
        <textarea id="urlText" name="urls" rows="10" cols="50"></textarea><br>
        <input type="submit" value="Open URLs">
    </form>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
