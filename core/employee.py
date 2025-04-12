class Employee:

  def __init__(self, name, department, age, seniority):
    self.name = name
    self.department = department
    self.age = age
    self.senority = seniority

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value

  @property
  def department(self):
    return self._department

  @department.setter
  def department(self, value):
    self._department = value

  @property
  def age(self):
    return self._age

  @age.setter
  def age(self, value):
    self._age = value

  @property
  def seniority(self):
    return self._seniority

  @seniority.setter
  def seniority(self, value):
    self._seniority = value