from collections import defaultdict
import weakref


class Student:
    __refs__ = defaultdict(list)


    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        self.__refs__[self.__class__].append(weakref.ref(self))
        

    def grade_lec(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            print('Ошибка: невозможно поставить отметку Лектору')


    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst


    def creat_average(self, course=None):        
        all_grades = []
        if course == None:
            for key in self.grades:              
                for i in self.grades[key]:
                    all_grades.append(i)
        else:
            for key in self.grades:
              if key == course:
                  for i in self.grades[key]:
                      all_grades.append(i)                             
        if len(all_grades) == 0:
            print('У', self.name, self.surname, 'пока нет оценок по курсу', course)
            av_rating = 0
        else:          
            av_rating = float(sum(all_grades) / len(all_grades))
        return round(av_rating, 1)  

    
    def differ_aver_grades(self, over):
        if isinstance(over, Student):
            if self.__lt__(over):
                print('Средняя оценка у студента', over.name, over.surname, 'круче, чем у студента', self.name, self.surname) 
            elif self.__eq__(over):
                print('Средняя оценка у студента', over.name, over.surname, 'на равных со студентом', self.name, self.surname)
            else:
                print('Средняя оценка у студента', over.name, over.surname, 'хуже, чем у студента', self.name, self.surname)
        else:
            print(over.name, over.surname,'не экземпляр класса Студент')


    def __str__(self):
      try:          
          return f"Имя:{self.name}\nФамилия:{self.surname}\nСредняя оценка за домашние задания:{self.creat_average()}\nКурсы в процессе изучения:{', '.join(self.courses_in_progress)}\nЗавершенные курсы:{', '.join(self.finished_courses)}"
      except:
          return f"У данного студента пока нет оценок!"
    

    def __lt__(self, over):        
        if self.creat_average() < over.creat_average():
            return True 
        else:
            return False


    def __eq__(self, over):        
        if self.creat_average() == over.creat_average():
            return True 
        else:
            return False
        

class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []
 

class Lecturer(Mentor):
    __refs__ = defaultdict(list)
    def __init__(self, *args):
        self.grades = {}
        super().__init__(*args)
        self.__refs__[self.__class__].append(weakref.ref(self))
        
  
    def __str__(self):
        try:
            grade = []
            for key in self.grades:              
                for i in self.grades[key]:
                  grade.append(i)
            av_rating = float(sum(grade) / len(grade))
            return f"Имя:{self.name}\nФамилия:{self.surname}\nСредняя   оценка за лекции:{round(av_rating, 1)}"

        except:
            return f"У данного лектора пока нет оценок!"
    

    def __lt__(self, over):        
        if self.creat_average() < over.creat_average():
            return True 
        else:
            return False


    def __eq__(self, over):        
        if self.creat_average() == over.creat_average():
            return True 
        else:
            return False


    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst


    def creat_average(self, course=None):      
        all_grades = []
        if course == None:
            for key in self.grades:              
                for i in self.grades[key]:
                    all_grades.append(i)
        else:
            for key in self.grades:
              if key == course:
                  for i in self.grades[key]:
                      all_grades.append(i)                             
        if len(all_grades) == 0:
            print('У', self.name, self.surname, 'пока нет оценок по курсу', course)
            av_rating = 0
        else:          
            av_rating = float(sum(all_grades) / len(all_grades))
        return round(av_rating, 1)

    
    def differ_aver_grades(self, over):
        if isinstance(over, Lecturer):
            if self.__lt__(over):
                print('Средняя оценка у лектора', over.name, over.surname, 'круче, чем у лектора', self.name, self.surname) 
            elif self.__eq__(over):
                print('Средняя оценка у лектора', over.name, over.surname, 'на равных с лектором', self.name, self.surname)
            else:
                print('Средняя оценка у лектора', over.name, over.surname, 'хуже, чем у лектора', self.name, self.surname)
        else:
            print(over.name, over.surname,'не экземпляр класса Лектор')


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            print('Ошибка: невозможно поставить отметку Студенту')
    def __str__(self):
          return f"Имя:{self.name}\nФамилия:{self.surname}"


def get_all_st_average(names, course):
    av_grade = []
    for num in range(len(list(Student.get_instances()))):
        if (list(Student.get_instances())[num].name + ' ' + list(Student.get_instances())[num].surname) in names:
            av_grade.append(list(Student.get_instances())[num].creat_average(course))
            
    print('средняя оценка всех студентов на курсе', course, ':', round(float(sum(av_grade) / len(av_grade)), 1))


def get_all_lec_average(names, course):
    av_grade = []
    for num in range(len(list(Lecturer.get_instances()))):
        if (list(Lecturer.get_instances())[num].name + ' ' + list(Lecturer.get_instances())[num].surname) in names:
            av_grade.append(list(Lecturer.get_instances())[num].creat_average(course))
            
    print('средняя оценка всех лекторов на курсе', course, ':', round(float(sum(av_grade) / len(av_grade)), 1))


best_student = Student('John', 'Wayne', 'male')
best_student.courses_in_progress += ['Python']
best_student.courses_in_progress += ['JAVA']
best_student.finished_courses += ['Dodge shooting']
bad_student = Student('Clint', 'Eastwood', 'male')
bad_student.courses_in_progress += ['Python', 'JAVA']
bad_student.finished_courses += ['Shooting at speed']

cool_reviewer = Reviewer('Some', 'Buddy')
middle_reviewer = Reviewer('Someone', 'Checker')
middle_reviewer.courses_attached += ['JAVA']
cool_reviewer.courses_attached += ['Python']
cool_lecturer = Lecturer('Andrey', 'Kalugin')
cool_lecturer.courses_attached += ['Python']
middle_lecturer = Lecturer('Ruoy', 'Eman')
middle_lecturer.courses_attached += ['Python', 'JAVA']
 
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 10)
cool_reviewer.rate_hw(best_student, 'Python', 11)
middle_reviewer.rate_hw(bad_student, 'JAVA', 10)
middle_reviewer.rate_hw(bad_student, 'JAVA', 10)
middle_reviewer.rate_hw(bad_student, 'JAVA', 10)

cool_reviewer.rate_hw(bad_student, 'Python', 10)
cool_reviewer.rate_hw(bad_student, 'Python', 10)
cool_reviewer.rate_hw(bad_student, 'Python', 10)
middle_reviewer.rate_hw(best_student, 'JAVA', 10)
middle_reviewer.rate_hw(best_student, 'JAVA', 10)
middle_reviewer.rate_hw(best_student, 'JAVA', 10)

best_student.grade_lec(cool_lecturer, 'Python', 10)
best_student.grade_lec(cool_lecturer, 'Python', 9)
best_student.grade_lec(cool_lecturer, 'Python', 10)
bad_student.grade_lec(middle_lecturer, 'JAVA', 1)
bad_student.grade_lec(middle_lecturer, 'JAVA', 3)
bad_student.grade_lec(middle_lecturer, 'JAVA', 5)

# print(cool_lecturer.grades)
# print(cool_reviewer.courses_attached)
print(best_student)
print(bad_student)
print(cool_reviewer)
print(middle_reviewer)
print(cool_lecturer)
print(middle_lecturer)

bad_student.differ_aver_grades(best_student)
cool_lecturer.differ_aver_grades(middle_lecturer)

List_students = ['John Wayne', 'Clint Eastwood']
List_lecturers = ['Ruoy Eman', 'Andrey Kalugin']

get_all_st_average(List_students, 'JAVA')  
get_all_lec_average(List_lecturers, 'JAVA')

print(middle_lecturer < cool_lecturer)
print(bad_student < best_student)
