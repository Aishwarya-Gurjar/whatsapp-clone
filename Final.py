import paho.mqtt.client as mqtt
import pandas as pd
import time
import csv

def on_log(client,userdata,level,buf):
	print("log : "+buf)

def on_connect(client,userdata,flags,rc):
	if rc==0:
		print("Connection OK")
	else :
		print("Bad connection with rc ",rc)

def on_message(mqttc, obj, msg):
	m_decode=str(msg.payload.decode("utf-8","ignore"))
	print("\n"+m_decode)

def on_disconnect(client,userdata,flags,rc=0):
	print("Disconnected "+str(rc))

def on_unsubscribe(client, userdata, mid):
	print("\nYou left the group successfully!\nYou wont receive further messages of this group\n")


broker="hivemq.com"
print("-------------Welcome to MY MQTT chat application--------------\n")
ln=raw_input("Press 1: Sign In(If you already have an account with us)\nPress 2 : Sign Up!(If you are a New User)\n")
login=int(ln)
name=raw_input("Enter your name:  ")
mob_no=raw_input("Enter Mobile number:  ")
new_row=[{'Name': name, 'Mobile_no' : mob_no }]
if login==2:
	print("**********Register yourself first***************")
	data_entry=pd.read_csv("Registration.csv")
	data_entry = data_entry.append(new_row, ignore_index=True)
	data_entry.to_csv('Registration.csv', index=False)

client=mqtt.Client(client_id=name, clean_session=False) 
df = pd.read_csv("online.csv")
df = df.append(new_row, ignore_index=True)
df.to_csv('online.csv', index=False)


client.on_connect=on_connect
client.on_disconnect=on_disconnect
client.on_message=on_message
client.on_unsubscribe=on_unsubscribe
print("connecting to broker ....",broker)
client.connect("127.0.0.1",9999,keepalive=60)

print("You are online now!")
client.subscribe(name,qos=1)
client.loop_start()
# Adding to the group if client is already a part of any exixting group
with open("Group.csv") as f:
	for row in f :
		rowx=row.rstrip()
		if rowx !="Name":
			row2=rowx+".csv"
			data_grp=pd.read_csv(row2)
			p1=data_grp.isin([name])
			if p1.any().any():
				client.subscribe(rowx)


#Menu driven approach starts from here
c2=input("Enter 1 : To send personal message\nEnter 2 : To start a group chat\nEnter 3: To leave a group chat\nEnter 4 : To Create Group\nEnter 0: To quit\n")
choice=int(c2)
while choice:
	#this loop is for one to one chat facility
	if choice==1:
		y=1
		while y: 
			ut=raw_input("Press 1 to see all available people\n Press 2 to see only online people\n")
			utt=int(ut)
			if utt==1:
				print("List of all available people:")
				data_ent=pd.read_csv("Registration.csv")
				print(data_ent)
			else:
				print("List of people who are online :")
				df2 = pd.read_csv("online.csv")
				print(df2)

			t2=raw_input("Enter 1 to wait and 2 to send message\n")
			temp=int(t2)
			if temp==1:
				time.sleep(3)
			elif temp==2:
				w=raw_input("Enter name of person you want to send message:\n")
				topic=str(w)
				msg=raw_input("Enter your message:\t")
				st=name+" has sent msg: "+msg
				client.publish(topic,st,qos=1, retain=False)
				time.sleep(2)	
			x =input("Enter 0 to exit from personal chat or press 1 to see people who are online\n")
			y=int(x)
	#This loop is for group chat facility
	elif choice==2:
		print("List of available groups:\n")
		temp=pd.read_csv("Group.csv")
		print(temp)
		q=raw_input("Enter Group name to see the members of that group\n press # to send messages in group \n")
		v=str(q)
		while v!='#':
			gpname=v+".csv"
			print("**********List of" + v +"People*************\n")
			dfs= pd.read_csv(gpname)
			print(dfs)
			q=raw_input("Enter Group name to see the members of that group\n press # to send messages in group \n")
			v=str(q)

		nm=raw_input("Enter name of group to which you want to send message\t")
		nm2=nm+".csv"
		gp_frame=pd.read_csv(nm2)
		present=gp_frame.isin([name])
		if present.any().any():
			client.subscribe(nm)
			msg=raw_input("Enter your message:\t")
			st=name+" has sent msg in "+nm+" :"+msg
			client.publish(nm,st,qos=1, retain=False)
			time.sleep(2)

		else:
			print("You are currently not the part of this group\n Do you want to become the member of this group?\n ")
			ch=raw_input("Enter Y or N\n")
			if ch=='Y' or ch=='y':
				ngp_frame = pd.read_csv(nm2)
				new_row=[{'Name': name, 'Mobile_no' : mob_no }]
				ngp_frame = ngp_frame.append(new_row, ignore_index=True)
				ngp_frame.to_csv(nm2, index=False)
				client.subscribe(nm)
				msg=raw_input("Enter your first message of the group:\t")
				st=name+" has sent msg in "+nm+" :"+msg
				client.publish(nm,st,qos=1, retain=False)
				time.sleep(2)
	#this option is for leving a group chat
	elif choice==3:
		print("List of available groups:\n")
		temp=pd.read_csv("Group.csv")
		print(temp)
		nm=raw_input("Enter name of group which you want to leave")
		nm2=nm+".csv"
		gp_frame=pd.read_csv(nm2)
		present=gp_frame.isin([name])
		if present.any().any():
			left=name+" has left the "+nm
			client.publish(nm,left,qos=1, retain=False)
			client.unsubscribe(nm)
			indexNames = gp_frame[ gp_frame['Name'] == name ].index
			gp_frame.drop(indexNames , inplace=True)
			gp_frame.to_csv(nm2, index=False)
			time.sleep(2)
		else :
			print("\nYou were never part of this group\n")
	#this option is for creating a group
	elif choice==4:
		xt=raw_input("Enter the name of group you want to create\n")
		xtt=str(xt)
		gpf=pd.read_csv("Group.csv")
		temp = gpf.isin([xtt])
		if temp.any().any():
			wq=raw_input("This group already exixts\nPress Y to join the current group or N to go back to main menu\n")
			wqq=str(wq)
			if wqq=='Y' or wqq=='y':
				hd2=xtt+".csv"
				ogp_frame = pd.read_csv(hd2)
				present=ogp_frame.isin([name])
				if present.any().any():
					print("You are already a member of this group\n")
				else:
					new_row=[{'Name': name, 'Mobile_no' : mob_no }]
					ogp_frame = ogp_frame.append(new_row, ignore_index=True,sort=False)
					ogp_frame.to_csv(hd2, index=False)
					client.subscribe(xtt)
					print("You are successfully added in "+xtt+" group\n")
		else:
			new=[{'Name':xtt}]
			gpf = gpf.append(new, ignore_index=True,sort=False)
			gpf.to_csv("Group.csv", index=False,header=True)
			cars = {'Name': [name], 'Mobile_no': [mob_no]}
			new_gf = pd.DataFrame(cars, columns= ['Name', 'Mobile_no'])
			filename=xtt+".csv"
			new_gf.to_csv(filename,index=False,header=True)
			client.subscribe(xtt)
			print(xtt+" Group is created successfully and you are added in it\n")

	x =input("Enter 1 : To send personal message\nEnter 2 : To start a group chat\nEnter 3: To leave a group chat\nEnter 4 : To Create Group\nEnter 0: To quit\n")
	choice=int(x)

df = pd.read_csv("online.csv")
indexNames = df[ df['Name'] == name ].index
df.drop(indexNames , inplace=True)
df.to_csv('online.csv', index=False)
client.loop_stop()
client.disconnect()
