from flask import Flask, render_template
from routes.scan import scan_bp
from routes.auth import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(scan_bp, url_prefix='/scan')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
