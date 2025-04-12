import uuid

class Employee:

  def __init__(self, client_id, employee_name, employee_email, literacy_score, seniority, degree_type,
                gender, department, age):
    self.client_id = client_id
    self.employee_id = str(uuid.uuid4())
    self.employee_name = employee_name
    self.email = employee_email
    self.literacy_score = literacy_score
    self.seniority = seniority
    self.degree_type = degree_type
    self.gender = gender
    self.department = department
    self.age = age
    