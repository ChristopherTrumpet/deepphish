class Client:
  """Client object"""

  def __init__(self, name, industry, email, config):
    self.name = name
    self.industry = industry
    self.email = email
    self.config = config

  @property
  def name(self):
    return self._name

  @name.setter
  def name(self, value):
    self._name = value

  @property
  def industry(self):
    return self._industry

  @industry.setter
  def industry(self, value):
    self._industry = value

  @property
  def email(self):
    return self._email

  @email.setter
  def email(self, value):
    self._email = value

  @property
  def config(self):
    return self._config

  @config.setter
  def config(self, value):
    self._config = value