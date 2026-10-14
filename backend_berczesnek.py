import oracledb
import ast

def get_all_orders(cursor):
    sql = "SELECT * FROM PERSONS"
    cursor.execute(sql)
    return cursor.fetchall()

def main():
    try:
        host = "codd.inf.unideb.hu"
        port = 1521
        service = "ora21cp.inf.unideb.hu"
        user = "u_ki4tgb"
        pwd = "*******"

        connection = oracledb.connect(
            host=host,
            port=port,
            service_name=service,
            user=user,
            password=pwd
        )
    
        print("Connection established")
        cursor = connection.cursor()
    
        order_list = get_all_orders(cursor)
        orders = []
        for order in order_list:
            orders.append({order[1] + " " + order[2]:order[4]})
        print(orders)

        names = set()
        for order in orders:
            for key in order.keys():
                names.add(key)
        print(names) 

        items = set()
        for order in orders:
            for key, value in order.items():
                value = ast.literal_eval(value)
                for key in value.keys():
                    items.add(key)
        print(items)

        item_count = dict.fromkeys(items, 0)
        item_count_by_person = dict.fromkeys(items, 0)
        person_count = set()
        current_item_list = set()

        for order in orders:
            for name, order_lists in order.items():
                order_lists = ast.literal_eval(order_lists)       
                for item in order_lists.keys():
                    if item in order_lists:
                        item_count[item] += order_lists[item]
                    if item in order_lists and item not in current_item_list:
                        item_count_by_person[item] += 1
                        if item in order_lists and item in current_item_list and name in person_count:
                            item_count_by_person[item] -= 1 
                current_item_list.add(item)
                person_count.add(name)

        for key, value in item_count.items():
            print(f"{key}: {value} darab ({item_count_by_person[key]} ember rendelte)")
        
        for key, value in item_count.items():
            if key == 'karfiol':
                print(f"{value} darab karfiolt rendelt {item_count_by_person[key]} különböző ember.")

        """
        for order in orders:
            order = ast.literal_eval(order)
            items.add(order.getkeys())
            orders.append(order)

        print(orders)
        items = set()
        for key in order.keys():
            items.add(key)
        print(items)
        item_count = dict.fromkeys(items, 0)
        item_count_by_person = dict.fromkeys(items, 0)
        for order in orders:
            order = ast.literal_eval(order)
            for key in items:
                if key in order:
                    item_count[key] += order[key]
                    item_count_by_person[key] += 1

        

        """
    except OperationalError:
        print("Could not connect to Oracle db.")

if __name__ == "__main__":
    main()
