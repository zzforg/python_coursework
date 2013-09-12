
###################################################################
#
#   CSSE1001 - Assignment 1
#
#   Student Number:41870288
#
#   Student Name:Zhiguo ZENG
#
###################################################################

def load_parts(filename):
    """load the parts.txt file and return as a dictionary.
    also a tuple is return as the value of the dictionary.
    {string:(string,int)}
    """
    parts = {}
    with open(filename, 'U') as f:
      for line in f:
        data = line.strip().split(',')
        if len(data) == 3:#split the data in to 3 parts
          cost = data[2].strip()
          if cost.isdigit():
            parts[data[0].strip()] = (data[1].strip(), int(cost))#dict final format
      return parts



def get_components(parts):
    """return the input dictionary into a list of pair.
    (string,int)
    """
    c = []  #components
    for i in parts:
      
        a = i.split(':')#dict-> list
        b = (a[0].strip(), int(a[1].strip()))#formating the list of pair
        c.append(b)
    return c
     


def load_products(filename):
    """load the products.txt file and array into a dictionary.
    {string:(string,[string,int])}
    """
    f = open(filename, 'U')
    p=f.readlines()
    f.close()

    products = {}
    for line in p:
        parts = line.strip().split(',')

        if len(parts) >=2:
            products[parts[0].strip()]=(parts[1].strip(),get_components(parts[2:]))
    return products

          

def get_product_id(product_dict, name):
    """"return the ID of product by the given name.
    getID(dict, str) -> ID
    precondition: define products from the function load_products
    """

    for id in product_dict:
        if product_dict[id][0] == name:
            return id
    return None #return none when the id is not existing


       
def get_product_name(product_dict, id):
    """takes a argument of dictionary and a str to return the name.
    getName(dict,str) -> Name
    precodition: define the products from load_products
    """
    for p_id in product_dict:
        if p_id == id:
            return product_dict[p_id][0]
    return None        



def get_parts(product_dict, id):
    """return the parts ID and number as a pair of list.
    getParts(dict,str)->list(str,int)
    precondition: load data from load_products
    """
    for p_id in product_dict:
        if p_id == id:
            return product_dict[p_id][1]
    return None



def compute_cost(product_dict, parts_dict, id):
    """caculate the total cost of the bike from input the ID.
    return the sum of all the parts cost.
    compute_cost(dict,dict,str)-> int(total cost)
    """
    total = 0
    
    if get_parts(product_dict, id) == None:
        return None #in case of the object is 'nonetype'
    
      
    for part, quantity in get_parts(product_dict, id):#define two parts in the get_parts(product_dict,id)
        total += parts_dict.get(part)[1] * quantity #sum up all parts(also caculate the quantity of parts)
    return total



def interact():
    """built up the top-level interface by input the valid command.
    valid commands run the previous functions
    precodition: load data into variable parts and products.
    """
    parts = load_parts('parts.txt')
    products = load_products('products.txt')

    while True:
        user_input = raw_input('command: ')
        
        if user_input[0] == 'e':
            break
        elif user_input[0] == 'i':
            result = get_product_id(products, user_input[2:])
        elif user_input[0] == 'n':
            result = get_product_name(products, user_input[2:])
        elif user_input[0] == 'p':
            result = get_parts(products,user_input[2:])  
        elif user_input[0] == 'c':
            result = "%.2f"%(compute_cost(products,parts, user_input[2:])/100)
        else:
            print 'Unknown command'#notes the user that to input the valid command
            continue #ensure not to exit the programme when inputing wrong comman
            
        if result:
            print result
        else:
            print 'No such item'#ensure user to input correct items

