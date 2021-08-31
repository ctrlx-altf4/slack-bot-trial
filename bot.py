import os;
import slack;
from pathlib import Path;
from dotenv import  load_dotenv;
from flask import Flask, request, Response;
from slackeventsapi import SlackEventAdapter;
import json;



env_path = Path('.') / '.env';
load_dotenv(dotenv_path=env_path)

app = Flask(__name__);
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/event',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

BOT_ID = client.api_call("auth.test")['user_id']

x={"type":"block_actions","message":{"bot_id":"B02D1H42D1P","type":"message","text":"This content can't be displayed.","user":"U02CP4WA64T","ts":"1630308984.007300","team":"T02CM1LSL3C","blocks":[{"type":"section","block_id":"voD","text":{"type":"mrkdwn","text":"Section block with radio buttons","verbatim":False},"accessory":{"type":"radio_buttons","action_id":"radio_buttons-action","options":[{"text":{"type":"plain_text","text":"*this is plain_text text*","emoji":True},"value":"value-0"},{"text":{"type":"plain_text","text":"*this is plain_text text*","emoji":True},"value":"value-1"},{"text":{"type":"plain_text","text":"*this is plain_text text*","emoji":True},"value":"value-2"}]}}]},"state":{"values":{"voD":{"radio_buttons-action":{"type":"radio_buttons","selected_option":{"text":{"type":"plain_text","text":"*this is plain_text text*","emoji":True},"value":"value-0"}}}}},"actions":[{"action_id":"radio_buttons-action","block_id":"voD","selected_option":{"text":{"type":"plain_text","text":"*this is plain_text text*","emoji":True},"value":"value-0"},"type":"radio_buttons","action_ts":"1630395445.519804"}]}

print(x.get('user'))

message={
	"type": "home",
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Welcome to your _App's Home_* :tada:"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Section block with radio buttons"
			},
			"accessory": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					}
				],
				"action_id": "radio_buttons-action"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Click me!"
					}
				}
			]
		}
	]
}

def json_formatter(json_data):
    formatted_json = json.dumps(json_data,indent=4)
    return formatted_json
    

welcome_messages={}


class WelcomeMessage:

    START_TEXT={
        'type':'section',
        'text':{
            'type':'mrkdwn',
            'text':"Welcome"
        }
    }

    DIVIDER={
        'type':'divider'
    }
    def __init__(self,channel,user,):
        self.channel = channel
        self.user = user
        self.icon_emoji = ':robot_face:'
        self.timestamp = ''
        self.completed = False

    def get_message(self):
        return {
            'ts':self.timestamp,
            'channel':self.channel,
            'username':'welcome Robot!',
            'icon_emoji':self.icon_emoji,
            'blocks':[
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }

    def _get_reaction_task(self):
        checkmark= ':white_check_mark:'

        if not self.completed:
            checkmark=':white_large_square:'
        text = f'{checkmark} *React to this message* '

        return {'type':'section','text':{'type':'mrkdwn','text':text}}


def send_welcome_message(channel,user): 
    welcome= WelcomeMessage(channel,user)
    message = welcome.get_message()
    response = client.chat_postMessage(**message)
    welcome.timestamp=response['ts']

    if channel not in welcome_messages:
        welcome_messages[channel] ={}
    welcome_messages[channel][user] =welcome

@slack_event_adapter.on('message')
def message(payload):

    event = payload.get('event',{})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if user_id != None and BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id,blocks=[{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Section block with radio buttons"
			},
			"accessory": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "*this is plain_text text*",
							"emoji": True
						},
						"value": "value-2"
					}
				],
				"action_id": "radio_buttons-action"
			}
		}])

@app.route("/message_count",methods=["POST"])
def message_count():
    client.chat_postMessage(channel="#test",text="I have entered")
    return Response(),200

@app.route("/slack/interaction",methods=["POST"])
def get_interaction():
	data= request.form
	selected = data.get('payload')

	jsonified = json.loads(selected)

	x=jsonified.get('actions')

	print("json",x)

	return Response(),200

	
# def get_interaction():
#     data = request.form

#     selected = data.get('payload')
# 	print("hello")
# jsonfied = json.loads(selected)

#     print('selected',type(selected))

#     client.chat_postMessage(channel="#test",text="Received with thans")
#     return Response(),200


if __name__ == '__main__':
    app.run(debug=True)