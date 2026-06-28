from google import genai
from flask import Flask , request,jsonify,session
app = Flask(__name__)
import psycopg2 as db
from flask_cors import CORS
import json
import pandas as pd 
import emails as em
import smtplib
from email.message import EmailMessage



d = {'host':'dpg-d8t9bi77f7vs73c0d8v0-a.oregon-postgres.render.com','password':'zG3dWR2oIyMKEHzSOE3sGwkqE3SgBfnj' , 'port': 5432, 'user': 'food_v1nx_user', 'database':'food_v1nx'}
sq = db.connect(**d)
s = sq.cursor()
s.execute("create table if not exists  book (id SERIAL PRIMARY KEY,name varchar(30)  , age varchar(30) ,de varchar(30)  , slot varchar(30) , date varchar(30),sex varchar(30),sy varchar(30)) ;")
sq.commit()
s.execute("create table if not exists login (email varchar(30) , psd varchar(30));")
sq.commit()
#msg = "Kya aap doctor se appointment lena chahte hain ya abhi baat karna chahte hain? ha "
app.secret_key = "ejjebjbjhhrbjhrbhjrbjhrbvhr"



#print(interaction.output_text)
CORS(app ,resources={r"/api/*": {"origins": "https://ai-agnetfrontend.vercel.app"}},supports_credentials=True)
@app.route("/api/login",methods = ["GET","POST"])
def login():
     if request.method == "POST":
         u = request.get_json()
         email = u.get("email")
         
         
         d5 = {'host':'dpg-d8t9bi77f7vs73c0d8v0-a.oregon-postgres.render.com','password':'zG3dWR2oIyMKEHzSOE3sGwkqE3SgBfnj' , 'port': 5432, 'user': 'food_v1nx_user', 'database':'food_v1nx'}
         sq5 = db.connect(**d5)
         
         
         p4 = pd.read_sql(f"select email from login where email = '{u["email"]}' and psd = '{u["password"]}'",sq5)
        
         if p4.empty != True:
            session["name"] = email
            print(session,email)
            return jsonify({"success":True, "message": "Login successful"})
            
            
         else:
             
             return jsonify({"success":False,"message":"Login"})
            
            
         
@app.route('/api/signup',methods = ["GET","POST"])
def signup():
   if request.method == "POST":
      u1 = request.get_json()
      
      d4 = {'host':'dpg-d8t9bi77f7vs73c0d8v0-a.oregon-postgres.render.com','password':'zG3dWR2oIyMKEHzSOE3sGwkqE3SgBfnj' , 'port': 5432, 'user': 'food_v1nx_user', 'database':'food_v1nx'}
      sq4 = db.connect(**d4)
      s4 = sq4.cursor()
      p3 = pd.read_sql(f"select email from login where email =  '{u1["email"]}' and psd = '{u1["password"]}' ;",sq4)
      if p3.empty:
         s4.execute(f"insert into login (email , psd) values ('{u1["email"]}','{u1["password"]}');")
         sq4.commit()
         
         message = em.html(
                     subject="SignUP",
                     html="<p>SignUP Successfull</p>",
                     mail_from=("SignUP","trishamgupta43@gmail.com" ),
         )
         message.send(
                     to=u1["email"],
                     smtp={
                         "host": "smtp.gmail.com",
                         "port": 587,
                         "tls": True,
                         "user": "trishamgupta43@gmail.com",
                         "password": "fkpa acxf kqdp eaoz",
                     },
          )
         print("Email sent successfully!")

         return jsonify({"sucess":True,"message":"Signup Sucess"})
      else:
         return jsonify({"success":False,"message":"Failed Login"})
      
@app.route('/api/chat',methods = ["GET","POST"])
def chat():
    if request.method == "POST":
       
       s = request.get_json()
       print(session.get('name'))
       if session.get('name') != None:
          prompt = f"""
          You are the Master Intent & Entity Extraction Agent.

          Extract information from the user's message. and rember the information also
          and if book_appointment please make sure ask the user for symptoms , date , time ,patientname , age , sex and you will decide the department according to situation we have department("GEnral pHysican" ,"Ortho"etc)and rember the patuent name , sex , age return in json 
          Return ONLY valid JSON.
          if cancel appoint please ask user for id and if reshedule appointment please ask them for date and time and id 
          Allowed intents:
          - BOOK_APPOINTMENT
          - CANCEL_APPOINTMENT
          - RESCHEDULE_APPOINTMENT
          - TRIAGE
          - NAVIGATION
          - Medical Medicine Info
          - EMERGENCY
          and give the answer explaiable how ?? 


          Output Schema:

          {{
            "intent": "",
            "department": null,
            "symptoms": [],
            "id" : null
            "date": null,
            "time": null,
            "age" : null,
            "sex" :null,
            "patient_name": null,
            "report_type": null,
            "destination": null,
            "priority": null,
            "language": "Hindi",
            "followup_required": "false",
            "followup_question": null,
            "response": null
          }}

          User:
          {s['message']}
          """ 
          client = genai.Client(api_key = "AQ.Ab8RN6LFsm0K7xV8eOcqwV-_QqD01kyPuns_ruxIXD6tlTiGzg")
          interaction = client.interactions.create(
          model="gemini-2.5-flash",
          input=prompt)
       
       
          text = interaction.output_text

          text = text.replace("```json", "")
          text = text.replace("```", "")
          text = text.strip()

          result = json.loads(text)
          if result["followup_required"] == "true":
          
             return jsonify({f"success":True,"message":result["followup_question"]})
          
          else:
             if result["intent"] == "TRIAGE":
                 client2 = genai.Client(api_key = "AQ.Ab8RN6LFsm0K7xV8eOcqwV-_QqD01kyPuns_ruxIXD6tlTiGzg")
                 interaction2 = client2.interactions.create(
                 model="gemini-2.5-flash",
                 input= f"{s['message']} GIve answer orignal and explainable as per language")
              
                  
                 return jsonify({'success':True,"message":interaction2.output_text})
             if result["intent"] == "BOOK_APPOINTMENT":
                 d1 = {'host':'dpg-d8t9bi77f7vs73c0d8v0-a.oregon-postgres.render.com','password':'zG3dWR2oIyMKEHzSOE3sGwkqE3SgBfnj' , 'port': 5432, 'user': 'food_v1nx_user', 'database':'food_v1nx'}
                 sq1 = db.connect(**d1)
                 s1 = sq1.cursor()
                 p = pd.read_sql(f"select id from book where date = '{result["date"]}' and slot = '{result["time"]}' and de = '{result["department"]}'",d1)
                 if p.empty:
                     
                     s1.execute(f"insert into book (age,de,slot,date,name,sex,sy) values ('{result["age"]}','{result["department"]}','{result["time"]}','{result["date"]}','{result["patient_name"]}','{result["sex"]}',{result["symptoms"]}) RETURNING id ;")
                     book_id = s1.fetchone()[0]

                     sq1.commit()
                     message = em.html(
                     subject="Booked Appointment",
                     html=f"<p>Your Booking ID is {book_id} Please remember and date , time , doctor is {result["date"]} , {result["time"]} ,{result["department"]} </p>",
                     mail_from=("Booked Appointment","trishamgupta43@gmail.com" ),
                     )
                     message.send(
                     to=session.get('name'),
                     smtp={
                         "host": "smtp.gmail.com",
                         "port": 587,
                         "tls": True,
                         "user": "trishamgupta43@gmail.com",
                         "password": "fkpa acxf kqdp eaoz",
                     },
                     )

                     return jsonify({'success':True , "message":f"Your Appointment With Booked Suceesfully . Please remember Your Booking ID!! Booking ID - {book_id} "})
                 else:
                     return jsonify({"success":True,"message":"Please Choose Other These Are Occupied we Have timings [10:00 AM , 10:30Am,11:00 Am , 11:30 AM ,12:00 PM ,1:00PM,1:30PM , 2:00 PM ,3:00PM]"})
              
             if result["intent"] == "EMERGENCY":
                 message1 = em.html(
                     subject="Emergency 🚨",
                     html=f"<p>Message Has been Sent to hospital and Ambulance is reaching your location as soon as possible </p>",
                     mail_from=("Emergency","trishamgupta43@gmail.com" ),
                     )
                 message1.send(
                     to=session.get('name'),
                     smtp={
                         "host": "smtp.gmail.com",
                         "port": 587,
                         "tls": True,
                         "user": "trishamgupta43@gmail.com",
                         "password": "fkpa acxf kqdp eaoz",
                     },
                     )
                 return jsonify({'success':True , "message":"MSG SENT TO HOSPITAL"})
             if result["intent"] == "CANCEL_APPOINTMENT":
                 d2 = {'host':'dpg-d8t9bi77f7vs73c0d8v0-a.oregon-postgres.render.com','password':'zG3dWR2oIyMKEHzSOE3sGwkqE3SgBfnj' , 'port': 5432, 'user': 'food_v1nx_user', 'database':'food_v1nx'}
                 sq3 = db.connect(**d2)
                 s2 = sq3.cursor()
                 s2.execute(f"delete  from book where id = {result["id"]}")
                 sq3.commit()
                 message2 = em.html(
                     subject="Cancled Appointment",
                     html=f"<p>Your Booking ID is {result["id"]} Cancel The Appointment</p>",
                     mail_from=("Canceled Appointment","trishamgupta43@gmail.com" ),
                     )
                 message2.send(
                     to=session.get('name'),
                     smtp={
                         "host": "smtp.gmail.com",
                         "port": 587,
                         "tls": True,
                         "user": "trishamgupta43@gmail.com",
                         "password": "fkpa acxf kqdp eaoz",
                     },
                     )
                 return jsonify({"success":True,"message":"Your Appointment is Cancled"})
             if result["intent"] == "RESCHEDULE_APPOINTMENT":
                 d3 = {'host':'dpg-d8t9bi77f7vs73c0d8v0-a.oregon-postgres.render.com','password':'zG3dWR2oIyMKEHzSOE3sGwkqE3SgBfnj' , 'port': 5432, 'user': 'food_v1nx_user', 'database':'food_v1nx'}
                 sq31 = db.connect(**d3)
                 s3 = sq31.cursor()
                 p1 = pd.read_sql(f"select id from book where date = '{result["date"]}' and slot = '{result["time"]}' and de = '{result["department"]}'",d3)
                 if p1.empty:
                     s3.execute(f"update book set date = '{result['date']}' , time = '{result["slot"]}' where id = {result['id']} ;")
                     sq31.commit()
                     message3 = em.html(
                     subject="Resechudle Appointment",
                     html=f"<p>Your Booking ID is {p1["id"].iloc[0]} Please remember and date , time , doctor is {result["date"]} , {result["time"]} ,{result["department"]} has been reshecudled </p>",
                     mail_from=("Reshecdule Appointment","trishamgupta43@gmail.com" ),
                     )
                     message3.send(
                     to=session.get('name'),
                     smtp={
                         "host": "smtp.gmail.com",
                         "port": 587,
                         "tls": True,
                         "user": "trishamgupta43@gmail.com",
                         "password": "fkpa acxf kqdp eaoz",
                     },
                     )
                     return jsonify({"success":True,"message":"Your Appointment is Suceessfully Reshedule"})
                 else:
                     return jsonify({"success":True,"message":"Please Choose Other These Are Occupied we Have timings [10:00 AM , 10:30Am,11:00 Am , 11:30 AM ,12:00 PM ,1:00PM,1:30PM , 2:00 PM ,3:00PM]"})
             
             if result["intent"] == "Medical Medicine Info":
                 client1 = genai.Client(api_key = "AQ.Ab8RN6LFsm0K7xV8eOcqwV-_QqD01kyPuns_ruxIXD6tlTiGzg")
                 interaction1 = client1.interactions.create(
                 model="gemini-2.5-flash",
                 input= f"{s['message']} You are medical medince assistant give orignal answeer only not fake and give brief")
                 return jsonify({"success":True,"message":interaction1.output_text})
       else:
           return jsonify({
           "success": False,
           "message": "Unauthorized access. Please login again."
           }), 401 
              
if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=5000) 




