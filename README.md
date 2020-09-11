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
