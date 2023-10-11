import os
from os.path import join, dirname
from dotenv import load_dotenv

from http import client
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("mongodb://ilham10ihsan:1lh4m1h54n@ac-qpbduu1-shard-00-00.uobexa5.mongodb.net:27017,ac-qpbduu1-shard-00-01.uobexa5.mongodb.net:27017,ac-qpbduu1-shard-00-02.uobexa5.mongodb.net:27017/?ssl=true&replicaSet=atlas-11enlv-shard-0&authSource=admin&retryWrites=true&w=majority")
DB_NAME =  os.environ.get("dbsparta")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('Movie.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    image = og_image['content']
    title = og_title['content']
    desc = og_description['content']
    doc ={
        'image': image,
        'title' : title,
        'description':desc,
        'star':star_receive,
        'comment':comment_receive
    }
    db.movies.insert_one(doc)

    return jsonify({'msg':'POST request!'})

@app.route("/movie", methods=["GET"])
def movie_get():
    movie_list = list(db.movies.find({},{'_id':False}))
    return jsonify({'movies':movie_list})

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
