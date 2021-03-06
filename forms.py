from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, IntegerField, TextField, SubmitField, validators, FieldList, FormField, FloatField, DateField
from wtforms_components.fields import SelectField
from wtforms.validators import DataRequired, Length, Email, Required
from wtforms import Form as NoCsrfForm
import datetime
import wtforms_json
from database_io import getTreatments

wtforms_json.init()
def getTreatmentForm(tariff = None):
    class Treatment(FlaskForm):
        treatments = SelectField(u'Treatments',  coerce=int)
        date = TextField('Date', validators=[DataRequired()])
        price = TextField(u'Value')
        modifier = SelectField(u'Modifier', choices= [(0, 'None'), (14,'Rendered hospital'),(13, 'Travelling cost')], default=0)
        submit = SubmitField('Submit')
        def initialise_SelectOption(self,list_ordered_by_category = None, featured_ordered_by_category = None,  *args, **kwargs):
            super(Treatment, self).__init__(*args, **kwargs)
            self.treatments.choices =  [(0, "Select treatment")] + featured_ordered_by_category + list_ordered_by_category

        def nestedObjects(something, filtered_result, featured_result):
            list_of_categories = []
            list_ordered_by_category = []
            featured_ordered_by_category = []
            for i in filtered_result:
                list_of_categories.append(i['category'])
            seen = {}
            dupes = []
            for x in list_of_categories:
                if x not in seen:
                    seen[x] = 1
            else:
                if seen[x] == 1:
                    dupes.append(x)
                seen[x] += 1
            for keys, values in seen.items():
                a = (keys, )
                b = []
                for x in filtered_result:
                    if x['category'] == keys:
                        b.append((x['item'],x['description']))
                c = a + (tuple(b,),)
                list_ordered_by_category.append(c)
            for i in featured_result:
                featured_ordered_by_category.append((i['item'],i['description']))
            featured_ordered_by_category  = [('Featured',) + (tuple(featured_ordered_by_category,),)]
            return list_ordered_by_category, featured_ordered_by_category

        def __init__(self, *args, **kwargs):
            if(tariff is not None):
                featured = [501, 303, 314, 703, 702, 401, 405, 317, 503, 107, 901]
                filtered_result = getTreatments(tariff)
                featured_result = getTreatments(tariff, featured)
                list_ordered_by_category, featured_ordered_by_category = self.nestedObjects(filtered_result, featured_result)
                self.initialise_SelectOption(list_ordered_by_category = list_ordered_by_category, featured_ordered_by_category = featured_ordered_by_category)
    return Treatment()



class Patient_mva(FlaskForm): 
    medical = StringField('Medical Aid')
    name = StringField(u'Full Name', validators=[DataRequired()])
    case = StringField(u'Case Number', validators=[DataRequired()])
    po = IntegerField(u'PO', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_pyhsio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])# default=datetime.datetime.today().date())
    submit = SubmitField('Continue')


class Patient_psemas(FlaskForm): 
    medical = StringField('Medical Aid')
    name = StringField(u'Full Name', validators=[DataRequired()])
    main = StringField(u'Main Member', validators=[DataRequired()])
    number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
    dob = StringField(u'Date of Birth', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_pyhsio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])# default=datetime.datetime.today().date())
    submit = SubmitField('Continue')

class Patient_other(FlaskForm): 
    medical = StringField('Medical Aid', validators=[DataRequired()])
    name = StringField(u'Full Name', validators=[DataRequired()])
    main = StringField(u'Main Member', validators=[DataRequired()])
    number = IntegerField(u'Medical Aid No:', validators=[DataRequired()])
    dob = StringField(u'Date of Birth', validators=[DataRequired()])
    tariff = SelectField(u'Tariff', choices = [("namaf_pyhsio_2014","Namaf Physio 2014"),("namaf_physio_2019", "Namaf Physio 2019"),("namaf_physio_2020", "Namaf Physio 2020")])
    date =  StringField(u'Invoice Date', validators=[DataRequired()])# default=datetime.datetime.today().date())
    submit = SubmitField('Continue')
