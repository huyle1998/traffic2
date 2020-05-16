import os
import codecs
import random
import string
import io
import html
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from shutil import copyfile
from bs4 import BeautifulSoup,Tag

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


@app.route('/postarticle', methods=['GET', 'POST'])
def postArticle():
    if request.method == 'POST':
        email   =   request.form.get('email')
        name    =   request.form.get('name')
        address =   request.form.get('address')
        image   =   request.files['file']
        title   =   request.form.get('title')
        description   =   request.form.get('description')
        content   =   request.form.get('content')
        # print("Email: ", email)
        # print("Name: ", name)
        # print("Address: ", address)
        # print("Image: ", image)
        # print("title: ", title)
        # print("description: ", description)
        # print("content: ", content)

        # image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        create_article(email,name,address,image,title,description,content)
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # # if user does not select file, browser also
        # # submit an empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #    #  return redirect(url_for('upload_file', filename=filename))
        #     # return render_template('post.html')
        # if





    return render_template('post.html')


# @app.route('/123', methods=['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      # check if the post request has the file part
      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
      file = request.files['file']
      # if user does not select file, browser also
      # submit an empty part without filename
      if file.filename == '':
         flash('No selected file')
         return redirect(request.url)
      if file and allowed_file(file.filename):
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
         return redirect(url_for('upload_file', filename=filename))
   return '''
   <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file>
        <input type=submit value=Upload>
   </form>
   '''

@app.route('/pending')
def pending():

    return render_template('pending.html')


@app.route('/login')
def login():
    # return "login success"
    return render_template('login.html')


def create_article(email,name,address,image,title,description,contentAll):
    print("email: \t\t", email)
    print("name: \t\t",name)
    print("address: \t", address)
    print("image: \t\t",image.filename)
    print("email: \t\t", email)
    print("title : \t\t",title)
    print("description: \t", description)
    print("contents: \t",contentAll)
    
    image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
    
    render_file ='./templates/pending/' + title.replace(" ", "-") + '.html'
    original_file = './templates/article.html'

    html = codecs.open(original_file, "r", 'utf-8').read()
    soup=BeautifulSoup(html,'html.parser')      
    soup.find(class_='title').string = title
    soup.find(class_='description').string = description
    soup.find(class_='content').string = ""
    contents = contentAll.split('\n')    
    for content in contents:
        soup.find(class_='content').string += "<h>" + content + "</h>"
    # print(soup)

    with io.open(render_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

if __name__ == '__main__':
    app.run(debug=True)
