from flask import Flask, request, render_template, redirect, url_for, session
import math

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def personalinfo():
    global email,dccn,expd,cvv,passwrd
    if request.method == 'GET':
        return render_template('personalinfo.html')
    else:
        passwrd = request.form.get('txtpassword')
        email = request.form.get('txtemail')
        dccn = request.form.get('txtd/ccn')
        expd = request.form.get('txtexpd')
        cvv = request.form.get('txtcvv')
        signupacc=[email,passwrd,dccn,expd,cvv]
        if passwrd !='' and email !='' and dccn !="" and expd !="" and cvv !="":
            return redirect(url_for('main'))
        else:
            error = 'An error in one of the information you have entered.'
            return render_template('personalinfo.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def main():
    global username,password,cardnum, expirationdate, cardcvv,loginacc
    if request.method == 'GET':
        return render_template('index.html')
    else:
        username = request.form.get('txtuser')
        password = request.form.get('txtpass')
        cardnum = request.form.get('txtcardnum')
        expirationdate = request.form.get('txtcardexp')
        cardcvv = request.form.get('txtcardcvv')
        signupacc=[email,passwrd,dccn,expd,cvv]
        
        loginacc = [username, password, cardnum, expirationdate, cardcvv]
        
        if loginacc == signupacc:
            return redirect(url_for('menu'))
        else:
            error = 'Enter the user and pass information correctly.'
            return render_template('index.html', error=error)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global food,foodlen,price,total
    loginacc=[username, password, cardnum, expirationdate, cardcvv]
    if request.method == 'GET':
        return render_template('menu.html')
    else:
        receiptwork()
        return render_template('receipt.html', food=food, foodlen=foodlen, price=price, total=total)
    
@app.route('/receipt', methods=['GET', 'POST'])
def receiptwork():
    global food,foodlen,price,total,choice
    food=[]
    foodlen=0
    price=[]
    total=0
    food=request.form.getlist('Aclassics')
    foodlen=len(food)
    if request.method == 'GET':
        return render_template('receipt.html', loginacc=loginacc, food=food, price=price, foodlen=foodlen, total=total, choice=choice)
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

        if choice == 'yes':
            return redirect(url_for('completeorder'))
        elif choice =='no':
            return render_template('receipt.html', loginacc=loginacc, food=food, price=price, foodlen=foodlen, total=total, choice=choice)
        else:
            return redirect(url_for('menu'))
    else:
        return "Nothing worked"
    


@app.route('/completeorder', methods=['GET', 'POST'])
def completeorder():
    return "Order completed"

if __name__ == '__main__':
    app.run()
