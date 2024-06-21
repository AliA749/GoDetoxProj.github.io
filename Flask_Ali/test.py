from flask import Flask, request, render_template, redirect, url_for, session
from os import path
import math

app = Flask(__name__)

global count
count=0

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
            error = "Don't leave any information blank"
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
            match (loginacc[0], loginacc[1], loginacc[2], loginacc[3], loginacc[4]):
                case (u, _, _, _, _) if u != signupacc[0]:
                    error = 'Enter the user information correctly.'
                case (_, p, _, _, _) if p != signupacc[1]:
                    error = 'Enter the password correctly.'
                case (_, _, c, _, _) if c != signupacc[2]:
                    error = 'Enter the correct card number.'
                case (_, _, _, e, _) if e != signupacc[3]:
                    error = 'Enter the correct expiration date.'
                case (_, _, _, _, cv) if cv != signupacc[4]:
                    error = 'Enter the correct CVV for your card.'
                case _:
                    error = 'Unknown error.'

            return render_template('index.html', error=error)

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    global food,foodlen,price,total
    loginacc=[username, password, cardnum, expirationdate, cardcvv]
    if request.method == 'GET':
        return render_template('menu.html')
    else:
        receiptwork()
        return redirect(url_for('completeorder'))
    
def receiptwork():
    global food,foodlen,price,total,choice
    food=[]
    foodlen=0
    price=[]
    total=0
    food=request.form.getlist('Aclassics')
    foodlen=len(food)
    for i in range(foodlen):
        switcher = {
                'Grilled Cheese Sandwich':4.95,
                'Fresh Baked Bagel with Peanut Butter':2.99,
                'Wheat Toast with Avocado':3.99,
                'Meat Lovers Wrap':7.99,
                'Super Veggie Wrap':7.99,
                'Classic Breakfast Wrap':7.99,
                'The Mexicalli Omelette':8.99,
                'Best Buy Omelette':8.99,
                'Acai Bowl':10.99,
                'Mega Burger':10.49,
                'The Big Dipper Burger':9.49,
                'The Hawaiian Burger':8.99,
                'Chopped Cheese Sandwich':9.95,
                'Go Detox Wrap':9.95,
                'Sweet and Sour Zinc Juice':6.99,
                'Arctic Zen Juice':6.99,
                'Kiwi Apple Juice':6.99,
                'Pina Coalda Madness Smoothie':6.99,
                'Tropical Bliss Smoothie':6.99,
                'Strawberry Banana Blast Smoothie':6.99
        }
        price.append(switcher.get(food[i],0))
        total=total+price[i]
        base_total=total+price[i]
    total=round(total,2)
    
@app.route('/change', methods=['GET', 'POST'])
def change():
    global total, count,base_total,error,choice
    base_total=total
    choice = request.form.get('yesorno')
    error=""
    if request.method == 'POST':
        addmore = request.form.get('addmore')
        if addmore == "+":
            count += 1
            base_total=total
            new_total = round(base_total*(count +1),2)
            return render_template('completeorder.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, total=base_total, count=count, new_total=new_total, error=error,choice=choice,current_url=request.path)
        elif addmore == "-" and count >0:
            count -= 1
            new_total = round(base_total* (count +1 ), 2)
            return render_template('completeorder.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, total=base_total, count=count, new_total=new_total, error=error,choice=choice,current_url=request.path)
        elif addmore == "-" and count <= 0:
            return redirect(url_for('menu'))
        else:
            total=base_total
            return redirect(url_for('completeorder'))
    else:
        return render_template('completeorder.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, choice=None, total=base_total, count=count,  current_url=request.path)
        

@app.route('/cardchecker', methods=['GET', 'POST'])
def cardchecker():
    global new_total
    choice = request.form.get('yesorno')
    cardcheck = request.form.get('cardcheckertxt')
    error=""
    base_total = total
    new_total = round(base_total * (count + 1), 2)
    if request.method == "POST":
        if error == "":
             if cardcheck == loginacc[2]:  # Check if the card number matches
                receipt()
                return render_template('receipt.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, total=base_total, count=count, new_total=new_total, error=error, choice=choice)
             else:
                error="This card information doesnt match with this account."
                return render_template('completeorder.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, choice=choice,  total=total,error=error,count=count, current_url=request.path)
    else:
        return render_template('completeorder.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, choice=choice, total=total,error=error, current_url=request.path)


@app.route('/completeorder', methods=['GET', 'POST'])    
def completeorder():
    choice=request.form.get('yesorno')
    if request.method =="POST":
         cardcheck = request.form.get('cardcheckertxt')
         if choice=='yes':
             return redirect(url_for('cardchecker'))
         else:
             return redirect(url_for('change'))
                
    else:
        return render_template('completeorder.html', loginacc=loginacc, food=food, foodlen=foodlen, price=price, choice=choice, total=total, current_url=request.path )

def receipt():
    global notice
    recieptforuser = loginacc[0] + ".txt"
    ifexist = path.exists(recieptforuser)

    if (ifexist != recieptforuser):
        with open(recieptforuser, "w") as receiptfile:
            receiptitems = f"{loginacc[0]}, {food},Amount of each food/drink:{count+1}, {price},total:{new_total}"
            receiptfile.write(receiptitems)
            notice= "Receipt downloaded to notes"
    else:
        with open(recieptforuser, "a") as receiptfile:
            receiptitems = f"{loginacc[0]}, {food}, {price}, total:{new_total}"
            receiptfile.write(receiptitems)
            notice= "Receipt updated with new items"


        
    
if __name__ == '__main__':
    app.run()
