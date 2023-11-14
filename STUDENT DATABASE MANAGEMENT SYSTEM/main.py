# packages
from flask import Flask,render_template,redirect,url_for,request,flash
from flask_mysqldb import MySQL

#cofiguration
app=Flask(__name__)
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="iamgroot@#$11"
app.config["MYSQL_DB"]="python_db"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql=MySQL(app)


#homepage
@app.route("/")
def home():
    cur=mysql.connection.cursor()
    sql="select id,s_name,age,upper(std) as std from student"
    cur.execute(sql)
    res=cur.fetchall()
    return render_template("home.html",a=res)


#insert new record
@app.route("/insert",methods=["GET","POST"])
def insert():
    if request.method=="POST":
        id=request.form["id"]
        name=request.form["name"]
        age=request.form["age"]
        std=request.form["std"]
        cur=mysql.connection.cursor()
        sql="insert into student values (%s,%s,%s,%s)"
        cur.execute(sql,[id,name,age,std])
        mysql.connection.commit()
        cur.close()
        flash("ADDED SUCCESSFULLY")
        return redirect(url_for("home"))

    return render_template("insert.html")

@app.route("/edit/<string:id>",methods=["GET","POST"])
def edit(id):
    cur=mysql.connection.cursor()
    if request.method=="POST":
        id = request.form["id"]
        name = request.form["name"]
        age = request.form["age"]
        std = request.form["std"]
        sql = "update student set s_name=%s,age=%s,std=%s where id=%s"
        cur.execute(sql, [name, age, std,id])
        mysql.connection.commit()
        cur.close()
        return redirect(url_for("home"))

    sql="select * from student where id=%s"
    cur.execute(sql,[id])
    res=cur.fetchone()
    flash("UPDATED SUCCESSFULLY")
    return render_template("edit.html",a=res)


@app.route("/delete/<string:id>",methods=["GET","POST"])
def delete(id):
    cur=mysql.connection.cursor()
    sql="delete from student where id=%s"
    cur.execute(sql,id)
    mysql.connection.commit()
    cur.close()
    flash("deleted successfully")
    return redirect(url_for("home"))


if(__name__=="__main__"):
    app.secret_key="abc123"
    app.run(debug=True)