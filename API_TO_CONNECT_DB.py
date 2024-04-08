#!/usr/bin/env python
# coding: utf-8

# In[2]:


from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database connection
db = mysql.connector.connect(
    host="localhost",
    user="your user id",
    password="your password",
    database="testing"
)
cursor = db.cursor()

# API endpoint for updating data
@app.route('/Post_data', methods=['POST'])
def Post_data():
    try:
        _json = request.json
        if _json is None:
            return jsonify({'error': 'Request body must be JSON'}), 400 
        
        _id  = _json.get('id')
        _name = _json.get('name')
        _email = _json.get('email')
        _phone = _json.get('phone')
        _address = _json.get('address')

        if _id and _name and _email and _phone and _address:
            sql = "INSERT INTO emp(id,name, email, phone, address) VALUES(%s, %s, %s, %s,%s)"
            bindData = (_id,_name, _email, _phone, _address)
            cursor.execute(sql, bindData)
            db.commit()

            return jsonify({'message': 'Data updated successfully'})
        else:
            return jsonify({'error': 'Missing data in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        # Extract id from query parameters
        id = request.args.get('id')
        if id is None:
            return jsonify({'error': 'ID parameter is missing'}), 400

        # Retrieve data from MySQL database
        sql = "SELECT * FROM emp WHERE id = %s"
        cursor.execute(sql, (id,))
        data = cursor.fetchone()

        if data is None:
            return jsonify({'error': 'No data found for the given ID'}), 404

        # Convert result to dictionary and return
        result = {
            'id': data[0],
            'name': data[1],
            'email': data[2],
            'phone': data[3],
            'address': data[4]
        }
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 

@app.route('/emp', methods=['GET'])
def get_emp():
    try:
        sql = 'SELECT * FROM emp'
        cursor.execute(sql)
        rows = cursor.fetchall()

        # Check if any data found
        if not rows:
            return jsonify({'error': 'No data found'}), 404

        # Prepare response data
        results = []
        for row in rows:
            emp_dict = {
                'id': row[0],
                'name': row[1],
                'email': row[2],
                'phone': row[3],
                'address': row[4]
            }
            results.append(emp_dict)

        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    
@app.route('/update', methods=['PUT'])
def update_data():
    try:
        _json = request.json
        if _json is None:
            return jsonify({'error': 'Request body must be JSON'}), 400 
        
        _id = _json.get('id')
        _name = _json.get('name')
        _email = _json.get('email')
        _phone = _json.get('phone')
        _address = _json.get('address')

        if _id and _name and _email and _phone and _address:
            # Ensure the order of variables in bindData matches the SQL placeholders
            sql = "UPDATE emp SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
            bindData = (_name, _email, _phone, _address, _id)  # Correct order
            cursor.execute(sql, bindData)
            db.commit()

            return jsonify({'message': 'Data updated successfully'})
        else:
            return jsonify({'error': 'Missing data in request'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500 
    
@app.route('/delete', methods=['DELETE'])
def delete():
    try:
        # Retrieve the id parameter from the request
        id = request.args.get('id')

        # Check if id parameter is provided
        if id is None:
            return jsonify({'error': 'ID parameter is missing'}), 400

        # Construct and execute SQL query
        sql = "DELETE FROM emp WHERE id = %s"
        cursor.execute(sql, (id,))
        db.commit()

        # Create and return response
        response = jsonify({'message': 'Employee deleted successfully!'})
        response.status_code = 200
        return response
    except Exception as e:
        # Return error response in case of any exception
        return jsonify({'error': str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:




