# whatsapp-clone
Implementation of Messenger Application using MQTT
This work implements the basic functionalities of chat application based on MQTT(Message Queue Telemetry Transport).
It is lightweight messaging protocol for machine to machine communication.
MQTT is based on Publish - Subscribe model in which there exits three main entities which are:
• Broker : controls the publish-subscribe message pattern
• Publisher : can be understood as source of data
• Subscriber : which is interested in the data

 
Publish/subscribe is event‐driven and enables messages to be pushed to clients. The central communication point is the MQTT broker, which is in charge of dispatching all messages between the senders and the rightful receivers. Each client that publishes a message to the broker, includes a topic into the message. The topic is the routing information for the broker. Each client that wants to receive messages subscribes to a certain topic and the broker delivers all messages with the matching topic to the client. The clients don’t have to know each other. They only communicate over the topic.
Also the topics can be any kind of string. It can be simple or hierarchical , separated by ‘/’.
Quality of Service Levels (Three levels) :
• 0 = At most once (Best effort, No Ack)! Fire and Forget
• 1= At least once (Acked, retransmitted ifAack not received)
• 2= Exactly once [Request to send (Publish), Clear-to-send (Pubrec), message (Pubrel), ack (Pubcomp).
There also exits concept of retained messages in which Server keeps messages even after sending it to all subscribers (New subscribers get the retained messages) .
Steps to run the code :
1. Run the HiveMQ server in background (go in the bin folder of hiveMQ).
 $ ./run.sh
2. Go to the extracted zip folder of the code and run the file “final.py”. Follow the steps as per your requirement ( the code is already menu driven). This will create one client for the chat application.
 $ python final.py
 3. The above step has to repeated for every client. Open a separate terminal and again run the same script using the above command. Make sure that all the CSV’s are in the same folder as the script file because these files will serve as a record for the entry of users.
Registration.csv := This will consists of all the registered user of the chat application.
Online.csv := This will consists of active (online) users of the application. Whenever any user disconnects from the application(goes offline), the entry will be deleted from this file.
Group_x.csv := This consists of users added in a particular group named as Group_x. 
