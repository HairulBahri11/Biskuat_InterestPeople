from instaloader import instaloader, Profile
import os
import time


def ambil_foto(username):
    pathku = 'static/' + username
    L = instaloader.Instaloader(download_pictures=True, download_videos=False, download_comments=False,
                                    save_metadata=False, download_video_thumbnails=False, download_geotags=False,  post_metadata_txt_pattern='' , dirname_pattern=pathku , filename_pattern=username)
    # L.interactive_login(username)
    PROFILE = username
    profile = Profile.from_username(L.context, PROFILE)

    posts_sorted_by_likes = sorted(
            profile.get_posts(), key=lambda post: post.date, reverse=True)

    i = 1
    
    for post in posts_sorted_by_likes:
        
        L.download_post(post, PROFILE)
        
        if i == 5:
            break
        i += 1 

   
   
    