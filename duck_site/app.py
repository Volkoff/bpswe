from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Duck</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: #ffffff;
                font-family: sans-serif;
            }
            h1 {
                font-size: 2rem;
                color: #333;
            }
        </style>
    </head>
    <body>
        <h1>duck</h1>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True, port=5000)
