from peewee import *

database = MySQLDatabase('time_table_test1', **{'user': 'root'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AuthGroup(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'auth_group'

class DjangoContentType(BaseModel):
    app_label = CharField()
    model = CharField()

    class Meta:
        db_table = 'django_content_type'
        indexes = (
            (('app_label', 'model'), True),
        )

class AuthPermission(BaseModel):
    codename = CharField()
    content_type = ForeignKeyField(db_column='content_type_id', rel_model=DjangoContentType, to_field='id')
    name = CharField()

    class Meta:
        db_table = 'auth_permission'
        indexes = (
            (('content_type', 'codename'), True),
        )

class AuthGroupPermissions(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')

    class Meta:
        db_table = 'auth_group_permissions'
        indexes = (
            (('group', 'permission'), True),
        )

class AuthUser(BaseModel):
    date_joined = DateTimeField()
    email = CharField()
    first_name = CharField()
    is_active = IntegerField()
    is_staff = IntegerField()
    is_superuser = IntegerField()
    last_login = DateTimeField(null=True)
    last_name = CharField()
    password = CharField()
    username = CharField(unique=True)

    class Meta:
        db_table = 'auth_user'

class AuthUserGroups(BaseModel):
    group = ForeignKeyField(db_column='group_id', rel_model=AuthGroup, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_groups'
        indexes = (
            (('user', 'group'), True),
        )

class AuthUserUserPermissions(BaseModel):
    permission = ForeignKeyField(db_column='permission_id', rel_model=AuthPermission, to_field='id')
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'auth_user_user_permissions'
        indexes = (
            (('user', 'permission'), True),
        )

class DjangoAdminLog(BaseModel):
    action_flag = IntegerField()
    action_time = DateTimeField()
    change_message = TextField()
    content_type = ForeignKeyField(db_column='content_type_id', null=True, rel_model=DjangoContentType, to_field='id')
    object = TextField(db_column='object_id', null=True)
    object_repr = CharField()
    user = ForeignKeyField(db_column='user_id', rel_model=AuthUser, to_field='id')

    class Meta:
        db_table = 'django_admin_log'

class DjangoMigrations(BaseModel):
    app = CharField()
    applied = DateTimeField()
    name = CharField()

    class Meta:
        db_table = 'django_migrations'

class DjangoSession(BaseModel):
    expire_date = DateTimeField(index=True)
    session_data = TextField()
    session_key = CharField(primary_key=True)

    class Meta:
        db_table = 'django_session'

class TimetableFinalCourse(BaseModel):
    course = PrimaryKeyField(db_column='course_id')
    course_name = CharField()

    class Meta:
        db_table = 'timetable_final_course'

class TimetableFinalDescipline(BaseModel):
    descipline_name = CharField()

    class Meta:
        db_table = 'timetable_final_descipline'

class TimetableFinalDesciplineCourse(BaseModel):
    course = ForeignKeyField(db_column='course_id', rel_model=TimetableFinalCourse, to_field='course')
    descipline_table_id = ForeignKeyField(db_column='descipline_table_id_id', rel_model=TimetableFinalDescipline, to_field='id')

    class Meta:
        db_table = 'timetable_final_descipline_course'

class TimetableFinalClassroom(BaseModel):
    classroom = PrimaryKeyField(db_column='classroom_id')
    classroom_name = CharField()
    descipline_course_table = ForeignKeyField(db_column='descipline_course_table_id', rel_model=TimetableFinalDesciplineCourse, to_field='id')

    class Meta:
        db_table = 'timetable_final_classroom'

class TimetableFinalDay(BaseModel):
    day_name = CharField()

    class Meta:
        db_table = 'timetable_final_day'

class TimetableFinalShift(BaseModel):
    shift_name = CharField()
    shift_time = CharField()

    class Meta:
        db_table = 'timetable_final_shift'

class TimetableFinalTimeslot(BaseModel):
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    timeslot_name = CharField()

    class Meta:
        db_table = 'timetable_final_timeslot'

class TimetableFinalClassroomAvailable(BaseModel):
    availability = IntegerField()
    classroom = ForeignKeyField(db_column='classroom_id', rel_model=TimetableFinalClassroom, to_field='classroom')
    day_id = ForeignKeyField(db_column='day_id_id', null=True, rel_model=TimetableFinalDay, to_field='id')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    timeslot_id = ForeignKeyField(db_column='timeslot_id_id', rel_model=TimetableFinalTimeslot, to_field='id')

    class Meta:
        db_table = 'timetable_final_classroom_available'

class TimetableFinalFaculty(BaseModel):
    descipline_course_table_id = ForeignKeyField(db_column='descipline_course_table_id_id', rel_model=TimetableFinalDesciplineCourse, to_field='id')
    faculty = PrimaryKeyField(db_column='faculty_id')
    faculty_name = CharField()
    position = IntegerField()
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    work_load = IntegerField()

    class Meta:
        db_table = 'timetable_final_faculty'

class TimetableFinalSubject(BaseModel):
    is_elective = IntegerField()
    sub_code = PrimaryKeyField()
    sub_name = CharField()

    class Meta:
        db_table = 'timetable_final_subject'

class TimetableFinalFacultySubject(BaseModel):
    faculty = ForeignKeyField(db_column='faculty_id', rel_model=TimetableFinalFaculty, to_field='faculty')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    sub_code = ForeignKeyField(db_column='sub_code', rel_model=TimetableFinalSubject, to_field='sub_code')

    class Meta:
        db_table = 'timetable_final_faculty_subject'

class TimetableFinalLab(BaseModel):
    descipline_course_table = ForeignKeyField(db_column='descipline_course_table_id', rel_model=TimetableFinalDesciplineCourse, to_field='id')
    lab = PrimaryKeyField(db_column='lab_id')
    lab_name = CharField()

    class Meta:
        db_table = 'timetable_final_lab'

class TimetableFinalLabAvailable(BaseModel):
    availability = IntegerField()
    day_id = ForeignKeyField(db_column='day_id_id', null=True, rel_model=TimetableFinalDay, to_field='id')
    lab = ForeignKeyField(db_column='lab_id', rel_model=TimetableFinalLab, to_field='lab')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    timeslot_id = ForeignKeyField(db_column='timeslot_id_id', rel_model=TimetableFinalTimeslot, to_field='id')

    class Meta:
        db_table = 'timetable_final_lab_available'

class TimetableFinalSemester(BaseModel):
    descipline_course_table_id = ForeignKeyField(db_column='descipline_course_table_id_id', rel_model=TimetableFinalDesciplineCourse, to_field='id')
    semester_name = CharField()
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    term = CharField()

    class Meta:
        db_table = 'timetable_final_semester'

class TimetableFinalSemesterBatch(BaseModel):
    no_batches = IntegerField()
    semester_table_id = ForeignKeyField(db_column='semester_table_id_id', rel_model=TimetableFinalSemester, to_field='id')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')

    class Meta:
        db_table = 'timetable_final_semester_batch'

class TimetableFinalSemesterClassroom(BaseModel):
    classroom = ForeignKeyField(db_column='classroom_id', rel_model=TimetableFinalClassroom, to_field='classroom')
    semester_table_id = ForeignKeyField(db_column='semester_table_id_id', rel_model=TimetableFinalSemester, to_field='id')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')

    class Meta:
        db_table = 'timetable_final_semester_classroom'

class TimetableFinalSemesterLab(BaseModel):
    lab = ForeignKeyField(db_column='lab_id', rel_model=TimetableFinalLab, to_field='lab')
    semester_table_id = ForeignKeyField(db_column='semester_table_id_id', rel_model=TimetableFinalSemester, to_field='id')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')

    class Meta:
        db_table = 'timetable_final_semester_lab'

class TimetableFinalSubjectBatch(BaseModel):
    batch_name = CharField()
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    sub_code = ForeignKeyField(db_column='sub_code', rel_model=TimetableFinalSubject, to_field='sub_code')

    class Meta:
        db_table = 'timetable_final_subject_batch'

class TimetableFinalSubjectDiscipline(BaseModel):
    descipline_course_table_id = ForeignKeyField(db_column='descipline_course_table_id_id', rel_model=TimetableFinalDesciplineCourse, to_field='id')
    semester_table_id = ForeignKeyField(db_column='semester_table_id_id', rel_model=TimetableFinalSemester, to_field='id')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    sub_code = ForeignKeyField(db_column='sub_code_id', rel_model=TimetableFinalSubject, to_field='sub_code')

    class Meta:
        db_table = 'timetable_final_subject_discipline'

class TimetableFinalSubjectLab(BaseModel):
    lab = ForeignKeyField(db_column='lab_id', rel_model=TimetableFinalLab, to_field='lab')
    sub_code = ForeignKeyField(db_column='sub_code_id', rel_model=TimetableFinalSubject, to_field='sub_code')

    class Meta:
        db_table = 'timetable_final_subject_lab'

class TimetableFinalSubjectNoStudent(BaseModel):
    no_batch = IntegerField()
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    sub_code = ForeignKeyField(db_column='sub_code', rel_model=TimetableFinalSubject, to_field='sub_code')

    class Meta:
        db_table = 'timetable_final_subject_no_student'

class TimetableFinalSubjectScheme(BaseModel):
    sub_code = ForeignKeyField(db_column='sub_code', rel_model=TimetableFinalSubject, to_field='sub_code')
    sub_load = IntegerField()
    sub_practical_class = IntegerField()
    sub_theory_class = IntegerField()
    sub_tutorial_class = IntegerField()

    class Meta:
        db_table = 'timetable_final_subject_scheme'

class TimetableFinalTimeslotDay(BaseModel):
    day_id = ForeignKeyField(db_column='day_id_id', rel_model=TimetableFinalDay, to_field='id')
    faculty_subject_table_id = ForeignKeyField(db_column='faculty_subject_table_id_id', rel_model=TimetableFinalFacultySubject, to_field='id')
    resource = IntegerField(db_column='resource_id')
    resource_type = IntegerField()
    semester_table_id = ForeignKeyField(db_column='semester_table_id_id', rel_model=TimetableFinalSemester, to_field='id')
    shift_table_id = ForeignKeyField(db_column='shift_table_id_id', rel_model=TimetableFinalShift, to_field='id')
    timeslot_table_id = ForeignKeyField(db_column='timeslot_table_id_id', rel_model=TimetableFinalTimeslot, to_field='id')

    class Meta:
        db_table = 'timetable_final_timeslot_day'

