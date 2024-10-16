from abc import ABCMeta,abstractmethod

solid_salary_m = float(12000)
solid_salary_s = float(2000)

class Employee(metaclass= ABCMeta):
    def __init__(self,name):
        self.name = name

    @abstractmethod
    def get_salary(self):
        pass

class Manager(Employee):
    def __init__(self,name):
        super().__init__(name)

    def get_salary(self):
        return solid_salary_m

class Programmer(Employee):
    def __init__(self,name,work_time):
        super().__init__(name)
        self.work_time = work_time
    def get_salary(self):
        return self.work_time*200

class Salesman(Employee):
    def __init__(self,name,sales = 0.0):
        super().__init__(name)
        self.sales = sales

    def get_salary(self):
        return solid_salary_s + self.sales * 0.2

if __name__ == '__main__':
    emps = [ Manager('Clip') , Programmer('pXiang',40) , Salesman('fangshou',10000) ]
    for emp in emps:
        print(f'{emp.name} 工资：-- {emp.get_salary()}')
