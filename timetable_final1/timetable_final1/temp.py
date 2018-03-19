# print(done_batch_list,"Done")
									faculties=sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['faculty']
									faculty_flag=0
									for k in faculties:
										inner_flag=0
										fac1=faculties[k]
										if fac1['work_load']<=0 or faculty_counter[str(fac1['name'])]>=1:
											continue
										else:
											batch_list1=sub_batch[str(sub)]
											# print(batch_list1,sem,sub)
											b=random.choice(batch_list1)
											# print(b,t)
											
											if b in done_batch_list:
												while b in done_batch_list:
													# print(b,t)
													b=random.choice(batch_list)
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
												batch_list1=sub_batch[str(sub)]
												# print(batch_list1,sem,sub)
												b=random.choice(batch_list1)
												if b in done_batch_list:
													while b in done_batch_list:
														# print(b,t)
														b=random.choice(batch_list)
												new_temp_dict[str(b)]={'faculty':str(fac1['name']),'subject':str(sub),'batch':str(b),'lab':str(lab.lab.lab_name)}
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
													sub_fac_detail[str(course)][str(discipline)][str(sem)][str(shift)][str(sub)]['sub_practical_class']-=1
													v+=1
													sem_lab[str(sem)][str(lab.lab.lab)][str(shift)][str(d)][str(timeslot)]=0
												done_batch_list.append(b)
												flag=1
												break#faculty[k]