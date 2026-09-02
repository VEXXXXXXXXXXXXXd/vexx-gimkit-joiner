from flask import Flask, request, render_template_string
import requests
import random
import string

app = Flask(__name__)

GIMKIT_JOIN_URL = "https://www.gimkit.com/api/match/join"

page = """
<!DOCTYPE html>
<html>
<head>
<title>[VEXX] - Gimkit Joiner Thing</title>
<style>
body {
    margin: 0;
    height: 100vh;
    background: linear-gradient(135deg, #000000, #330000, #990000);
    background-size: 400% 400%;
    animation: gradientMove 12s ease infinite;
    font-family: Arial;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
}
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.container {
    background: rgba(0,0,0,0.6);
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 0 25px #ff0000;
    text-align: center;
    width: 450px;
}
input {
    padding: 12px;
    width: 350px;
    border-radius: 6px;
    border: none;
    margin-top: 10px;
    background:#222;
    color:#fff;
}
button {
    padding: 12px 20px;
    margin-top: 15px;
    background: #ff0000;
    border: none;
    border-radius: 6px;
    color: white;
    font-weight: bold;
    cursor: pointer;
    transition: 0.3s;
}
button:hover {
    background: #cc0000;
    box-shadow: 0 0 15px #ff0000;
}
.header {
    color: #cccccc;
    font-size: 22px;
    margin-bottom: 20px;
}
pre {
    background: #222;
    padding: 15px;
    border-radius: 8px;
    margin-top: 20px;
    max-height: 300px;
    overflow-y: auto;
    text-align: left;
}
</style>
</head>
<body>
<div class="container">
    <div class="header">[VEXX] - Gimkit Joiner Thing</div>

    <form method="POST" action="/join">
        <input type="text" name="code" placeholder="Room Code"><br><br>
        <input type="text" name="prefix" placeholder="Bot Name Prefix (ex: VEXXBot_)"><br><br>
        <input type="number" name="count" placeholder="How Many Bots"><br><br>
        <button type="submit">JOIN BOTS</button>
    </form>

    {% if results %}
    <pre>{{ results }}</pre>
    {% endif %}
</div>
</body>
</html>
"""

def join_bot(code, name):
    payload = {"code": str(code), "name": name}
    try:
        r = requests.post(GIMKIT_JOIN_URL, json=payload, timeout=10)
        return r.status_code, r.text
    except Exception as e:
        return 0, f"ERROR: {e}"

@app.route("/", methods=["GET"])
def home():
    return render_template_string(page)

@app.route("/join", methods=["POST"])
def join():
    code = request.form.get("code", "").strip()
    prefix = request.form.get("prefix", "").strip()
    count_raw = request.form.get("count", "0").strip()

    results = ""

    if not code or not prefix or not count_raw:
        results = "Error: Missing room code, prefix, or count."
        return render_template_string(page, results=results)

    try:
        count = int(count_raw)
        if count <= 0:
            raise ValueError()
    except ValueError:
        results = "Error: Bot count must be a positive number."
        return render_template_string(page, results=results)

    for i in range(count):
        bot_name = prefix + ''.join(random.choice(string.ascii_letters) for _ in range(5))
        status, text = join_bot(code, bot_name)

        short_text = text.replace("\n", " ")
        if len(short_text) > 200:
            short_text = short_text[:200] + "..."

        results += f"{bot_name} → status={status} | {short_text}\n"

    return render_template_string(page, results=results)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
