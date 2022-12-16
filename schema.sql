CREATE TABLE IF NOT EXISTS Users(
  user_id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  date_created TEXT,
  hire_date TEXT,
  user_type INTEGER,
  active INTEGER DEFAULT 1
);

CREATE TABLE IF NOT EXISTS Competencies(
  competency_id INTEGER PRIMARY KEY,
  name TEXT,
  date_created TEXT
);
CREATE TABLE IF NOT EXISTS Assessments(
  assessment_id INTEGER PRIMARY KEY AUTOINCREMENT,
  competency_id INTEGER,
  name TEXT,
  date_created TEXT,
  FOREIGN KEY (competency_id) REFERENCES Competencies (competency_id)
);

CREATE TABLE IF NOT EXISTS Assessment_Results(
  assessment_res_id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  assessment_id INTEGER,
  score INTEGER, 
  date_taken date,
  manager INTEGER,
  active INTEGER DEFAULT 1,
  FOREIGN KEY (manager) REFERENCES Users (user_type),
  FOREIGN KEY (user_id) REFERENCES Users (user_id),
  FOREIGN KEY (assessment_id) REFERENCES Assessment (assessment_id)
);