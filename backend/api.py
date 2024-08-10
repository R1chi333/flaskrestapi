from flask import Flask
from flask_restful import Resource, Api, reqparse
import pyodbc
from flask_cors import CORS
import textwrap
from datetime import datetime

app = Flask(__name__)
CORS(app)
api = Api(app)


class Houses(Resource):
    server = 'localhost, 1433'
    database = 'Flask Tutorial'
    username = 'sa'  
    password = 'FlaskTut101'  
    def get(self):
        cnxn = pyodbc.connect(
        f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
         )
        cursor = cnxn.cursor()
        cursor.execute('SELECT * FROM houses')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        houses = [dict(zip(columns, row)) for row in rows]
        cursor.close()
        cnxn.close()
        houses.reverse()
        return houses
    
    def post(self):
        house_args = reqparse.RequestParser()
        house_args.add_argument('house_address', type=str, required=True, help="House address cannot be blank")
        house_args.add_argument('zip_code', type=str, required=True, help="Zip code cannot be blank")
        house_args.add_argument('price', type=float, required=True, help="Price cannot be blank")
        house_args.add_argument('beds', type=int, required=True, help="Number of beds cannot be blank")
        house_args.add_argument('baths', type=float, required=True, help="Number of baths cannot be blank")
        house_args.add_argument('sqft', type=int, required=True, help="Square footage cannot be blank")
        house_args.add_argument('property_type', type=str, required=True, help="Property type cannot be blank")
        house_args.add_argument('current_status', type=str, required=True, help="Current status cannot be blank")
        house_args.add_argument('image_link', type=str, required=False, help="Image link for the house")
        args = house_args.parse_args()


        server = 'localhost, 1433'
        database = 'Flask Tutorial'
        username = 'sa'  
        password = 'FlaskTut101'  
        cnxn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        )
        cursor = cnxn.cursor()
        insert_query = textwrap.dedent('''
            INSERT INTO houses (house_address, zip_code, price, beds, baths, sqft, property_type, current_status, image_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        ''')
        cursor.execute(insert_query, (args['house_address'], args['zip_code'], args['price'], args['beds'], args['baths'], args['sqft'], args['property_type'], args['current_status'], args.get('image_link')))
        cnxn.commit()
        cursor.execute('SELECT * FROM houses')    
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        def convert_row(row):
            row_dict = dict(zip(columns, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = value.isoformat()  # Convert datetime to ISO format
            return row_dict
        # Convert rows to dictionaries
        result = [convert_row(row) for row in rows]

        cursor.close()
        cnxn.close()
        return {'houses': result}, 201
    
    def put(self):
        house_args = reqparse.RequestParser()
        house_args.add_argument('id', type=int, required=True, help="ID cannot be blank")
        house_args.add_argument('house_address', type=str, required=True, help="House address cannot be blank")
        house_args.add_argument('zip_code', type=str, required=True, help="Zip code cannot be blank")
        house_args.add_argument('price', type=float, required=True, help="Price cannot be blank")
        house_args.add_argument('beds', type=int, required=True, help="Number of beds cannot be blank")
        house_args.add_argument('baths', type=float, required=True, help="Number of baths cannot be blank")
        house_args.add_argument('sqft', type=int, required=True, help="Square footage cannot be blank")
        house_args.add_argument('property_type', type=str, required=True, help="Property type cannot be blank")
        house_args.add_argument('current_status', type=str, required=True, help="Current status cannot be blank")
        house_args.add_argument('image_link', type=str, required=False, help="Image link for the house")
        args = house_args.parse_args()

        cnxn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        )
        cursor = cnxn.cursor()
        update_query = textwrap.dedent('''
            UPDATE houses
            SET house_address = ?, zip_code = ?, price = ?, beds = ?, baths = ?, sqft = ?, property_type = ?, current_status = ?, image_link = ?
            WHERE ID = ?;
        ''')
        cursor.execute(update_query, (args['house_address'], args['zip_code'], args['price'], args['beds'], args['baths'], args['sqft'], args['property_type'], args['current_status'], args.get('image_link'), args['id']))
        cnxn.commit()
        cursor.execute('SELECT * FROM houses WHERE ID = ?', (args['id'],))
        row = cursor.fetchone()
        columns = [desc[0] for desc in cursor.description]

        def convert_row(row):
            row_dict = dict(zip(columns, row))
            for key, value in row_dict.items():
                if isinstance(value, datetime):
                    row_dict[key] = value.isoformat()  # Convert datetime to ISO format
            return row_dict

        result = convert_row(row)
        cursor.close()
        cnxn.close()
        return {'house': result}, 200

    def delete(self):
        house_args = reqparse.RequestParser()
        house_args.add_argument('id', type=int, required=True, help="ID cannot be blank")
        args = house_args.parse_args()
        cnxn = pyodbc.connect(
            f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        )
        cursor = cnxn.cursor()
        delete_query = textwrap.dedent('''
            DELETE FROM houses
            WHERE id = ?;
        ''')
        cursor.execute(delete_query, (args['id'],))
        cnxn.commit()
        cursor.close()
        cnxn.close()
        return {'message': 'House deleted'}, 200

api.add_resource(Houses, '/api/houses/')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'



if __name__ == '__main__':
    app.run(debug=True)