from flask import Flask, redirect, render_template, request, url_for
from flask_pymongo import PyMongo
from pymongo import collection

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ITI"
mongo = PyMongo(app)


# to retrieve all record ->> find({})
# to retrieve specific record ->> find({"_id":1})
def next_id():
    user_flask_collection = mongo.db.users
    result =list(user_flask_collection.find().sort("_id",-1).limit(1))
    if len(result)>0:
        return result[0]['_id']+1
    else:
        return 1


############################ to retrieve table ############################ done
@app.route('/')
def retrieve_doc():
    user_flask_collection = mongo.db.users
    result = list(user_flask_collection.find())
    return render_template('index.html', users_html = result)

############################# to delete table ############################# done
@app.route('/delete/<int:id>')
def delete_doc(id):
    user_flask_collection = mongo.db.users
    user_flask_collection.delete_one({"_id":id})
    return redirect(url_for('retrieve_doc'))

############################# to update table ########################## done
@app.route('/update')
def update_doc():
    id=int(request.args.get("id"))
    name= request.args.get("name")
    age= request.args.get("age")
    location= request.args.get("location")
    user_flask_collection =mongo.db.users
    user_flask_collection.update_one({"_id":int(id)},{'$set':{"_id":id,"name":name,"age":age,"location":location}})
    return "user updated .."

############################# to create table ####################### done
@app.route('/adduser', methods=['GET', 'POST'])
def create_doc():
    if request.method == 'GET':
        return render_template('adduser.html')
    else:
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        if name != None or age != None or location != None:
            user_flask_collection = mongo.db.users
            user_flask_collection.insert_one({"_id": next_id(), "name": name, "age": age, "location": location})
        return redirect(url_for('retrieve_doc'))

#to run application.
if __name__ == "__main__":
    app.run(debug=True)
