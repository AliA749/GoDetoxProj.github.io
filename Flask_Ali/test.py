from flask import Flask,request,render_template,redirect,url_for
import math

app=Flask(__name__)

@app.route('/',methods=['GET','POST'])
def main():
    global user,password,count
    user=request.form.get('txtuser')
    password=request.form.get('txtpass')
    count=0
    if request.method=='GET':
        return render_template('index.html')
    else:
        if user==password:
            error='Username and password cannot be the same.'
            return render_template('index.html',error=error)
        if len(user)>3 and len(password)>3:
            return redirect(url_for('personalinfo'))
        else:
            error='Username or password is not over 3 characters.'
            return render_template('index.html',error=error)
        
@app.route('/signup',methods=['GET','POST'])
def personalinfo():
    global fname,lname,dob,pnum,address,email,dccn,expd,cvv,count
    if request.method=='GET':
        if count==0:
            return render_template('personalinfo.html',user=user)
        else:
            return render_template('personalinfo.html',user=user,firstn=fname,
                                   lastn=lname,dob=dob,pnum=pnum,address=address,
                                   email=email,dccn=dccn,expd=expd,cvv=cvv)
    else:
        count=1
        fname=request.form.get('txtfirst')
        lname=request.form.get('txtlast')
        dob=request.form.get('txtdob')
        pnum=request.form.get('txtphone')
        address=request.form.get('txtaddress')
        email=request.form.get('txtemail')
        dccn=request.form.get('txtd/ccn')
        expd=request.form.get('txtexpd')
        cvv=request.form.get('txtcvv')
        if fname!='' and lname!='' and len(dob)>0 and len(pnum)==10 and address!='' and email!='' and len(dccn)>12 and len(expd)>0 and len(cvv)>2:
             return redirect(url_for(''))
        else:
            error='An error in one the information you have entered.'
            return render_template('personalinfo.html',user=user,error=error)

@app.route('/homepage',methods=['GET','POST'])
def homepage():
    if request.method=='GET':
        return render_template('homepage.html',firstn=fname,user=user,lastn=lname)
    else:
        info=request.form.get('btninfo')
        if info=='a':
            return redirect(url_for('personalinfo'))
        else:
            return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html',firstn=fname,user=user,lastn=lname)
    else:
        username=request.form.get('txtuser')
        passwordo=request.form.get('txtpass')
        if username==user and passwordo==password:
            return redirect(url_for('homepage'))
        else:
            error='Username or password is not correct'
            return render_template('login.html',firstn=fname,user=user,lastn=lname,error=error)

@app.route('/menu',methods=['GET','POST'])
def menu():
    if request.method=='GET':
        return render_template('menu.html')
    else:
        dotheting()
        print(food)
        print(foodlen)
        print(price)
        return render_template('receipt.html',food=food,foodlen=foodlen,price=price,total=total,
                               fname=fname,lname=lname,dob=dob,pnum=pnum,address=address,email=email,
                               dccn=dccn,expd=expd,cvv=cvv)

def dotheting():
    global food,foodlen,price,total
    food=[]
    foodlen=0
    price=[]
    total=0
    food=request.form.getlist('Aclassics')
    foodlen=len(food)
    for i in range(foodlen):
        switcher = {
            'Ham & Provolone':8.15,
            'Tuna Fish':9.15,
            'Roast Beef & Provolone':10.15,
            'The Veggie':8.15,
            'Turkey & Provolone':9.15,
            'Jersey Shores Favorite':8.15,
            'The Super Sub':9.15,
            'The Original Italian':10.15,
            'Club Sub':10.15,
            'Club Supreme':10.15,
            'Portabella Musrooms & Swiss':7.55,
            'Chicken Philly':9.25,
            'Chicken Bacon Ranch':9.65,
            'Chipotle Chicken':9.55,
            'Buffalo Chicken':9.65,
            'Big Kahuna Chicken':9.85,
            'Famous Philly':9.45,
            'Chipotle':9.35,
            'The Big Kahuna':10.35
        }
        price.append(switcher.get(food[i],0))
        total=total+price[i]
    total=round(total,2)

if __name__=='__main__':
    app.run()
