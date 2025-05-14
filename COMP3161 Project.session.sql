CREATE DATABASE comp3161project;

-- User Table
CREATE TABLE user (
    userName VARCHAR(255) PRIMARY KEY NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Student Table

CREATE TABLE student (
    studentID INT PRIMARY KEY NOT NULL,
    userName VARCHAR(255),
    s_fname VARCHAR(255) NOT NULL,
    s_lname VARCHAR(255) NOT NULL,
    
    CONSTRAINT FK_StudentUser 
        FOREIGN KEY (userName) 
        REFERENCES user(userName) 
        ON UPDATE CASCADE
);

CREATE TABLE lecturer (
    lectureID INT PRIMARY KEY NOT NULL,
    userName VARCHAR(255),
    lec_fname VARCHAR(255) NOT NULL,
    lec_lname VARCHAR(255) NOT NULL,
    
    CONSTRAINT FK_LectureUser 
        FOREIGN KEY (userName) 
        REFERENCES user(userName) 
        ON UPDATE CASCADE
);

CREATE TABLE adminUser (
    adminID INT PRIMARY KEY NOT NULL,
    userName VARCHAR(255),
    ad_fname VARCHAR(255) NOT NULL,
    ad_lname VARCHAR(255) NOT NULL,
    
    CONSTRAINT FK_AdminUser 
        FOREIGN KEY (userName) 
        REFERENCES user(userName) 
        ON UPDATE CASCADE
);


CREATE TABLE account (
    accountID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    ownerID INT NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE course (
    courseID VARCHAR(15) PRIMARY KEY NOT NULL,
    courseName VARCHAR(255) NOT NULL UNIQUE,
    assigned_lec INT NOT NULL
);

CREATE TABLE createcourse (
    createID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    courseID VARCHAR(15) UNIQUE NOT NULL,
    adminID INT NOT NULL
);

CREATE TABLE registers (
    studentID INT KEY NOT NULL,
    courseID VARCHAR(15) NOT NULL,
    academic_year YEAR NOT NULL,
    academic_term VARCHAR(10),
    final_avg DECIMAL(5,2)

);

CREATE TABLE content (
    contentID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    courseID VARCHAR(15) NOT NULL,
    links VARCHAR(255),
    files VARCHAR(255),
    slides VARCHAR(255),

    CONSTRAINT FK_coursecontent
        FOREIGN KEY (courseID)
        REFERENCES course(courseID)
        ON DELETE CASCADE
);

CREATE TABLE addcontent (
    addID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    contentID INT UNIQUE NOT NULL,
    lectureID INT NOT NULL,
    add_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE section (
    sectionID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    contentID INT NOT NULL,
    title VARCHAR(255) NOT NULL,

    CONSTRAINT FK_contentsection
        FOREIGN KEY (contentID)
        REFERENCES content(contentID)
        ON DELETE CASCADE
);

CREATE TABLE calendarEvents (
    calendarID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    courseID VARCHAR(15) NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    event_date Date NOT NULL,
    event_desc VARCHAR(1000),

    CONSTRAINT FK_coursecalendar
        FOREIGN KEY (courseID)
        REFERENCES course(courseID)
        ON DELETE CASCADE

);


CREATE TABLE forum (
    forumID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    courseID VARCHAR(15) NOT NULL,
    topic VARCHAR(300) NOT NULL,
    forum_desc VARCHAR(1000),
    startdate Date,


    CONSTRAINT FK_courseforum
        FOREIGN KEY (courseID)
        REFERENCES course(courseID)
        ON DELETE CASCADE

);

CREATE TABLE thread (
    threadID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    forumID INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    post VARCHAR(1500) NOT NULL,
    post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


    CONSTRAINT FK_forumthread
        FOREIGN KEY (forumID)
        REFERENCES forum(forumID)
        ON DELETE CASCADE

); 


CREATE TABLE addthread (
    addID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    threadID INT NOT NULL,
    lectureID INT NOT NULL
);


CREATE TABLE reply (
    replyID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    threadID INT NOT NULL,
    reply_to INT,
    body VARCHAR(1500) Not NULL,
    who_reply INT NOT NULL,


    CONSTRAINT FK_threadreply
        FOREIGN KEY (threadID)
        REFERENCES thread(threadID)
        ON DELETE CASCADE
); 

CREATE TABLE assignment (
    assignID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    courseID VARCHAR(15) NOT NULL,
    assign_name VARCHAR(255) Not NULL,
    due_date Date NOT NULL,
    a_desc VARCHAR(1500) NOT NULL,


    CONSTRAINT FK_courseassignment
        FOREIGN KEY (courseID)
        REFERENCES course(courseID)
        ON DELETE CASCADE

);

CREATE TABLE grade (
    gradeID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    assignID INT NOT NULL,
    studentID INT NOT NULL,
    lectureID INT NOT NULL,
    grade INT NOT NULL
    
);


CREATE TABLE submit (
    submissionID INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    assignID INT NOT NULL,
    studentID INT NOT NULL,
    submission VARCHAR(3000) NOT NULL,
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

