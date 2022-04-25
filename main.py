from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, url
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'THE KEY'
Bootstrap(app)

# Creating WTF form
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), url()])
    opening = StringField('Opening time e.g. 8am', validators=[DataRequired()])
    closing = StringField('Closing time e.g. 5pm', validators=[DataRequired()])
    cafe_rating = SelectField('Cafe rating', choices=[('1', '✘'), ('2', '☕'), ('3', '☕☕'), ('4', '☕☕☕'), ('5', '☕☕☕☕'),
                                                      ('6', '☕☕☕☕☕')], validators=[DataRequired()])
    wifi_rating = SelectField('Wifi strength rating', choices=[('1', '✘'), ('2', '💪'), ('3', '💪💪'), ('4', '💪💪💪'),
                                                   ('5', '💪💪💪💪'), ('6', '💪💪💪💪💪')],  validators=[DataRequired()])
    power_socket = SelectField('Power socket availability', choices=[('1', '✘'), ('2', '🔌'), ('3', '🔌🔌'), ('4', '🔌🔌🔌'),
                                                 ('5', '🔌🔌🔌🔌'), ('6', '🔌🔌🔌🔌🔌')],  validators=[DataRequired()])

    submit = SubmitField('Submit')



# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")

# Secret path - Admin interface - adding new value
@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    # Initialiying form
    form = CafeForm()
    # Execute on submit
    if form.validate_on_submit():
        # EXAMPLE: -->
        # power_soc_dict = dict(form.power_socket.choices).get(form.power_socket.data)

    # Getting SelectFields value by converting it into a dict
        caf_rating_dict = dict(form.cafe_rating.choices).get(form.cafe_rating.data)
        wifi_rating_dict = dict(form.wifi_rating.choices).get(form.wifi_rating.data)
        power_soc_dict = dict(form.power_socket.choices).get(form.power_socket.data)
    # Store the in a list - easier to save
        list_of_items_to_Save = [f'{form.cafe.data},{form.location.data},{form.opening.data},{form.closing.data},'
                                 f'{caf_rating_dict},{wifi_rating_dict},{power_soc_dict}']

        with open('cafe-data.csv', 'a', newline='', encoding='utf8') as csv_file:
            csv_file.write(f'\n{list_of_items_to_Save[0]}')

        return redirect('/add')
    else:
        return render_template('add.html', form=form)

# Root of caffe
@app.route('/cafes')
def cafes():
    # Open and read current content in 'cafe-data.csv'
    with open('cafe-data.csv', newline='', encoding='utf8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            print(row)
            list_of_rows.append(row)
    # Declaring max length of all items so that in cafes.html I can use it when I loop with a slice
    # NOTE: I use it because -1 did not work to find last element
    total_of_cafe_items = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, total_of_cafe_items=total_of_cafe_items)

# Secret path - Render only
@app.route('/add')
def add():
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
