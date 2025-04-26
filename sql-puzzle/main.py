from flask import Flask, request, g
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'products.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(_):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL
            );
        ''')
        cursor.execute(f'''
            INSERT INTO products (name, category) VALUES ('Easy flag: {os.environ.get("FLAG")}', 'MISC')
        ''')
        cursor.execute(f'''
            INSERT INTO products (name, category) VALUES ('Not The Flag', 'MISC')
        ''')
        cursor.execute(f'''
            INSERT INTO products (name, category) VALUES ('Keyboard', 'PC');
        ''')
        cursor.execute(f'''
            INSERT INTO products (name, category) VALUES ('Mouse', 'PC');
        ''')
        db.commit()


@app.route('/', methods=['GET'])
def index():
    return f"""
        <html>
            <head>
                <title>Online Store</title>
            </head>
            <body>
                <h1>Add a new product or view the last one!</h1>
               <form action="/add" method="POST">
                    <label for="product_name">Product Name: </label>
                    <input name="product_name" type="text"/>
               </form> 
               <hr/>
                <a href="/last?category=MISC">View the last product in the <code>MISC</code> category</a>
                <br/>
                <a href="/last?category=PC">View the last product in the <code>PC Components</code> category</a>
            </body>
        </html>
    """

@app.route('/last', methods=['GET'])
def profile():
    db = get_db()
    cursor = db.cursor()
    category = request.args.get('category')
    if category is None:
        return "Expected a category"

    if len(category) > 15:
        return "Category name is too long"

    query = f"SELECT name FROM products WHERE category = '{category}'"
    cursor.execute(query)
    result = cursor.fetchall()

    if len(result) == 0:
        return "No products found"
    last = result[-1]

    return f"'{last[0]}' is the last product", 200

@app.route('/add', methods=['POST'])
def add():
    return "You can't add items :/"

if __name__ == '__main__':
    init_db()
    app.run(debug=False, port=3000, host='0.0.0.0')
