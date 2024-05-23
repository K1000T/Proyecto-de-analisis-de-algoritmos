import instaloader
import json
import re
import time


def extract_shortcode(instagram_url):
    pattern = r"(?:https?://)?(?:www\.)?(?:instagram\.com(?:/\w+)?/p/)([\w-]+)(?:/)?(\?.*)?$"
    match = re.match(pattern, instagram_url)

    if match:
        shortcode = match.group(1)
        return shortcode
    else:
        return "Invalid Instagram URL"


def get_post_info(short_code):
    L = instaloader.Instaloader()
    L.login("fawolot216", "fawolot216-2024")
    try:
        post = instaloader.Post.from_shortcode(L.context, short_code)        
        comments = []
        contador_comentarios = 0
        for comment in post.get_comments():            
            contador_comentarios += 1            
            current_comment = {
                'user' : comment.owner.username,
                'text' : comment.text,
                'timestamp' : comment.created_at_utc.strftime('%Y-%m-%d %H:%M'),
                'likes' : comment.likes_count
            }            
            comments.append(current_comment)            
            if contador_comentarios == 30:
                break
            if contador_comentarios//10 == 0:
                time.sleep(5)     
        post_info = {
            'shortcode': post.shortcode,
            'owner': post.owner_username,
            'caption': post.caption,
            'likes': post.likes,
            'comments': comments
        }
        return post_info

    except instaloader.exceptions.ConnectionException:
        print("Error: Connection error. Retrying...")
        time.sleep(120)
        return get_post_info(short_code)
        


def get_user_posts(username):
    L = instaloader.Instaloader()
    L.login("hoyiro8829", "hoyiro8829-2024")  # (login)
    profile = instaloader.Profile.from_username(L.context, username)
    
    try:                 
        posts = []
        contador = 0
        
        for post in profile.get_posts():
            if contador == 15:
                break
            contador += 1
            if contador // 5 == 0:
                time.sleep(20)
                
            shortcode = post.shortcode,
            owner = post.owner_username,
            caption = post.caption,
            likes = post.likes,
            comments = []
            contador_comentarios = 0
            
            for comment in post.get_comments():            
                contador_comentarios += 1            
                current_comment = {
                    'user' : comment.owner.username,
                    'text' : comment.text,
                    'timestamp' : comment.created_at_utc.strftime('%Y-%m-%d %H:%M'),
                    'likes' : comment.likes_count
                }            
                comments.append(current_comment)            
                if contador_comentarios == 30:
                    break
                if contador_comentarios//10 == 0:
                    time.sleep(5)
                    
            post_info = {
                'shortcode': shortcode,
                'owner': owner,
                'caption': caption,
                'likes': likes,
                'comments': comments
            }
            
            posts.append(post_info)
        return posts 
    except instaloader.exceptions.ConnectionException:
        print("Error: Connection error. Retrying...")
        time.sleep(120)
        return get_user_posts(username)
    
    
    
    
    


"""

# Leer la primera URL del archivo
with open('urls_publicaciones.txt', 'r') as f:
    post_url = f.readline().strip()

# Extraer el shortcode
shortcode = extract_shortcode(post_url)

# Obtener información del post
post_info = get_post_info(shortcode)

# Guardar el diccionario JSON en un archivo
with open('post_info.json', 'w') as f:
    json.dump(post_info, f, indent=4)

print(f'Información del post guardada en post_info.json')

def main():
    username = 'gustavopetrourrego'

    shortcodes = get_user_posts(username) #Obtener los shortcode de los posts del usuario

    infoposts = []

    for shortcode in shortcodes:
        post_info = get_post_info(shortcode)#Obtener la info del post
        infoposts.append(post_info)

    with open('posts.json', 'w') as f:
        json.dump(infoposts, f, indent=4)

"""


def main():
    username = 'gustavopetrourrego'    
    
    infoposts = get_user_posts(username)

    with open('posts.json', 'w') as f:
        json.dump(infoposts, f, indent=4)

    

main()
