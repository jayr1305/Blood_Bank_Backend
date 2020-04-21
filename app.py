#C:/Users/Jay/Anaconda3/python app.py

from flask import Flask,jsonify,request
from flask_mysqldb import MySQL 
from datetime import date
from flask_cors import CORS

#=============================================================================================#

app = Flask(__name__)
CORS(app)

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_DB'] = 'ConnectGroup'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config["DEBUG"] = True

app.config['MYSQL_PASSWORD'] = 'dbms_123'
# app.config['MYSQL_PASSWORD'] = 'lakshay'

mysql = MySQL(app)


#=============================================================================================#


@app.route('/')
def home():
	return "<h1>Hello World</h1>"


@app.route('/table/<table>')
def getTableDetails(table):
	#To see updated tables, just for development purpose
	cur = mysql.connection.cursor()
	print_it(table)
	query = " SELECT * FROM "+ table
	# print_it(query)
	results = ""
	try: 
		cur.execute(query)
		results = cur.fetchall()
	except:
		results = {Error: 'True'}

	return jsonify(results)


#=============================================================================================#


@app.route('/updateuser',methods = ['POST'])
def updateUser():

	id_ = request.json['UserID']
	user = request.json['user']
	print_it(user)
	
	#Calculate age from given DOB
	dob = list(map(int,user['Dob'].split('-')))
	print_it(dob)
	user['Age'] = calculateAge(date(dob[0],dob[1],dob[2]))
	print_it(user['Age'])

	response = ""
	
	try:
		mycursor = mysql.connection.cursor()	

		#Update values in user table
		sqlFormula = "UPDATE user SET Type=%s,Username=%s,Phone=%s,Email=%s,Address=%s,Pincode=%s,Age=%s WHERE UserID=%s"
		toPut = (user["Type"],user["Username"],user["Phone"],user["Email"],user["Address"],user["Pincode"],user["Age"],id_)
		print(sqlFormula,toPut)
		mycursor.execute(sqlFormula,toPut)
		mysql.connection.commit()


		#Update values in password table
		sqlPass = "UPDATE passwords SET Password=%s,Username=%s WHERE UserID=%s"
		toPut = (user["Password"],user["Username"],id_)
		mycursor.execute(sqlPass,toPut)
		mysql.connection.commit()
		

		#Update values in Donor table
		if(user['Type']=="Donor"):
			query = "UPDATE available_donor SET BloodGroup=%s,WillingToDonate=%s WHERE UserID=%s"
			toPut = (user["Bloodgroup"],user["WTD"],id_)
			mycursor.execute(query,toPut)
			mysql.connection.commit()

		#Make succesfull response
		response = {'userid':id_, 'status': 200, 'message':'Success'}
	
	except Exception as e:
		return jsonify({'Error': 'True','message': str(e)})

	#Send back the response
	return jsonify(response)


@app.route('/addbloodbank',methods = ['POST'])
def addBloodBank():
	name = request.json['Name']
	address = request.json['Address']
	pincode = request.json['Pincode']
	user_list = request.json['UserID']
	totalCap = request.json['TotalCapacity']
	capLeft = request.json['CapacityLeft']

	try:
		mycursor = mysql.connection.cursor()	
		query = "SELECT count(*) FROM Blood_Bank"
		mycursor.execute(query)
		
		#New id as total blood_banks + 1
		id_ = mycursor.fetchall()[0]['count(*)'] + 1
		print_it(id_)
		
		sqlFormula = "INSERT INTO Blood_Bank VALUES(%s,%s,%s,%s,%s,%s)"
		toPut = (name,pincode,id_,address,capLeft,totalCap)

		mycursor.execute(sqlFormula,toPut)
		mysql.connection.commit()

		for uid in user_list:
			query = " SELECT * FROM user where UserID=%s"%(uid)
			mycursor.execute(query)
			results = mycursor.fetchall()
			if(len(results)==0):
				return jsonify({'Error': 'True','message':'No such user'+str(uid)})
			else:
				sqlFormula = "INSERT INTO Blood_Bank_Employee VALUES(%s,%s)"
				toPut = (uid,id_)
				mycursor.execute(sqlFormula,toPut)
				mysql.connection.commit()

		response = {'status':200,'message':'Success'}
		return jsonify(response)

	except Exception as e:
		return jsonify({'status':401,'Error': 'True','message': str(e)})


@app.route('/adddonationcenter',methods = ['POST'])
def addDonCen():
	name = request.json['Name']
	address = request.json['Address']
	pincode = request.json['Pincode']
	user_list = request.json['UserID']
	bbid = request.json['BBID']

	try:
		mycursor = mysql.connection.cursor()	
		query = "SELECT count(*) FROM Donation_Centers"
		mycursor.execute(query)
		
		#New id as total Donation_Centers + 1
		id_ = mycursor.fetchall()[0]['count(*)'] + 1
		print_it(id_)
		
		sqlFormula = "INSERT INTO Donation_Centers VALUES(%s,%s,%s,%s,%s)"
		toPut = (name,id_,pincode,address,bbid)

		mycursor.execute(sqlFormula,toPut)
		mysql.connection.commit()

		for uid in user_list:
			query = " SELECT * FROM user where UserID=%s"%(uid)
			mycursor.execute(query)
			results = mycursor.fetchall()
			if(len(results)==0):
				return jsonify({'Error': 'True','message':'No such user'+str(uid)})
			else:
				sqlFormula = "INSERT INTO Donation_Centers_Employee VALUES(%s,%s)"
				toPut = (uid,id_)
				mycursor.execute(sqlFormula,toPut)
				mysql.connection.commit()

		response = {'status':200,'message':'Success'}
		return jsonify(response)

	except Exception as e:
		return jsonify({'status':401,'Error': 'True','message': str(e)})


@app.route('/addhospital',methods = ['POST'])
def addHospital():
	name = request.json['Name']
	address = request.json['Address']
	pincode = request.json['Pincode']
	user_list = request.json['UserID']
	admPatient = request.json['AdmittedPatients']

	try:
		mycursor = mysql.connection.cursor()	
		query = "SELECT count(*) FROM Hospital"
		mycursor.execute(query)
		
		#New id as total Hospital + 1
		id_ = mycursor.fetchall()[0]['count(*)'] + 1
		print_it(id_)
		
		sqlFormula = "INSERT INTO hospital VALUES(%s,%s,%s,%s,%s)"
		toPut = (id_,name,pincode,address,admPatient)

		mycursor.execute(sqlFormula,toPut)
		mysql.connection.commit()

		for uid in user_list:
			query = " SELECT * FROM user where UserID=%s"%(uid)
			mycursor.execute(query)
			results = mycursor.fetchall()
			if(len(results)==0):
				return jsonify({'Error': 'True','message':'No such user'+str(uid)})
			else:
				sqlFormula = "INSERT INTO Hospital_Employee VALUES(%s,%s)"
				toPut = (uid,id_)
				mycursor.execute(sqlFormula,toPut)
				mysql.connection.commit()

		response = {'status':200,'message':'Success'}
		return jsonify(response)

	except Exception as e:
		return jsonify({'status':401,'Error': 'True','message': str(e)})


@app.route('/addemployee',methods = ['POST'])
def addEmp():
	userId = request.json['UserID']
	place = request.json['place']

	cur = mysql.connection.cursor()
	query = " SELECT * FROM user where UserID=%s"%(userId)

	try: 
		cur.execute(query)
		results = cur.fetchall()
		if(len(results)==0):
			return jsonify({'Error': 'True','message':'No such user'})
		else:
			
			if(place == 'hospital'):
				hid = request.json['HID']
				sqlFormula = "INSERT INTO Hospital_Employee VALUES(%s,%s)"
				toPut = (userId,hid)
			
			elif(place == 'blood_bank'):
				bbid = request.json['BBID']
				sqlFormula = "INSERT INTO Blood_Bank_Employee VALUES(%s,%s)"
				toPut = (userId,bbid)

			elif(place == 'donation_centers'):
				dcid = request.json['DCID']
				sqlFormula = "INSERT INTO Donation_Centers_Employee VALUES(%s,%s)"
				toPut = (userId,dcid)

			else:
				return  jsonify({'Error': 'True','message':'Not a valid place'})
			
			cur.execute(sqlFormula,toPut)
			mysql.connection.commit()

			response = {'status':200,'message':'Success Add Emp'}
			return jsonify(response)
	
	except Exception as e:
		return jsonify({'Error': 'True','message': str(e)})

# Working
@app.route('/donateblood',methods = ['POST'])
def donateBlood():
	userId = request.json['UserID']
	dateRec = request.json['DateRecieved']
	bloodGrp = request.json['BloodGroup']
	amt = request.json['Amount']
	dcid = request.json['DCID']
	avb = request.json['Available']

	try:
		mycursor = mysql.connection.cursor()
		
		sqlFormula = "INSERT INTO Donated_Blood VALUES(%s,%s,%s,%s,%s,%s)"
		toPut = (userId,dateRec,bloodGrp,amt,dcid,avb)

		print(sqlFormula,toPut)
		mycursor.execute(sqlFormula,toPut)
		mysql.connection.commit()

		response = {'status':200,'message':'Successfully Updated Donation Record'}

		return jsonify(response)

	except Exception as e:
		return jsonify({'status':401,'Error': 'True','message': str(e)})

# Working
@app.route('/showprofile/<userId>')
def showProfile(userId):
	cur = mysql.connection.cursor()
	query = " SELECT * FROM user where UserID=%s"%(userId)

	try: 
		cur.execute(query)
		results = cur.fetchall()[0]
		if(results['Type']=='Donor'):
			subquery = 'SELECT BloodGroup FROM available_donor where UserID=%s'%(userId)
			cur.execute(subquery)
			bloodGroup = cur.fetchall()[0]
			results.update(bloodGroup)
		print_it(type(results))
		return jsonify(results)
	except Exception as e:
		return jsonify({'Error': 'True','message': str(e)})

# Working
@app.route('/login', methods=['POST'])
def loginFunction():
	# dcid/hid/bbid FETCH
	userId = request.json["UserID"]
	cur = mysql.connection.cursor()
	query = " SELECT * FROM passwords where UserID=%d"%(userId)
	try: 
		cur.execute(query)
		results = cur.fetchall()[0]
		if(results['Password']==request.json["Password"]):
			response = {'status':200,'message':'Logged in successfully'}
		else:
			response = {'status':401,'message':'Wrong Password'}
		
		return jsonify(response)
	except Exception as e:
		return jsonify({'Error': 'True','message': str(e)})

# Working
@app.route('/createuser', methods=['POST'])
def createUser():

	#Get total number of users
	mycursor = mysql.connection.cursor()
	query = "SELECT count(*) FROM User"
	mycursor.execute(query)
	
	#New id as total users + 1
	id_ = mycursor.fetchall()[0]['count(*)'] + 1
	print_it(id_)
	
	#Print the acquired user details from request
	user = request.json['user']
	print_it(user)
	
	#Calculate age from given DOB
	dob = list(map(int,user['Dob'].split('-')))
	print_it(dob)
	user['Age'] = calculateAge(date(dob[0],dob[1],dob[2]))
	print_it(user['Age'])

	response = ""
	
	try:
		#Insert values in user table
		sqlFormula = "INSERT INTO user VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
		toPut = (id_,user["Type"],user["Username"],user["Phone"],user["Email"],user["Address"],user["Pincode"],user["Age"])
		print(sqlFormula,toPut)
		mycursor.execute(sqlFormula,toPut)
		mysql.connection.commit()


		#Insert values in password table
		sqlPass = "INSERT INTO passwords VALUES(%s,%s,%s)"
		toPut = (id_,user["Password"],user["Username"])
		mycursor.execute(sqlPass,toPut)
		mysql.connection.commit()
		

		#Insert values in Donor table
		if(user['Type']=="Donor"):
			query = "INSERT into available_donor values(%s,%s,%s,%s)"
			toPut = (id_,date.today(),user["Bloodgroup"],user["WTD"])
			mycursor.execute(query,toPut)
			mysql.connection.commit()

		#Make succesfull response
		response = {'userid':id_, 'status': 200, 'message':'Success'}
	
	except Exception as e:
		return jsonify({'Error': 'True','message': str(e)})

	#Send back the response
	return jsonify(response)

# Working
@app.route('/getpastdonations/<userId>')
def getpastdonations(userId):
	cur = mysql.connection.cursor()
	query = " SELECT * FROM donated_blood where UserID=%s"%(userId)
	try: 
		cur.execute(query)
		results = cur.fetchall()

		for i in range(len(results)):
			donationDate = results[i]['DateRecieved']
			formattedDate = donationDate.strftime("%Y")+'-'+donationDate.strftime("%m")+'-'+donationDate.strftime("%d")
			results[i]['DateRecieved'] = formattedDate
			DCID = results[i]['DCID']
			subquery = "SELECT Name FROM donation_centers where DCID=%s"%(DCID)  # SUBQUERY to get Donation Center Name
			cur.execute(subquery)
			Name = cur.fetchall()[0]
			print(Name)
			results[i].update(Name)
		print_it(type(results))
		return jsonify(results)
	except Exception as e:
		return jsonify({'Error': 'True','message': str(e)})

#=============================================================================================#

# Helper function to calculate age from DOB 
def calculateAge(birthDate): 
	today = date.today() 
	age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
	return age


#Helper function to print in DEBUG mode
def print_it(s):
	if(app.config["DEBUG"]):
		print(s)

#=============================================================================================#

#Command to run the app
app.run()