import json

class Poll:
  def __init__(self, question, answers, duration, allow_multiselect):
    self.question = question
    self.answers = answers
    self.duration = duration
    self.allow_multiselect = allow_multiselect
    
  def toJSON(self):
      return json.dumps(
          self,
          default=lambda o: o.__dict__, 
          sort_keys=True,
          indent=4)

class PollMedia:
  def __init__(self, text):
    self.text = text
  
  # def __init__(self, text, emoji):
  #   self.text = text
  #   self.emoji = emoji

class PollAnswer:
  def __init__(self, poll_media):
    self.poll_media = poll_media