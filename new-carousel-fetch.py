import os
import time
import pandas as pd
from instaloader import Instaloader, Post
from instaloader.exceptions import QueryReturnedBadRequestException, ConnectionException

# Credentials
username = "USERNAME"
password = "PWD"
excel_file = r"E:\LOCATION.xlsx"

# Create main directory
main_directory = "./InstagramPosts"
os.makedirs(main_directory, exist_ok=True)

def delete_old_session():
    try:
        os.remove(f"{username}.session")
    except FileNotFoundError:
        pass

def login_instaloader():
    delete_old_session()
    L = Instaloader()
    try:
        L.context.log("Logging in.")
        L.login(username, password)
        L.save_session_to_file()
        print("Instaloader login successful")
    except QueryReturnedBadRequestException:
        print("Instaloader login failed")
    return L

# Function to download post
def download_post(post_url, index, L):
    try:
        post = Post.from_shortcode(L.context, post_url.split("/")[-2])
        folder_name = os.path.join(main_directory, f"{post.owner_username}_{post.date.strftime('%Y-%m-%d')}")
        os.makedirs(folder_name, exist_ok=True)
        if not post.is_video:
            L.download_post(post, target=folder_name)
            print(f"Downloaded URL {index} type: successful at {folder_name}")
        else:
            print(f"Downloaded URL {index} type: failed. Not an image.")
    except ConnectionException as e:
        print(f"Downloaded URL {index} type: failed. Error: {e}")
        if "429" in str(e):
            wait_time = 20 * 60  # Wait for 20 minutes
            print(f"Too many requests. Pausing downloads. Will continue at {time.strftime('%H:%M', time.localtime(time.time() + wait_time))}")
            time.sleep(wait_time)
            download_post(post_url, index, L)  # Retry the download
    except Exception as e:
        print(f"Downloaded URL {index} type: failed. Error: {e}")

# Main function
def main():
    # Login to Instaloader
    L = login_instaloader()

    # Load excel file
    try:
        df = pd.read_excel(excel_file)
    except FileNotFoundError:
        print("Excel file not found.")
        exit()

    # Download posts
    for index, row in df.iterrows():
        post_url = row['Link']
        download_post(post_url, index+1, L)
        if (index+1) % 11 == 0:
            print("Taking a 3 min break to avoid too many requests.")
            time.sleep(180)  # Take a 3 min break to avoid too many requests

if __name__ == "__main__":
    main()
