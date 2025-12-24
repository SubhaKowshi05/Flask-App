from flask import Flask, redirect, render_template, request,url_for
from flask_sqlalchemy import SQLAlchemy
from flask import flash
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime

local_server = True
app = Flask(__name__)
app.secret_key = "subhaloguuu#25"

# Login Manager
login_manager=LoginManager(app)
login_manager.login_view='login'


@login_manager.unauthorized_handler
def unauthorized():
    flash("Please log in to access this page", "warning")
    return redirect(url_for("login"))


# Databse Connection
# app.config['SQLALCHEMY_DATABASE_URI']='mysql://username:password@localhost/databasename'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/capstone'
db=SQLAlchemy(app)

# Configuration for file handling
app.config['UPLOAD_FOLDER']="static/uploads"
app.config['ALLOWED_EXTENSIONS']=['png','jpg','jpeg','gif','pdf']
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 #16 MB max file size

# Load User Using user_id
@login_manager.user_loader
def load_user(user_id):
    return Signup.query.get(int(user_id))

#Defining Models in another file models.py
class Socialmedia(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))

# Signup Model Defining
class Signup(UserMixin,db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100),unique=True)
    phone = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(1000))
    profileimage=db.Column(db.String(500))

    def get_id(self):
       return self.user_id
    
# Post Model Defining
class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(100))
    post_title = db.Column(db.String(100))
    post_description = db.Column(db.String(500))
    image = db.Column(db.String(500))
    date = db.Column(db.String(500))
    time = db.Column(db.String(500))
    likes = db.Column(db.Integer,nullable=True)

# Comments Model Defining
class Comments(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    comment = db.Column(db.String(500))
    commented_by = db.Column(db.String(100))
    commented_on = db.Column(db.String(100))

# Friend Request Model Defining
class Friends(db.Model):
    friend_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    requested_id = db.Column(db.Integer)
    isAccepted = db.Column(db.String(20))

# Contact Page Model Defining
class Contact(db.Model):
    contact_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    description = db.Column(db.String(800))

# #Return Index Templates
# @app.route("/")
# def index():
#     return render_template("home.html")

@app.route("/")
def home():
    data=Posts.query.all()
    return render_template("home.html",data=data)

# Backend code for the app
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":  
        firstName = request.form.get("fname")
        lastName = request.form.get("lname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirmPassword = request.form.get("confirmpassword")

        # print(firstName, lastName, email, phone, password, confirmPassword)

        # Password match check
        if password != confirmPassword:
            flash("Passwords do not match!", "warning")
            return redirect(url_for("signup"))

        # Existing user check
        fetchemail = Signup.query.filter_by(email=email).first()
        fetchphone = Signup.query.filter_by(phone=phone).first()
        if fetchemail or fetchphone:
            flash("User email or phone number already exists!", "warning")
            return redirect(url_for("signup"))
        
        if len(phone)!=10:
            flash("Phone number should be a 10-digit number!")
            return redirect(url_for("signup"))
        
        gen_pass=generate_password_hash(password)

        # Insert data using SQLAlchemy ORM (not raw SQL)
        new_user = Signup(
            first_name=firstName,
            last_name=lastName,
            email=email,
            phone=phone,
            password=gen_pass
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Signed Up Successfully!", "success")
        return redirect(url_for("login"))

    # For GET requests
    return render_template("signup.html")

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = Signup.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Logged in Successfully!", "success")
            return redirect(url_for("home"))  # redirect to home after login
        else:
            flash("Invalid User Details!", "danger")
            return render_template("login.html")

    return render_template("login.html")

# Allowed files in backend
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/posts", methods=['GET', 'POST'])
@login_required
def posts():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        post_title = request.form['title']
        post_description = request.form['description']
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            time_str = now.strftime("%H:%M:%S")

            new_post = Posts(
                email=email,
                name=name,
                post_title=post_title,
                post_description=post_description,
                image=filename,
                date=date_str,
                time=time_str
            )

            db.session.add(new_post)
            db.session.commit()

            flash("Post Uploaded Successfully", "success")
            return redirect(url_for("posts"))

        else:
            flash("Allowed file types: png, jpg, jpeg, gif, pdf", "danger")

    # FETCH only this user's posts
    user_posts = Posts.query.filter_by(email=current_user.email).all()
    return render_template("posts.html", user_posts=user_posts)


# Likes Function
@app.route("/like/<int:id>",methods=['GET','POST'])
@login_required
def like(id):
    post=Posts.query.filter_by(post_id=id).first()
    if post.likes is None:
       post.likes = 1
    else:
       post.likes = post.likes + 1
    db.session.commit()
    return redirect(url_for('home'))

# Comments Function
@app.route("/comment/<int:id>", methods=['GET', 'POST'])
@login_required
def comment(id):
    if request.method == 'POST':
        comment = request.form['comment']
        commented_by = request.form['commented']
        commented_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_comment=Comments(post_id=id,comment=comment,commented_by=commented_by,commented_on=commented_on)
        db.session.add(new_comment)
        db.session.commit()
        flash("Comment Added","success")
        return redirect(url_for("home"))
    
# View Comments Function
@app.route("/viewcomment/<int:id>",methods=['GET','POST'])
@login_required
def viewcomment(id):
    post=Comments.query.filter_by(post_id=id).all()
    return render_template("comments.html",post=post)

# Friends Request Section
@app.route("/connect", methods=['GET'])
@login_required
def connect():
    users = Signup.query.filter(Signup.user_id != current_user.user_id).all()
    return render_template("connect.html", users=users)


# Connect or add With Friends Function
@app.route("/connectfriend/<path:ids>",methods=['GET'])
@login_required
def connectFriend(ids):
    # print(ids)
    data=ids.split("/")
    # print(data)
    users=Signup.query.all()
    sender = int(data[0])     # current user sending request
    receiver = int(data[1])   # the user receiving request

    query = Friends(
         user_id=sender,
         requested_id=receiver,
         isAccepted="False")
    d1 = Friends.query.filter_by(user_id=sender, requested_id=receiver).first()
    d2 = Friends.query.filter_by(user_id=receiver, requested_id=sender).first()

    if d1 or d2:
        flash("Request has already been sent!", "warning")
        return redirect(url_for("connect"))
    
    db.session.add(query)
    db.session.commit()
    flash("Request sent","success")
    return redirect(url_for("connect"))


# Remove Friend from the friend request
@app.route("/removefriend/<path:ids>", methods=['GET'])
@login_required
def removeFriend(ids):
    data = ids.split("/")
    sender = int(data[0])      # other user
    receiver = int(data[1])    # current user

    # CORRECT search direction
    record = Friends.query.filter_by(user_id=sender, requested_id=receiver).first()

    if record:
        db.session.delete(record)
        db.session.commit()
        flash("Friend request cancelled!", "success")
    else:
        flash("No friend request found to remove.", "warning")

    return redirect(url_for("connect"))

@app.route("/acceptfriend/<path:ids>",methods=['GET'])
@login_required
def acceptFriendrequest(ids):
    # print(ids)
    data=ids.split("/")
    # print(data)
    users=Signup.query.all()
    sender = int(data[0])     # current user sending request
    receiver = int(data[1])   # the user receiving request

    query = Friends(user_id=sender,requested_id=receiver,isAccepted="True")
    
    db.session.add(query)
    db.session.commit()
    flash("Friend Request Accepted!","success")
    return redirect(url_for("profile"))


# Profile page function
@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    userdata = Signup.query.filter_by(email=current_user.email).first()

    # Show requests RECEIVED by current_user
    received_requests = Friends.query.filter_by(requested_id=current_user.user_id, isAccepted="False").all()
    myids = []
    for req in received_requests:
        sender = Signup.query.filter_by(user_id=req.user_id).first()
        myids.append(sender)
    return render_template("profile.html", userdata=userdata, myids=myids)


# Edit Your Profile Function
@app.route("/editprofile/<int:id>",methods=['GET','POST'])
@login_required
def editprofile(id):
    userdata=Signup.query.filter_by(user_id=id).first()
    return render_template("editprofile.html",userdata=userdata)

# Update Profile Function
@app.route("/updateprofile/<int:id>", methods=['GET','POST'])
@login_required
def updateprofile(id):
    userdata = Signup.query.filter_by(user_id=id).first()

    if request.method == "POST":

        firstName = request.form['fname']
        lastName = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']

        # Validate phone number
        if len(phone) != 10:
            flash("Phone number should be a 10-digit number!", "warning")
            return redirect(url_for("editprofile", id=id))

        # Check if file is uploaded
        file = request.files.get('profile')

        if file and file.filename != "":
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Update with image
                userdata.first_name = firstName
                userdata.last_name = lastName
                userdata.email = email
                userdata.phone = phone
                userdata.profileimage = filename
            else:
                flash("Invalid file format!", "danger")
                return redirect(url_for("editprofile", id=id))
        else:
            # Update without image
            userdata.first_name = firstName
            userdata.last_name = lastName
            userdata.email = email
            userdata.phone = phone

        db.session.commit()
        flash("Profile Updated Successfully!", "success")
        return redirect(url_for("profile"))

    return render_template("editprofile.html", userdata=userdata)

# About Page
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact/",methods=['GET','POST'])
def contact():
    if request.method=="POST":
        email=request.form.get("email")
        description=request.form.get("description")
        query=Contact(email=email,description=description)
        db.session.add(query)
        db.session.commit()
        flash("We Will Get Back To You Soon..","success")
    return render_template("contact.html")

# Logout Function
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out Successfully!","primary")
    return redirect(url_for("login"))

#Testing database
@app.route("/test/")
def test():
    try:
        sql_query = "SELECT * FROM socialmedia"
        with db.engine.begin() as conn:
            response = conn.exec_driver_sql(sql_query).all()
            # print(response)
        return "Database is connected"
    except Exception as e:
        return f"Database is not connected, {e}"