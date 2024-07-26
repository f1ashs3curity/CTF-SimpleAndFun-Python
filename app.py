from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Initialize the flags for challenges
flags = {
    'sql_injection': 'goSQL',
    'xxe': 'Xtreme',
    'lfi': 'LeafEye',
    'rce': 'RaCeE'
}

@app.route('/')
def index():
    return render_template('index.html', session=session)

@app.route('/sql_injection', methods=['GET', 'POST'])
def sql_injection():
    if request.method == 'POST':
        username = request.form.get('username')
        if username == 'admin':  # Simulating SQL Injection vulnerability
            session['completed_challenges'] = session.get('completed_challenges', []) + ['sql_injection']
            return redirect(url_for('index'))
        else:
            error = "No user found."
            return render_template('sql_injection.html', error=error)
    return render_template('sql_injection.html')

@app.route('/xxe', methods=['GET', 'POST'])
def xxe():
    if 'sql_injection' not in session.get('completed_challenges', []):
        return redirect(url_for('index'))

    if request.method == 'POST':
        xml_data = request.form.get('xml')
        if 'XXE' in xml_data:  # Simulating XXE vulnerability
            session['completed_challenges'] = session.get('completed_challenges', []) + ['xxe']
            return redirect(url_for('index'))
        else:
            error = "Invalid XML."
            return render_template('xxe.html', error=error)
    return render_template('xxe.html')

@app.route('/lfi', methods=['GET', 'POST'])
def lfi():
    if 'xxe' not in session.get('completed_challenges', []):
        return redirect(url_for('index'))

    if request.method == 'POST':
        file = request.form.get('file')
        if file == 'flag.txt':  # Simulating LFI vulnerability
            session['completed_challenges'] = session.get('completed_challenges', []) + ['lfi']
            return redirect(url_for('index'))
        else:
            error = "File not found."
            return render_template('lfi.html', error=error)
    return render_template('lfi.html')

@app.route('/rce', methods=['GET', 'POST'])
def rce():
    if 'lfi' not in session.get('completed_challenges', []):
        return redirect(url_for('index'))

    if request.method == 'POST':
        cmd = request.form.get('cmd')
        if 'echo' in cmd:  # Simulating RCE vulnerability
            session['completed_challenges'] = session.get('completed_challenges', []) + ['rce']
            return redirect(url_for('index'))
        else:
            error = "Invalid command."
            return render_template('rce.html', error=error)
    return render_template('rce.html')

if __name__ == '__main__':
    app.run(debug=True)
