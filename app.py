from flask import Flask, render_template_string, request, redirect, url_for
from minidb import MiniDB

app = Flask(__name__)
db = MiniDB()

# HTML Template inside the file for simplicity
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pesapal Challenge App</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .form-group { margin-bottom: 10px; }
        input { padding: 5px; width: 200px; }
        button { padding: 5px 15px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>🛒 Simple Order System</h1>
    <p><i>Powered by Custom Python RDBMS</i></p>

    <div style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
        <h3>1. Create User</h3>
        <form action="/add_user" method="POST">
            <input type="text" name="id" placeholder="User ID (e.g., 1)" required>
            <input type="text" name="name" placeholder="Name" required>
            <input type="text" name="email" placeholder="Email" required>
            <button type="submit">Add User</button>
        </form>
    </div>
    <br>
    
    <div style="background: #f0f0f5; padding: 15px; border-radius: 5px;">
        <h3>2. Create Order</h3>
        <form action="/add_order" method="POST">
            <input type="text" name="order_id" placeholder="Order ID (e.g., 101)" required>
            <input type="text" name="user_id" placeholder="User ID (must exist)" required>
            <input type="text" name="item" placeholder="Item Name" required>
            <button type="submit">Place Order</button>
        </form>
    </div>

    <hr>

    <h3>📊 Admin View: Who Ordered What? (SQL JOIN)</h3>
    <p><i>Query: SELECT * FROM users JOIN orders ON users.id = orders.user_id</i></p>
    
    <table>
        <tr>
            <th>User ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Order ID</th>
            <th>User ID (FK)</th>
            <th>Item</th>
        </tr>
        {% for row in rows %}
        <tr>
            {% for col in row %}
            <td>{{ col }}</td>
            {% endfor %}
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

# Initialize DB with Tables if they don't exist
db.execute("CREATE TABLE users (id, name, email)")
db.execute("CREATE TABLE orders (id, user_id, item)")

@app.route('/')
def index():
    # Perform a JOIN to show the "RDBMS" power
    # Note: Our mini parser expects this specific syntax
    data = db.execute("SELECT * FROM users JOIN orders ON users.id = orders.user_id")
    
    # If DB is empty, data might be a string message, handle that
    if isinstance(data, str): 
        data = []
        
    return render_template_string(HTML, rows=data)

@app.route('/add_user', methods=['POST'])
def add_user():
    id = request.form['id']
    name = request.form['name']
    email = request.form['email']
    # Insert
    db.execute(f"INSERT INTO users VALUES ('{id}', '{name}', '{email}')")
    return redirect(url_for('index'))

@app.route('/add_order', methods=['POST'])
def add_order():
    o_id = request.form['order_id']
    u_id = request.form['user_id']
    item = request.form['item']
    # Insert
    db.execute(f"INSERT INTO orders VALUES ('{o_id}', '{u_id}', '{item}')")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)