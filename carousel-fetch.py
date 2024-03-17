import os
import time
import pandas as pd
from instaloader import Instaloader, Post
from instaloader.exceptions import QueryReturnedBadRequestException

# Credentials
username = "alofrutcc"
password = "SECURE@alo24"
excel_file = r"E:\clubhouse\mega-plan\DOWNLOAD-Posts-IG.xlsx"

# Create main directory
main_directory = "./InstagramPosts"
os.makedirs(main_directory, exist_ok=True)

# Function to authenticate Instaloader
def authenticate_instaloader():
    L = Instaloader()
    try:
        L.load_session_from_file(username)
    except FileNotFoundError:
        L.context.log("Session file does not exist yet - Logging in.")
    if not L.context.is_logged_in:
        try:
            L.context.log("Logging in.")
            L.login(username, password)
            L.save_session_to_file()
            print("Instaloader login successful")
        except QueryReturnedBadRequestException:
            print("Instaloader login failed. Retrying in 10 seconds...")
            time.sleep(10)
            authenticate_instaloader()
            return
    return L

# Authenticate Instaloader
L = authenticate_instaloader()

# Load excel file
try:
    df = pd.read_excel(excel_file)
except FileNotFoundError:
    print("Excel file not found.")
    exit()

# Function to download post
def download_post(post_url, index):
    post = Post.from_shortcode(L.context, post_url.split("/")[-2])
    folder_name = os.path.join(main_directory, f"{post.owner_username}_{post.date.strftime('%Y-%m-%d')}")
    os.makedirs(folder_name, exist_ok=True)
    try:
        if not post.is_video:
            L.download_post(post, target=folder_name)
            print(f"Downloaded URL {index} type: successful at {folder_name}")
        else:
            print(f"Downloaded URL {index} type: failed. Not an image.")
    except Exception as e:
        print(f"Downloaded URL {index} type: failed. Error: {e}")

# Download posts
for index, row in df.iterrows():
    post_url = row['Link']
    download_post(post_url, index+1)
    if (index+1) % 30 == 0:
        print("Taking long delay of 30s")
        time.sleep(30)
    else:
        print("Taking 10s gap")
        time.sleep(10)
