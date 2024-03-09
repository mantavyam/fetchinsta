# first install this:
# pip install instaloader

import instaloader
import os

def download_instagram_posts(username, target_folder):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Retrieve the profile of the given username
        profile = instaloader.Profile.from_username(loader.context, username)

        # Create target folder if it doesn't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        # Iterate over each post and download it
        for post in profile.get_posts():
            loader.download_post(post, target_folder)
        
        print("All posts downloaded successfully.")

    except instaloader.exceptions.ProfileNotExistsException:
        print("The specified Instagram user does not exist.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    username = input("Enter the username of the Instagram account (format: @username): ")
    target_folder = input("Enter the location to save the files: ")

    download_instagram_posts(username[1:], target_folder)  # remove "@" symbol from username


