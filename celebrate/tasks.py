import frappe
import random
from frappe.utils import pretty_date, now
from discord_webhook import DiscordWebhook, DiscordEmbed

def notify_chat(title, color, message, attachments):
    print(attachments)
    try:
        webhook = DiscordWebhook(
            url=frappe.db.get_value('Celebrate Settings', None, 'discord_url'))
        
        embed = DiscordEmbed(
            title=title, description=message, color=color)
        for attach in attachments:
            if str(attach['name']).strip() == '':
                tenant_name = 'Vacant'
            else:
                tenant_name = str(attach['name']).strip()

            if "name" in attach:
                embed.add_embed_field(
                    name=tenant_name, value=attach['device'])
            else:
                embed.add_embed_field(name='Message', value=attach['text'])
        webhook.add_embed(embed)
        response = webhook.execute()
    except:
        None


def greet_birthday():
    greet_message('birthday')


def greet_work_anniversary():
    greet_message('work_anniversary')
            
def greet_message(type: str):
    if type == 'birthday':
        message_field = 'birthday_messages'
        field_date = 'date_of_birth'
        title = 'Happy Birthday'
        color = 'FFC0CB'
        
    elif type == 'work_anniversary':
        message_field = 'work_anniversary_messages'
        field_date = 'date_of_joining'
        title = 'Happy Work Anniversary'
        color = '355E3B'
        
    messages = frappe.db.get_value('Celebrate Settings', None, message_field)
    messages = messages.splitlines()
    
    for message in messages:
        if message.strip() == '':
            messages.remove(message)    
    
    date_today  = frappe.utils.data.getdate()
    day = date_today.strftime("%d")
    month = date_today.strftime("%m")
    year_now = date_today.strftime("%Y")
    
    employees = frappe.db.sql("""select first_name, last_name, {0} from tabEmployee where status='Active' and DAY({0})={1} and MONTH({0})={2}""".format(field_date, day, month))
    for employee in employees:
        first_name = employee[0]
        last_name = employee[1]
        celebrate_date = employee[2]
        
        year_celebrate = celebrate_date.strftime('%Y')
        if year_now != year_celebrate:

            employee_name = first_name.strip() + " " + last_name.strip()
            years = pretty_date(celebrate_date.strftime('%Y-%m-%d %H:%M:%S.%f')).replace(' ago', '')        

            pick_message = random.randint(0, len(messages) - 1)
            greeting_message = messages[pick_message].strip().replace('{name}', employee_name).replace('{years}', years)
            notify_chat(title + ', ' + employee_name, color, greeting_message, [])
