from flask import Flask
from flask import render_template, redirect, request, url_for
import sqlite3
from datetime import datetime
from __init__ import app, db
# импорт модулей
from models import Polls,Choice


@app.route('/',methods=['GET'])
def polls():
    question = Polls.query.all()
    return render_template('polls.html',question=question)


@app.route('/choice/<int:id>',methods=['GET','POST'])
def choice(id):
    choices = Choice.query.filter_by(question_id=id)
    question = Polls.query.get_or_404(id)
    if request.method == 'POST':
        conn = sqlite3.connect("polls.db")
        c = conn.cursor()
        choice_key = request.form['choice']
        print(choice_key)
        # choice_id = request.form['id']
        c.execute("SELECT votes FROM choice WHERE choice_id=? AND question_id=?",(choice_key,id))
        votes = c.fetchall()
        votes = votes[0][0]+1
        print(votes)
        c.execute("UPDATE choice set votes=? WHERE choice_id=? and question_id=?",(votes,choice_key,id))
        conn.commit()
        return redirect("/")
    elif request.method == 'GET':
        return render_template('choice.html',choices=choices,question=question)


@app.route("/result/<int:id>/",methods=['GET'])
def result(id):
    question = Polls.query.get_or_404(id)
    results = Choice.query.filter_by(question_id=id)
    return render_template("results.html",question=question,results=results)


if __name__=="__main__":
    app.run(debug=True)
