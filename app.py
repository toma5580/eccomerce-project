from flask import *
import pymysql

# Server starts
app = Flask(__name__)
# SESSIONS
# step 1: Provide secret key to your application
# Avoid session hijacking, cross -site scripting
app.secret_key = "$%6^^%4587" "qwedguyrterehgddkjhfj~``1```1...:;;;';ljefgtyhfdjh12457k"


#  Vendor Registration
@app.route("/vendor_registration", methods=["POST", "GET"])
def register_vendor():
    if request.method == "POST":
        vendor_name = request.form["name"]
        vendor_contact = request.form["contact"]
        vendor_email = request.form["email"]
        vendor_location = request.form["location"]
        vendor_password = request.form["password"]

        vendor_photo = request.files["photo"]
        vendor_photo.save("static/images/" + vendor_photo.filename)

        vendor_desc = request.form["desc"]

        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )

        cursor = connection.cursor()

        data = (
            vendor_name,
            vendor_contact,
            vendor_email,
            vendor_location,
            vendor_password,
            vendor_photo.filename,
            vendor_desc,
        )

        sql = "insert into vendors (vendor_name, vendor_contact, vendor_email, vendor_location,vendor_password,vendor_profilephoto,vendor_desc) values(%s,%s,%s,%s,%s,%s,%s)"

        cursor.execute(sql, data)
        connection.commit()
        return render_template(
            "vendor_register.html", message="Vendor Registered Successfully"
        )

    else:
        return render_template("vendor_register.html", message="Please Register Here")


@app.route("/vendor_login", methods=["POST", "GET"])
def vendor_login():
    if request.method == "POST":
        username = request.form["name"]
        password = request.form["password"]
        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )

        cursor = connection.cursor()
        sql = "select * from vendors where vendor_name =%s and vendor_password =%s"
        data = (username, password)
        cursor.execute(sql, data)

        count = cursor.rowcount
        if count == 0:
            return render_template("vendor_login.html", message="Invalid Credential")
        else:
            # sessions : Store Information About a specific user
            user_record = cursor.fetchone()
            session["key"] = user_record[1]
            session["vendor_id"] = user_record[0]
            session["contact"] = user_record[2]
            session["location"] = user_record[4]
            session["profile"] = user_record[5]
            session["desc"] = user_record[7]
            return redirect("/vendor_profile")
    else:
        return render_template("vendor_login.html", mesage="Please Login Here")


@app.route("/vendor_profile")
def vendor_profile():
    if "key" in session:
        return render_template("vendor_profile.html")
    else:
        return redirect("/vendor_login")


@app.route("/vendor_logout")
def vendor_logout():
    if "key" in session:
        session.clear()
    return redirect("/vendor_login")


@app.route("/add_product", methods=["POST", "GET"])
def add_product():
    if request.method == "POST":
        product_name = request.form["name"]
        product_desc = request.form["desc"]
        product_cost = request.form["cost"]
        product_discount = request.form["discount"]
        product_category = request.form["category"]
        product_brand = request.form["brand"]
        image_url = request.files["image"]
        image_url.save("static/products/" + image_url.filename)

        vendor_id = request.form["vendor"]

        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


        cursor = connection.cursor()
        data = (
            product_name,
            product_desc,
            product_cost,
            product_discount,
            product_category,
            product_brand,
            image_url.filename,
            vendor_id,
        )
        sql = "insert into products(product_name, product_desc, product_cost, product_discount, product_category,product_brand,image_url, vendor_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql, data)
        connection.commit()

        return render_template(
            "vendor_profile.html", message="Product Added Successfully"
        )
    else:
        return render_template(
            "vendor_profile.html", message="Please Add Product Details"
        )


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view_products")
def view_products():
    connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


    cursor = connection.cursor()

    sql = "select * from products where vendor_id = %s"

    cursor.execute(sql, session["vendor_id"])
    count = cursor.rowcount

    if count == 0:
        return render_template("view_products.html", message="No products available")
    else:
        data = cursor.fetchall()
        return render_template("view_products.html", products=data)


@app.route("/buy_products")
def buy_products():
    connection = pymysql.connect(
        host="localhost", user="root", password="Admin", database="IshopDB"
    )

    #  phones

    cursor_Phones = connection.cursor()
    sql_Phones = "select * from products where product_category = 'phones' order by rand() limit 6"
    cursor_Phones.execute(sql_Phones)
    Phones = cursor_Phones.fetchall()

    #  Laptops

    cursor_laptop = connection.cursor()
    sql_laptop = "select * from products where product_category = 'laptops'order by rand() limit 6"
    cursor_laptop.execute(sql_laptop)
    laptop = cursor_laptop.fetchall()

    #  shoes

    cursor_Clothes = connection.cursor()
    sql_Clothes = "select * from products where product_category = 'Clothes'order by rand() limit 6"
    cursor_Clothes.execute(sql_Clothes)
    Clothes = cursor_Clothes.fetchall()

    return render_template(
        "buy_products.html", Phones=Phones, laptop=laptop, Clothes=Clothes
    )


@app.route("/single_item/<product_id>")
def single_item(product_id):
    connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )

    cursor = connection.cursor()
    sql = "select * from products where product_id =%s"
    cursor.execute(sql, product_id)

    single_record = cursor.fetchone()

    category = single_record[5]
    cursor_similar = connection.cursor()
    sql_similar = (
        "select * from products where product_category =%s ORDER BY RAND() limit 3"
    )
    cursor_similar.execute(sql_similar, category)

    similar_products = cursor_similar.fetchall()

    return render_template(
        "single_item.html",
        single_record=single_record,
        similar_products=similar_products,
    )


@app.route("/user_register", methods=["POST", "GET"])
def user_register():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        password = request.form["password"]
        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


        cursor = connection.cursor()
        data = (username, phone, password)
        sql = "insert into users(username, phone, password) values(%s,%s,%s)"
        cursor.execute(sql, data)
        connection.commit()

        return render_template("user_register.html", message="Success!..")
    else:
        return render_template("user_register.html", message="Register Here..")
    
# User Login
@app.route("/user_login", methods=["POST", "GET"])
def user_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


        cursor = connection.cursor()
        sql = "select * from users where username =%s and password =%s"
        data = (username, password)
        cursor.execute(sql, data)

        count = cursor.rowcount
        if count == 0:
            return render_template("user_login.html", message="Invalid Credential")
        else:
            # sessions : Store Information About a specific user
            user_record = cursor.fetchone()
            session['user_key'] = user_record[1]
            session['phone'] = user_record[2]
             
            return redirect("/buy_products")
    else:
        return render_template("user_login.html", message="Please Login Here")
    
@app.route('/user_logout')
def user_logout():
    if 'user_key' in session:
        session.clear()
    return redirect('/user_login')

import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/mpesa', methods=['POST', 'GET'])
def mpesa_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])
        amount = str(request.form['amount'])
        # GENERATING THE ACCESS TOKEN
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "amount",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
            "AccountReference": "Modcom",
            "TransactionDesc": "Modcom"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return render_template("payment.html", message="Please Check Your Phone to Complete")
    else:
        return render_template('single_item.html')

@app.route('/delete/<product_id>')
def delete(product_id):
    connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )

    cursor = connection.cursor()

    sql = "delete from products where product_id =%s"
    cursor.execute(sql,product_id)
    connection.commit()

    return redirect('/view_products')

# Add/ post_feedback
@app.route("/save_feedback", methods=["POST", "GET"])
def user_feedback():
    if request.method == "POST":
        feedback_desc = request.form['feedback_desc']
        username = request.form["name"]
       
        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


        cursor = connection.cursor()
        data = (username,feedback_desc)
        sql = "insert into feedback (username,feedback_desc) values(%s,%s)"
        cursor.execute(sql,data)
        connection.commit()

        return render_template("feedback.html", message="Feedback Sent Successfully!..")
    else:
        return render_template('feedback.html')

   







# Add/ view_feedback
@app.route('/view_feedback')
def view_feedback():
    connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


    cursor = connection.cursor()

    sql = "select * from feedback"
    cursor.execute(sql)
    count = cursor.rowcount
    if count == 0:
        return render_template('view_feedback.html', message= 'No feedback Available')
    else:
        feedback=cursor.fetchall()
        return render_template('view_feedback.html', feedback =feedback)

# product update
@app.route('/update/<product_id>')
def update_products(product_id):
    if request.method =='POST':
        pass
    else:

        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )


        cursor = connection.cursor()
        sql = "select * from products where product_id = %s"
        cursor.execute(sql,product_id)
        data = cursor.fetchone()
        return render_template('update.html',data=data)
    
# update data


@app.route("/update/<product_id>", methods=["POST", "GET"])
def update_product(product_id):
    if request.method == "POST":
        product_name = request.form["name"]
        product_desc = request.form["desc"]
        product_cost = request.form["cost"]
        product_discount = request.form["discount"]
        product_category = request.form["category"]
        product_brand = request.form["brand"]
        image_url = request.files["image"]
        image_url.save("static/products/" + image_url.filename)

        vendor_id = request.form["vendor"]

        connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )

        cursor =connection.cursor()
        sql ="update products set product_name =%s,product_desc=%s,product_cost=%s, product_discount=%s, product_category=%s, product_brand=%s, image_url=%s where product_id =%s"
        data =(product_name,product_desc,product_cost,product_discount,product_category,product_brand,image_url.filename,product_id)
        cursor.execute(sql, data)
        connection.commit()
        return redirect('/view_products')

    else:
       connection = pymysql.connect(
            host="Toma254.mysql.pythonanywhere-services.com", user="Toma254", password="PzigraMM5580", database="Toma254$default"
        )



    cursor=connection.cursor()

    sql = 'select * from products where products_id = %s'
    cursor.execute(sql, product_id)
    data = cursor.fetchone()
    return render_template('update.html', data=data)









    


# app.run(debug=True)
# End

#  APPLICATIONS: CRUD operation
#  C - Create Record to a Database (INSERT INTO)
# R - Read/ Reatrieve (select)
# U - Update/PUT
# D- Delete
