import csv
import bcrypt
import sqlite3

connection = sqlite3.connect("competency_tracking_tool.db")
cursor = connection.cursor()


class Users:
    def __init__(
        self,
        first_name,
        last_name,
        phone,
        email,
        password,
        date_created,
        hire_date,
        user_type=1,
        active=True,
        user_id=None,
    ):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.password = password
        self.date_created = date_created
        self.hire_date = hire_date
        self.user_type = user_type
        self.active = active

    def db_add_user(self):
        query = "INSERT INTO Users (first_name, last_name, phone, email, password, date_created, hire_date) VALUES (?,?,?,?,?,?,?)"
        cursor.execute(
            query,
            (
                self.first_name,
                self.last_name,
                self.phone,
                self.email,
                self.password,
                self.date_created,
                self.hire_date,
            ),
        )
        connection.commit()

    def db_update_users(self):
        query = "UPDATE Users SET first_name = ?, last_name = ?, phone = ?, email = ?, password = ?, date_created = ?, hire_date = ?, user_type = ?, active = ? WHERE user_id = ?;"
        cursor.execute(
            query,
            (
                self.first_name,
                self.last_name,
                self.phone,
                self.email,
                self.password,
                self.date_created,
                self.hire_date,
                self.user_type,
                self.active,
                self.user_id,
            ),
        )
        connection.commit()

    def user_info(self):
        print(
            f"User_id: {self.user_id}\nFirst Name: {self.first_name}\nLast Name: {self.last_name}\nPhone: {self.phone}\nEmail: {self.email}\nPassword: {self.password}\nDate Created: {self.date_created}\nHire Date: {self.hire_date}\nUser Type: {self.user_type}\nActive: {self.active}"
        )


class Competencies:
    def __init__(
        self,
        name,
        date_created,
        competency_id=None,
    ):
        self.competency_id = competency_id
        self.name = name
        self.date_created = date_created

    def db_add_comp(self):
        query = "INSERT INTO Competencies (competency_id, name, date_created) VALUES (?,?,?)"
        cursor.execute(
            query,
            (
                self.competency_id,
                self.name,
                self.date_created,
            ),
        )
        connection.commit()

    def db_update_comp(self):
        query = "UPDATE Competencies SET name = ?, date_created = ? WHERE competency_id = ?;"
        cursor.execute(
            query,
            (
                self.name,
                self.date_created,
                self.competency_id,
            ),
        )
        connection.commit()

    def comp_info(self):
        print(
            f"Competecy ID: {self.competency_id}\nName: {self.name}\nDate Created: {self.date_created}"
        )


class Assessments:
    def __init__(
        self,
        competency_id,
        name,
        date_created,
        assessment_id=None,
    ):
        self.assessment_id = assessment_id
        self.competency_id = competency_id
        self.name = name
        self.date_created = date_created

    def db_add_assess(self):
        query = "INSERT INTO Assessments (assessment_id, competency_id, name, date_created) VALUES (?,?,?,?)"
        cursor.execute(
            query,
            (
                self.assessment_id,
                self.competency_id,
                self.name,
                self.date_created,
            ),
        )
        connection.commit()

    def db_update_assess(self):
        query = (
            "UPDATE Assessments SET name = ?, date_created = ? WHERE assessment_id = ?;"
        )
        cursor.execute(
            query,
            (
                self.name,
                self.date_created,
                self.assessment_id,
            ),
        )
        connection.commit()

    def assess_info(self):
        print(
            f"Assessment ID: {self.assessment_id}\nCompetecy ID: {self.competency_id}\nName: {self.name}\nDate Created: {self.date_created}"
        )


class Assessments_Results:
    def __init__(
        self,
        score,
        date_taken,
        manager,
        active=1,
        user_id=None,
        assessment_id=None,
        assessment_res_id=None,
    ):
        self.assessment_res_id = assessment_res_id
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.score = score
        self.date_taken = date_taken
        self.manager = manager
        self.active = active

    def db_add_assess_res(self):
        query = "INSERT INTO Assessment_results (user_id, assessment_id, score, date_taken, manager) VALUES (?,?,?,?,?)"
        cursor.execute(
            query,
            (
                self.user_id,
                self.assessment_id,
                self.score,
                self.date_taken,
                self.manager,
            ),
        )
        connection.commit()

    def db_update_assess_res(self):
        query = "UPDATE Assessment_Results SET score = ?, date_taken = ?, manager = ?, active = ? WHERE assessment_res_id = ?;"
        cursor.execute(
            query,
            (
                self.score,
                self.date_taken,
                self.manager,
                self.active,
                self.assessment_res_id,
            ),
        )
        connection.commit()

    def assess_info_res(self):
        print(
            f"Assessment Results ID: {self.assessment_res_id}User ID: {self.user_id}\nAssessment ID: {self.assessment_id}\nScore: {self.score}\nDate Taken: {self.date_taken}\nManager: {self.manager}"
        )


def create_schema():

    with open("schema.sql", "rt") as sql_queries:
        queries = sql_queries.read()
        cursor.executescript(queries)

    connection.commit()


def import_comp_list():

    insert_query = "INSERT INTO Competencies (name, date_created) VALUES (?,?)"

    with open("comp_list.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        fields = next(
            reader
        )  # Header row, WE WILL NOT USE, but this will remove it from the dataset

        for row in reader:
            cursor.execute(insert_query, row)

    connection.commit()


def import_users():
    insert_query = "INSERT INTO Users (first_name, last_name, phone, email, password, date_created, hire_date, user_type) VALUES (?,?,?,?,?,?,?,?)"

    with open("users.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        fields = next(
            reader
        )  # Header row, WE WILL NOT USE, but this will remove it from the dataset

        for row in reader:
            # first_name =
            row = list(row)
            row[4] = bcrypt.hashpw(row[4].encode(), salt=bcrypt.gensalt()).decode()
            cursor.execute(insert_query, row)

    connection.commit()


def import_asses():
    insert_query = (
        "INSERT INTO Assessments (competency_id, name, date_created) VALUES (?,?,?)"
    )

    with open("assessment.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        fields = next(reader)

        for row in reader:
            cursor.execute(insert_query, row)
    connection.commit()


def import_asses_res():
    insert_query = "INSERT INTO Assessment_Results (user_id, assessment_id, score, date_taken, manager) VALUES (?,?,?,?,?)"

    with open("assessment_result.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        fields = next(reader)

        for row in reader:
            cursor.execute(insert_query, row)
    connection.commit()


def user_add_add():
    required_fields = [
        "first_name",
        "last_name",
        "phone",
        "email",
        "password",
        "date_created",
        "hire_date",
    ]
    values = []

    for field in required_fields:
        values.append(input(f"{field}: "))

    first_name = values[0]
    last_name = values[1]
    phone = values[2]
    email = values[3]
    password = bcrypt.hashpw(values[4].encode(), salt=bcrypt.gensalt()).decode()
    date_created = values[5]
    hire_date = values[6]
    new_user = Users(
        first_name, last_name, phone, email, password, date_created, hire_date
    )
    new_user.db_add_user()


def comp_add():
    required_fields = [
        "name",
        "date_created",
    ]
    values = []

    for field in required_fields:
        values.append(input(f"{field}: "))
    name = values[0]
    date_created = values[1]

    new_user = Competencies(name, date_created)
    new_user.db_add_comp()


def assess_add():
    required_fields = [
        "name",
        "date_created",
    ]
    values = []
    view_all_comps()
    competency_id = int(
        input(
            "Which competency would you like to be with this Assessment?(Competency_id)\n>>> "
        )
    )
    for field in required_fields:
        values.append(input(f"{field}: "))
    name = values[0]
    date_created = values[1]

    new_user = Assessments(competency_id, name, date_created)
    new_user.db_add_assess()


def assess_res_add():
    required_fields = [
        "score",
        "date_taken",
        "manager",
    ]
    values = []
    view_all_users()
    user_id = int(
        input(
            "Which User would you like to be with this Assessment Result?(user_id)\n>>> "
        )
    )
    manager = int(
        input(
            "Which Manager administered this Assessment Result? if any?(user_id)\n>>> "
        )
    )
    view_all_assess()
    assessment_id = int(
        input(
            "Which Assessment would you like to be with this Assessment Result?(assessemnt_id)\n>>> "
        )
    )

    for field in required_fields:
        values.append(input(f"{field}: "))
    score = values[0]
    date_taken = values[1]

    new_user = Assessments_Results(
        score, date_taken, manager, user_id=user_id, assessment_id=assessment_id
    )
    new_user.db_add_assess_res()


def view_all_users(where=None):

    if where:
        where = f"%{where}%"
        rows = cursor.execute(
            "SELECT * FROM Users WHERE first_name LIKE ? OR last_name LIKE ?",
            (where, where),
        ).fetchall()
    else:
        rows = cursor.execute("SELECT * FROM Users").fetchall()

    headers = [
        "user_id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "password",
        "date_created",
        "hire_date",
        "user_type",
        "active",
    ]
    print(
        f"{headers[0]:15}{headers[1]:15}{headers[2]:15}{headers[3]:15}{headers[4]:30}{headers[7]:15}{headers[8]:15}{headers[9]}"
    )
    print(
        f'{"---------":15}{"---------":15}{"---------":15}{"---------":15}{"---------":30}{"---------":15}{"---------":15}{"---------"}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<15}{row[1]:15}{row[2]:15}{row[3]:15}{row[4]:30}{row[7]:15}{row[8]:15}{row[9]}"
        )


def view_all_comps(where=None):

    if where:
        where = f"%{where}%"
        rows = cursor.execute(
            "SELECT * FROM Competencies WHERE name LIKE ?", (where,)
        ).fetchall()
    else:
        rows = cursor.execute("SELECT * FROM Competencies").fetchall()

    headers = [
        "competency_id",
        "name",
        "date_created",
    ]
    print(f"{headers[0]:18}{headers[1]:30}{headers[2]}")
    print(f'{"---------":18}{"---------":30}{"---------"}')

    for row in rows:
        row = [str(i) for i in row]
        print(f"{row[0]:<18}{row[1]:30}{row[2]}")


def view_all_assess(where=None):

    if where:
        where = f"%{where}%"
        rows = cursor.execute(
            "SELECT * FROM Assessments WHERE name LIKE ?", (where,)
        ).fetchall()
    else:
        rows = cursor.execute("SELECT * FROM Assessments").fetchall()

    headers = [
        "assessments_id",
        "competency_id",
        "name",
        "date_created",
    ]
    print(f"{headers[0]:15}{headers[1]:15}{headers[2]:15}{headers[3]}")
    print(f'{"---------":15}{"---------":15}{"---------":15}{"---------"}')

    for row in rows:
        row = [str(i) for i in row]
        print(f"{row[0]:<15}{row[1]:15}{row[2]:15}{row[3]}")


def view_all_assess_res():

    rows = cursor.execute(
        "SELECT * FROM Assessment_Results ORDER BY assessment_res_id"
    ).fetchall()

    headers = [
        "assessment_res_id",
        "user_id",
        "assessment_id",
        "score",
        "date_taken",
        "manager",
    ]
    print(
        f"{headers[0]:15}{headers[1]:15}{headers[2]:15}{headers[3]:15}{headers[4]:25}{headers[5]}"
    )
    print(
        f'{"---------":15}{"---------":15}{"---------":15}{"---------":15}{"---------":25}{"---------"}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(f"{row[0]:<15}{row[1]:15}{row[2]:15}{row[3]:15}{row[4]:25}{row[5]}")


def view_comp_level():
    view_all_comps()
    comp_id = input("What Competency you want?(competency_id)\n>>> ")
    rows = cursor.execute(
        """
    SELECT Users.user_id, Users.first_name, Users.last_name, Assessments.name,
    Assessment_Results.score, Competencies.name
    FROM Assessment_Results
    JOIN Users
    ON Users.user_id = Assessment_Results.user_id
    JOIN Assessments 
    ON Assessment_Results.assessment_id = Assessments.assessment_id
    JOIN Competencies
    ON Assessments.competency_id = Competencies.competency_id
    WHERE Competencies.competency_id = ?
    """,
        (comp_id,),
    ).fetchall()

    headers = [
        "user_id",
        "first_name",
        "last_name",
        "assessemnt_name",
        "score",
        "competency_name",
    ]
    print(
        f"{headers[0]:15}{headers[1]:15}{headers[2]:15}{headers[3]:35}{headers[4]:15}{headers[5]}"
    )
    print(
        f'{"---------":15}{"---------":15}{"---------":15}{"---------":35}{"---------":15}{"---------"}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(f"{row[0]:<15}{row[1]:15}{row[2]:15}{row[3]:35}{row[4]:15}{row[5]}")


def view_user_comp_level(user_id=None):
    if user_id:
        rows = cursor.execute(
            """
    SELECT DISTINCT Users.user_id, Assessments.name, MAX(Assessment_Results.score), Competencies.name
    FROM Assessment_Results
    JOIN Users
    ON Users.user_id = Assessment_Results.user_id
    JOIN Assessments 
    ON Assessment_Results.assessment_id = Assessments.assessment_id
    JOIN Competencies
    ON Assessments.competency_id = Competencies.competency_id
    WHERE Users.user_id = ?
    GROUP BY Users.user_id,Competencies.competency_id
    
        
    """,
            (user_id,),
        ).fetchall()
    else:
        view_all_users()
        user_id = input(
            "Which user would you like to see there competency report? (user_id)\n>>> "
        )
        rows = cursor.execute(
            """
        SELECT Users.user_id, Assessments.name, Assessment_Results.score, Competencies.name
        FROM Assessment_Results
        JOIN Users
        ON Users.user_id = Assessment_Results.user_id
        JOIN Assessments 
        ON Assessment_Results.assessment_id = Assessments.assessment_id
        JOIN Competencies
        ON Assessments.competency_id = Competencies.competency_id
        WHERE Users.user_id = ?
        """,
            (user_id,),
        ).fetchall()

    headers = [
        "user_id",
        "assessemnt_name",
        "score",
        "competency_name",
    ]
    print(f"{headers[0]:15}{headers[1]:35}{headers[2]:15}{headers[3]}")
    print(f'{"---------":15}{"---------":35}{"---------":15}{"---------"}')

    for row in rows:
        row = [str(i) for i in row]
        print(f"{row[0]:<15}{row[1]:35}{row[2]:15}{row[3]}")


def user_comp_sum(export=False):
    view_all_users()
    comp_id = input("Which user would you like to view?(user_id)\n>>> ")
    rows = cursor.execute(
        """
    SELECT Users.first_name, Users.last_name, Assessments.name,
    AVG(Assessment_Results.score), Competencies.name
    FROM Assessment_Results
    JOIN Users
    ON Users.user_id = Assessment_Results.user_id
    JOIN Assessments 
    ON Assessment_Results.assessment_id = Assessments.assessment_id
    JOIN Competencies
    ON Assessments.competency_id = Competencies.competency_id
    WHERE Users.user_id = ?
    GROUP BY Competencies.competency_id
    ORDER BY Assessment_Results.date_taken DESC
    """,
        (comp_id,),
    ).fetchall()

    headers = [
        "first_name",
        "last_name",
        "assessemnt_name",
        "score",
        "competency_name",
    ]
    print(f"{headers[0]:15}{headers[1]:15}{headers[2]:35}{headers[3]:10}{headers[4]}")
    print(
        f'{"---------":15}{"---------":15}{"---------":35}{"---------":10}{"---------"}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(f"{row[0]:<15}{row[1]:15}{row[2]:35}{row[3]:10}{row[4]}")

    if export == True:
        name = input("What would you like to call the CSV file?\n>>> ")
        with open(f"{name}.csv", "wt") as comp_file:
            wrt = csv.writer(comp_file)
            wrt.writerow(headers)
            wrt.writerows(rows)


def comp_res_sum(export=False):
    view_all_comps()
    comp_id = input(
        "Which competency would you like to use for the Competency Results Summary?(competency_id)\n>>> "
    )
    rows = cursor.execute(
        """
    SELECT Competencies.name, ROUND(AVG(Assessment_Results.score),2),Users.first_name, Users.last_name, Assessment_Results.score, Assessments.name, Assessment_Results.date_taken
    FROM Assessment_Results
    JOIN Users
    ON Users.user_id = Assessment_Results.user_id
    JOIN competencies
    ON Assessments.competency_id = Competencies.competency_id
    JOIN Assessments
    ON Assessments.assessment_id = Assessment_Results.assessment_id
    WHERE Assessment_Results.assessment_id = ?
    GROUP BY Users.user_id
    ORDER BY Assessment_Results.date_taken DESC
    """,
        (comp_id,),
    ).fetchall()

    headers = [
        "Competency Name",
        "Average Score",
        "First Name",
        "Last Name",
        "Assessment Score",
        "assessemnt_name",
        "Date Taken",
    ]
    print(
        f"{headers[0]:15}{headers[1]:15}{headers[2]:35}{headers[3]:10}{headers[4]:10}{headers[5]:10}{headers[6]}"
    )
    print(
        f'{"---------":15}{"---------":15}{"---------":35}{"---------":10}{"---------":10}{"---------":10}{"---------"}'
    )

    for row in rows:
        row = [str(i) for i in row]
        print(
            f"{row[0]:<15}{row[1]:15}{row[2]:35}{row[3]:10}{row[4]:10}{row[5]:10}{row[6]}"
        )
    if export == True:
        name = input("What would you like to name the file?\n>>> ")
        with open(f"{name}.csv", "wt") as comp_file:
            wrt = csv.writer(comp_file)
            wrt.writerow(headers)
            wrt.writerows(rows)


def get_user(user=None):
    if user == None:

        user_name = input("Search for user using first name or last name:\n>>>  ")
        view_all_users(user_name)

        user_id = input("Which ID?\n>>> ")
        query = "SELECT * FROM Users WHERE user_id = ?"
    else:
        user_id = user
        query = "SELECT * FROM Users WHERE user_id = ?"

    (
        user_id,
        first_name,
        last_name,
        phone,
        email,
        password,
        date_created,
        hire_date,
        user_type,
        active,
    ) = cursor.execute(query, (user_id,)).fetchone()

    user = Users(
        first_name,
        last_name,
        phone,
        email,
        password,
        date_created,
        hire_date,
        user_type,
        active,
        user_id,
    )
    return user


def get_comp():
    search_comp = input("Search for competencies using the competency name:\n>>>  ")
    view_all_comps(search_comp)

    comp_name = input("Which Competency?\n>>> ")
    query = "SELECT * FROM Competencies WHERE competency_id LIKE ?"

    (competency_id, name, date_created) = cursor.execute(query, (comp_name,)).fetchone()

    comp = Competencies(
        name,
        date_created,
        competency_id,
    )
    return comp


def get_ass():
    search_ass = input("Which Assessment Results?(user_id)\n>>> ")
    view_all_assess(search_ass)
    assessment_id_1 = input("Search for Assessments using the Assessment name:\n>>>  ")
    query = "SELECT * FROM Assessments WHERE assessment_id LIKE ?"

    (
        assessment_id,
        competency_id,
        name,
        date_created,
    ) = cursor.execute(query, (assessment_id_1,)).fetchone()

    ass = Assessments(
        competency_id,
        name,
        date_created,
        assessment_id,
    )
    return ass


def get_ass_res():
    view_all_assess_res()
    assessment_id_1 = input("Which Assessment?(Assessment_id)\n>>> ")
    query = "SELECT * FROM Assessment_Results WHERE assessment_res_id LIKE ?"

    (
        assessment_res_id,
        user_id,
        assessment_id,
        score,
        date_taken,
        manager,
        active,
    ) = cursor.execute(query, (assessment_id_1,)).fetchone()

    ass_res = Assessments_Results(
        score,
        date_taken,
        manager,
        active,
        user_id,
        assessment_id,
        assessment_res_id,
    )
    return ass_res


def login():
    user_email = input("What is your email?\n>>> ")
    user_password = input("What is your password?\n>>> ").encode()
    user = cursor.execute(
        "SELECT password, user_type, user_id FROM Users WHERE email = ?", (user_email,)
    ).fetchone()
    hashed_password = user[0].encode()
    user_type = user[1]
    user_id = user[2]
    if bcrypt.checkpw(user_password, hashed_password):
        if user_type == 2:
            manager_menu(user_id)
        elif user_type == 1:
            user_menu(user_id)
        else:
            print("Incorrect information please try again")
    else:
        print("Incorrect information please try again")


def user_menu(current_user_id):
    while True:
        print(
            """
        [1] View competency and assessment data.
        [2] Change name, phone, gmail, and password.
        [3] Quit.
        """
        )
        user_choice = input("What would you like to do?\n>>> ")
        if user_choice == "1":
            view_user_comp_level(current_user_id)
        elif user_choice == "2":
            print(
                """
            [1] First Name
            [2] Last Name
            [3] Phone
            [4] Gmail
            [5] Password
            [6] Quit
            """
            )
            edit_choice = input("What would you like to do?\n>>> ")
            if edit_choice == "1":
                my_user = get_user(current_user_id)
                my_user.user_info()
                my_user.first_name = input(
                    "What's the updated first name you want?\n>>> "
                )
                my_user.db_update_users()
                break
            elif edit_choice == "2":
                my_user = get_user(current_user_id)
                my_user.user_info()
                my_user.last_name = input(
                    "What's the updated last name you want?\n>>> "
                )
                my_user.db_update_users()
                break
            elif edit_choice == "3":
                my_user = get_user(current_user_id)
                my_user.user_info()
                my_user.phone = input("What's the updated Phone Number you want?\n>>> ")
                my_user.db_update_users()
                break
            elif edit_choice == "4":
                my_user = get_user(current_user_id)
                my_user.user_info()
                my_user.email = input("What's the updated Email you want?\n>>> ")
                my_user.db_update_users()
                break
            elif edit_choice == "5":
                my_user = get_user(current_user_id)
                my_user.user_info()
                password = input("What's the updated Password you want?\n>>> ")
                my_user.password = bcrypt.hashpw(
                    password.encode(), salt=bcrypt.gensalt()
                ).decode()
                my_user.db_update_users()
                break
            elif edit_choice == "6":
                print("Goodbye")
                break
            else:
                print("Invaild option please try again")
        elif user_choice == "3":
            print("Goodbye")
            break
        else:
            print("Invaild option please try again")


def manager_menu(current_user_id):
    while True:
        print(
            """ 
            [1] Add Users, Competencies, Assessments, and Assessements results to the table.
            [2] Edit Users, Competencies, Assessments, and Assessements results for the table.
            [3] View Users, A report of all users and their competency levels,
                view a competency level for an individual user, view a list of assessments for a given user.
            [4] Delete an Assessment result.
            [5] View or export to csv competency summary, or competency results summary 
            [6] Quit.
            """
        )
        user_choices = input("What would you like to do?\n>>> ")
        if user_choices == "1":
            print(
                """ 
                [1] Add to Users table
                [2] Add to Competencies table
                [3] Add to Assessments table
                [4] Add to Assessents Results
                [5] Quit
                """
            )
            add_choice = input("What would you like to do?\n>>> ")
            if add_choice == "1":
                user_add_add()
                break
            elif add_choice == "2":
                comp_add()
                break
            elif add_choice == "3":
                assess_add()
            elif add_choice == "4":
                assess_res_add()
                break
            elif add_choice == "5":
                print("Goodbye")
                break
            else:
                print("Invaild option please try again")
        elif user_choices == "2":
            print(
                """ 
                [1] Edit Users table
                [2] Edit Competencies table
                [3] Edit Assessments table
                [4] Edit Assessents Results
                [5] Quit
                """
            )
            user_add = input("What would you like to edit?\n>>> ")
            if user_add == "1":
                print(
                    """
                    [1] First name
                    [2] Last Name
                    [3] Phone
                    [4] Email
                    [5] Password
                    [6] Date Created
                    [7] Hire Date
                    [8] User Type
                    [9] Active
                    [10] Quit

                    """
                )

                edit_choice = input("Which option would you like to update?\n>>> ")

                my_user = get_user()
                my_user.user_info()

                if edit_choice == "1":
                    my_user.first_name = input(
                        "What's the updated First Name you want?\n>>> "
                    )
                    my_user.db_update_users()
                    break
                elif edit_choice == "2":
                    my_user.last_name = input(
                        "What's the updated Last Name you want?\n>>> "
                    )
                    my_user.db_update_users()
                    break
                elif edit_choice == "3":
                    my_user.phone = input(
                        "What's the updated Phone Number you want?\n>>> "
                    )
                    my_user.db_update_users()
                    break
                elif edit_choice == "4":
                    my_user.email = input("What's the updated Email you want?\n>>> ")
                    my_user.db_update_users()
                    break
                elif edit_choice == "5":
                    password = input("What's the updated Password you want?\n>>> ")
                    my_user.password = bcrypt.hashpw(
                        password.encode(), salt=bcrypt.gensalt()
                    ).decode()
                    my_user.db_update_users()
                    break
                elif edit_choice == "6":
                    my_user.date_created = input(
                        "What's the updated Date Created you want?\n>>> "
                    )
                    my_user.db_update_users()
                    break
                elif edit_choice == "7":
                    my_user.hire_date = input(
                        "What's the updated Hire Date you want?\n>>> "
                    )
                    my_user.db_update_users()
                    break
                elif edit_choice == "8":
                    my_user.user_type = input(
                        "What's the updated user type you want?\n>>> "
                    )
                    print(my_user.user_type)
                    my_user.db_update_users()
                    break
                elif edit_choice == "9":
                    my_user.active = input("What's the updated Active you want?\n>>> ")
                    my_user.db_update_users()
                    break
                elif edit_choice == "10":
                    print("Goodbye")
                    break
                else:
                    print("Invalid option try again")
            elif user_add == "2":
                print(
                    """
                    [1] Competency Name
                    [2] Date Created
                    [3] Quit

                    """
                )
                user_choice_2 = input("Which option would you like to update?\n>>> ")
                my_user = get_comp()
                my_user.comp_info()

                if user_choice_2 == "1":
                    my_user.name = input(
                        "What's the new updated competency name you want?\n>>> "
                    )
                    my_user.db_update_comp()
                    break
                elif user_choice_2 == "2":
                    my_user.date_created = input(
                        "What's the new date created you want?\n>>> "
                    )
                    my_user.db_update_comp()
                    break
                elif user_choice_2 == "3":
                    print("Goodbye")
                    break
                else:
                    print("Invaild option try again")

            elif user_add == "3":
                my_user = get_ass()
                my_user.assess_info()
                print(
                    """
                    [1] Assessment Name
                    [2] Date Created
                    [3] Quit

                    """
                )
                assess_choice = input("What would you like to do?\n>>> ")
                if assess_choice == "1":
                    my_user.name = input(
                        "What's the new Assessment name you want?\n>>> "
                    )
                    my_user.db_update_assess()
                    break
                elif assess_choice == "2":
                    my_user.date_created = input(
                        "What's the new Date Created you want?\n>>> "
                    )
                    my_user.db_update_assess()
                    break
                elif assess_choice == "3":
                    print("Goodbye")
                    break
                else:
                    print("Invaild option please try again")

            elif user_add == "4":
                my_user = get_ass_res()
                my_user.assess_info_res()
                print(
                    """
                        [1] Score
                        [2] Date Taken
                        [3] quit

                        """
                )
                assess_choice = input("What would you like to do?\n>>> ")
                if assess_choice == "1":
                    my_user.score = input(
                        "What's the new Assessment name you want?\n>>> "
                    )
                    my_user.db_update_assess_res()
                    break
                elif assess_choice == "2":
                    my_user.date_taken = input(
                        "What's the new Date Created you want?\n>>> "
                    )
                    my_user.db_update_assess_res()
                    break
                elif assess_choice == "3":
                    print("Goodbye")
                    break
                else:
                    print("Invaild option please try again")
            elif user_add == "5":
                print("GoodBye")
                break
            else:
                print("Invaild option please try again")
        elif user_choices == "3":
            print(
                """
            [1] View all users or search for a user with first name or last name.
            [2] View a report of all users and their competency levels for a given competency
            [3] View a competency level report for an individual user
            [4] View a list of assessments for a given user
            [5] Quit
            """
            )
            view_choice = input("What would you like to do?\n>>> ")
            if view_choice == "1":
                view_all_users()
            elif view_choice == "2":
                view_comp_level()
            elif view_choice == "3":
                view_user_comp_level()
            elif view_choice == "4":
                user_comp_sum()
            elif view_choice == "5":
                print("Goodbye")
                break
            else:
                print("Invaild option please try again")

        elif user_choices == "4":
            my_user = get_ass_res()
            my_user.assess_info_res()
            my_user.active = 0
            my_user.db_update_assess_res()
        elif user_choices == "5":
            print(
                """
            [1] View User Competency Summary
            [2] Competency Results Summary
            [3] Export User Competency Summary
            [4] Export Competency Results Summary
            [5] Quit
            """
            )
            sum = input("Which one would you like?\n>>> ")
            if sum == "1":
                user_comp_sum()
            elif sum == "2":
                comp_res_sum()
            elif sum == "3":
                user_comp_sum(True)
            elif sum == "4":
                comp_res_sum(True)
            elif sum == "5":
                print("Goodbye")
                break
            else:
                print("Invaild option please try again.")

        elif user_choices == "6":
            print("Goodbye")
            break
        else:
            print("Invalid option pleade try again")


login()
