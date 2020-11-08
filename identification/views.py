from django.shortcuts import render,redirect
from django.db import connection

import hashlib

def home(request):
    return render(request, 'identification/home.html')

#ROLE_ID
#AGENT-1
#Customer-0

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'identification/signupuser.html')
    else:
        cursor = connection.cursor()
        name = request.POST['username']
        sql = "SELECT * FROM LOGIN WHERE LogIn_Username = %s"
        cursor.execute(sql,[name])
        result = cursor.fetchone()
        cursor.close()
        if result is not None:
            return render(request, 'identification/signupuser.html', {'error':'Username already exist! Try another one.'})
        else:
            if request.POST['password1'] == request.POST['password2']:
                s = request.POST['username']
                a = abs(hash(s)) % (10 ** 5)
                if request.POST['role'].upper() == 'AGENT' or request.POST['role'].upper() == 'CUSTOMER':
                    cursor = connection.cursor()
                    sql = "INSERT INTO LOGIN VALUES(%s,%s,%s)"
                    cursor.execute(sql,[a,request.POST['username'],request.POST['password1']])
                    connection.commit()
                    cursor.close()
                else:
                    return render(request, 'identification/signupuser.html', {'error':'Role must be Agent or Customer'})


                cursor = connection.cursor()
                sql = "INSERT INTO ACCOUNT VALUES(%s,%s,%s)"
                cursor.execute(sql,[a,'0.0',''])
                connection.commit()
                cursor.close()


                # is_agent = request.POST.get('is_agent', False)
                # if is_agent:
                #     cursor = connection.cursor()
                #     sql = "INSERT INTO ROLE VALUES(%s,%s,%s)"
                #     cursor.execute(sql,['1','Agent',''])
                #     connection.commit()
                #     cursor.close()
                # else:
                #     cursor = connection.cursor()
                #     sql = "INSERT INTO ROLE VALUES(%s,%s,%s)"
                #     cursor.execute(sql,['0','Customer',''])
                #     connection.commit()
                #     cursor.close()

                cursor = connection.cursor()
                sql = "INSERT INTO eUSER VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, [a,request.POST['name'], request.POST['mobile'], request.POST['email'], request.POST['address'], a, a, request.POST['role']])
                connection.commit()
                cursor.close()


                return render(request, 'identification/current.html')
            else:
                return render(request, 'identification/signupuser.html', {'error':'Password did not match'})




def loginuser(request):
    if request.method == 'GET':
        return render(request, 'identification/loginuser.html')
    else:
        cursor = connection.cursor()
        name = request.POST['username']
        password = request.POST['password']
        sql = "SELECT * FROM LOGIN WHERE LogIn_Username = %s"
        cursor.execute(sql,[name])
        result = cursor.fetchone()
        cursor.close()

        if result is not None:
            r = result[2]
            if password == r:
                return render(request, 'identification/current.html')
            else:
                return render(request, 'identification/loginuser.html' , {'error':'Username or password did not match'})
        else:
            return render(request, 'identification/loginuser.html' , {'error':'Username or password did not match'})


def currentuser(request):
    return render(request, 'identification/current.html')


def accountinfo(request):
    return render(request, 'identification/accountinfo.html')

def billpayment(request):
    return render(request, 'identification/billpayment.html')

def moneysending(request):
    return render(request, 'identification/moneysending.html')

def pulloutmoney(request):
    return render(request, 'identification/pulloutmoney.html')

def showreceipts(request):
    return render(request, 'identification/showreceipts.html')
