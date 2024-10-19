import random
import string
    

def gen_fakeurls(n):
    base_domains=['https://scikit-image.org/docs/stable/api/skimage.feature.html',
                 'https://scikit-image.org/docs/stable/api/skimage.color.html','https://github.com/','https://medium.com/@']
    
    all_urls=[]
    short_codes=set()

    while len(short_codes)<n:
        short_code=gen_unique_codes(5)
        short_codes.add(short_code)

    short_codes=list(short_codes)  # unique short_codes pregenerated and converted back to list
            
    for i in range(n):
        first_part=random.choice(base_domains)
        last_part=f'?param{gen_unique_codes(13)}' if first_part in base_domains[:2] else f'{gen_unique_codes(7)}'
        long_url=f'{first_part}{last_part}'
        short_code=short_codes[i]
        all_urls.append((long_url,short_code))
            
    return all_urls


def gen_unique_codes(length=5):
    chars=string.digits + string.ascii_letters
    return ''.join(random.choice(chars) for _ in range(length))