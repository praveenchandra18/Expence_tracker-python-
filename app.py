from flask import Flask,render_template,request
import mysql.connector

database=mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="expences"
)
cursor=database.cursor()

app=Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-expense',methods=['GET','POST'])
def add_expense():
    date=request.form['date']
    amount=request.form['amount']
    reason=request.form['description']
    query="""INSERT INTO expences (date,amount,reason)
                VALUES (%s,%s,%s)"""
    data=(date,amount,reason)
    cursor.execute(query,data)
    database.commit()
    message="data saved successfully!!"
    return render_template("home.html",add_message=message)

@app.route('/get-expenses',methods=['GET','POST'])
def get_expenses():
    month=request.form['month']
    year=month[:4]
    month=month[5:]
    query="""SELECT *
            FROM expences
            WHERE MONTH(date) =%s AND YEAR(date) = %s"""
    data=(month,year)
    cursor.execute(query,data)
    lst=cursor.fetchall()
    sum=0
    print(lst)
    for i in range(0,len(lst)):
        sum=sum+lst[i][1]
    message="The total amount spent is Rs. {}".format(sum)
    return render_template('home.html',list=lst,get_message=message)

if(__name__=='__main__'):
    app.run(debug=True)