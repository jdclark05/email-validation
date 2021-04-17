from flask import Flask,render_template,redirect,request,session,flash
import re
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)

app.secret_key = "validation"
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


@app.route('/', methods=['POST', 'GET'])
def add_email():
    if request.form:
        is_valid = True
        if not EMAIL_REGEX.match(request.form['email']):    # test whether a field matches the pattern
            flash("Invalid email address!")
            return redirect('/')
        else:
            query = "INSERT INTO email_addresses (email) VALUES (%(email)s);"
            data = {
                "email":request.form['email']
            }
            email_addresses = connectToMySQL('email-validation').query_db(query, data)
            if email_addresses is False:
                flash("Email already exists!")
                return redirect('/')
            return redirect("/display")
    else:
        return render_template("index.html")

@app.route('/display', methods=["GET"])
def display():
        query = "SELECT * FROM email_addresses;"
        email_addresses = connectToMySQL('email-validation').query_db(query)
        flash(f"The email address you entered {email_addresses[0]['email']} is valid!")
        return render_template("display.html", email_addresses=email_addresses)

@app.route('/delete_email/<int:id>', methods=["GET"])
def delete_user(id):
    query = "DELETE FROM email_addresses WHERE id = %(id)s;"
    data = {
        'id':id
    }

    email_addresses = connectToMySQL('email-validation').query_db(query, data)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)