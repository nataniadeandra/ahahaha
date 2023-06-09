from collections import namedtuple

from django.db import connection

# Create your views here.
def is_authenticated(request):
    '''Check if user in a session'''
    try:
        request.session["email"]
        return True
    except KeyError:
        return False

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_query(str):
    '''Execute SQL query and return its result as a list'''
    cursor = connection.cursor()
    result = []
    try:
        cursor.execute(str)
        result = namedtuplefetchall(cursor)
    except Exception as e:
        result = e
    finally:
        cursor.close()
        return result

def get_role(email, password):
    print("x")
    admin_query = get_query(
        f'''
        SELECT ua.email
        FROM sirest.user_acc ua
        INNER JOIN sirest.admin a
        ON ua.email = a.email
        WHERE ua.email='{email}' AND ua.password='{password}';
        '''
    )
    if type(admin_query) == list and len(admin_query) != 0:
        print("admin")
        return "admin"

    customer_query = get_query(
        f'''
        SELECT ua.email
        FROM sirest.user_acc ua
        INNER JOIN sirest.customer a
        ON ua.email = a.email
        WHERE ua.email='{email}' AND ua.password='{password}';
        '''
    )
    if type(customer_query) == list and len(customer_query) != 0:
        print("customer")
        return "customer"

    restaurant_query = get_query(
        f'''
        SELECT ua.email
        FROM sirest.user_acc ua
        INNER JOIN sirest.restaurant r
        ON ua.email = r.email
        WHERE ua.email='{email}' AND ua.password='{password}';
        '''
    )
    if type(restaurant_query) == list and len(restaurant_query) != 0:
        print("restaurant")
        return "restaurant"

    courier_query = get_query(
        f'''
        SELECT ua.email
        FROM sirest.user_acc ua
        INNER JOIN sirest.courier c
        ON ua.email = c.email
        WHERE ua.email='{email}' AND ua.password='{password}';
        '''
    )
    if type(courier_query) == list and len(courier_query) != 0:
        print("courier")
        return "courier"

    print("not verified")
    return ""

def get_session_data(request):
    if not is_authenticated(request):
        return {}
    try:
        return {"email": request.session["email"], "role": request.session["role"]}
    except:
        return {}