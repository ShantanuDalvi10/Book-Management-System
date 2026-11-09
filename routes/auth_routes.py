from flask import Blueprint, current_app, flash, render_template, redirect, url_for,request
from flask_login import login_required, login_user, logout_user
from services.auth_services import register_user,authenticate_user

auth = Blueprint("auth",__name__)

@auth.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username","").strip()
        password = request.form.get("password","")
        confirm_password = request.form.get("confirm_password","")

        try:
            register_user(username=username,password=password,
                          confirm_password=confirm_password)
            flash("Registration Successful","success")
            return redirect(url_for("auth.login"))
        except ValueError as error:
            flash(str(error),"error")
        except Exception:
            current_app.logger.exception("Registration Failed")
            flash("Registration Failed","error")

    return render_template("register.html")

@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        try:
            user = authenticate_user(username=username,password=password)
            login_user(user)
            flash("Login is successful.","success")
            return redirect(url_for("dash.dashboard"))
        except ValueError as error:
            flash(str(error),"error")
        except Exception:
            current_app.logger.exception("User couldn't logged in.")
            flash("User couldn't logged in.","error")
    return render_template("login.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("User is successfully logged out.","success")
    return redirect(url_for("auth.login"))