import telegram
import time
import os
import re
from flask import Flask, request, abort

app = Flask(__name__)

bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", default='358005772:AAEzqBAhUCKPIeIxi1IozFrxl04qauIuCVg')
bot = telegram.Bot(token=bot_token)
@app.route('/notify', methods=['POST'])
def web():
    if request.method == 'POST':
        pipeline_branch=request.json['object_attributes']['ref']
        pipeline_project_namespace=request.json['project']['namespace']
        pipeline_project_name=request.json['project']['name']
        chat_id = request.args.get('chat_id')
        branch_notify = request.args.get('notify_branches').replace(',', '|')
        if re.match(branch_notify, pipeline_branch):
            #print(request.json)
            print("Notify sending: project {0}/{1}, branch: {2}".format(pipeline_project_namespace, pipeline_project_name, pipeline_branch))

        else:
            abort(400)
        pipeline_project_url=request.json['project']['web_url']
        pipeline_user=request.json['user']['name']
        pipeline_id=request.json['object_attributes']['id']
        pipeline_status=request.json['object_attributes']['status']
        pipeline_duration=time.strftime('%H:%M:%S', time.gmtime(request.json['object_attributes']['duration']))
        msg = "Project: {0}/{1}\nBranch: {2}\nUser: {3}\nDuration: {4}".format(str(pipeline_project_namespace),
                                                                               str(pipeline_project_name), str(pipeline_branch),
                                                                               str(pipeline_user), str(pipeline_duration))
        if pipeline_status == 'success':
            msg = "✅ *Прошла успешная сборка:*\n{0}\n{1}/pipelines/{2}".format(msg, str(pipeline_project_url), str(pipeline_id))
            bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
        elif pipeline_status == 'failed':
            msg = "❌ *Провалилась сборка:*\n{0}\n{1}/pipelines/{2}".format(msg, str(pipeline_project_url), str(pipeline_id ))
            bot.send_message(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)
        else:
            print('Other status')
        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run('0.0.0.0')
