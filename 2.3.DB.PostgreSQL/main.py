import psycopg2 as pg

dbname = 'mydb'
user = 'rk0f'


def create():
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                create table Student (
                    id serial PRIMARY KEY,
                    name varchar(100) not null,
                    gpa numeric(10,2),
                    birth timestamp with time zone
                    );
                """)
            cur.execute("""
                create table Course (
                    id serial PRIMARY KEY,
                    name varchar(100) not null
                    );
                """)
            cur.execute("""
                create table Student_Course (
                    id serial PRIMARY KEY,
                    student_id INTEGER REFERENCES Student(id),
                    course_id INTEGER REFERENCES Course(id)
                    );
                """)


def get_students(course_id):
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""      
                select s.id, s.name, course.name from student s
                join student_course on student_course.student_id = s.id
                join course on course.id = (%s)""", (course_id,))
            return cur.fetchall()


def add_student(student):
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""
               insert into student (name, gpa, birth) values (%s, %s, %s);
               """, (student['name'], student['gpa'], student['birth']))


def add_students(course_id, students):
    for i in students:
        add_student(i)
        with pg.connect(dbname=dbname, user=user) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    select id from student where name = (%s);
                    """, (i['name'],))
                id_s = cur.fetchall()[0][0]
                cur.execute("""
                   insert into Student_Course (student_id, course_id) values
                   (%s, %s);
                   """, (id_s, course_id))


def get_student(student_id):
    with pg.connect(dbname=dbname, user=user) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                select * from student where id = (%s);
                """, (student_id,))
            return cur.fetchall()


if __name__ == '__main__':
    print(get_students(1))
