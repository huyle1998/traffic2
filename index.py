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
import base64

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

@app.route('/thanhvien', methods=['GET', 'POST'])
def thanhvien():
    if request.method =='POST':
        username = request.form.get('username')
        password = request.form.get('password')        
        
        if isTacgia(username,password):
            mydb = mysql.connector.connect(
                host        ="localhost",
                user        ="root",
                passwd      ="maylanhmayquat@410vui",
                database    ="traffic2",
                use_pure=True
            )
            mycursor = mydb.cursor()
            mycursor.execute("SELECT id_tg  FROM tac_gia WHERE ten_dn_tg =  " + "'"+ username + "'")  
            id_tg = mycursor.fetchall()  
            print("id_tg: ", id_tg)  
            # return render_template('post.html', id_tg=id_tg)  
            # return "Dang nhap thanh cong"                  
            return redirect('/postarticle/1')
            
        else:
            return render_template('thanhvien.html')
            # return "Dang nhap that bai"
    else:
        return render_template('thanhvien.html')

@app.route('/postarticle/<id_tg>', methods=['GET', 'POST'])
def postarticle(id_tg):
    title_unidecode = ""
    if request.method == 'POST':
        email   =   request.form.get('email')
        address =   request.form.get('address')
        image   =   request.files['file'].read()
        image_64_encode = base64.b64encode(image)
        title   =   request.form.get('title')
        description   =   request.form.get('description')
        content   =   request.form.get('content')
        thoi_gian = datetime.datetime.now()

        # # with open("test.txt", "wb") as text_file:
        # #     text_file.write(image_64_encode)
       
        # # title_unidecode = create_article(email,name,address,image,title,description,content)
        save_baiviet_to_database(email,address,image_64_encode,title,description,content)
        return redirect('/')
    # if len(title_unidecode)>0:
    #     return render_template('/pending/'+title_unidecode+'.html')
    # else:
    return render_template('post.html')  


@app.route('/pending')
def pending():

    return render_template('pending.html')

@app.route('/duyetbai')
def duyetbai():
    a = request.args.get('a', 0, type=int) # baiviet_id
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="maylanhmayquat@410vui",
    database="traffic2"
    )

    mycursor = mydb.cursor()

    sql = "UPDATE bai_viet SET duyet_bai = '1' WHERE baiviet_id = " + str(a)

    mycursor.execute(sql)

    mydb.commit()    


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')        
        
        if isAdmin(username,password):
            mydb = mysql.connector.connect(
                host        ="localhost",
                user        ="root",
                passwd      ="maylanhmayquat@410vui",
                database    ="traffic2",
                use_pure=True
            )

            mycursor = mydb.cursor()
            mycursor.execute("""SELECT  baiviet_id,     
                                        tieu_de, 
                                        mo_ta,                                         
                                        van_ban,
                                        hinh_anh                                         
                                FROM bai_viet WHERE duyet_bai = 0 """, ()) 
            print("-------------Selected----------------")
            bai_vietS = mycursor.fetchall()
            tieu_deS = []
            mo_taS = []            
            van_banS = []
            baiviet_idS = []
            # hinh_anhS = []
            img_dataS = []
            for bai_viet in bai_vietS:
                baiviet_idS.append(bai_viet[0])
                tieu_deS.append(bai_viet[1])
                mo_taS.append(bai_viet[2])
                van_banS.append(bai_viet[3])
                # hinh_anhS.append(bai_viet[4])
                img_dataS.append('data:image/jpg;base64,' + str(bai_viet[4]))   
            # return "Dang nh''ap thanh cong"
            # # return redirect(url_for('index'))
            # print("---------------------------------hinh_anhS: ", hinh_anhS)
            return render_template('pending.html', img_dataS=img_dataS , bai_vietS=bai_vietS, tieu_deS=tieu_deS, mo_taS=mo_taS, van_banS=van_banS,len=len(bai_vietS), baiviet_idS=baiviet_idS)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    # return "login success"    
    
@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        ten_dn_tg   =   request.form.get('user_name')
        mk_tg       =   request.form.get('password')
        ten_tg   =   request.form.get('name')
        email_tg    =   request.form.get('email')
        sdt_tg      =   request.form.get('sdt')
        ns_tg       =   request.form.get('ngaysinh')        
        thoi_gian = datetime.datetime.now()

        save_thongtin_to_database(ten_dn_tg, mk_tg, ten_tg, email_tg, sdt_tg, ns_tg)
        return render_template('dangky.html')
    else:
        return render_template('dangky.html')

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
    mydb = mysql.connector.connect(
        host        ="localhost",
        user        ="root",
        passwd      ="maylanhmayquat@410vui",
        database    ="traffic2"
    )
    thoigian_dang = datetime.datetime.now()
    mycursor = mydb.cursor()
    id_bai = mycursor.lastrowid
    duyet_bai = False
    sql = """INSERT INTO bai_viet ( id_bai,
                                    thoigian_dang,
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
    val = (id_bai,thoigian_dang,)
    mycursor.execute(sql, val)
    mydb.commit()

def save_thongtin_to_database(ten_dn_tg, mk_tg, ten_tg, email_tg, sdt_tg, ns_tg):
    mydb = mysql.connector.connect(
        host        ="localhost",
        user        ="root",
        passwd      ="maylanhmayquat@410vui",
        database    ="traffic2"
    )
    mycursor = mydb.cursor()
    id_tg = mycursor.lastrowid
    sql = """INSERT INTO tac_gia ( id_tg,
                                    ten_tg,
                                    email_tg,
                                    sdt_tg, 
                                    ns_tg, 
                                    ten_dn_tg, 
                                    mk_tg 
                                   ) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    val = (id_tg,ten_tg,email_tg,sdt_tg,ns_tg,ten_dn_tg, mk_tg)
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
    for admin in admins:
        if username == admin[0] and password == admin[1]:
            return True
    return False

def isTacgia(username,password):
    mydb = mysql.connector.connect(
        host        ="localhost",
        user        ="root",
        passwd      ="maylanhmayquat@410vui",
        database    ="traffic2"
    )
    mycursor = mydb.cursor()    
    mycursor.execute("SELECT ten_dn_tg, mk_tg FROM tac_gia")
    tac_giaS = mycursor.fetchall()    
    for tac_gia in tac_giaS:        
        if username == tac_gia[0] and password == tac_gia[1]:
            print("dung mat kahu")
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)