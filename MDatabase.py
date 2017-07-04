from pymongo import MongoClient


class Database: 
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")
        self.countt = 0

    def print_db(self,database,tabel): # tabel is collection
        db = self.client[database] # Name of Database
        collection = db[tabel] # tabel (collection) like in Rational Database
        count = 0
        for item in collection.find({}): # getting all the products in database
            print(">>Item : ", item) # printing every product 

    def clear_db(self,database):
        self.client.drop_database(database)
        print('\n\n  ******  Database {} Cleared.  ***************'.format(database))

    def insert_item(self,database,tabel,dic,attribute):
        db = self.client[database]
        collection = db[tabel]

        if attribute == None:
            collection.insert(dic)
            print(">>Item Inserted  DB : ",dic)
            return

        #print()
        if collection.find_one({attribute :dic[attribute]}) == None:
            collection.insert(dic)
            print(">>Item Inserted  DB : ",dic[attribute])
        else:
            print(">>Already existed in database ### {} : ".format(dic[attribute]))

        return

    def get_item(self,database,tabel,attribute,attribute_value):
        db = self.client[database]
        collection = db[tabel]
        result = collection.find_one({attribute : attribute_value})
        return result

    def get_all(self,database,tabel):
        li = []
        db = self.client[database] # Name of Database
        collection = db[tabel] # tabel (collection) like in Rational Database
        count = 0
        for item in collection.find({}): # getting all the products in database
            li.append(item)

        return li    




# if __name__ == "__main__":
#     database = "Test1"
#     tabel = "Tabel1"
#     dic = {}
#     dic['1'] = "hello1"
#     dic['2'] = "hello2"
#     dic['3'] = "hello3"
#     dic['4'] = "hello4"

#     dic2 = {}
#     dic2['1'] = "hello1"
#     dic2['2'] = "hello2"
#     dic2['3'] = "hello3"
#     dic2['4'] = "hello44444"


#     db = Database()
#     db.clear_db(database)
#     #db.insert_item(database,tabel,dic,None)
#     print("check 1")
#     db.insert_item(database,tabel,dic,'4')
#     dic['4'] = "hello test"
#     print("check 2")
#     db.insert_item(database,tabel,dic2,'4')
#     print("check 3")
#     db.print_db(database,tabel)
#     print("check 4")
#     item = db.get_item(database,tabel,'4',"hello test")
#     print("check 5")
#     print(item)






