from faker import Faker
import random
from collections import defaultdict

NUM_SYSADMIN = 10
NUM_STUDENTS = 100000
NUM_LECTURERS = 60
NUM_COURSES = 200
MIN_COURSES_PER_STUDENT = 3
MAX_COURSES_PER_STUDENT = 6
MIN_STUDENTS_PER_COURSE = 10
ACADEMIC_YEAR = 2025
ACADEMIC_TERM = "SEMESTER 1"
username = {"":None}



    # studentID INT PRIMARY KEY NOT NULL,
    # userName VARCHAR(255),
    # s_fname VARCHAR(255) NOT NULL,
    # s_lname VARCHAR(255) NOT NULL,
    
    # INSERT INTO student (studentID, userName, s_fname, s_lname) VALUES (6200160000, "Damion_Henry", "Damion", "Henry")
    
faker = Faker()

department_prefixes = {
    "Biology": "BIO",
    "Chemistry": "CHEM",
    "Computer": "COMP",
    "Mathematics": "MATH",
    "Physics": "PHYS"
    # "English and Linguistics": "ENG",
    # "Art": "ART",
}
    # "ENG": ["Literary Criticism","Syntax and Semantics","Creative Writing","Language Acquisition","English Literature","Phonetics","Sociolinguistics","Discourse Analysis","World Literature","Historical Linguistics"],
    # "ART": ["Painting Techniques","Art History","Digital Illustration","Sculpture","Modern Art","Drawing Fundamentals","Graphic Design","Photography","Textile Arts","Printmaking"]

department_topics = {
    "BIO": [{"name": "Cell Structure", "code": "01"},{"name": "Genetics", "code": "02"},{"name": "Microbiology", "code": "03"},{"name": "Botany", "code": "04"},{"name": "Zoology", "code": "05"},{"name": "Ecology", "code": "06"},{"name": "Human Anatomy", "code": "07"},{"name": "Neuroscience", "code": "08"},{"name": "Evolutionary Biology", "code": "09"},{"name": "Immunology", "code": "10"}],
    "CHEM": [{"name": "Organic Chemistry", "code": "11"},{"name": "Inorganic Chemistry", "code": "12"},{"name": "Thermodynamics", "code": "13"},{"name": "Chemical Bonding", "code": "14"},{"name": "Analytical Chemistry", "code": "15"},{"name": "Biochemistry", "code": "16"},{"name": "Physical Chemistry", "code": "17"},{"name": "Environmental Chemistry", "code": "18"},{"name": "Polymer Chemistry", "code": "19"},{"name": "Quantum Chemistry", "code": "20"}],
    "COMP": [{"name": "Data Structures", "code": "21"},{"name": "Algorithms", "code": "22"},{"name": "Operating Systems", "code": "23"},{"name": "Databases", "code": "24"},{"name": "Computer Networks", "code": "25"},{"name": "Artificial Intelligence", "code": "26"},{"name": "Machine Learning", "code": "27"},{"name": "Software Engineering", "code": "28"},{"name": "Cybersecurity", "code": "29"},{"name": "Web Development", "code": "30"}],
    "MATH": [{"name": "Calculus", "code": "31"},{"name": "Linear Algebra", "code": "32"},{"name": "Probability", "code": "33"},{"name": "Statistics", "code": "34"},{"name": "Number Theory", "code": "35"},{"name": "Discrete Mathematics", "code": "36"},{"name": "Differential Equations", "code": "37"},{"name": "Topology", "code": "38"},{"name": "Complex Analysis", "code": "39"},{"name": "Real Analysis", "code": "40"}],
    "PHYS": [{"name": "Classical Mechanics", "code": "41"},{"name": "Quantum Physics", "code": "42"},{"name": "Electromagnetism", "code": "43"},{"name": "Thermodynamics", "code": "44"},{"name": "Nuclear Physics", "code": "45"},{"name": "Optics", "code": "46"},{"name": "Relativity", "code": "47"},{"name": "Astrophysics", "code": "48"},{"name": "Particle Physics", "code": "49"},{"name": "Fluid Mechanics", "code": "50"}]
}


course_prefixes = {
    "intro": ["Introduction to", "10"],
    "appl": ["Applications of", "22"],
    "adv": ["Advanced Topics in", "32"],
    "cap": ["Capstone in", "33"]   
}

def generate_course(dprefix, cprefix, ccode, topic, ctopic):
    return (f"{dprefix}{ccode}{ctopic}", f"{cprefix} {topic}")

sql_users = []
sql_users.append("\n-- Insert Users")
def get_username():
    
    user_name = ""
    while user_name in username:
            first_name = faker.first_name().replace("'", "''")
            last_name = faker.last_name().replace("'", "''")
            user_name = f"{first_name}_{last_name}"
            
    username[user_name] = user_name
    
    sql_users.append(f"INSERT INTO user (userName, password) VALUES ('{user_name}', '123456789');") 
    return {"user_name": user_name, "first_name": first_name, "last_name": last_name}

def split_statment_into_four(sqlstatment):
    n = len(sqlstatment)
    k = n // 4
    remainder = n % 4
    
    parts = []
    start = 0
    
    for i in range(4):
        end = start + k + (1 if i < remainder else 0)
        parts.append(sqlstatment[start:end])
        start = end
    
    return parts
    
    


def generate_sql():
    
    #  Insert Students
    sql_statements = []
    sql_statements.append("\n-- Insert Students")
    user_name = ""
    students = []
    for i in range(1, NUM_STUDENTS + 1):
        studentID = 6200160000 + i  
        user_name = get_username()
        students.append(studentID)
        
        sql_statements.append(f"INSERT INTO student (studentID, userName, s_fname, s_lname) VALUES ({studentID}, '{user_name["user_name"]}', '{user_name["first_name"]}', '{user_name["last_name"]}');")
        
    with open("vle_students_data.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_statements)) 
        

    # Insert Admin 
    sql_statements = []
    sql_statements.append("\n-- Insert SysAdmin")
    sysAdmin = []
    for i in range(1, NUM_SYSADMIN + 1):
        sysAdminID = 400010000 + i
        user_name = get_username()
        sysAdmin.append(sysAdminID)
        
        sql_statements.append(f"INSERT INTO sysadmin (adminID, userName, ad_fname, ad_lname) VALUES ({sysAdminID}, '{user_name["user_name"]}', '{user_name["first_name"]}', '{user_name["last_name"]}');")
        
    with open("vle_sysadmins_data.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_statements)) 
        
    #  Insert Lecturers
    sql_statements = []
    sql_statements.append("\n-- Insert Lecturers")
    lecturers = []
    for i in range(1, NUM_LECTURERS + 1):
        lectureID = 100010000 + i
        user_name = get_username()
        lecturers.append(lectureID)
        sql_statements.append(f"INSERT INTO lecturer (lectureID, userName, lec_fname, lec_lname) VALUES ({lectureID}, '{user_name["user_name"]}', '{user_name["first_name"]}', '{user_name["last_name"]}');")
        
        
    with open("vle_lecturer_data.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_statements)) 
    
    
    with open("vle_users_data.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_users)) 
        
    
    #  Insert Courses
    sql_statements = []
    sql_statements.append("\n-- Insert Courses")
    courses = []

    # Store unique course codes
    courses = []
    for i in range(1, NUM_COURSES + 1):
        for dcode in department_prefixes.values():
            topics = department_topics[dcode]
            for topic in topics:
                for courseNamePrefixes, courseCode in course_prefixes.values():
                    courses.append(generate_course(dcode, courseNamePrefixes, courseCode, topic['name'],topic['code']))
              
                
    # Assign Lecturer to courses
    sql_createByStatements = []
    sql_statements.append("\n-- Assign Lecturer to courses")
    sql_createByStatements.append("\n-- Course Create by SysAdmin")
    j = 0    
    for i in range(200):
        # 20 lecturers teach 5 courses, total courses 100
        if i < 100:
            if i == 0:
                sql_statements.append("\n-- 20 lecturers each teaches 5 courses")
                     
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ('{courses[i][0]}', '{courses[i][1]}', '{lecturers[j]}');")
            
            # Move to the next Lecture if five course is assign to the current lecture
            if (i+1)%5 == 0:
                j = j+1
        
        # 10 lecturers teach 4 courses, total courses 140
        if 100 <= i < 140:
            if i == 100:
                sql_statements.append("\n-- 10 lecturers each teaches 4 courses")
            
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ('{courses[i][0]}', '{courses[i][1]}', '{lecturers[j]}');")
            
            # Move to the next Lecture if five course is assign to the current lecture
            if (i+1)%4 == 0:
                j = j+1
        
        # 10 lecturers teach 3 courses, total courses 170
        if 140 <= i < 170:
            if i == 140:
                sql_statements.append("\n-- 10 lecturers each teaches 3 courses")
            
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ('{courses[i][0]}', '{courses[i][1]}', '{lecturers[j]}');")
            
            # Move to the next Lecture if five course is assign to the current lecture
            # if i in [143, 146, 149, 152, 155, 158, 161, 164, 167]:
            if ((i+1) - 140) % 3 == 0:
                j = j+1
        
        # 10 lecturers teach 2 courses, total courses 190
        if 170 <= i < 190:
            if i == 170:
                sql_statements.append("\n-- 10 lecturers each teaches 2 courses")
                
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ('{courses[i][0]}', '{courses[i][1]}', '{lecturers[j]}');")
            
            # Move to the next Lecture if five course is assign to the current lecture
            if ((i+1) - 170) % 2 == 0:
                j = j+1
        
        # 10 lecturers teach 1 courses, total courses 200
        if (i+1) > 190:
            if i == 190:
                sql_statements.append("\n-- 10 lecturers each teaches 1 course")
                
            sql_statements.append(f"INSERT INTO course (courseID, courseName, assigned_lec) VALUES ('{courses[i][0]}', '{courses[i][1]}', '{lecturers[j]}');")
            
            # Move to the next Lecture if five course is assign to the current lecture
            j = j+1
        

        # Course Create by which admin user
        adminID = random.choice(sysAdmin)
        sql_createByStatements.append(f"INSERT INTO createcourse (courseID, adminID) VALUES ('{courses[i][0]}', {adminID});")
        
    
    with open("vle_courses_data.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_statements)) 
            
    with open("vle_courses_create_by_data.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_createByStatements))       
    
    
    #  Insert Registration info for student
    sql_statements = []
    sql_statements.append("\n-- Registering Students to courses")
    register = {}
    student_enrollments = defaultdict(list)
    # Register 3–6 random courses to each student  
    i = 0  
    for std_id in students:
        num_courses = random.randint(MIN_COURSES_PER_STUDENT, MAX_COURSES_PER_STUDENT)
        
        # Registering 3-6 courses to the current student
        numAssignedCourses = 0
        assigned_courses = []
        while numAssignedCourses < num_courses:
            courseID = courses[i][0]
            
            # Ensure we don't register the student to the same course more than once
            if courseID in assigned_courses:
                i = (i + random.randint(0, NUM_COURSES)) % NUM_COURSES
                continue
            
            grade = round(random.uniform(30, 100), 2)
            sql_statements.append(f"INSERT INTO registers (studentID, courseID, academic_year,academic_term, final_avg) " 
                                    f"VALUES ({std_id}, '{courses[i][0]}', {ACADEMIC_YEAR}, '{ACADEMIC_TERM}', {grade});")
            
            
            # Tracking the students who registered for a given course
            student_enrollments[std_id].append(courses[i][0])
            
            # Track the student-course assignment
            assigned_courses.append(courseID)
                
            
            # Tracking the number of student registered for a course
            if courses[i][0] in register:
                # Update the number of student register for the current course
                register[courses[i][0]] += 1
            else:
                # Add the course to the register tracker with the first student count
                 register[courses[i][0]] = 1
                 
            numAssignedCourses += 1
            i = (i + random.randint(0, NUM_COURSES)) % NUM_COURSES
            
            
            
    # Ensure each course has at least 10 student
    for course in courses:
        
        if course[0] in register:
            while  register[course[0]] < MIN_STUDENTS_PER_COURSE:
                # randomly pick a student who isn’t already in this course and has < 6 courses

                candidates = [s for s in students if course[0] not in student_enrollments[s] and len(student_enrollments[s]) < MAX_COURSES_PER_STUDENT]
                
                if not candidates:
                    break # all students are maxed out
                
                random_std = random.choice(candidates)
                
                grade = round(random.uniform(30, 100), 2)
                sql_statements.append(f"INSERT INTO registers (studentID, courseID, academic_year,academic_term, final_avg) " 
                                    f"VALUES ({random_std}, '{course[0]}', {ACADEMIC_YEAR}, '{ACADEMIC_TERM}', {grade});")
                
                # Tracking the students who registered for a given course
                student_enrollments[random_std].append(course[0])
                
            
                # Tracking the number of student registered for a course
                if course[0] in register:
                    # Update the number of student register for the current course
                    register[course[0]] += 1
                else:
                    # Add the course to the register tracker with the first student count
                    register[course[0]] = 1
    
    
    sql_parts = split_statment_into_four(sql_statements)
    with open("vle_registration_data1.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_parts[0]))  
           
    with open("vle_registration_data2.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_parts[1])) 
            
    with open("vle_registration_data3.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_parts[2])) 
            
    with open("vle_registration_data4.sql", "w", encoding="utf-8") as file:
        file.write("\n".join(sql_parts[3]))     
        



generate_sql()
    
print("SQL file generated successfully!")
       


    
    