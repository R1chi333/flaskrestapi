from flask import Flask
from flask_restful import Resource, Api
import pyodbc
import textwrap

app = Flask(__name__)
api = Api(app)

def getData(Resource):
    server = 'localhost, 1433'
    database = 'Flask Tutorial'
    username = 'sa'  
    password = 'FlaskTut101'  

    cnxn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    )
    cursor = cnxn.cursor()

    cursor.execute('SELECT * FROM People')
    rows = cursor.fetchall()

    # Get column names from cursor description
    columns = [desc[0] for desc in cursor.description]

    # Highlighted Conversion Part
    # Convert rows to list of dictionaries
    data = [dict(zip(columns, row)) for row in rows]
    data.reverse()
    cursor.close()
    cnxn.close()    
    return data


api.add_resource(getData, '/api/')





if __name__ == '__main__':
    app.run(debug=True)