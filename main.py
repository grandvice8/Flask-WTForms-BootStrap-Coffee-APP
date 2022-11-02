from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SomeSecretKey'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location URL', validators=[DataRequired(), URL()])
    open = StringField('open time', validators=[DataRequired()])
    close = StringField('closing time', validators=[DataRequired()])
    coffee_rating = SelectField('coffee rating', validators=[DataRequired()], choices=('☕', '☕☕', '☕☕☕', '☕☕☕☕', '☕☕☕☕☕'))
    wifi_rating = SelectField('wifi Strength', validators=[DataRequired()], choices=('💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'))
    power_rating = SelectField('Power sockets?', validators=[DataRequired()], choices=('🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'))
    submit = SubmitField('Submit', validators=[DataRequired()])


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        new_row = []
        for item in form:
            if item != form.submit and item != form.csrf_token:
                new_row.append(item.data)
        print(new_row)
        with open('cafe-data.csv', 'a', newline='', encoding="utf8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(new_row)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
