from django.db import models

class descipline(models.Model):
    descipline_name=models.CharField(max_length=200)

    def __str__(self):
        return self.descipline_name

class course(models.Model):
    course_id=models.IntegerField(primary_key=True)
    course_name=models.CharField(max_length=200)

    def __str__(self):
        return self.course_name

class descipline_course(models.Model):
    descipline_table_id=models.ForeignKey('descipline',on_delete=models.CASCADE)
    course_id=models.ForeignKey('course',db_column='course_id',on_delete=models.CASCADE)

    def __str__(self):
        return self.descipline_table_id+" "+self.course_id

class day(models.Model):
    day_name=models.CharField(max_length=200)

    def __str__(self):
        return self.day_name

class timeslot(models.Model):
    timeslot_name=models.CharField(max_length=200)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)

    def __str__(self):
        return self.timeslot_name+" "+self.shift_table_id

class lab(models.Model):
    lab_id=models.AutoField(primary_key=True)
    lab_name=models.CharField(max_length=200)
    descipline_course_table=models.ForeignKey('descipline_course',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.lab_name
class classroom(models.Model):
    classroom_id=models.AutoField(primary_key=True)
    classroom_name=models.CharField(max_length=200)
    descipline_course_table=models.ForeignKey('descipline_course',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.classroom_name
class lab_available(models.Model):
    day_id=models.ForeignKey('day',on_delete=models.CASCADE,null=True)
    timeslot_id=models.ForeignKey('timeslot',on_delete=models.CASCADE)
    lab_id=models.ForeignKey('lab',db_column='lab_id',on_delete=models.CASCADE)
    availability=models.BooleanField(default=True)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.timeslot_id+" "+self.lab_id+" "+self.availability

class classroom_available(models.Model):
    day_id=models.ForeignKey('day',on_delete=models.CASCADE,null=True)
    timeslot_id=models.ForeignKey('timeslot',on_delete=models.CASCADE)
    classroom_id=models.ForeignKey('classroom',db_column='classroom_id',on_delete=models.CASCADE)
    availability=models.BooleanField(default=True)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.classroom_id+" "+self.timeslot_id+" "+self.availability

class semester(models.Model):
    semester_name=models.CharField(max_length=200)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)
    descipline_course_table_id=models.ForeignKey('descipline_course',on_delete=models.CASCADE)
    term=models.CharField(max_length=200,default="odd")

    def __str__(self):
        return self.semester_name+" "+self.shift_table_id+" "+self.descipline_course_table_id

class subject_no_student(models.Model):
    sub_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    no_batch=models.IntegerField()
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.sub_code+" "+self.no_batch

class shift(models.Model):
    shift_name=models.CharField(max_length=200)
    shift_time=models.CharField(max_length=200)

    def __str__(self):
        return self.shift_name+" "+self.shift_time

class semester_classroom(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    classroom_id=models.ForeignKey('classroom',db_column='classroom_id',on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.classroom_id+" "+self.semester_table_id

class semester_lab(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    lab_id=models.ForeignKey('lab',db_column='lab_id',on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.semester_table_id+" "+self.lab_id

class subject_batch(models.Model):
    subject_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    batch_name=models.CharField(max_length=200)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.subject_code+" "+self.batch_name

class semester_batch(models.Model):
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    no_batches=models.IntegerField()
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)
    def __str__(self):
        return self.semester_table_id+" "+self.no_batches

class subject(models.Model):
    sub_code=models.IntegerField(primary_key=True)
    sub_name=models.CharField(max_length=200)
    is_elective=models.BooleanField(default=False)

    def __str__(self):
        return self.sub_code+" "+self.sub_name

class subject_scheme(models.Model):
    sub_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    sub_load=models.IntegerField()
    sub_theory_class=models.IntegerField()
    sub_practical_class=models.IntegerField()
    sub_tutorial_class=models.IntegerField(default=0)

    def __str__(self):
        return self.sub_code+" "+self.sub_load

class faculty(models.Model):
    faculty_id=models.AutoField(primary_key=True)
    faculty_name=models.CharField(max_length=200)
    position=models.IntegerField()
    work_load=models.IntegerField()
    descipline_course_table_id=models.ForeignKey('descipline_course',on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.faculty_id+" "+self.faculty_name+" "+self.position

class faculty_subject(models.Model):
    faculty_id=models.ForeignKey('faculty',db_column='faculty_id',on_delete=models.CASCADE)
    sub_code=models.ForeignKey('subject',db_column='sub_code',on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE,default=1)

    def __str__(self):
        return self.faculty_id+" "+self.sub_code

class timeslot_day(models.Model):
    day_id=models.ForeignKey('day',on_delete=models.CASCADE)
    timeslot_table_id=models.ForeignKey('timeslot',on_delete=models.CASCADE)
    resource_type=models.BooleanField()
    resource_id=models.IntegerField()
    faculty_subject_table_id=models.ForeignKey('faculty_subject',on_delete=models.CASCADE)
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)

    def __str__(self):
        return self.day_id+" "+self.timeslot_table_id+" "+self.faculty_subject_table_id+" "+self.resource_id+" "+self.resource_type+" "+self.semester_table_id+" "+self.shift_table_id
class subject_discipline(models.Model):
    sub_code=models.ForeignKey('subject',on_delete=models.CASCADE)
    semester_table_id=models.ForeignKey('semester',on_delete=models.CASCADE)
    descipline_course_table_id=models.ForeignKey('descipline_course',on_delete=models.CASCADE)
    shift_table_id=models.ForeignKey('shift',on_delete=models.CASCADE)
class subject_lab(models.Model):
    sub_code=models.ForeignKey('subject',on_delete=models.CASCADE)
    lab_id=models.ForeignKey('lab',db_column='lab_id',on_delete=models.CASCADE)