import instaloader
import os
import sys

def download_instagram_posts(username, target_folder, download_videos=False):
    # Create an instance of Instaloader
    loader = instaloader.Instaloader()

    try:
        # Retrieve the profile of the given username
        profile = instaloader.Profile.from_username(loader.context, username)

        # Create target folder if it doesn't exist
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        print("Downloading posts...")

        # Iterate over each post
        for post in profile.get_posts():
            if post.is_video and not download_videos:
                continue  # Skip downloading videos if download_videos is set to False

            # Create directory for carousel posts
            if post.typename == 'GraphSidecar':
                carousel_folder = os.path.join(target_folder, f"{post.owner_username}_carousel_{post.shortcode}")
                os.makedirs(carousel_folder, exist_ok=True)

            # Download post
            try:
                loader.download_post(post, target=target_folder)
            except Exception as e:
                print(f"Error downloading post {post.shortcode}: {e}")

        print("All posts downloaded successfully.")

    except instaloader.exceptions.ProfileNotExistsException:
        print("The specified Instagram user does not exist.")
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    username = input("Enter the username of the Instagram account (format: @username): ")
    target_folder = input("Enter the location to save the files: ")
    download_videos = input("Do you want to download videos? (yes/no): ").lower() == 'yes'

    download_instagram_posts(username[1:], target_folder, download_videos)
