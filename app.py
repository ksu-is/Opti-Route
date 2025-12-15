from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/route', methods=['POST'])
def route():
    origin = request.form['origin']
    dest = request.form['destination']
    mode = request.form['mode']
    
    # For now, just show the input back
    # You can add a fake route here for testing
    route_points = ["Start", "Middle", "End"]
    distance = 5.2
    time = 10
    
    return f"Origin: {origin}, Destination: {dest}, Mode: {mode}<br>" \
           f"Route: {route_points}, Distance: {distance} km, Time: {time} min"

if __name__ == '__main__':
    app.run(debug=True)
