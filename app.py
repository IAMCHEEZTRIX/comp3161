import random
from flask import Flask, jsonify, make_response, request, session
from db import get_db_connection

app = Flask(__name__)
app.secret_key = 'COMP3161 Project'

class UserTypes:
    STUDENT_USER = "student"
    LECTURER_USER = "lecturer"
    ADMIN_USER = "sysadmin"


def is_valid_userType(userType):
    return userType.lower() == UserTypes.STUDENT_USER or userType.lower() == UserTypes.LECTURER_USER or userType.lower() == UserTypes.ADMIN_USER 

def is_valid_accountType(userType):
    return userType.lower() == UserTypes.STUDENT_USER or userType.lower() == UserTypes.LECTURER_USER

def is_student_or_lecturer(userName):
    return is_exist([userName], ["userName"],"student") or is_exist([userName], ["userName"],"lecturer")

def get_userName_by_userID(userID, userType):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT userName from {userType} WHERE {"studentID" if userType == UserTypes.STUDENT_USER else "lectureID"} = " + "%s", (userID,))
        val = cursor.fetchone()
        return val
    except Exception as e:
        print(e)
        return False

def get_usertype(userName):
    if is_exist([userName], ["userName"],"student"):
        return UserTypes.STUDENT_USER
    if is_exist([userName], ["userName"],"lecturer"):
        return UserTypes.LECTURER_USER
    return False
    
def get_userID_by_userName(userName):
    userType = get_usertype(userName)
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT {"studentID" if userType == UserTypes.STUDENT_USER else "lectureID"} from {"student" if userType == UserTypes.STUDENT_USER else "lecturer"} where userName = " + "%s", (userName,))
        val = cursor.fetchone()
        if val:
            return val[0]
        return val
    except Exception as e:
        print(e)
        return False

def is_login(userID):
    if userID in session["userName"]:
        return True
    else:
        userName = get_userName_by_userID(userID, UserTypes.STUDENT_USER)
        if not userName:
            userName = get_userName_by_userID(userID, UserTypes.LECTURER_USER)
            if not userName:
                return False
            
    if userName[0] == session["userName"]:
        return True
    return False



def is_exist(value, column, table):
    # where conditions
    con = ""
    add_and = False
    for index, val in enumerate(value):
        if add_and:
            con += " and "
        con += f"{column[index]} = '{val}'" 
        add_and = True
        
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(f"SELECT * from {table} WHERE {con}")
        val = cursor.fetchone()
        if val:
            return True
        return False
    except Exception as e:
        print(e)
        return False
    
def get_userColumns(userType):
    match userType:
        case UserTypes.STUDENT_USER:
            return {"userID": "studentID",
                    "fname": "s_fname",
                    "lname": "s_lname"}
        case UserTypes.LECTURER_USER:
            return {"userID": "lectureID",
                    "fname": "lec_fname",
                    "lname": "lec_lname"}
        case UserTypes.ADMIN_USER:
            return {"userID": "adminID",
                    "fname": "ad_fname",
                    "lname": "ad_lname"}
        case _:
            return make_response(jsonify({"error": "Invalid User Type. Should be either student, lecture or admin"}), 400)

def is_password_correct(userName, password):
    query = "SELECT * from user where username = %s and password = %s"
    user = ""
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (userName, password))
       user = cursor.fetchone()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
    if user:
        return True
    return False

def is_max_course_teaches(lectureID):
    # prepare sql statement to get the total courses a lecturer teaches
    selectData = (lectureID,)
    query = "SELECT assigned_lec, count(courseID) totalcourse FROM course WHERE assigned_lec = %s group by assigned_lec"
    
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, selectData)
       result = cursor.fetchone()
       cursor.close()
       db.close()

    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
    if not result:
        return False
    
    if result[1] >= 5:
        return True
    return False

def is_max_course_taken(studentID):
    # prepare sql statement to get the total courses a taken by a student
    selectData = (studentID,)
    query = "SELECT studentID, count(courseID) totalcoursetaken FROM registers WHERE studentID = %s GROUP BY studentID"
    
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, selectData)
       result = cursor.fetchone()
       cursor.close()
       db.close()

    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
    if not result:
        return False
    
    if result[1] >= 6:
        return True
    
    return False

def is_already_registered(studentID, courseID, academic_year, academic_term):
    # prepare sql statement
    selectData = (studentID, courseID, academic_year, academic_term)
    query = "SELECT courseID from registers where studentID = %s and courseID = %s and academic_year = %s and  academic_term = %s"
    
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, selectData)
       result = cursor.fetchone()
       cursor.close()
       db.close()
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)

    if result:
        return True
    return False

def is_lecturer_login():
    # prepare sql statement
    query = f"SELECT lectureID from {UserTypes.LECTURER_USER} where userName = " + "%s"
    
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (session["userName"],))
       result = cursor.fetchone()
       cursor.close()
       db.close()
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
    if result:
        return True
    return False

def is_student_login():
    # prepare sql statement
    query = f"SELECT studentID from {UserTypes.STUDENT_USER} where userName = " + "%s"
    
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (session["userName"],))
       result = cursor.fetchone()
       cursor.close()
       db.close()
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
    if result:
        return True
    return False

@app.route("/register/user/<userType>", methods=["POST"])
def register_user(userType):
    data = request.json
    
    # Check if user type is a valid userType
    if not is_valid_userType(userType):
        return make_response(jsonify({"error": "Invalid User type, a valid user types are student, lecturer or sysadmin"}), 400)
    
    # Users can register as a Student, Lecturer or an Admin
    # Note that a given user can be register for all user type
    if is_exist([data['userName']], ["userName"], "user"):
        
        # If user already registered as an student and want to register again as a student
        if userType == UserTypes.STUDENT_USER:
            if is_exist([data['userName']], ["userName"], "student"):
                return make_response(jsonify({"error": "User is Already Registered as a Student!"}), 400)
        
        # If user already registered as an lecture and want to register again as a lecture
        if userType == UserTypes.LECTURER_USER:
            if is_exist([data['userName']], ["userName"], "lecturer"):
                return make_response(jsonify({"error": "User is Already Registered as a Lecturer!"}), 400)
            
        # If user already registered as an admin and want to register again as a admin
        if userType == UserTypes.ADMIN_USER:
            if is_exist([data['userName']], ["userName"], "sysadmin"):
                return make_response(jsonify({"error": "User is Already Registered as a Admin!"}), 400)
    else: # User doesnt exist hence add user to the user table
        
        # Prepare sql statement for user table
        insertUserData = (data["userName"],
                    data["password"])
        Userquery = "INSERT INTO user (userName, password) VALUES (%s, %s);"
    
    # get the columns name for the type of user
    columns = get_userColumns(userType)
       
    # Prepare sql statement for the type of user table (student, lecturer or admin table)    
    insertUserTypeData = (data["userID"], data["userName"], data["fname"], data["lname"])
    UserTypequery = f"INSERT INTO {userType} ({columns["userID"]}, userName, {columns["fname"]}, {columns["lname"]}) VALUES " + "(%s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
       
       if not is_exist([data['userName']], ["userName"], "user"):
           cursor.execute(Userquery, insertUserData)
           db.commit()
           
       cursor.execute(UserTypequery, insertUserTypeData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": "User was successfully Registered!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
 

    
@app.route("/create/account/<accountType>", methods=["POST"])
def create_account(accountType):
    accountType = accountType.lower()
    data = request.json
    
    # check if account type is a valid accountType
    if not is_valid_accountType(accountType):
        return make_response(jsonify({"error": "Invalid account type, a valid account types are student and lecturer"}), 400)
    
    # You most be a User before you can create an account
    if not is_exist([data['userName']], ["userName"], "user"):
        return make_response(jsonify({"error": f"The user {data["userName"]} is not yet registered!"}), 400)
    
    # Only Student and Lecturer Users can create an account
    if not is_student_or_lecturer(data['userName']):
        return make_response(jsonify({"error": "Cannot create an account. User is not a Student or Lecturer!"}), 400)
    
    # check if a user already have an account of the same type
    if is_exist([data['ownerID'], accountType], ["ownerID", "account_type"], "account"):
        return make_response(jsonify({"error": f"User already has an {accountType} account!"}), 400)
    
    
    # Prepare sql statement for account table
    insertData = (data["ownerID"], accountType)
    query = "INSERT INTO account (ownerID, account_type) VALUES (%s, %s);"
    
    
     # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"{accountType.title()} account was created successfully!!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    
    # check if user exist
    if is_exist([data['userName']], ["userName"], "student") or is_exist([data['userName']], ["userName"], "lecturer"):
        # check if password correct
        if is_password_correct(data['userName'], data['password']):
            session["userName"] = data['userName'] 
            return make_response(jsonify({"Success": "User successfully login!"}), 201)
    
    return make_response(jsonify({"error": "incorrect Username or Password!"}), 400)   
   
        
@app.route("/logout", methods=["POST"])  
def logout():
    session.clear()
    return make_response(jsonify({"Success": "User successfully logout!"}), 201)




@app.route("/create/course", methods=["POST"])
def create_course():
    data = request.json
    
    # check if the admin is an sysadmin
    if not is_exist([data['adminID'], ], ["adminID"], "sysadmin"):
        return make_response(jsonify({"error": "This user cannot create a course. The user must be an Admin user."}), 400) 
        
    # check if course already exist
    if is_exist([data['courseID'], ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {data['courseID']} already exist."}), 400) 
        
    # check if the lecturer is a lecturer user
    if not is_exist([data['assigned_lec'], ], ["lectureID"], "lecturer"):
        return make_response(jsonify({"error": f"The lecturer with ID ({data['assigned_lec']}) does not exist."}), 400)
    
    # check if the lecture reach its allowable max course to teach
    if is_max_course_teaches(data['assigned_lec']):
        return make_response(jsonify({"error": f"The lecturer({data['assigned_lec']}) reaches his/her allowable max teachable courses"}), 400)
    
    
    # Prepare sql statement for course table
    insertCourseData = (data["courseID"], data["courseName"], data["assigned_lec"])
    coursequery = "INSERT INTO course (courseID, courseName, assigned_lec) VALUES (%s, %s, %s);"
    
    # Prepare sql statement for createcourse table
    insertCreateCourseData = (data["courseID"], data["adminID"])
    createCoursequery = "INSERT INTO createcourse (courseID, adminID) VALUES (%s, %s);"
    
    
     # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(coursequery, insertCourseData)
       db.commit()
       
       cursor.execute(createCoursequery, insertCreateCourseData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The course({data["courseID"]}) successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)

@app.route("/courses", methods=["GET"])
def get_courses():
    courses = []
    courses_list = []
    # Prepare sql statement for course table
    query = "SELECT * from course"
    
     # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query)
       courses = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, courseName, assigned_lec in courses:
        courses_list.append({
            "courseID": courseID,
            "courseName": courseName,
            "assigned_lec": assigned_lec
        })
    
    return make_response(jsonify(courses_list), 200)

@app.route("/courses/student/<studentID>", methods=["GET"])
def get_courses_by_studentID(studentID):
    courses = []
    courses_list = []
    # Prepare sql statement for course table
    query = "SELECT * from course WHERE courseID in (SELECT courseID FROM registers WHERE studentID = %s)"
    
     # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (studentID,))
       courses = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, courseName, assigned_lec in courses:
        courses_list.append({
            "courseID": courseID,
            "courseName": courseName,
            "assigned_lec": assigned_lec
        })
    
    return make_response(jsonify(courses_list), 200)


@app.route("/courses/lecturer/<lectureID>", methods=["GET"])
def get_courses_by_lectureID(lectureID):
    courses = []
    courses_list = []
    # Prepare sql statement for course table
    query = "SELECT * from course where assigned_lec = %s"
    
     # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (lectureID,))
       courses = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, courseName, assigned_lec in courses:
        courses_list.append({
            "courseID": courseID,
            "courseName": courseName,
            "assigned_lec": assigned_lec
        })
    
    return make_response(jsonify(courses_list), 200)


# CREATE TABLE registers (
#     studentID BIGINT NOT NULL,
#     courseID VARCHAR(15) NOT NULL,
#     academic_year YEAR NOT NULL,
#     academic_term VARCHAR(10) NOT NULL,
#     final_avg DECIMAL(5,2),

#     PRIMARY KEY (studentID, courseID, academic_year, academic_term)
# );
@app.route("/register/course", methods=["POST"])
def register_for_course():
    data = request.json
    
    # Check if student login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": f"The student {data['studentID']} is not login!"}), 400)
    
    # Check if student exist
    if not is_exist([data['studentID'], ], ["studentID"], "student"):
        return make_response(jsonify({"error": f"The student {data['studentID']} does not exist!"}), 400)
    
    # Check if course exist
    if not is_exist([data['courseID'], ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {data['studentID']} does not exist!"}), 400)
    
    # ckeck if student already registered for the course in the same academic year and term
    if is_already_registered(data['studentID'], data['courseID'], data['academic_year'], data['academic_term']):
        return make_response(jsonify({"error": f"The student already registered for the course {data['courseID']}"}), 400)
    
    # check if student reach their max allowable course
    if is_max_course_taken(data['studentID']):
        return make_response(jsonify({"error": f"The student {data['studentID']} reaches its max allowable course taken"}), 400)
    
    
    # Prepare sql statement for course table
    insertData = (data['studentID'], data['courseID'], data['academic_year'], data['academic_term'])
    query = "INSERT INTO registers (studentID, courseID, academic_year, academic_term) VALUES (%s,%s,%s,%s);" 
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The student({data["studentID"]}) successfully registered for the course {data["courseID"]}!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)

     
@app.route("/members/<courseID>", methods=["GET"])
def get_members_by_courseID(courseID):
    
    # Check if student login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    members = []
    members_list = []
    # Prepare sql statement for registers table
    query = "SELECT studentID FROM registers WHERE courseID = %s"
    
     # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (courseID,))
       members = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for studentID in members:
        members_list.append({
            "studentID": studentID[0]
        })
    
    return make_response(jsonify(members_list), 200)

@app.route("/create/calendar/<courseID>", methods=["POST"])
def create_calendar(courseID):
    data = request.json
    
    # Check if student login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if its a lecturer login
    if not is_lecturer_login():
        return make_response(jsonify({"error": "Only a Lecturer can create a calendar event!"}), 400)
        
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    # Prepare sql statement for calendarEvents table
    insertData = (courseID, data["event_name"], data["event_date"], data["event_desc"])
    query = "INSERT INTO calendarevents (courseID, event_name, event_date, event_desc) VALUES (%s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Calendar Event was successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)  
    
@app.route("/calendar/<courseID>", methods=["GET"])
def get_calendar_event(courseID):
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    calendar_events = []
    calendar_event_list = []
    # Prepare sql statement for registers table
    query = "SELECT courseID, event_name, event_date, event_desc FROM calendarevents WHERE courseID = %s"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (courseID,))
       calendar_events = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, event_name, event_date, event_desc in calendar_events:
        calendar_event_list.append({
            "courseID": courseID,
            "event_name": event_name,
            "event_date": event_date,
            "event_desc": event_desc
        })
    
    return make_response(jsonify(calendar_event_list), 200)


@app.route("/calendar/<studentID>/<date>", methods=["GET"])
def get_all_calendar_event_for_student_at_date(studentID, date):
    
        
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    
    calendar_events = []
    calendar_event_list = []
    # Prepare sql statement for registers table
    query = "SELECT courseID, event_name, event_date, event_desc FROM calendarEvents WHERE courseID in (SELECT courseID FROM registers WHERE studentID = %s) and event_date = %s;"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (studentID, date))
       calendar_events = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, event_name, event_date, event_desc in calendar_events:
        calendar_event_list.append({
            "courseID": courseID,
            "event_name": event_name,
            "event_date": event_date,
            "event_desc": event_desc
        })
    
    return make_response(jsonify(calendar_event_list), 200)

@app.route("/create/forum/<courseID>", methods=["POST"])
def create_forum(courseID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if its a lecturer login
    if not is_lecturer_login():
        return make_response(jsonify({"error": "Only a Lecturer can create a Forum!"}), 400)
        
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    # Prepare sql statement for calendarEvents table
    insertData = (courseID, data["topic"], data["forum_desc"], data["startdate"])
    query = "INSERT INTO forum (courseID, topic, forum_desc, startdate) VALUES (%s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Forum was successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)  
    

@app.route("/forum/<courseID>", methods=["GET"])
def get_forums(courseID):
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    forums = []
    forums_list = []
    # Prepare sql statement for registers table
    query = "SELECT courseID, topic, forum_desc, startdate FROM forum WHERE courseID = %s"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (courseID,))
       forums = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, topic, forum_desc, startdate in forums:
        forums_list.append({
            "courseID": courseID,
            "topic": topic,
            "forum_desc": forum_desc,
            "startdate": startdate
        })
    
    return make_response(jsonify(forums_list), 200)  

@app.route("/create/thread/<forumID>", methods=["POST"])  
def create_thread(forumID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
        
    # Check if forum exist
    if not is_exist([forumID, ], ["forumID"], "forum"):
        return make_response(jsonify({"error": f"The forum with ID({forumID}) does not exist!"}), 400)
    
    # Prepare sql statement for thread table
    insertData = (forumID, data["title"], data["post"])
    query = "INSERT INTO thread (forumID, title, post) VALUES (%s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"A thread was successfully added to forum {forumID}"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    

@app.route("/thread/<forumID>", methods=["GET"])
def get_threads(forumID):
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if forum exist
    if not is_exist([forumID, ], ["forumID"], "forum"):
        return make_response(jsonify({"error": f"The forum with ID({forumID}) does not exist!"}), 400)
    
    forums = []
    forums_list = []
    # Prepare sql statement for registers table
    query = "SELECT forumID, title, post, post_date FROM thread WHERE forumID = %s"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (forumID,))
       forums = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for forumID, title, post, post_date in forums:
        forums_list.append({
            "forumID": forumID,
            "title": title,
            "post": post,
            "post_date": post_date
        })
    
    return make_response(jsonify(forums_list), 200)  


@app.route("/create/reply/<threadID>", methods=["POST"])  
def create_reply(threadID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
        
    # Check if forum exist
    if not is_exist([threadID, ], ["threadID"], "thread"):
        return make_response(jsonify({"error": f"The thread with ID({threadID}) does not exist!"}), 400)
    
    # Prepare sql statement for thread table
    insertData = (threadID, data["body"], get_userID_by_userName(session["userName"]))
    query = "INSERT INTO reply (threadID, body, who_reply) VALUES (%s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"A Reply was successfully added to thread {threadID}"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    
@app.route("/reply/<threadID>/<replyID>", methods=["POST"])  
def create_reply_to_reply(threadID, replyID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if thread exist
    if not is_exist([threadID, ], ["threadID"], "thread"):
        return make_response(jsonify({"error": f"The thread with ID({threadID}) does not exist!"}), 400)
        
    # Check if reply exist
    if not is_exist([replyID, ], ["replyID"], "reply"):
        return make_response(jsonify({"error": f"The reply with ID({replyID}) does not exist!"}), 400)
    
    
    # Prepare sql statement for thread table
    insertData = (threadID, replyID, data["body"], get_userID_by_userName(session["userName"]))
    query = "INSERT INTO reply (threadID, reply_to, body, who_reply) VALUES (%s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"A Reply was successfully added to reply {replyID} of thread {threadID}"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)

@app.route("/create/section/<courseID>", methods = ["POST"])
def create_section(courseID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if its a lecturer login
    if not is_lecturer_login():
        return make_response(jsonify({"error": "Only a Lecturer can create a Section!"}), 400)
        
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    # Prepare sql statement for content table
    insertData = (courseID, data["title"], )
    query = "INSERT INTO section (courseID, title) VALUES (%s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Section was successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    
@app.route("/create/content/<sectionID>", methods=["POST"])
def create_content(sectionID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if its a lecturer login
    if not is_lecturer_login():
        return make_response(jsonify({"error": "Only a Lecturer can create a Content!"}), 400)
    
    # Check if section exist
    if not is_exist([sectionID, ], ["sectionID"], "section"):
        return make_response(jsonify({"error": f"The section {sectionID} does not exist!"}), 400)
    
    # Prepare sql statement for content table
    insertData = (sectionID, get_userID_by_userName(session["userName"]), data["links"], data["files"], data["slides"])
    query = "INSERT INTO content (sectionID, addBy, links, files, slides) VALUES (%s, %s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Content was successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    
@app.route("/content/<courseID>", methods=["GET"])
def get_contents(courseID):
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    contents = []
    contents_list = []
    # Prepare sql statement for registers table
    query = "SELECT sectionID, addBy, links, files, slides, add_date FROM content WHERE sectionID in (SELECT sectionID FROM section WHERE courseID = %s)"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (courseID,))
       contents = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for sectionID, addBy, links, files, slides, add_date in contents:
        contents_list.append({
            "sectionID": sectionID,
            "addBy": addBy,
            "links": links,
            "files": files,
            "slides": slides,
            "add_date": add_date
        })
    
    return make_response(jsonify(contents_list), 200) 

@app.route("/create/assignment/<courseID>", methods=["POST"])
def create_assignment(courseID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
        
    # Check if course exist
    if not is_exist([courseID, ], ["courseID"], "course"):
        return make_response(jsonify({"error": f"The course {courseID} does not exist!"}), 400)
    
    # Prepare sql statement for assignment table
    insertData = (courseID, data["assign_name"], data["due_date"], data["a_desc"] )
    query = "INSERT INTO assignment (courseID, assign_name, due_date,  a_desc) VALUES (%s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Assignment was successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    
@app.route("/submit/assignment/<assignmentID>", methods=["POST"])
def submit_assignment(assignmentID):
    
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
        
    # Check if assignment exist
    if not is_exist([assignmentID, ], ["assignID"], "assignment"):
        return make_response(jsonify({"error": f"The assignment {assignmentID} does not exist!"}), 400)
    
    # Check if its a lecturer login
    if not is_student_login():
        return make_response(jsonify({"error": "Only a Student can create a submit an assignment!"}), 400)
    
    # Prepare sql statement for submit table
    insertData = (assignmentID, get_userID_by_userName(session["userName"]), data["submission"] )
    query = "INSERT INTO submit (assignID, studentID, submission) VALUES (%s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Assignment was successfully created!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    
@app.route("/grade/<assignmentID>/<studentID>", methods=["POST"]) 
def grade_submistion(assignmentID, studentID):
    data = request.json
    
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
        
    # Check if assignment exist
    if not is_exist([assignmentID, ], ["assignID"], "assignment"):
        return make_response(jsonify({"error": f"The assignment {assignmentID} does not exist!"}), 400)
    
    # Check if its a lecturer login
    if not is_lecturer_login():
        return make_response(jsonify({"error": "Only a Lecturer can grade an assignment!"}), 400)
    
    # Prepare sql statement for submit table
    insertData = (assignmentID, studentID, get_userID_by_userName(["userName"]), data["grade"])
    query = "INSERT INTO grade (assignID, studentID, lectureID, grade) VALUES (%s, %s, %s, %s);"
    
    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 

       cursor.execute(query, insertData)
       db.commit()
       cursor.close()
       db.close()
       
       return make_response(jsonify({"Success": f"The Assignment was successfully graded!"}), 201)
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400) 
    

@app.route("/report/courses_over/<value>", methods=["GET"])
def course_report(value):
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    course = []
    course_list = []
    # Prepare sql statement for registers table
    query = "SELECT c.courseID, c.courseName, c.assigned_lec, COUNT(r.studentID) AS student_count FROM course c JOIN  registers r ON c.courseID = r.courseID GROUP BY  c.courseID, c.courseName, c.assigned_lec HAVING  COUNT(r.studentID) >= %s;"

    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (value,))
       course = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, courseName, assigned_lec, student_count in course:
        course_list.append({
            "courseID": courseID,
            "courseName": courseName,
            "assigned_lec": assigned_lec,
            "student_count": student_count,
   
        })
    
    return make_response(jsonify(course_list), 200) 

@app.route("/report/students_registered_for/<value>", methods=["GET"])
def student_report(value):
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    students = []
    student_list = []
    # Prepare sql statement for registers table
    query = "SELECT s.studentID, s.s_fname, s.s_lname, COUNT(r.courseID) AS course_count FROM student s JOIN  registers r ON s.studentID = r.studentID GROUP BY  s.studentID, s.s_fname, s.s_lname HAVING  COUNT(r.courseID) >= %s;"

    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (value,))
       students = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for studentID, s_fname, s_lname, course_count in students:
        student_list.append({
            "studentID": studentID,
            "s_fname": s_fname,
            "s_lname": s_lname,
            "course_count": course_count,
   
        })
    
    return make_response(jsonify(student_list), 200) 

@app.route("/report/lecturer_teaches_over_a_number_of_course/<value>", methods=["GET"])
def lecturer_report(value):
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    lecturers = []
    lecturers_List = []
    # Prepare sql statement for registers table
    query = "SELECT l.lectureID, l.lec_fname, l.lec_lname, COUNT(c.courseID) AS course_count FROM lecturer l JOIN course c ON l.lectureID = c.assigned_lec GROUP BY l.lectureID, l.lec_fname, l.lec_lname HAVING COUNT(c.courseID) >= %s;"

    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (value,))
       lecturers = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for lectureID, lec_fname, lec_lname, course_count in lecturers:
        lecturers_List.append({
            "lectureID": lectureID,
            "lec_fname": lec_fname,
            "lec_lname": lec_lname,
            "course_count": course_count,
   
        })
    
    return make_response(jsonify(lecturers_List), 200) 


@app.route("/report/most_registered_courses_report/<value>", methods=["GET"])
def most_registered_courses_report(value):
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    lecturers = []
    lecturers_List = []
    # Prepare sql statement for registers table
    query = "SELECT c.courseID, c.courseName, COUNT(r.studentID) AS student_count FROM course c JOIN registers r ON c.courseID = r.courseID GROUP BY c.courseID, c.courseName ORDER BY student_count DESC LIMIT %s;"

    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (int(value),))
       lecturers = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for courseID, courseName, student_count in lecturers:
        lecturers_List.append({
            "courseID": courseID,
            "courseName": courseName,
            "student_count": student_count
        })
    
    return make_response(jsonify(lecturers_List), 200) 
    
    
@app.route("/report/top_students/<value>", methods=["GET"])
def top_student(value):
    # Check if user login
    if not is_login(session["userName"]):
        return make_response(jsonify({"error": "No user is login!"}), 400)
    
    students = []
    students_List = []
    # Prepare sql statement for registers table
    query = "SELECT s.studentID, s.s_fname, s.s_lname, AVG(r.final_avg) AS avg_final_grade FROM student s JOIN registers r ON s.studentID = r.studentID GROUP BY s.studentID, s.s_fname, s.s_lname ORDER BY avg_final_grade DESC LIMIT %s;"

    # Connect to the database and execute the sql statement
    try:
       db = get_db_connection()
       cursor = db.cursor() 
    
       cursor.execute(query, (int(value),))
       students = cursor.fetchall()
       cursor.close()
       db.close()
       
    except Exception as e:
        print(e)
        return make_response(jsonify({"error": "Something went wrong!"}), 400)
    
   
    for studentID, s_fname, s_lname, avg_final_grade in students:
        students_List.append({
            "studentID": studentID,
            "s_fname": s_fname,
            "s_lname": s_lname,
            "avg_final_grade": avg_final_grade
        })
    
    return make_response(jsonify(students_List), 200) 
  
if __name__ in "__main__":
    app.run(debug=True)       
