import sqlite3
import uuid

class DatabaseManager:
  def __init__(self, db_name=":memory:"):
    self.db_name = db_name
    self.conn = None
    self.cursor = None
    self.connect()
    self._create_tables()

  def connect(self):
    """Connect to the SQLite database."""
    self.conn = sqlite3.connect(self.db_name)
    self.cursor = self.conn.cursor()

  def close(self):
    """Close the database connection."""
    if self.conn:
      self.conn.close()

  def _create_tables(self):
    """Create the companies and employees tables if they don't exist."""
    try:
      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
          company_id TEXT PRIMARY KEY,
          company_name TEXT,
          company_email TEXT
        )
      """)
      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
          employee_id TEXT PRIMARY KEY,
          employee_name TEXT,
          company_id TEXT,
          email TEXT,
          literacy_score INTEGER,
          seniority INTEGER,
          degree_type INTEGER,
          gender INTEGER,
          department TEXT,
          age TEXT,
          risk_text TEXT,
          risk_value REAL,
          FOREIGN KEY (company_id) REFERENCES companies(company_id)
        )
      """)

      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
          company_id TEXT PRIMARY KEY REFERENCES companies(company_id),
          campaign_id TEXT, 
          company_name TEXT,
          company_email TEXT, 
          type TEXT, 
          start_time TEXT, 
          end_time TEXT, 
          status TEXT, 
          description TEXT            
          )                  
      """)

      self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS actions (
          campaign_id TEXT PRIMARY KEY REFERENCES campaigns(campaign_id), 
          company_id TEXT PRIMARY KEY REFERENCEs ccompanies(company_id), 
          company_name TEXT, 
          company_email TEXT, 
          type TEXT, 
          start_time TEXT, 
          end_time TEXT, 
          status TEXT, 
          description TEXT, 
          UNIQUE (campaign_id, company_id)                       
          )"""
        )

      self.cursor.execute()
      self.conn.commit()
    except sqlite3.Error as e:
      print(f"Error creating tables: {e}")

  def create_campaign(self, company_name, company_email, type, start_time, end_time="None", status="scheduled", description=""): 
    campaign_id = str(uuid.uuid4())

    self.cursor.execute("SELECT company_id from companies WHERE company_email = ? AND company_name = ?", (company_email, company_name))

    company_id = self.cursor.fetchone()

    try:
        self.cursor.execute("INSERT into campaigns (campaign_id, company_id, company_name, company_email, type, start_time, end_time, status, description) VALUES (?, ?, ? ,?, ?, ?, ?, ?, ?)",
                             (campaign_id, company_id, company_name, company_email, type, start_time, end_time, status, description))
        self.conn.commit()

        
        return campaign_id
    except sqlite3.Error as e: 
      print(f"Error creating campaign: {e}")
      return None

  def create_company(self, company_name, contact_email):
    """Create a new company."""
    company_id = str(uuid.uuid4())
    try:
      self.cursor.execute("""
        INSERT INTO companies (company_id, company_name, contact_email)
        VALUES (?, ?, ?)
      """, (company_id, company_name, contact_email))
      self.conn.commit()
      return company_id
    except sqlite3.Error as e:
      print(f"Error creating company: {e}")
      return None

  def get_company(self, company_id):
    """Retrieve a company by its ID."""
    try:
      self.cursor.execute("""
        SELECT * FROM companies WHERE company_id = ?
      """, (company_id,))
      company_data = self.cursor.fetchone()
      if company_data:
        columns = [description[0] for description in self.cursor.description]
        return dict(zip(columns, company_data))
      return None
    except sqlite3.Error as e:
      print(f"Error retrieving company: {e}")
      return None

  def get_company_by_name(self, company_name):
    """Retrieve a company by its name."""
    try:
      self.cursor.execute("""
          SELECT * FROM companies WHERE company_name = ?
      """, (company_name,))
      company_data = self.cursor.fetchone()
      if company_data:
        columns = [description[0] for description in self.cursor.description]
        return dict(zip(columns, company_data))
      return None
    except sqlite3.Error as e:
      print(f"Error retrieving company: {e}")
      return None

  def get_employee(self, employee_id):
    """Retrieve an employee by their ID."""
    try:
      self.cursor.execute("""
        SELECT * FROM employees WHERE employee_id = ?
      """, (employee_id,))
      employee_data = self.cursor.fetchone()
      if employee_data:
        columns = [description[0] for description in self.cursor.description]
        return dict(zip(columns, employee_data))
      return None
    except sqlite3.Error as e:
      print(f"Error retrieving employee: {e}")
      return None

  def get_employees_by_company(self, company_id):
    """Retrieve all employees belonging to a specific company."""
    try:
      self.cursor.execute("""
          SELECT * FROM employees WHERE company_id = ?
      """, (company_id,))
      employee_data_list = self.cursor.fetchall()
      if employee_data_list:
        columns = [description[0] for description in self.cursor.description]
        employees = [dict(zip(columns, employee_data)) for employee_data in employee_data_list]
        return employees
      return []
    except sqlite3.Error as e:
      print(f"Error retrieving employees for company {company_id}: {e}")
      return []
  
  def get_campaigns(self, company_id): 
    """Retrieve all employees belonging to a specific company."""
    try:
      self.cursor.execute("""
          SELECT * FROM campaigns WHERE company = ?
      """, (company_id))
      campaigns_list = self.cursor.fetchall()
      if campaigns_list:
        columns = [description[0] for description in self.cursor.description]
        campaigns = [dict(zip(columns, campaign_data)) for campaign_data in campaigns_list]
        return campaigns
      return []
    except sqlite3.Error as e:
      print(f"Error retrieving employees for company {company_id}: {e}")
      return []

  def update_employee(self, employee_id, employee_name=None, company_id=None, email=None,
                      literacy_score=None, seniority=None, degree_type=None, gender=None,
                      department=None, age=None, risk_text=None, risk_value=None):
    """Update an existing employee's information."""
    try:
      update_fields = {}
      if employee_name is not None:
        update_fields['employee_name'] = employee_name
      if company_id is not None:
        update_fields['company_id'] = company_id
      if email is not None:
        update_fields['email'] = email
      if literacy_score is not None:
        update_fields['literacy_score'] = literacy_score
      if seniority is not None:
        update_fields['seniority'] = seniority
      if degree_type is not None:
        update_fields['degree_type'] = degree_type
      if gender is not None:
        update_fields['gender'] = gender
      if department is not None:
        update_fields['department'] = department
      if age is not None:
        update_fields['age'] = age
      if risk_text is not None:
        update_fields['risk_text'] = risk_text
      if risk_value is not None:
        update_fields['risk_value'] = risk_value

      if not update_fields:
        return True  # No fields to update

      set_clause = ", ".join(f"{key} = ?" for key in update_fields)
      values = list(update_fields.values())
      values.append(employee_id)

      self.cursor.execute(f"""
        UPDATE employees
        SET {set_clause}
        WHERE employee_id = ?
      """, tuple(values))
      self.conn.commit()
      return True

    except sqlite3.Error as e:
      print(f"Error updating employee: {e}")
      return False

  def add_employee_to_company(self, company_id, employee_name, email, literacy_score,
                              seniority, degree_type, gender, department, age,
                              risk_text=None, risk_value=None):
    """Add a new employee to a specific company."""
    employee_id = str(uuid.uuid4())
    try:
      self.cursor.execute("""
          INSERT INTO employees (employee_id, employee_name, company_id, email,
                                  literacy_score, seniority, degree_type, gender,
                                  department, age, risk_text, risk_value)
          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      """, (employee_id, employee_name, company_id, email, literacy_score,
            seniority, degree_type, gender, department, age, risk_text, risk_value))
      self.conn.commit()
      return employee_id
    except sqlite3.Error as e:
      print(f"Error adding employee to company: {e}")
      return None

  def delete_company(self, company_id):
    """Delete a company and all associated employees."""
    try:
      # Delete associated employees first (optional, depends on requirements)
      self.cursor.execute("""
          DELETE FROM employees WHERE company_id = ?
      """, (company_id,))
      # Then delete the company
      self.cursor.execute("""
          DELETE FROM companies WHERE company_id = ?
      """, (company_id,))
      self.conn.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error deleting company: {e}")
      return False

  def remove_employee_from_company(self, employee_id):
    """Remove an employee from their current company (set company_id to NULL)."""
    try:
      self.cursor.execute("""
          UPDATE employees SET company_id = NULL WHERE employee_id = ?
      """, (employee_id,))
      self.conn.commit()
      return True
    except sqlite3.Error as e:
      print(f"Error removing employee from company: {e}")
      return False

