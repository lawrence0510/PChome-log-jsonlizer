from flask import Flask, request, render_template_string
import json

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>JSON Visualizer</title>
</head>
<body>
    <h1>Simple JSON Output</h1>
    <form action="/" method="post">
        <textarea name="input_string" rows="10" cols="50">{{ current_input }}</textarea><br>
        <button type="submit">Convert to JSON</button>
    </form>
    {% if json_data %}
    <h2>JSON Output:</h2>
    <pre>{{ json_data }}</pre>
    {% elif error_message %}
    <h2>Error:</h2>
    <p>{{ error_message }}</p>
    {% endif %}
</body>
</html>
"""

def parse_to_json(input_string):
    try:
        lines = input_string.strip().split('\n')
        timestamp = lines[0].strip()
        event_type = lines[1].split('：')[1].strip()
        event_name = lines[2].split('：')[1].strip()
        args_part = lines[3].split('：')[1].strip('{}')
        
        args_dict = {}
        current_key = None
        buffer = []
        for part in args_part.split(','):
            if '=' in part:
                if current_key:
                    args_dict[current_key] = ''.join(buffer).strip()
                    buffer = []
                key, value = part.split('=', 1)
                current_key = key.strip()
                buffer.append(value.strip())
            else:
                buffer.append(part)

        # 添加最後一個鍵值對
        if current_key and buffer:
            args_dict[current_key] = ''.join(buffer).strip()

        event_info = {
            "timestamp": timestamp,
            "type": event_type,
            "name": event_name,
            "args": args_dict
        }
        return json.dumps(event_info, indent=4), None
    except Exception as e:
        return None, f"Error parsing input: {str(e)}"

@app.route("/", methods=["GET", "POST"])
def home():
    json_data = None
    error_message = None
    current_input = "2024-05-06 07:13:00\nType：sst\nName：pageView\nArgs：{eventId=9d48987e-a70b-4660-ad59-133ac4851b99, deviceCategory=app.android, userAgent=Mozilla/5.0 (Linux; Android 9; HTC_U-3u Build/PQ2A.190205.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.91 Mobile Safari/537.36 PChome_APP_and_4.0.0, sessionId=a534aaba-a022-4e19-b9b8-8af5e993f351, deviceId=9ac453be16ef60db, userId=23687777, timestamp=1714950780609, pageType=sign, pageId=cp, pageName=周邊}"
    
    if request.method == "POST":
        current_input = request.form['input_string']
        json_data, error_message = parse_to_json(current_input)
    
    return render_template_string(HTML_TEMPLATE, json_data=json_data, error_message=error_message, current_input=current_input)

if __name__ == "__main__":
    app.run(debug=True, port=5050)
