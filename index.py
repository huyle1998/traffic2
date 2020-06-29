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
    mydb = mysql.connector.connect(
                host        ="localhost",
                user        ="root",
                passwd      ="maylanhmayquat@410vui",
                database    ="traffic2",
                use_pure=True
            )

    mycursor = mydb.cursor()
    mycursor.execute("""SELECT  tieu_de, 
                                mo_ta,   
                                hinh_anh,
                                khu_vuc,
                                id_bai                                         
                        FROM bai_viet WHERE trang_thai = 1 """, ()) 
    bai_vietS = mycursor.fetchall()
    tieu_deS = []
    mo_taS = [] 
    hinh_anhS = []
    khu_vucS = []
    id_baiS = []
    for bai_viet in bai_vietS:
        tieu_deS.append(bai_viet[0])
        mo_taS.append(bai_viet[1])
        hinh_anhS.append('data:image/jpg;base64,' + str(bai_viet[2])) 
        khu_vucS.append(bai_viet[3])
        id_baiS.append(bai_viet[4])
    print(id_baiS)
    return render_template('index.html', len=len(bai_vietS), tieu_deS=tieu_deS, mo_taS=mo_taS, hinh_anhS=hinh_anhS, khu_vucS=khu_vucS, id_baiS=id_baiS)


@app.route('/<khu_vuc>/<id_bai>')
def khuvuc_render(khu_vuc, id_bai):
    if id_bai == '0':
        mydb = mysql.connector.connect(
                    host        ="localhost",
                    user        ="root",
                    passwd      ="maylanhmayquat@410vui",
                    database    ="traffic2",
                    use_pure=True
                )

        mycursor = mydb.cursor()
        mycursor.execute("""SELECT  id_bai,
                                    tieu_de, 
                                    mo_ta,   
                                    hinh_anh                                         
                            FROM bai_viet WHERE khu_vuc = """ + "'" + khu_vuc + "'"+"AND trang_thai = '1'") 
        bai_vietS = mycursor.fetchall()
        id_baiS = []
        tieu_deS = []
        mo_taS = [] 
        hinh_anhS = []
        for bai_viet in bai_vietS:
            id_baiS.append(bai_viet[0])
            tieu_deS.append(bai_viet[1])
            mo_taS.append(bai_viet[2])
            hinh_anhS.append('data:image/jpg;base64,' + str(bai_viet[3])) 
        return render_template('khuvuc.html', len=len(bai_vietS),id_baiS=id_baiS ,tieu_deS=tieu_deS, mo_taS=mo_taS, hinh_anhS=hinh_anhS,khu_vuc=khu_vuc)
    else:
        mydb = mysql.connector.connect(
                    host        ="localhost",
                    user        ="root",
                    passwd      ="maylanhmayquat@410vui",
                    database    ="traffic2",
                    use_pure=True
                )

        mycursor = mydb.cursor()
        mycursor.execute("""SELECT  tieu_de, 
                                    mo_ta,   
                                    hinh_anh,
                                    van_ban                                         
                            FROM bai_viet WHERE id_bai = """+  "'"+id_bai+"'") 
        bai_viet = mycursor.fetchall()
        tieu_de = bai_viet[0][0]
        mo_ta = bai_viet[0][1]
        hinh_anh = 'data:image/jpg;base64,' + str(bai_viet[0][2])
        van_ban = bai_viet[0][3]       
        return render_template('baiviet.html', tieu_de=tieu_de,mo_ta=mo_ta,hinh_anh=hinh_anh,van_ban=van_ban)

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
            return redirect('/postarticle/' + str(id_tg[0][0]))
            
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
        khu_vuc =   request.form.get('address')
        image   =   request.files['file'].read()
        image_64_encode = base64.b64encode(image)
        title   =   request.form.get('title')
        description   =   request.form.get('description')
        content   =   request.form.get('content')
        thoi_gian = datetime.datetime.now()

        # # with open("test.txt", "wb") as text_file:
        # #     text_file.write(image_64_encode)
       
        # # title_unidecode = create_article(email,name,khu_vuc,image,title,description,content)
        save_baiviet_to_database(email,khu_vuc,image_64_encode,title,description,content,id_tg)
        return redirect('/')
    # if len(title_unidecode)>0:
    #     return render_template('/pending/'+title_unidecode+'.html')
    # else:
    return render_template('post.html')  


@app.route('/pending')
def pending():

    return render_template('pending.html')

@app.route('/duyetbai/<id_admin>/<id_bai>/')
def duyetbai(id_admin, id_bai):   
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="maylanhmayquat@410vui",
    database="traffic2"
    )

    mycursor = mydb.cursor()

    sql = "UPDATE bai_viet SET trang_thai = '1', id_ad_duyet = " + str(id_admin) + " WHERE id_bai = " + str(id_bai)

    mycursor.execute(sql)

    mydb.commit()    
    return redirect('/login')
   


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')        
        checkAdmin, id_admin =  isAdmin(username,password)
        if checkAdmin:
            mydb = mysql.connector.connect(
                host        ="localhost",
                user        ="root",
                passwd      ="maylanhmayquat@410vui",
                database    ="traffic2",
                use_pure=True
            )

            mycursor = mydb.cursor()
            mycursor.execute("""SELECT  id_bai,     
                                        tieu_de, 
                                        mo_ta,                                         
                                        van_ban,
                                        hinh_anh                                         
                                FROM bai_viet WHERE trang_thai = 0 """, ()) 
            bai_vietS = mycursor.fetchall()
            tieu_deS = []
            mo_taS = []            
            van_banS = []
            id_baiS = []
            # hinh_anhS = []
            hinh_anhS = []
            for bai_viet in bai_vietS:
                id_baiS.append(bai_viet[0])
                tieu_deS.append(bai_viet[1])
                mo_taS.append(bai_viet[2])
                van_banS.append(bai_viet[3])
                hinh_anhS.append('data:image/jpg;base64,' + str(bai_viet[4]))   
            return render_template('pending.html', hinh_anhS=hinh_anhS , bai_vietS=bai_vietS, tieu_deS=tieu_deS, mo_taS=mo_taS, van_banS=van_banS,len=len(bai_vietS), id_baiS=id_baiS,id_admin=id_admin)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    # return "login success"
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')         
        id_admin = 1
        if isAdmin(username,password):
            mydb = mysql.connector.connect(
                host        ="localhost",
                user        ="root",
                passwd      ="maylanhmayquat@410vui",
                database    ="traffic2",
                use_pure=True
            )

            mycursor = mydb.cursor()
            mycursor.execute("""SELECT  id_bai,     
                                        tieu_de, 
                                        mo_ta,                                         
                                        van_ban,
                                        hinh_anh                                         
                                FROM bai_viet WHERE trang_thai = 0 """, ()) 
            bai_vietS = mycursor.fetchall()
            tieu_deS = []
            mo_taS = []            
            van_banS = []
            id_baiS = []
            # hinh_anhS = []
            hinh_anhS = []
            for bai_viet in bai_vietS:
                id_baiS.append(bai_viet[0])
                tieu_deS.append(bai_viet[1])
                mo_taS.append(bai_viet[2])
                van_banS.append(bai_viet[3])
                # hinh_anhS.append(bai_viet[4])
                hinh_anhS.append('data:image/jpg;base64,' + str(bai_viet[4]))   
            return render_template('pending.html', hinh_anhS=hinh_anhS , bai_vietS=bai_vietS, tieu_deS=tieu_deS, mo_taS=mo_taS, van_banS=van_banS,len=len(bai_vietS), id_baiS=id_baiS,id_admin=id_admin)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')        
    
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

def create_article(email,name,khu_vuc,image,title,description,contentAll): 
    
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
    soup = str(soup).replace("&lt;", "<").replace("&gt;", ">")
    with io.open(render_file, "w", encoding="utf-8") as f:
        f.write(str(soup))
    
    return title_unidecode


def save_baiviet_to_database(email,khu_vuc,image,title,description,content,id_tg):
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
                                    khu_vuc,                                    
                                    tieu_de, 
                                    mo_ta, 
                                    hinh_anh, 
                                    van_ban, 
                                    luot_xem, 
                                    id_ad_duyet, 
                                    id_ad_go, 
                                    id_tg, 
                                    email_dong_tg, 
                                    trang_thai,
                                    thoi_gian_duyet,
                                    thoi_gian_go,
                                    ly_do_go) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"""
    val = (id_bai,thoigian_dang,khu_vuc,title,description,image,content,'1','1','1',id_tg,email,'0', thoigian_dang, thoigian_dang, 'thich')
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
    mycursor.execute("SELECT ten_dn_admin, mk_admin, id_admin FROM admins")
    admins = mycursor.fetchall()
    for admin in admins:
        if username == admin[0] and password == admin[1]:

            return True, admin[2]
    return False, 0

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
            return True
    return False


if __name__ == '__main__':
    app.run(debug=True)