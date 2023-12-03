create database student_management_system

use student_management_system

create table student(
	s_no nchar(20) primary key,
	s_name nchar(20) not null,
	s_sex nchar(20) not null check (s_sex = 'ÄÐ' or s_sex = 'Å®'),
	s_age int not null,
	s_classno nchar(20) not null
)

create table class(
	c_no nchar(20) primary key,
	c_major nchar(20) not null,
	c_college nchar(20) not null
)

create table choice(
	ch_student_no nchar(20),
	ch_course_no nchar(20),
	ch_score int not null,
	primary key (ch_student_no, ch_course_no)
)

create table course(
	co_no nchar(20) primary key,
	co_name nchar(40),
	co_time int not null,
	co_credit int not null 
)