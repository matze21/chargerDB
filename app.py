from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import configparser

app = Flask(__name__)

def get_db_connection():
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    db_config = config['database']
    conn = psycopg2.connect(
        host=db_config['host'],
        database=db_config['database'],
        user=db_config['username'],
        password=db_config['password']
    )
    return conn

@app.route('/api/v1/pricing/current', methods=['GET'])
def get_current_pricing():
    """ Get price from a time and charger id, this is independent of the server time 
        example: http://127.0.0.1:5000/api/v1/pricing/current?charger_id=1&time=12:00
    """
    charger_id = request.args.get('charger_id')
    time = request.args.get('time')

    if not charger_id or not time:
        return jsonify({'error': 'Missing required parameters'}), 400

    query = """
        WITH filteredChargers AS (
          SELECT *
          FROM EV_Chargers c
          WHERE c.charger_id = %s
        )
        SELECT fc.charger_id, ts.start_time, ts.end_time, ts.price_per_kwh
        FROM filteredChargers fc 
        JOIN Charger_Schedule_Assignment csa ON fc.charger_id = csa.charger_id
        JOIN Pricing_Schedules ps ON csa.schedule_id = ps.schedule_id
        JOIN Time_Slots ts ON ps.schedule_id = ts.schedule_id
        WHERE %s BETWEEN ts.start_time AND ts.end_time;
    """
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(query, (charger_id, time))
    pricing_info = cursor.fetchall()
    cursor.close()
    conn.close()

    # Convert datetime objects to strings
    for item in pricing_info:
        if 'start_time' in item:
            item['start_time'] = item['start_time'].strftime('%H:%M:%S')
        if 'end_time' in item:
            item['end_time'] = item['end_time'].strftime('%H:%M:%S')

    return jsonify(pricing_info)

@app.route('/api/v1/schedules/<string:charger_id>', methods=['PUT'])
def update_schedule(charger_id):
    """ update schedule of a charger station
        e.g. changing charger 1 to schedule 2
        curl -X PUT http://127.0.0.1:5000/api/v1/schedules/1 \
        -H "Content-Type: application/json" \
        -d '{"schedule_id": "2"}'
    """
    data = request.json
    schedule_id = data.get('schedule_id')
    
    if not schedule_id:
        return jsonify({'error': 'Missing schedule ID'}), 400

    query = """
        UPDATE Charger_Schedule_Assignment 
        SET schedule_id = %s 
        WHERE charger_id = %s;
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, (schedule_id,charger_id))
    
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'Schedule updated successfully.'}), 200

@app.route('/api/v1/pricing/<int:schedule_id>', methods=['PATCH'])
def update_price(schedule_id):
    """ update price of a specific time bin of a schedule
        e.g. changing charger 1 to schedule 2
        curl -X PATCH http://127.0.0.1:5000/api/v1/pricing/1 \
        -H "Content-Type: application/json" \
        -d '{"start_time": "00:00", "end_time": "06:00", "price_per_kwh": 0.3}'
    """
    data = request.json
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    price_per_kwh = data.get('price_per_kwh')

    if not start_time or not end_time or price_per_kwh is None:
        return jsonify({'error': 'Missing required fields'}), 400

    query = """
        UPDATE time_slots 
        SET price_per_kwh = %s 
        WHERE schedule_id = %s AND start_time = %s AND end_time = %s;
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(query, (price_per_kwh, schedule_id, start_time, end_time))
    
    conn.commit()
    
    if cursor.rowcount == 0:
        return jsonify({'error': 'No matching time slot found.'}), 404
    
    cursor.close()
    conn.close()

    return jsonify({'message': 'Price updated successfully.'}), 200

@app.route('/api/v1/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """ delete a schedule with its time slots and remove references
        sets the id of the charger to NULL!
        e.g.
        curl -X DELETE http://127.0.0.1:5000/api/v1/schedules/1
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")

        cursor.execute("UPDATE Charger_Schedule_Assignment SET schedule_id = NULL WHERE schedule_id = %s", (schedule_id,))
        cursor.execute("DELETE FROM time_slots WHERE schedule_id = %s", (schedule_id,))
        cursor.execute("DELETE FROM Pricing_Schedules WHERE schedule_id = %s", (schedule_id,))
        
        # If no rows were affected, rollback and return an error
        if cursor.rowcount == 0:
            cursor.execute("ROLLBACK")
            return jsonify({'error': 'No schedule found to delete.'}), 404

        cursor.execute("COMMIT")
        return jsonify({'message': 'Schedule deleted successfully.'}), 200

    except Exception as e:
        # If any error occurs, rollback the transaction
        cursor.execute("ROLLBACK")
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

@app.route('/api/v1/schedules', methods=['POST'])
def create_schedule():
    """ create a schedule with its timeslots
        curl -X POST http://127.0.0.1:5000/api/v1/schedules \
        -H "Content-Type: application/json" \
        -d '{
            "schedule_name":"weekday_2","effective_from":"2024-11-01","effective_to":"2024-12-01",
            "time_slots":[
                {"start_time": "00:00", "end_time": "06:00", "price_per_kwh": 0.1},
                {"start_time": "06:00", "end_time": "15:00", "price_per_kwh": 0.2},
                {"start_time": "15:00", "end_time": "21:00", "price_per_kwh": 0.3},
                {"start_time": "21:00", "end_time": "23:59", "price_per_kwh": 0.4}
            ]
        }'
    """
    data = request.json
    schedule_name = data.get('schedule_name')
    eff_from = data.get('effective_from')
    eff_to = data.get('effective_to')
    
    if not schedule_name or 'time_slots' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("BEGIN")
        query_schedule = "INSERT INTO pricing_schedules (schedule_name,effective_from,effective_to) VALUES (%s,%s,%s) RETURNING schedule_id;"

        cursor.execute(query_schedule, (schedule_name,eff_from,eff_to,))
        new_schedule_id = cursor.fetchone()['schedule_id']

        # Insert time slots for this schedule
        time_slots = data['time_slots']

        for slot in time_slots:
            start_time = slot['start_time']
            end_time = slot['end_time']
            price_per_kwh = slot['price_per_kwh']

            query_timeslot = """
                INSERT INTO time_slots (schedule_id, start_time, end_time, price_per_kwh)
                VALUES (%s, %s, %s, %s);
            """

            cursor.execute(query_timeslot, (new_schedule_id, start_time, end_time, price_per_kwh))

        conn.commit()

    except Exception as e:
        # If any error occurs, rollback the transaction
        cursor.execute("ROLLBACK")
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conn.close()

    return jsonify({
        'message': 'Schedule and time slots created successfully.',
        'schedule_id': new_schedule_id
     }), 201

if __name__ == '__main__':
     app.run(debug=True)