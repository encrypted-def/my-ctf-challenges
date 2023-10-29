from flask import Flask, abort, Response

app = Flask(__name__)

FLAG = "WACON2023{2060923e53fa205a48b2f9ad47d943c4}"

@app.route('/robots.txt', methods=['GET'])
def robots_txt():
    content = """User-agent: *
allow: /W/A/C/O/N/2/"""
    return Response(content, content_type="text/plain")


@app.route('/<path:guess>', methods=['GET'])
def guess_flag(guess):
    fake_contents = '''
<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>'''
    # Split the URL path into individual bytes
    parts = guess.split('/')
    
    # Check each byte with the corresponding byte of the FLAG
    for i, part in enumerate(parts):
        if i >= len(FLAG) or FLAG[i] != part:
            abort(404)
    # If the guess so far is correct, but not the full flag, return 200
    if len(parts) <= len(FLAG):
        return fake_contents, 200
    else:
        abort(404)

if __name__ == '__main__':
    app.run()