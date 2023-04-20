from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import mysql.connector


app = Flask(__name__)

# Route to render index.html template


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# Connect to the database
mydb = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "parking_database",
    "port": "3307",
}

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_size=31, **mydb)


@app.route('/get_slots', methods=['POST'])
def get_slots():
    cnx = cnxpool.get_connection()
    cur = cnx.cursor()
    # Get the mall_id from the AJAX request
    mall_id = request.form.get('mall_id')

    if not mall_id:

        return jsonify({'error': 'Invalid mall_id', 'abc': mall_id})

    # Query the database for the latest entry for the given mall_id
    cur.execute(
        'SELECT slots_available, slots_occupied, slots_total FROM parking_data WHERE client_id = %s ORDER BY id DESC LIMIT 1', (mall_id,))
    row = cur.fetchone()
    print(row)
    # Check if row is None, and return an error response if it is
    if row is None:
        return jsonify({'error': 'No data found for mall_id {}'.format(mall_id)})

    # Create a dictionary of the slot data and return as a JSON response
    slot_data = {
        'available_slots': row[0], 'occupied_slots': row[1], 'total_slots': row[2]}

    print(slot_data)
    return jsonify(slot_data)


@app.route('/get-data/<int:mall_id>', methods=['GET'])
def get_mall_data(mall_id):
    # Connect to the database
    cnx = cnxpool.get_connection()
    cur = cnx.cursor()

    # Query the database to fetch data for the specified mall
    cur.execute(
        'SELECT zone_id, slots_available, slots_occupied, slots_total FROM parking_data WHERE client_id = %s', (mall_id,))
    rows = cur.fetchall()

    # Convert the result set to a list of dictionaries
    result = []
    for row in rows:
        data = {}
        data['floor'] = row[0]
        data['available'] = row[1]
        data['occupied'] = row[2]
        data['total'] = row[3]
        result.append(data)

    print(result)
    # Close the database connection
    cur.close()

    # Return the result as JSON
    return jsonify(result)


@app.route('/search')
def search():
    query = request.args.get('q')
    # handle search query and return results as JSON
    results = [{"name": "Result 1", "url": "/result1"},
               {"name": "Result 2", "url": "/result2"}]
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)
