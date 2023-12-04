import frappe
import random
from frappe.utils import pretty_date, now

def greet_birthday():
    greet_message('birthday')


def greet_work_anniversary():
    greet_message('work_anniversary')
            
def greet_message(type: str):
    if type == 'birthday':
        message_field = 'birthday_messages'
        field_date = 'date_of_birth'
    elif type == 'work_anniversary':
        message_field = 'work_anniversary_messages'
        field_date = 'date_of_joining'

    messages = frappe.db.get_value('Celebrate Settings', None, message_field)
    messages = messages.splitlines()
    
    for message in messages:
        if message.strip() == '':
            messages.remove(message)    
    
    date_today  = frappe.utils.data.getdate()
    day = date_today.strftime("%d")
    month = date_today.strftime("%m")
    employees = frappe.db.sql("""select first_name, last_name, {0} from tabEmployee where status='Active' and DAY({0})={1} and MONTH({0})={2}""".format(field_date, day, month))
    for employee in employees:
        first_name = employee[0]
        last_name = employee[1]
        celebrate_date = employee[2]
        employee_name = first_name.strip() + " " + last_name.strip()
        years = pretty_date(celebrate_date.strftime('%Y-%m-%d %H:%M:%S.%f')).replace(' ago', '')        

        pick_message = random.randint(0, len(messages) - 1)
        greeting_message = messages[pick_message].strip().replace('{name}', employee_name).replace('{years}', years)

        
        print(employee_name + ", " + greeting_message)            