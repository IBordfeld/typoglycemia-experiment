from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length

class StartScreen(FlaskForm):   
    first = StringField('First', validators=[DataRequired(), Length(min=2, max=20)])
    last = StringField('Last', validators=[DataRequired(), Length(min=2, max=20)])

    age = IntegerField("Age", validators=[DataRequired()])

    updatef = [(1,"Male"),(2,"Female")]
    sex = SelectField(u'Sex: ', choices = updatef, validators = [DataRequired()])

    submit = SubmitField('Sign Up')

    def get_info(self):
        return self.first.data, self.last.data, self.age.data, self.sex.data

class ExperimentScreen(FlaskForm):
    answer = StringField("Enter your response in the box", validators=[DataRequired()])
    submit = SubmitField('Submit Answer')

    def getAnswer(self):
        return self.answer

    def eraseAnswer(self):
        # Not sure if this works lol
        self.answer = ""
