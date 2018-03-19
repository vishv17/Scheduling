from django.shortcuts import render,redirect
from django.views import generic
from django.views.generic import View
from django import views
from rest_framework import serializers
import MySQLdb,json,operator,random
from collections import OrderedDict
from operator import itemgetter
from random import randint
from peewee import *
from django.shortcuts import render_to_response,render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from time_table_models1 import TimetableFinalCourse,TimetableFinalDescipline,TimetableFinalDesciplineCourse,TimetableFinalClassroom,TimetableFinalShift,TimetableFinalTimeslot,TimetableFinalClassroomAvailable,TimetableFinalDay,TimetableFinalFaculty,TimetableFinalSemester,TimetableFinalSubject,TimetableFinalFacultySubject,TimetableFinalLab,TimetableFinalLabAvailable,TimetableFinalSemesterBatch,TimetableFinalSemesterClassroom,TimetableFinalSemesterLab,TimetableFinalSubjectBatch,TimetableFinalSubjectNoStudent,TimetableFinalSubjectScheme,TimetableFinalTimeslotDay,TimetableFinalSubjectDiscipline,TimetableFinalSubjectLab
from .models import descipline,course,descipline_course,day,timeslot,lab,classroom,lab_available,classroom_available,semester,subject_no_student,shift,semester_classroom,semester_lab,subject_batch,semester_batch,subject,subject_scheme,faculty,faculty_subject,timeslot_day,subject_discipline,subject_lab

@csrf_exempt
def timetable_gen2(request):
	db=MySQLDatabase('time_table_test1',user='root',password='',host='localhost')
	db.connect()

	term="odd"
	course="B.E."
	discipline="Computer Enginnering"
	shift="Morning"
	temp_lab_list=[0,1,3,5]
	# temp_course=TimetableFinalCourse.get(TimetableFinalCourse.course_name==str(course)).course_name
	# temp_discipline=TimetableFinalDescipline.get(TimetableFinalDescipline.descipline_name==str(discipline)).descipline_name
	temp_course=TimetableFinalCourse.select().where(TimetableFinalCourse.course_name==course).get()

	# print("Hello")
	day_list=[]
	for d in TimetableFinalDay.select():
		day_list.append(str(d.day_name))

	timeslot_list=[]
	for t in TimetableFinalTimeslot.select():
		timeslot_list.append(str(t.timeslot_name))

	shift_list=[]
	for shift1 in TimetableFinalShift.select():
		shift_list.append(str(shift1.shift_name))

	semester_list=[]
	temp_discipline=TimetableFinalDescipline.select().where(TimetableFinalDescipline.descipline_name==discipline).get()
	temp_shift=TimetableFinalShift.get(TimetableFinalShift.shift_name==str(shift))
	temp_course_discipline=TimetableFinalDesciplineCourse.select().where((TimetableFinalDesciplineCourse.descipline_table_id==temp_discipline.id)&(TimetableFinalDesciplineCourse.course==temp_course.course)).get()
	temp_sem=TimetableFinalSemester.select().where((TimetableFinalSemester.term==term)&(TimetableFinalSemester.descipline_course_table_id==temp_course_discipline.id)&(TimetableFinalSemester.shift_table_id==temp_shift.id)&(TimetableFinalSemester.term==str(term)))
	for sem in temp_sem:
		semester_list.append(str(sem.semester_name))

	sem_sub={}
	for cou in TimetableFinalCourse.select():
		disc_dict={}
		for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
			sem_dict={}
			for sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==disc.id):
				sub_list=[]
				for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
					sub_list.append(str(sub.sub_code.sub_name))
                    # print(sem.semester_name,sub.sub_name)
					sem_dict[str(sem.semester_name)]=sub_list
			disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
		sem_sub[str(cou.course_name)]=disc_dict

	# sub_fac_detail={}
	# for temp_course in TimetableFinalCourse.select():
	# 	temp_discipline_dict={}
	# 	for temp_discipline in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
	# 		temp_sem_dict={}
	# 		for temp_sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline.id):
	# 			temp_sub_dict={}
	# 			for temp_sub_discipline in TimetableFinalSubjectDiscipline.select().where(TimetableFinalSubjectDiscipline.semester_table_id==temp_sem.id):
	# 				for temp_sub in TimetableFinalSubject.select().where(TimetableFinalSubject.sub_code==temp_sub_discipline.sub_code):
	# 					temp_fac_list=[]
	# 					for temp_fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==temp_sub.sub_code):
	# 						temp_fac_list.append((temp_fac.faculty.faculty,temp_fac.faculty.position,temp_fac.faculty.faculty_name,temp_fac.faculty.work_load))
	# 					temp_fac_list.sort(key=lambda tup:tup[1],reverse=True)
	# 					temp_i=0
	# 					temp_fac_dict={}
	# 					for temp_fac_2 in temp_fac_list:
	# 						temp_fac_dict[temp_i]={
	# 												'id':temp_fac_2[0],
	# 												'name':temp_fac_2[2],
	# 												'position':temp_fac_2[1],
	# 												'work_load':temp_fac_2[3]
	# 												}
	# 						temp_i+=1
	# 					sub_scheme_detail=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub).get()
	# 					no_batch=TimetableFinalSubjectNoStudent.get(TimetableFinalSubjectNoStudent.sub_code==temp_sub.sub_code).no_batch
	# 					temp_sub_dict[str(temp_sub.sub_name)]={
 #                                                                # 'sub_code':temp_sub.sub_code,
	# 															'sub_code':temp_sub.sub_code,
	# 															'sub_name':temp_sub.sub_name,
	# 															'is_elective':temp_sub.is_elective,
	# 															'faculty':temp_fac_dict,
	# 															'sub_load':sub_scheme_detail.sub_load,
	# 															'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
	# 															'sub_theory_class':sub_scheme_detail.sub_theory_class,
	# 															'sub_tutorial_class':sub_scheme_detail.sub_tutorial_class
	# 															}

	# 				temp_sem_dict[str(temp_sem.semester_name)]=temp_sub_dict
	# 		temp_discipline_dict[str(temp_discipline.descipline_table_id.descipline_name)]=temp_sem_dict
	# 	sub_fac_detail[str(temp_course.course_name)]=temp_discipline_dict
	
	sub_fac_detail={}
	for temp_course in TimetableFinalCourse.select():
		temp_discipline_dict={}
		for temp_discipline in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==temp_course.course):
			temp_sem_dict={}
			for temp_sem in TimetableFinalSemester.select().where(TimetableFinalSemester.descipline_course_table_id==temp_discipline.id):
				temp_shift_dict={}
				for shift in shift_list:
					temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
					temp_sub_dict={}
					for temp_sub_discipline in TimetableFinalSubjectDiscipline.select().where(TimetableFinalSubjectDiscipline.semester_table_id==temp_sem.id):
						for temp_sub in TimetableFinalSubject.select().where(TimetableFinalSubject.sub_code==temp_sub_discipline.sub_code):
							temp_fac_list=[]
							for temp_fac in TimetableFinalFacultySubject.select().where(TimetableFinalFacultySubject.sub_code==temp_sub.sub_code):
								# print(temp_fac.faculty.faculty)
								# print(str(temp_fac.shift_table_id.id),str(temp_shift.id))
								if temp_fac.shift_table_id.id==temp_shift.id:
									temp_fac_list.append((temp_fac.faculty.faculty,temp_fac.faculty.position,temp_fac.faculty.faculty_name,temp_fac.faculty.work_load))
							temp_fac_list.sort(key=lambda tup:tup[1],reverse=True)
							# print(temp_fac_list)
							temp_i=0
							temp_fac_dict={}
							for temp_fac_2 in temp_fac_list:
								temp_fac_dict[temp_i]={
													'id':temp_fac_2[0],
													'name':temp_fac_2[2],
													'position':temp_fac_2[1],
													'work_load':temp_fac_2[3]
													}
								temp_i+=1
							# print(temp_fac_dict)
							sub_scheme_detail=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub).get()
							no_batch=TimetableFinalSubjectNoStudent.get(TimetableFinalSubjectNoStudent.sub_code==temp_sub.sub_code).no_batch
							temp_sub_dict[str(temp_sub.sub_name)]={
																	'sub_code':temp_sub.sub_code,
																'sub_name':temp_sub.sub_name,
																'is_elective':temp_sub.is_elective,
																'faculty':temp_fac_dict,
																'sub_load':sub_scheme_detail.sub_load,
																# 'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
																'sub_practical_class':(sub_scheme_detail.sub_practical_class)*(no_batch),
																'sub_theory_class':sub_scheme_detail.sub_theory_class,
																'sub_tutorial_class':sub_scheme_detail.sub_tutorial_class
																}
					temp_shift_dict[str(shift)]=temp_sub_dict
				temp_sem_dict[str(temp_sem.semester_name)]=temp_shift_dict
			temp_discipline_dict[str(temp_discipline.descipline_table_id.descipline_name)]=temp_sem_dict
		sub_fac_detail[str(temp_course.course_name)]=temp_discipline_dict

	# print(sub_fac_detail)

	sem_sub={}		
	for cou in TimetableFinalCourse.select():
		disc_dict={}
		for disc in TimetableFinalDesciplineCourse.select().where(TimetableFinalDesciplineCourse.course==cou.course):
			sem_dict={}
			for sem in TimetableFinalSemester.select().where((TimetableFinalSemester.descipline_course_table_id==disc.id)&(TimetableFinalSemester.term==str(term))):
				sub_list=[]
				for sub in TimetableFinalSubjectDiscipline.select().where((TimetableFinalSubjectDiscipline.semester_table_id==sem.id)&(TimetableFinalSubjectDiscipline.descipline_course_table_id==disc.id)):
					temp_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==sub.sub_code).get()
					practical=temp_scheme.sub_practical_class
					if practical>0:
						sub_list.append(str(sub.sub_code.sub_name))
                    # print(sem.semester_name,sub.sub_name)
				sem_dict[str(sem.semester_name)]=sub_list
			disc_dict[str(disc.descipline_table_id.descipline_name)]=sem_dict
		sem_sub[str(cou.course_name)]=disc_dict

	sem_batch={}
	# for d in day_list:
	for sem in semester_list:
		batch_list=[]
		subject_list1=sem_sub[str(course)][str(discipline)][str(sem)]
		for sub in subject_list1:
			sub_code1=TimetableFinalSubject.get(TimetableFinalSubject.sub_name==sub).sub_code
			for batch in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==sub_code1):
				if str(batch.batch_name) not in batch_list:
					batch_list.append(str(batch.batch_name))
		sem_batch[str(sem)]=batch_list
	print(sem_batch)
		# for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
		# 	info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
		# 	for k1 in info3.keys():
		# 		temp_sub_name=info3['sub_name']
		# 		temp_sub_code=info3['sub_code']
		# 		batch_list=[]
		# 		for b in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==temp_sub_code):
		# 			batch_list.append(str(b.batch_name))
		# 		sub_batch[str(temp_sub_name)]=batch_list

	# sem_batch={}
	# for sem in semester_list:
	# 	batch_list=[]
	# 	subject_list1=sem_sub[str(course)][str(discipline)][str(sem)]
	# 	for sub in subject_list1:
	# 		temp_batch_list=sub_batch[str(sub)]
	# 		for b in temp_batch_list:
	# 			if b not in batch_list:
	# 				batch_list.append(b)
	# 	sem_batch[str(sem)]=batch_list
	# print(sub_batch)

	sem_timeslot={}
	for sem in semester_list:
		subject_list=sem_sub[str(course)][str(discipline)][str(sem)]
		length_of_subject_list=len(subject_list)
		temp1=(length_of_subject_list*2)+2
		timeslot_list1=[]
		if temp1>len(timeslot_list):
			timeslot_list1=timeslot_list
		else:
			for i in range(0,temp1+1):
				timeslot_list1[i]=timeslot_list[i]
		sem_timeslot[str(sem)]=timeslot_list1

	sem_lab={}
	for sem in semester_list:

		lab_list=[]

		temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
		# print(str(temp_sem.id))
		total_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_sem.id).no_batches
		for l in TimetableFinalSemesterLab.select().where(TimetableFinalSemesterLab.semester_table_id==temp_sem.id):
			# print(l.lab.lab)
			# print(str(l.semester_table_id_id))
			# lab_list.append(l.lab.lab)
			# print(str(l.lab_id),str(l.semester_table_id_id))
			lab_list.append(l.lab.lab)

	lab_available={}
	for l in TimetableFinalLabAvailable.select():
		shift_ava={}
		for shift in shift_list:
			day_ava={}
			temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
			for d in day_list:
				temp_day=TimetableFinalDay.select().where(TimetableFinalDay.day_name==str(d)).get()
				timeslot_ava={}
				for t in timeslot_list:
					temp_timeslot=TimetableFinalTimeslot.select().where((TimetableFinalTimeslot.timeslot_name==str(t))&(TimetableFinalTimeslot.shift_table_id==temp_shift.id)).get()
					timeslot_ava[str(temp_timeslot.timeslot_name)]=1
				day_ava[str(temp_day.day_name)]=timeslot_ava
			shift_ava[str(shift)]=day_ava
		lab_available[str(l.lab.lab)]=shift_ava
		# sem_lab[str(sem)]=lab_available



	# print(sem_batch)


	# print(lab_available)

	course_dict={}
	discipline_dict={}
	sem_dict={}
	for sem in semester_list:
		temp_sem=TimetableFinalSemester.select().where(TimetableFinalSemester.semester_name==sem).get()
		timeslot_list=sem_timeslot[str(sem)]
		subject_list=sem_sub[str(course)][str(discipline)][str(sem)]
		# print(sem,subject_list)
		# print(subject_list)
		total_batch=TimetableFinalSemesterBatch.get(TimetableFinalSemesterBatch.semester_table_id==temp_sem.id).no_batches	
		print(total_batch,sem)
		shift_dict={}
		for shift in shift_list:
			
			temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
			# print("Hello")

			days_dict={}

			subject_batch_counter={}
			for sub in subject_list:
				temp_sub=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==sub).get()
				batch_dict={}
				for batch in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==temp_sub.sub_code):
					batch_dict[str(batch.batch_name)]=0
				subject_batch_counter[str(temp_sub.sub_name)]=batch_dict

			for d in day_list:
				new_temp_dict={}

				subject_counter={}
				for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
					info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
					for k1 in info3.keys():
						# sub1=info3[k1]
						subject_counter[str(info3['sub_name'])]=0
				# print(subject_counter)
				sub_batch={}
				# for d in day_list:
				for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
					info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
					for k1 in info3.keys():
						temp_sub_name=info3['sub_name']
						temp_sub_code=info3['sub_code']
						batch_list=[]
						for b in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==temp_sub_code):
							batch_list.append(str(b.batch_name))
						sub_batch[str(temp_sub_name)]=batch_list
				# print(sub_batch)

				faculty_counter={}
				for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)]:
					info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][info4]
	            	# print(sub_fac_detail[str(course)][str(discipline)][str(sem)][info4])
	            	# print(info3)
					for k1 in info3.keys():
	               	# sub1=info3[k1]
	               	# print(info3[k1],"Hello")
						faculties=info3['faculty']
						for k2 in faculties.keys():
							fac1=faculties[k2]
							faculty_counter[str(fac1['name'])]=0

				


				done_dict={}
				temp_done_batch_list=[]
				for sub in subject_list:
					done_dict[str(sub)]=temp_done_batch_list

				done_batch_list=[]

				timeslot_dict={}
				flag1=0
				for i in range(0,len(timeslot_list)):
					# print("Hello")
					t=randint(0,6)
					# print(t)
					timeslot=timeslot_list[t]
					if t not in temp_lab_list:
						while t not in temp_lab_list:
							t=randint(0,6)
					timeslot=timeslot_list[t]
					# print(timeslot,d)
					# print(t)
					# print("Hello",t)
					flag=0
					for lab in TimetableFinalSemesterLab.select().where(TimetableFinalSemesterLab.semester_table_id==temp_sem.id):
						# if sem_lab[str(sem)][str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]==1:
						if lab_available[str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]==1:
							# lab_name=lab.lab.lab_name
							# print("Hello")
							# print(t)
							
							for x in range(0,total_batch):
								# print(subject_list)
								sub=random.choice(subject_list)
								subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]
								prac=subject_detail['sub_practical_class']
								batch_list1=sub_batch[str(sub)]
								for b1 in batch_list:
									if b1 in done_batch_list:
										continue
									else:
										b=b1
								# b=random.choice(batch_list1)
								# if b in done_batch_list:
								# 	print(d)
								# 	b=random.choice(batch_list1)
								if subject_batch_counter[str(sub)][str(b)]>=prac:
									while subject_batch_counter[str(sub)][str(b)]>=prac:
										print(sub,prac)
										sub=random.choice(subject_list)
										subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]
										prac=subject_detail['sub_practical_class']
								# print(b,sub,d)
										# batch_list1=sub_batch[str(sub)]
										# b=random.choice(batch_list1)
								# if subject_counter[str(sub)]>=4 or prac<=0 or prac%2!=0:
								# 	print(subject_counter[str(sub)],sub,prac)
									# while subject_counter[str(sub)]>=2 or prac<=0 or prac%2!=0:
									# 	sub=random.choice(subject_list)						
									# 	subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]
									# 	print("Hello",sub,subject_counter[str(sub)])
									# 	prac=subject_detail['sub_practical_class']
								# print(sub)
								if len(course_dict)>0:
									pass
								elif len(sem_dict)>0:
									# print(b,d,sem<"UP")
									faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['faculty']
									faculty_flag=0
									for k in faculties:
										inner_flag=0
										fac1=faculties[k]
										if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=4:
											continue
										else:
											
											# print(batch_list1,sem,sub)
											# b=random.choice(batch_list1)
											# print(b,t)
											
											
											for k1 in sem_dict.keys():
												temp_shift_dict=sem_dict[str(k1)]
												for k2 in temp_shift_dict.keys():
													temp_days_dict=temp_shift_dict[str(k2)]
													temp_timeslot_dict=temp_days_dict[str(d)]
													if str(t) in temp_timeslot_dict:
														temp_info=temp_timeslot_dict[str(t)]
														info=temp_info['value']
														if info['faculty']==str(fac1['name']):
															inner_flag=1
											if inner_flag==1:
												continue
											else:
												# print(done_batch_list)
												# batch_list1=sub_batch[str(sub)]
												# print(batch_list1,sem,sub)
												# b=random.choice(batch_list1)
												# if b in done_batch_list:
												# 	while b in done_batch_list:
												# 		# print(b,t)
												# 		b=random.choice(batch_list)
												new_temp_dict[str(b)]={'faculty':str(fac1['name']),'subject':str(sub),'batch':str(b),'lab':str(lab.lab.lab_name)}
												# print(b,sub,d,"Down",sem)
												v=t
												for t1 in range(0,2):
													timeslot=timeslot_list[v]
													timeslot_dict[str(timeslot)]={'lab':1,'classroom':0,'value':new_temp_dict}
													if str(fac1['name']) in faculty_counter:
														faculty_counter[str(fac1['name'])]+=1
													else:
														faculty_counter[str(fac1['name'])]=1
													fac1['work_load']-=1
													if str(sub) in subject_counter:
														subject_counter[str(sub)]+=1
													else:
														subject_counter[str(sub)]=1
													# sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']-=1
													subject_batch_counter[str(sub)][str(b)]+=1
													v+=1
													lab_available[str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]=0

												done_batch_list.append(b)
												# print(done_batch_list,d)
												flag=1
												break#faculty[k]
								else:
									# print(b)
									# print("Hello")
									# print(b,d,sem,"Down")
									# print(sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)])
									faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['faculty']
									# print(faculties)
									# print(t)
									faculty_flag=0
									for k in faculties:
										fac1=faculties[k]
										if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=4:
											# print("Hello","no")
											continue
										else:
											# print("Hello")
											# batch_list1=sub_batch[str(sub)]
											# print(batch_list1,sem,sub,d)
											# b=random.choice(batch_list1)
											# # print(b,t)
											# # print(done_batch_list)
											# if b in done_batch_list:
											# 	while b in done_batch_list:
											# 		# print(b,t)
											# 		b=random.choice(batch_list)
										
											# print(done_batch_list,d)
											new_temp_dict[str(b)]={'faculty':str(fac1['name']),'subject':str(sub),'batch':str(b),'lab':str(lab.lab.lab_name)}
											v=t
											print(b,sub,d,"Down",sem)
											# print(v)
											for t1 in range(0,2):
												# print(t)
												timeslot=timeslot_list[v]
												timeslot_dict[str(timeslot)]={'lab':1,'classroom':0,'value':new_temp_dict}
												# print(timeslot_dict)
												if str(fac1['name']) in faculty_counter:
													faculty_counter[str(fac1['name'])]+=1
												else:
													faculty_counter[str(fac1['name'])]=1
												fac1['work_load']-=1
												if str(sub) in subject_counter:
													subject_counter[str(sub)]+=1
												else:
													subject_counter[str(sub)]=1
												# sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']-=1
												subject_batch_counter[str(sub)][str(b)]+=1
												v+=1
												lab_available[str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]=0
											done_batch_list.append(b)
											flag=1
											break#faculty['k']
											# faculty_flag=1
											# if faculty_flag==1:
											# 	inner_flag=1
											# 	flag1=1
											# 	break#k['faculty']
							if flag==1:
								flag1=1
								break#l['lab']
						# else:
						# 	#search for lab available
						# 	continue
					if flag1==1:
						break#timeslot
					# if flag1==1:
					# 	break		
				days_dict[str(d)]=timeslot_dict
			shift_dict[str(shift)]=days_dict
		sem_dict[str(sem)]=shift_dict
	discipline_dict[str(discipline)]=sem_dict
	course_dict[str(course)]=discipline_dict


							
							# sub=random.choice(subject_list)
							# subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(sub)]
							# prac=subject_detail['sub_practical_class']
							# if subject_counter[str(sub)]>=2 or prac<=0 or prac%2!=0:
							# 	while subject_counter[str(sub)]>=2 or prac<=0 or prac%2!=0:
							# 		sub=random.choice(subject_list)
							# 		subject_detail=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(sub)]
							# 		prac=subject_detail['sub_practical_class']
							# for batch in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==subject_detail['sub_code']):
							# 	if subject_batch_counter[str(subject_detail['sub_name'])][str(batch.batch_name)]>=2:
							# 		continue
							# 	else:
							# 		for lab in TimetableFinalSubjectLab.select().where(TimetableFinalSubjectLab.sub_code==subject_detail['sub_code']):
							# 			if sem_lab[str(sem)][str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]==1:


		

		# course_dict={}
		# subject_list=sem_sub[str(course)][str(discipline)][str(sem)]
		# for shift in shift_list:

		# 	# lab_available={}
		# 	# for l in lab_list:
		# 	# 	shift_ava={}
		# 	# 	for shift in shift_list:
		# 	# 		day_ava={}
		# 	# 		temp_shift=TimetableFinalShift.select().where(TimetableFinalShift.shift_name==str(shift)).get()
		# 	# 		for d in day_list:
		# 	# 			temp_day=TimetableFinalDay.select().where(TimetableFinalDay.day_name==str(d)).get()
		# 	# 			timeslot_ava={}
		# 	# 			for t in timeslot_list:
		# 	# 				temp_timeslot=TimetableFinalTimeslot.select().where((TimetableFinalTimeslot.timeslot_name==str(t))&(TimetableFinalTimeslot.shift_table_id==temp_shift.id)).get()
		# 	# 				timeslot_ava[str(temp_timeslot.timeslot_name)]=1
		# 	# 			day_ava[str(temp_day.day_name)]=timeslot_ava
		# 	# 		shift_ava[str(shift)]=day_ava
		# 	# 	lab_available[str(l)]=shift_ava

		# 	days_dict={}
		# 	subject_batch_counter={}
		# 	faculty_counter={}
		# 	subject_counter={}
		# 	for d in day_list:
		# 		for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)]:
		# 			info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][info4]
		# 			for k1 in info3.keys():
		# 				# sub1=info3[k1]
		# 				subject_counter[str(info3['sub_name'])]=0
		# 		timeslot_dict={}

		# 		sub_batch={}
		# 		for d in day_list:
		# 			for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)]:
		# 				info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][info4]
		# 				for k1 in info3.keys():
		# 					temp_sub_name=info3['sub_name']
		# 					temp_sub_code=info3['sub_code']
		# 					batch_list=[]
		# 					for b in TimetableFinalSubjectBatch.select().where(TimetableFinalSubjectBatch.sub_code==temp_sub_code):
		# 						batch_list.append(str(b.batch_name))
		# 					sub_batch[str(temp_sub_name)]=batch_list

		# 		for info4 in sub_fac_detail[str(course)][str(discipline)][str(sem)]:
		# 			info3=sub_fac_detail[str(course)][str(discipline)][str(sem)][info4]
	 #            	# print(sub_fac_detail[str(course)][str(discipline)][str(sem)][info4])
	 #            	# print(info3)
		# 			for k1 in info3.keys():
	 #                	# sub1=info3[k1]
	 #                	# print(info3[k1],"Hello")
		# 				faculties=info3['faculty']
		# 				for k2 in faculties.keys():
		# 					fac1=faculties[k2]
		# 					faculty_counter[str(fac1['name'])]=0
		# 		flag=0
		# 		while flag==0:
		# 			i=randint(0, 6)
		# 			if i not in temp_lab_list:
		# 				while i not in temp_lab_list:
		# 					i=randint(0, 6)
		# 			if len(course_dict)>0:
		# 				pass
		# 			elif len(days_dict)>0:
		# 				pass
		# 			else:
		# 				get_batch_list=[]
		# 				for x in range(0,total_batch+1):
		# 					sub=random.choice(subject_list)
		# 					temp_sub=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==str(sub)).get()
		# 					temp_sub_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code==temp_sub.sub_code).get()
		# 					if temp_sub_scheme.sub_practical_class<=0 and subject_counter[str(sub)]>=2:
		# 						while temp_sub_scheme.sub_practical_class<=0 and subject_counter[str(sub)]>=2:
		# 							sub=random.choice(subject_list)
		# 							temp_sub_scheme=TimetableFinalSubjectScheme.select().where(TimetableFinalSubjectScheme.sub_code.sub_name==sub).get()
		# 					subject_val=TimetableFinalSubject.select().where(TimetableFinalSubject.sub_name==sub).get()
		# 					t=timeslot_list[i]
		# 					for l in TimetableFinalSubjectLab.select().where(TimetableFinalSubjectLab.sub_code==subject_val.sub_code):
		# 						print(str(l.lab_id))
		# 						if lab_available[str(l.lab_id)][str(shift)][str(d)][str(t)]==1:
		# 							faculties=sub_fac_detail[str(course)][str(discipline)][str(temp_sem.semester_name)][str(sub)]['faculty']
		# 							inner_flag=0
		# 							for k in faculties:
		# 								fac1=faculties[k]
		# 								if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>1:
		# 									continue
		# 								else:
		# 									if len(get_batch_list)>0:
		# 										pass
		# 									else:
		# 										batch_list=sub_batch[str(sub)]
		# 										batch=random.choice(batch_list)
		# 										new_temp_dict[str(batch)]={'faculty':fac1['name'],'subject':str(sub)}
		# 										for x in range(0,2):
		# 											timeslot_dict[str(t)]={'lab':1,'classroom':0,'value':new_temp_dict}
		# 											if str(sub) in subject_counter:
		# 												subject_counter[str(sub)]+=1
		# 											else:
		# 												subject_counter[str(sub)]=1
		# 											fac1['work_load']-=1
		# 											sub_fac_detail[str(course)][str(discipline)][str(temp_sem.semester_name)][str(sub)]['sub_practical_class']-=1
		# 											if str(fac1['name']) in faculty_counter:
		# 												faculty_counter[str(fac1['name'])]+=1
		# 											else:
		# 												faculty_counter[str(fac1['name'])]=1
		# 											i+=1
		# 											inner_flag=1
		# 								if inner_flag==1:
		# 									break
		# 							if inner_flag==1:
		# 								flag=1
		# 								break


		# 						else:
		# 							continue
		# 		days_dict[str(d)]=timeslot_dict
		# 	course_dict[str(shift_name)]=days_dict
	# return HttpResponse({"Hello":"Hello"}, content_type="application/json")
	return HttpResponse(json.dumps(course_dict), content_type="application/json")