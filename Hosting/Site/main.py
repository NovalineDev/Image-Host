from http.client import REQUEST_URI_TOO_LONG
from random import randint
from types import MethodDescriptorType
from typing import Type
from flask import *
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import render_template
from matplotlib.style import use

import requests
from PIL import Image
from discord_webhook import DiscordWebhook
import os
from os.path import splitext
import json
import time
import datetime

import random
import string

from threading import Thread

# Custom Functions
from functions.imageHostv2 import *

domain = getDomain()

app = Flask(__name__,
            static_url_path='',
            static_folder='web',
            template_folder='web'
            )

def sizeof_fmt(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

# image host v2
@app.route("/api/v2/upload", methods=["POST"])
def imageHostv2_Upload():
    # Check if the method is post
    if request.method == 'POST':
        # Get the information linked with the ID given with the request from the databse
        userInfo = requestDataWithID(request.form.to_dict(flat=False)['user_id'][0])
        # Check if it's equal to 404
        if(userInfo == 404):
            return "don't even try", 404
        # Check if the private key matches
        if request.form.to_dict(flat=False)['secret_key'][0] == userInfo["privateKey"]:
            # Get file object from POST request, extract and define needed variables for future use
            file = request.files['image']
            extension = splitext(file.filename)[1]
            file.flush()
            size = os.fstat(file.fileno()).st_size
            # Checking the file extention
            if extension not in ['.png', '.jpeg', '.jpg', '.gif']:
                return 'File type is not supported', 415
            # Check if the file is too large, limit = 15 mb
            elif size > 15000000:
                return 'File size too large', 400
            # Storing the file in the correct location
            else:
                letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
                filename = ''.join(random.choice(letters) for i in range(7))
                savedFileLocation = os.path.join(f"/home/Hosting/Site/web/UploadCache", userInfo["userName"], filename + extension)
                file.save(savedFileLocation)
                domain = userInfo["domain"]

                # Removing the MetaData to prtect user's privacy
                if extension != ".gif":
                    print(os.popen(f"exif_delete --replace {savedFileLocation}").read())

                # Sending a post request for logs in the Discord server
                requests.post("put your log webhook here", data={"content": f"A new file has been uploaded, size: {sizeof_fmt(size)}."})
                return json.dumps({"domain": getDomain(),"filename": filename, "extension": extension}), 200
        
        else:
            return 'Unauthorized use', 401

    else:
        return "no"

@app.route('/i/<filename>')
def imageHostv2_Embed(filename):
    filelist = []
    uploadCachePath = "/home/Hosting/Site/web/UploadCache"

    for root, dirs, files in os.walk(uploadCachePath):
        for file in files:
            filelist.append(os.path.join(root, file))

    for name in filelist:
        splitName = name.split("/")
        if splitName[7] == filename:
            foundFile = splitName[5] + "/" + splitName[6] + "/" + filename
            sitename = "Upload"

            # All known info
            uploader = splitName[6]
            settingsJson = requestDataWithUserName(uploader)
            embedDisabled = settingsJson["embedDisabled"]
            embedColor = settingsJson["embedColor"]
            embedTitle = settingsJson["embedTitle"]
            embedSmallText = settingsJson["embedSmallText"]
            embedDescription = settingsJson["embedDescription"]

            embedTitle = embedTitle.replace("%1%", '"') # %1% = "
            embedTitle = embedTitle.replace("%2%", "’") # %2% = ’

            embedDescription = embedDescription.replace("%1%", '"') # %1% = "
            embedDescription = embedDescription.replace("%2%", "’") # %2% = ’

            embedSmallText = embedSmallText.replace("%1%", '"') # %1% = "
            embedSmallText = embedSmallText.replace("%2%", "’") # %2% = ’

            fileName = filename
            foundFile = foundFile

            # if someone ever reads this, stfu it works :)
            if(embedDisabled == "True"):
                return f"""
                <title>{sitename} - {fileName}</title>
                <link rel="stylesheet" href="https://{domain}/secure/imageUploader.css">
                <meta name="og:image" itemprop="image" content="https://{domain}/{foundFile}">
                <meta name="twitter:card" content="summary_large_image">
                <div class="container">
                    <h1 class="info">Hi, this file was uploaded by {uploader}.</h1>
                    <img src='https://{domain}/{foundFile}' class="image">
                </div>
                """
            else:
                # only og image == embedless image
                return f"""
                <title>{sitename} - {fileName}</title>
                <link rel="stylesheet" href="https://{domain}/secure/imageUploader.css">
                <meta property="og:site_name" content='{embedSmallText}'>
                <meta name="theme-color" content="#{embedColor}" >
                <meta content='{embedDescription}' property="og:description">
                <meta property="og:title" content='{embedTitle}'>
                <meta name="og:image" itemprop="image" content="https://{domain}/{foundFile}">
                <meta name="twitter:card" content="summary_large_image">
                <div class="container">
                    <h1 class="info">Hi, this file was uploaded by {uploader}.</h1>
                    <img src='https://{domain}/{foundFile}' class="image">
                </div>
                """

    return f'''
	    <title>File not found</title>
        <link rel="stylesheet" href="https://{domain}/secure/imageUploader.css">
        <meta property="og:title" content='File not found.'>
	    <div class="container">
	   	    <h1 class="error">File not found, looks like you reached a dead end.</h1>
            <img src='https://{domain}/UploadCache/Admin/NIH.png' class="image">
        </div>
	   '''

# add # with random int
@app.route("/api/v2/preview/<user>")
def imageHostv2_embedPreview(user):
    # All known info
    try:
        domain = getDomain()

        settingsJson = requestDataWithUserName(user)
        embedDisabled = settingsJson["embedDisabled"]
        embedColor = settingsJson["embedColor"]
        embedTitle = settingsJson["embedTitle"]
        embedSmallText = settingsJson["embedSmallText"]
        embedDescription = settingsJson["embedDescription"]

        embedTitle = embedTitle.replace("%1%", '"') # %1% = "
        embedTitle = embedTitle.replace("%2%", "’") # %2% = ’

        embedDescription = embedDescription.replace("%1%", '"') # %1% = "
        embedDescription = embedDescription.replace("%2%", "’") # %2% = ’

        embedSmallText = embedSmallText.replace("%1%", '"') # %1% = "
        embedSmallText = embedSmallText.replace("%2%", "’") # %2% = ’
        
        sitename = "Upload"
        foundFile = "UploadCache/Admin/NIH.png"
        uploader = settingsJson["userName"]

        # if someone ever reads this, it works :)
        if(embedDisabled == "True"):
            return f"""
                <title>{sitename} - Test Embed</title>
                <link rel="stylesheet" href="https://{domain}/secure/imageUploader.css">
                <meta name="og:image" itemprop="image" content="https://{domain}/{foundFile}">
                <meta name="twitter:card" content="summary_large_image">
                <div class="container">
                    <h1 class="info">Hi, this file was uploaded by {uploader}.</h1>
                    <img src='https://{domain}/{foundFile}' class="image">
                </div>
                """
        else:
                # only og image == embedless image
            return f"""
                <title>{sitename} - Test Embed</title>
                <link rel="stylesheet" href="https://{domain}/secure/imageUploader.css">
                <meta property="og:site_name" content='{embedSmallText}'>
                <meta name="theme-color" content="#{embedColor}" >
                <meta content='{embedDescription}' property="og:description">
                <meta property="og:title" content='{embedTitle}'>
                <meta name="og:image" itemprop="image" content="https://{domain}/{foundFile}">
                <meta name="twitter:card" content="summary_large_image">
                <div class="container">
                    <h1 class="info">Hi, this file was uploaded by {uploader}.</h1>
                    <img src='https://{domain}/{foundFile}' class="image">
                </div>
                """

    except Exception:
        return f'''<title>User not found</title>
        <link rel="stylesheet" href="https://{domain}/secure/imageUploader.css">
        <meta property="og:title" content='User not found.'>
	    <div class="container">
	   	    <h1 class="error">User not found.</h1>
            <img src='https://{domain}/UploadCache/Admin/NIH.png' class="image">
        </div>
	   '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=80) # Port 80 because default http port
