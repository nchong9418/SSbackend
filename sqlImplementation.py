import os
import sqlite3
from flask import Flask, g, request, jsonify    
import datetime
from flask_cors import CORS

app = Flask(__name__)
DATABASE = os.path.join(os.path.dirname(__file__), 'SoakedSocks.db')
db = sqlite3.connect(DATABASE)
lastrowid = None

CORS(app) #communicate to frontend


'''
To-Do
- Implement CORS for React front-end communication
- Implement React functions by doing @app.route(/path) for each function that needs to be called to return .json data
    @app.route('/path') — Map a URL path to a function (GET by default)
    @app.route('/path', methods=['GET', 'POST']) — Specify allowed HTTP methods
    @app.post('/path') — Shorthand for POST-only route
    @app.get('/path') — Shorthand for GET-only route
    @app.put('/path'), @app.delete('/path'), @app.patch('/path') — Other HTTP verbs 
- Write-up Full documentation.
'''

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row #access col by name
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def get_item(item_id):
    db = get_db()
    cur = db.execute('SELECT * FROM "Study Groups" WHERE id = ?', (item_id,))
    item = cur.fetchone()
    if item is None:
        #Case where it isn't found 
        print('Item with id {} not found.'.format(item_id))
        return None
    return item

@app.post('/addItem')  # note: lowercase to match your frontend fetch
def add_item():
    data = request.get_json(force=True) or {}

    # pull fields with minimal touching; keep tags exactly as sent
    title         = data.get('title')
    courseCode    = data.get('courseCode')
    focusLevel    = data.get('focusLevel')
    startTime     = data.get('startTime')
    endTime       = data.get('endTime')
    location      = data.get('location')
    tags          = data.get('tags')              # string like "a,b" or "[a, b]"
    description   = data.get('description')
    hostName      = data.get('hostName')
    personLimit   = int(data.get('personLimit', 0))
    peopleSignedUp= int(data.get('peopleSignedUp', 0))
    createdAt     = datetime.datetime.now().isoformat(timespec='seconds')

    db = get_db()
    cur = db.execute(
        'INSERT INTO "Study Groups" '
        '(title, courseCode, focusLevel, startTime, endTime, location, tags, description, hostName, personLimit, peopleSignedUp, createdAt) '
        'VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
        (title, courseCode, focusLevel, startTime, endTime, location, tags, description, hostName, personLimit, peopleSignedUp, createdAt)
    )
    db.commit()

    new_id = cur.lastrowid
    row = db.execute('SELECT * FROM "Study Groups" WHERE id = ?', (new_id,)).fetchone()
    return jsonify(dict(row)), 201

def update_item(item):
    db = get_db()
    db.execute('UPDATE "Study Groups" SET title = ?, courseCode = ?, focusLevel = ?, startTime = ?, endTime = ?, location = ?, tags = ?, description = ?, hostName = ?, personLimit = ?, peopleSignedUp = ? WHERE id = ?', 
               (item['title'], item['courseCode'], item['focusLevel'], item['startTime'], item['endTime'], item['location'], item['tags'], item['description'], item['hostName'], item['personLimit'], item['peopleSignedUp'], item['id']))
    db.commit()

def personSignedUp(item_id):
    db = get_db()
    db.execute('UPDATE "Study Groups" SET peopleSignedUp = peopleSignedUp + 1 WHERE id = ?', (item_id,))
    db.commit()

@app.route('/dataBase')
def dataBase():
    db = get_db()
    cur = db.execute('SELECT * FROM "Study Groups"')
    rows = cur.fetchall()
    return jsonify([dict(row) for row in rows])


@app.get('/dataBase/singleItem/<int:id>')
def singleItem(id):
    db = get_db()
    row = db.execute('SELECT * FROM "Study Groups" WHERE id = ?', (id,)).fetchone()
    if row is None:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(dict(row))

@app.route('/SignUpPerson/<int:id>')
def SignUpPerson(id):
    personSignedUp(id)
    return jsonify({"success": True})

@app.delete('/deleteItem/<int:id>')
def deleteItem(id):
    db = get_db()
    cur = db.execute('DELETE FROM "Study Groups" WHERE id = ?', (id,))
    db.commit()
    # say whether something was deleted
    return jsonify({'deleted': cur.rowcount > 0})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
    # with app.app_context():
    #     while True:
    #         option = input("Choose an option: 1) Get Item 2) Add Item 3) Update Item 4) Sign Up Person 5) PrintTable 6) Delete item 7) Exit: ")
    #         match option:
    #             case '1':
    #                 item_id = int(input("Enter item ID: "))
    #                 item = get_item(item_id)
    #                 if item:
    #                     print(dict(item))
    #             case '2':
    #                 title = input("Enter study group title: ")
    #                 courseCode = input("Enter course code: ")
    #                 focusLevel = input("Enter focus level (Low, Medium, High): ")
    #                 startTime = input("Enter start time (YYYY-MM-DD HH:MM): ")
    #                 endTime = input("Enter end time (YYYY-MM-DD HH:MM): ")
    #                 location = input("Enter location: ")
    #                 tags = input("Enter tags (comma-separated): ")
    #                 description = input("Enter description: ")
    #                 hostName = input("Enter host name: ")
    #                 personLimit = int(input("Enter person limit: "))
    #                 peopleSignedUp = int(input("Enter number of people signed up: "))
    #                 add_item(title, courseCode, focusLevel, startTime, endTime, location, tags, description, hostName, personLimit, peopleSignedUp)
    #             case '3':
    #                 item_id = int(input("Enter item ID to update: "))
    #                 item = get_item(item_id)
    #                 if item:
    #                     item = dict(item)
    #                     item['title'] = input(f"Enter new title (current: {item['title']}): ") or item['title']
    #                     item['courseCode'] = input(f"Enter new course code (current: {item['courseCode']}): ") or item['courseCode']
    #                     item['focusLevel'] = input(f"Enter new focus level (current: {item['focusLevel']}): ") or item['focusLevel']
    #                     item['startTime'] = input(f"Enter new start time (current: {item['startTime']}): ") or item['startTime']
    #                     item['endTime'] = input(f"Enter new end time (current: {item['endTime']}): ") or item['endTime']
    #                     item['location'] = input(f"Enter new location (current: {item['location']}): ") or item['location']
    #                     item['tags'] = input(f"Enter new tags (current: {item['tags']}): ") or item['tags']
    #                     item['description'] = input(f"Enter new description (current: {item['description']}): ") or item['description']
    #                     item['hostname'] = input(f"Enter new host name (current: {item['hostName']}): ") or item['hostName']
    #                     item['personLimit'] = int(input(f"Enter new person limit (current: {item['personLimit']}): ") or item['personLimit'])
    #                     item['peopleSignedUp'] = int(input(f"Enter new number of people signed up (current: {item['peopleSignedUp']}): ") or item['peopleSignedUp'])
    #                     update_item(item)
    #                 else:
    #                     print("Item not found.")
    #             case '4':
    #                 item_id = int(input("Enter item ID to sign up a person: "))
    #                 db = get_db()
    #                 cur = db.execute('SELECT personLimit, peopleSignedUp FROM "Study Groups" WHERE id = ?', (item_id,))
    #                 item = cur.fetchone()
    #                 if item:
    #                     if item['peopleSignedUp'] < item['personLimit']:
    #                         db.execute('UPDATE "Study Groups" SET peopleSignedUp = peopleSignedUp + 1 WHERE id = ?', (item_id,))
    #                         db.commit()
    #                         print("Person signed up successfully.")
    #                     else:
    #                         print("Cannot sign up person: limit reached.")
    #                 else:
    #                     print("No item found with that ID.")
    #             case '5':
    #                 db = get_db()
    #                 cur = db.execute('SELECT * FROM "Study Groups"')
    #                 rows = cur.fetchall()
    #                 for row in rows:
    #                     print(dict(row))
    #             case '6':
    #                 get_db().execute('DELETE FROM "Study Groups" WHERE id = ?', (int(input("Enter item ID to delete: ")),))
    #                 get_db().commit()
    #                 print("Item deleted.")
    #             case '7':
    #                 break
