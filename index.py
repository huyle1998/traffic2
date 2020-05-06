from flask import Flask, render_template
app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/hochiminh/<int:hochiminhID>')
def hochiminhRender(hochiminhID):

   return render_template('/hochiminh/about.html')

@app.route('/hanoi/<int:hanoiID>')
def hanoiRender(hanoiID):

   return "hello Ha Noi"

@app.route('/danang/<int:danangID>')
def danangRender(danangID):

   return "hello Da Nang"

@app.route('/tinhkhac/<int:tinhkhacID>')
def tinhkhacRender(tinhkhacID):

   return "hello Tinh Khac"

if __name__ == '__main__':
   app.run(debug = True)