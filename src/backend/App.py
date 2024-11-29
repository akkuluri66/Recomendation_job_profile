# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from flask_socketio import SocketIO
# from pymongo import MongoClient, errors
# import google.generativeai as genai
# import time
# import json


# app = Flask(__name__)
# # CORS(app)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
# socketio = SocketIO(app, cors_allowed_origins="*")
# uri = "mongodb+srv://suryatejaaiproject:ZgQ7ACyPHcVUyHW2@cluster0.atwu66p.mongodb.net/"
# global ans
# ans = ""

# try:
#     client = MongoClient(uri)
#     client.admin.command('ismaster')
#     print("Connected to the database successfully.")
# except errors.ConnectionFailure:
#     print("Failed to connect to the database.")

# db = client['RealTimeDataAnalysis']
# users_collection = db['profiles_ind']
# jobs = db['companies']


# @app.route('/signup', methods=['POST'])
# def signup():
#     data = request.get_json()
#     # print(data)

#     # Retrieve form data
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     email = data.get('email')
#     password = data.get('password')
#     confirm_password = data.get('confirm_password')
  

#     # Additional fields for recruiter
    
#     # Check if the email already exists
#     if users_collection.find_one({'email': email}):
#         return jsonify({'error': 'User already exists'}), 409

#     # Hash the password
#     password_hash = password

#     # Create common user data with role
#     user_data = {
#         'firstname': first_name,
#         'lastname': last_name,
#         'email': email,
#         'password': password_hash,
        
#     }
  
#     users_collection.insert_one(user_data)  # Insert user into UsersDetails

#     # Insert the common user data into the users collection


#     return jsonify({'message': 'User created successfully'}), 201


# global_mail=""
# @app.route('/login', methods=['POST'])
# def login():
#     global global_mail
#     data = request.get_json()
#     email = data.get('mail')
#     global_mail = email
#     password = data.get('password')
    

#     # print(data)
    
    
#     # Check if email, password, and role are provided
#     if not email or not password:
#         return jsonify({'error': 'email, password, and role are required'}), 400
    
    
    
#     # Find the user by email
    
#     user = users_collection.find_one({'email': email})
    
#     # Check if the user exists, if password is correct, and if the role matches
#     if not user:
#         return jsonify({'error': 'Invalid credentials'}), 401
    
#     if user["password"]!=password:
#         return jsonify({'error': 'Invalid credentials'}), 401
    
   
#     # Login successful
#     return jsonify({
#         'message': 'Login successful', 
#         'user': {
#             'firstname': user['firstname'], 
#             'lastname': user['lastname'], 
#             'email': user['email'], 
#         }
#     }), 200

# def convert_objectid(user):
#     if user and '_id' in user:
#         user['_id'] = str(user['_id'])
#     return user

# @app.route('/profile', methods=['GET'])
# def get_profile():
#     # Assuming you have authenticated the user and have their email available
#     email = request.args.get('email')  # Get email from query parameter or session
#     role=request.args.get('role')
    
#     user = users_collection.find_one({'email': email})
    
#     user = convert_objectid(user)
#     # print(user)
#     if user:
#         return jsonify({'data':user})
#     else:
#         return jsonify({'error': 'User not found'})
    
# @app.route('/editprofile', methods=['POST'])
# def edprofile():
#     data = request.get_json()
#     email = data.get('email')
#     update_data = data.get('data')
#     # print(update_data)
#     update_data = {k: v for k, v in update_data.items() if v is not None}
#     if not update_data:
#         return jsonify({'error': 'No valid fields to update'})
#     try:
#         result = users_collection.update_one({'email': email}, {'$set': update_data})
#         if result.modified_count == 0:
#             return jsonify({'error': 'No profile found to update'})
#         return jsonify({'message': 'Profile updated successfully'})
#     except Exception as e:
#         # print(f"Error updating profile: {e}")
#         return jsonify({'error': 'An error occurred while updating the profile'})
    
    
# import math
# from pymongo import MongoClient
# import time
# import requests

# def haversine_distance(lat1, lon1, lat2, lon2):
#     # Radius of the Earth in kilometers (use 3958.8 for miles)
#     R = 6371.0  

#     # Convert latitude and longitude from degrees to radians
#     lat1_rad = math.radians(lat1)
#     lon1_rad = math.radians(lon1)
#     lat2_rad = math.radians(lat2)
#     lon2_rad = math.radians(lon2)

#     # Differences in coordinates
#     dlat = lat2_rad - lat1_rad
#     dlon = lon2_rad - lon1_rad

#     # Haversine formula
#     a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

#     # Distance in kilometers
#     distance = R * c
#     return distance

# def calculate_priority(user1, user2):
#     # Check if 'education' exists and has at least one entry for both users
#     if 'education' in user1 and 'education' in user2:
#         if len(user1['education']) > 0 and len(user2['education']) > 0:
#             if user1['education'][0]['institution'] == user2['education'][0]['institution']:
#                 return 1  # Same current school

#     # Check if 'companies' exists and has at least one entry for both users
#     if 'companies' in user1 and 'companies' in user2:
#         if len(user1['companies']) > 0 and len(user2['companies']) > 0:
#             if user1['companies'][0]['name'] == user2['companies'][0]['name']:
#                 return 2  # Same current company

#     # Check for matching past schools
#     if 'education' in user1 and 'education' in user2:
#         for edu1 in user1['education'][1:]:
#             for edu2 in user2['education'][1:]:
#                 if edu1['institution'] == edu2['institution']:
#                     return 3  # Same past school

#     # Check for matching past companies
#     if 'companies' in user1 and 'companies' in user2:
#         for comp1 in user1['companies'][1:]:
#             for comp2 in user2['companies'][1:]:
#                 if comp1['name'] == comp2['name']:
#                     return 4  # Same past company

#     return 5  # No match


# def calculate_distances_for_all_users(main_user,users):
    
   
#     v=0
   
#     priority=[]
  

#     distances=[]
#     priority=[]
#     # print(main_user['location'])
#     origin=[float(main_user['location']['lat']),float(main_user['location']['lon'])]
   
#     for user in users:
#         if user["_id"] == main_user["_id"]:
#             continue  # Skip comparing the user with themselves
#         # distance = haversine_distance(float(main_user['location']['lat']), float(main_user['location']['lon']),
#         #                               float(user['location']['lat']), float(user['location']['lon']))
#         priority.append(calculate_priority(main_user, user))
#         des=[float(user['location']['lat']),float(user['location']['lon'])]

#         distances.append(haversine_distance(origin[0],origin[1],des[0],des[1]))
        
  
       
#     return distances,priority

# def gmain(email):
#       # Start time tracking
#     # start_time = time.time()

#     # MongoDB connection
#     client = MongoClient('mongodb+srv://suryatejaaiproject:ZgQ7ACyPHcVUyHW2@cluster0.atwu66p.mongodb.net/')
#     db = client['RealTimeDataAnalysis']
#     collection = db['profiles_ind']
    
#     # Fetch all users
#     users = list(collection.find())
#     # print(email)
#     main_user = collection.find_one({'email': email})
#     # print(main_user)
#     # main_user={"_id":{"$oid":"672282bc1e5d932bd8e85d71"},"firstname":"Anika","lastname":"Gupta","education":[{"degree":"B.Tech Computer Science","institution":"Indian Institute of Technology Delhi","graduatedyear":{"$numberInt":"2018"}},{"degree":"M.Tech Computer Science","institution":"Indian Institute of Technology Bombay","graduatedyear":{"$numberInt":"2020"}},{"degree":"PhD Computer Science","institution":"Indian Institute of Science","graduatedyear":{"$numberInt":"2024"}}],"companies":[{"name":"Google India","position":"Software Engineer","experience":{"$numberInt":"3"}},{"name":"Amazon India","position":"Senior Software Engineer","experience":{"$numberInt":"2"}},{"name":"Microsoft India","position":"Software Development Manager","experience":{"$numberInt":"1"}}],"skills":["Java","Python","Cloud Computing","AWS","Azure","DevOps"],"location":{"lat":"28.6139","lon":"77.2090","address":"New Delhi"}}

#     distances,priority = calculate_distances_for_all_users(main_user,users)

#     # print(len(distances),len(priority),len(users))

#     sorted_users=[]
#     for i in range(len(users)-1):

#         sorted_users.append([priority[i],distances[i],i+1])

#     sorted_users.sort()
    
#     # print(sorted_users[:20])

#     result=[]
#     for i in range(len(sorted_users)):
#         ind=sorted_users[i][2]
#         result.append(users[ind])
#     return result



# from bson import ObjectId

# @app.route('/usersrec', methods=['POST'])
# def fun():
#     data = request.json  
#     # print(data)
#     email = data['params']['email']
#     result = gmain(email)  # Assuming `gmain(email)` returns a list of MongoDB documents
    
#     # Convert each document's ObjectId to a string
#     for doc in result:
#         if "_id" in doc:
#             doc["_id"] = str(doc["_id"])
    
#     # print(result)
#     return jsonify(result)

# g_apikey = "AIzaSyAJfU8UX4Uz4YlfIawrzfZ81Xz8bIeBZAE"
# genai.configure(api_key=g_apikey)
# model = genai.GenerativeModel('gemini-1.5-flash',
#                               generation_config={"response_mime_type": "application/json"})

# @app.route('/jobrec', methods=['POST'])
# def funnn():
#     data = request.json 
#     print(data)
#     email = data['params']['email']
#     user = users_collection.find_one({'email': email})
#     lst=[]
#     l = list(jobs.find())
#     st=0
#     cnt=15
#     while cnt<=len(l):
#         response = model.generate_content(str(l[st:cnt])+"""\n\n\nfor the above all 15 job description rate the below candidate out of 100 by considering skills, past experience and education of the candidate. If the eligibility criteria is not met by the candidate give rating as 0  in the given format:\n\n {{"_id":{"$oid":"6727856bfd969e51f45506de"},'rating':int},{..},..}, \n\n\n"""+ str(user))
#         score = json.loads(response.text)
#         # print(response.text)
#         # print(score)
#         # for i in range(15):
#         #     jd = l[i]
#         #     response = model.generate_content(str(jd)+"""\n\n\nfor the above job description rate the below candidate out of 5 by considering skills, past experience and education of the candidate. If the eligibility criteria is not met by the candidate give rating as 0  in the given format:\n\n{'rating':int, 'parameters':{'str':'int',etc..}, 'factors':{'str','str',etc...}}\n\n\n"""+ str(user))
#         #     score = json.loads(response.text)
#         #     rating = score['rating']
#         #     lst.append([rating,i])
#         k=st
#         for i in score:
#             sc=int(i['rating'])
#             lst.append([sc,k])
#             k+=1
#         st=cnt
#         if cnt+15<len(l):
#             cnt+=15
#         elif cnt<len(l):
#             cnt=len(l)
#         else:
#             break
#         print(cnt)
#     print(lst)
#     lst.sort(reverse=True)
#     ans = []
#     for i in lst:
#         ans.append(l[i[1]])
#     for doc in ans:
#         if "_id" in doc:
#             doc["_id"] = str(doc["_id"])
#     # print(ans)
#     return jsonify(ans)
    
# if __name__ == '__main__':
#     socketio.run(app, debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from pymongo import MongoClient, errors
import google.generativeai as genai
import time
import json


app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
socketio = SocketIO(app, cors_allowed_origins="*")
uri = "mongodb+srv://suryatejaaiproject:ZgQ7ACyPHcVUyHW2@cluster0.atwu66p.mongodb.net/"
global ans
ans = ""

try:
    client = MongoClient(uri)
    client.admin.command('ismaster')
    print("Connected to the database successfully.")
except errors.ConnectionFailure:
    print("Failed to connect to the database.")

db = client['RealTimeDataAnalysis']
users_collection = db['profiles_ind']
jobs = db['companies']


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    # print(data)

    # Retrieve form data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
  

    # Additional fields for recruiter
    
    # Check if the email already exists
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'User already exists'}), 409

    # Hash the password
    password_hash = password

    # Create common user data with role
    user_data = {
        'firstname': first_name,
        'lastname': last_name,
        'email': email,
        'password': password_hash,
        
    }
  
    users_collection.insert_one(user_data)  # Insert user into UsersDetails

    # Insert the common user data into the users collection


    return jsonify({'message': 'User created successfully'}), 201


global_mail=""
@app.route('/login', methods=['POST'])
def login():
    global global_mail
    data = request.get_json()
    email = data.get('mail')
    global_mail = email
    password = data.get('password')
    

    # print(data)
    
    
    # Check if email, password, and role are provided
    if not email or not password:
        return jsonify({'error': 'email, password, and role are required'}), 400
    
    
    
    # Find the user by email
    
    user = users_collection.find_one({'email': email})
    
    # Check if the user exists, if password is correct, and if the role matches
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if user["password"]!=password:
        return jsonify({'error': 'Invalid credentials'}), 401
    
   
    # Login successful
    return jsonify({
        'message': 'Login successful', 
        'user': {
            'firstname': user['firstname'], 
            'lastname': user['lastname'], 
            'email': user['email'], 
        }
    }), 200

def convert_objectid(user):
    if user and '_id' in user:
        user['_id'] = str(user['_id'])
    return user

@app.route('/profile', methods=['GET'])
def get_profile():
    # Assuming you have authenticated the user and have their email available
    email = request.args.get('email')  # Get email from query parameter or session
    role=request.args.get('role')
    
    user = users_collection.find_one({'email': email})
    
    user = convert_objectid(user)
    # print(user)
    if user:
        return jsonify({'data':user})
    else:
        return jsonify({'error': 'User not found'})
    
@app.route('/editprofile', methods=['POST'])
def edprofile():
    data = request.get_json()
    email = data.get('email')
    update_data = data.get('data')
    print(update_data)
    update_data = {k: v for k, v in update_data.items() if v is not None}
    user_data = users_collection.find_one({'email': email})
    for data in update_data:
        if data not in user_data:
            user_data[data] = update_data[data]
        if data =="education":
            for edu in update_data[data]:
                if edu['graduatedyear']!='':
                    if edu not in user_data[data]:
                        user_data[data].append(edu)
        elif data =="companies":
            for company in update_data[data]:
                if company['name']!='':
                    if company not in user_data[data]:
                        user_data[data].append(company) 
        elif data=="skills":
            if update_data[data]!='':
                l=update_data[data]
                for i in l:
                    chk=0
                    for j in user_data[data]:
                        if i.lower()==j.lower():
                            chk=1
                            break
                    if chk==0:
                        user_data[data].append(i)
        else:
            if update_data[data]!='':
                user_data[data] = update_data[data]                    
        
    if not update_data:
        return jsonify({'error': 'No valid fields to update'})
    try:
        result = users_collection.update_one({'email': email}, {'$set': user_data})
        if result.modified_count == 0:
            return jsonify({'error': 'No profile found to update'})
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        # print(f"Error updating profile: {e}")
        return jsonify({'error': 'An error occurred while updating the profile'})
    
    
import math
from pymongo import MongoClient
import time
import requests

def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers (use 3958.8 for miles)
    R = 6371.0  

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    return distance

def calculate_priority(user1, user2):
    # Check if 'education' exists and has at least one entry for both users
    if 'education' in user1 and 'education' in user2:
        if len(user1['education']) > 0 and len(user2['education']) > 0:
            if user1['education'][0]['institution'] == user2['education'][0]['institution']:
                return 1  # Same current school

    # Check if 'companies' exists and has at least one entry for both users
    if 'companies' in user1 and 'companies' in user2:
        if len(user1['companies']) > 0 and len(user2['companies']) > 0:
            if user1['companies'][0]['name'] == user2['companies'][0]['name']:
                return 2  # Same current company

    # Check for matching past schools
    if 'education' in user1 and 'education' in user2:
        for edu1 in user1['education'][1:]:
            for edu2 in user2['education'][1:]:
                if edu1['institution'] == edu2['institution']:
                    return 3  # Same past school

    # Check for matching past companies
    if 'companies' in user1 and 'companies' in user2:
        for comp1 in user1['companies'][1:]:
            for comp2 in user2['companies'][1:]:
                if comp1['name'] == comp2['name']:
                    return 4  # Same past company

    return 5  # No match


def calculate_distances_for_all_users(main_user,users):
    
   
    v=0
   
    priority=[]
  

    distances=[]
    priority=[]
    # print(main_user['location'])
    origin=[float(main_user['location']['lat']),float(main_user['location']['lon'])]
   
    for user in users:
        if user["_id"] == main_user["_id"]:
            continue  # Skip comparing the user with themselves
        # distance = haversine_distance(float(main_user['location']['lat']), float(main_user['location']['lon']),
        #                               float(user['location']['lat']), float(user['location']['lon']))
        priority.append(calculate_priority(main_user, user))
        des=[float(user['location']['lat']),float(user['location']['lon'])]

        distances.append(haversine_distance(origin[0],origin[1],des[0],des[1]))
        
  
       
    return distances,priority

def gmain(email):
      # Start time tracking
    # start_time = time.time()

    # MongoDB connection
    client = MongoClient('mongodb+srv://suryatejaaiproject:ZgQ7ACyPHcVUyHW2@cluster0.atwu66p.mongodb.net/')
    db = client['RealTimeDataAnalysis']
    collection = db['profiles_ind']
    
    # Fetch all users
    users = list(collection.find())
    # print(email)
    main_user = collection.find_one({'email': email})
    # print(main_user)
    # main_user={"_id":{"$oid":"672282bc1e5d932bd8e85d71"},"firstname":"Anika","lastname":"Gupta","education":[{"degree":"B.Tech Computer Science","institution":"Indian Institute of Technology Delhi","graduatedyear":{"$numberInt":"2018"}},{"degree":"M.Tech Computer Science","institution":"Indian Institute of Technology Bombay","graduatedyear":{"$numberInt":"2020"}},{"degree":"PhD Computer Science","institution":"Indian Institute of Science","graduatedyear":{"$numberInt":"2024"}}],"companies":[{"name":"Google India","position":"Software Engineer","experience":{"$numberInt":"3"}},{"name":"Amazon India","position":"Senior Software Engineer","experience":{"$numberInt":"2"}},{"name":"Microsoft India","position":"Software Development Manager","experience":{"$numberInt":"1"}}],"skills":["Java","Python","Cloud Computing","AWS","Azure","DevOps"],"location":{"lat":"28.6139","lon":"77.2090","address":"New Delhi"}}

    distances,priority = calculate_distances_for_all_users(main_user,users)

    # print(len(distances),len(priority),len(users))

    sorted_users=[]
    for i in range(len(users)-1):

        sorted_users.append([priority[i],distances[i],i+1])

    sorted_users.sort()
    
    # print(sorted_users[:20])

    result=[]
    for i in range(len(sorted_users)):
        ind=sorted_users[i][2]
        result.append(users[ind])
    return result



from bson import ObjectId

@app.route('/usersrec', methods=['POST'])
def fun():
    data = request.json  
    # print(data)
    email = data['params']['email']
    result = gmain(email)  # Assuming `gmain(email)` returns a list of MongoDB documents
    
    # Convert each document's ObjectId to a string
    for doc in result:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    
    # print(result)
    return jsonify(result)

g_apikey = "AIzaSyAJfU8UX4Uz4YlfIawrzfZ81Xz8bIeBZAE"
genai.configure(api_key=g_apikey)
model = genai.GenerativeModel('gemini-1.5-flash',
                              generation_config={"response_mime_type": "application/json"})

@app.route('/jobrec', methods=['POST'])
def funnn():
    data = request.json 
    print(data)
    email = data['params']['email']
    user = users_collection.find_one({'email': email})
    lst=[]
    l = list(jobs.find())
    st=0
    cnt=15
    while cnt<=len(l):
        response = model.generate_content(str(l[st:cnt])+"""\n\n\nfor the above all 15 job description rate the below candidate out of 100 by considering skills, past experience and education of the candidate. If the eligibility criteria is not met by the candidate give rating as 0  in the given format:\n\n {{"_id":{"$oid":"6727856bfd969e51f45506de"},'rating':int},{..},..}, \n\n\n"""+ str(user))
        score = json.loads(response.text)
        # print(response.text)
        # print(score)
        # for i in range(15):
        #     jd = l[i]
        #     response = model.generate_content(str(jd)+"""\n\n\nfor the above job description rate the below candidate out of 5 by considering skills, past experience and education of the candidate. If the eligibility criteria is not met by the candidate give rating as 0  in the given format:\n\n{'rating':int, 'parameters':{'str':'int',etc..}, 'factors':{'str','str',etc...}}\n\n\n"""+ str(user))
        #     score = json.loads(response.text)
        #     rating = score['rating']
        #     lst.append([rating,i])
        k=st
        for i in score:
            sc=int(i['rating'])
            lst.append([sc,k])
            k+=1
        st=cnt
        if cnt+15<len(l):
            cnt+=15
        elif cnt<len(l):
            cnt=len(l)
        else:
            break
        print(cnt)
    print(lst)
    lst.sort(reverse=True)
    ans = []
    for i in lst:
        ans.append(l[i[1]])
    for doc in ans:
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
    # print(ans)
    return jsonify(ans)
    
if __name__ == '__main__':
    socketio.run(app, debug=True)