import os
import codecs
import random
import string
import io
import html
import datetime
import mysql.connector
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from shutil import copyfile
from bs4 import BeautifulSoup,Tag
from unidecode import unidecode

UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = {'jpg', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.static_folder = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hochiminh/<int:hochiminhID>')
def hochiminhRender(hochiminhID):

    return render_template('/article.html')


@app.route('/hanoi/<int:hanoiID>')
def hanoiRender(hanoiID):

    return "hello Ha Noi"


@app.route('/danang/<int:danangID>')
def danangRender(danangID):

    return "hello Da Nang"


@app.route('/tinhkhac/<int:tinhkhacID>')
def tinhkhacRender(tinhkhacID):

    return "hello Tinh Khac"

@app.route('/demo')
def demo():
    return render_template('/pending/tieu-de-19.html')


@app.route('/postarticle', methods=['GET', 'POST'])
def postArticle():
    title_unidecode = ""
    if request.method == 'POST':
        email   =   request.form.get('email')
        name    =   request.form.get('name')
        address =   request.form.get('address');
        image   =   request.files['file'].read()
        title   =   request.form.get('title')
        description   =   request.form.get('description')
        content   =   request.form.get('content')
        thoi_gian = datetime.datetime.now()
       
        # title_unidecode = create_article(email,name,address,image,title,description,content)
        save_baiviet_to_database(email,name,address,image,title,description,content);

    # if len(title_unidecode)>0:
    #     return render_template('/pending/'+title_unidecode+'.html')
    # else:
    return render_template('post.html')  


@app.route('/pending')
def pending():

    return render_template('pending.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print("---------------------username", username)
        print("---------------------password", password)
        if isAdmin(username,password):
            # return redirect(url_for('index'))
            return "Dang nhap thanh cong"
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    # return "login success"
    


def create_article(email,name,address,image,title,description,contentAll): 
    
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    
    title_unidecode = unidecode(title.replace(" ", "-")).lower()
    render_file ='./templates/pending/' + title_unidecode + '.html'
    original_file = './templates/article.html'

    html = codecs.open(original_file, "r", 'utf-8').read()
    soup=BeautifulSoup(html,'html.parser')      
    soup.find(class_='title').string = title
    soup.find(class_='description').string = description
    soup.find(class_='content').string = ""

    image_tag = soup.find(class_='alignright')
    image_tag['src'] = "{{url_for('static', filename='images/"+ image.filename +"')}}"

    contents = contentAll.split('\n')    
    for content in contents:
        soup.find(class_='content').string += "<p>" + content + "</p>"
    # print(soup)
    soup = str(soup).replace("&lt;", "<").replace("&gt;", ">")
    with io.open(render_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    
    return title_unidecode


def save_baiviet_to_database(email,name,address,image,title,description,content):
    # print("save bai viet to databases -----------------------------------")
    mydb = mysql.connector.connect(
        host        ="localhost",
        user        ="root",
        passwd      ="maylanhmayquat@410vui",
        database    ="traffic2"
    )
    thoi_gian = datetime.datetime.now()
    mycursor = mydb.cursor()
    id_baiviet = mycursor.lastrowid
    duyet_bai = False
    sql = """INSERT INTO bai_viet ( baiviet_id,
                                    ten_tacgia,
                                    email_tacgia,
                                    thoigian_dang, 
                                    khu_vuc, 
                                    tieu_de, 
                                    mo_ta, 
                                    hinh_anh, 
                                    van_ban, 
                                    luot_xem, 
                                    id_ad, 
                                    thoi_gian_duyet,
                                    duyet_bai) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s)"""
    val = (id_baiviet,name,email,thoi_gian,address,title,description,image,content,"15", "222", thoi_gian, duyet_bai)
    mycursor.execute(sql, val)
    mydb.commit()

def isAdmin(username,password):
    mydb = mysql.connector.connect(
        host        ="localhost",
        user        ="root",
        passwd      ="maylanhmayquat@410vui",
        database    ="traffic2"
    )
    mycursor = mydb.cursor()    
    mycursor.execute("SELECT ten_dang_nhap, mat_khau FROM admins")
    admins = mycursor.fetchall()
    print("----------------------------------admins", admins)
    for admin in admins:
        print('----------------------------------admin:',admin)
        if username == admin[0] and password == admin[1]:
            print("dung mat khau -----------------------------")
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)