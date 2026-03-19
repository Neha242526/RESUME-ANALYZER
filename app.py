import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text', '').lower()
    
    # चेक करने के लिए कुछ स्किल्स
    keywords = ["python", "java", "sql", "html", "css", "javascript", "react", "excel"]
    found = [word for word in keywords if word in text]
    
    score = (len(found) / len(keywords)) * 100 if keywords else 0

    return jsonify({
        "score": round(score, 2),
        "skills_found": found
    })

if _name_ == '_main_':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
