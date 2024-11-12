import os
from flask import Flask, render_template

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Use host='0.0.0.0' for external access and get PORT from environment variables
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=False)
