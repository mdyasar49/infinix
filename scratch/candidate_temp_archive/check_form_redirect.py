import requests

r = requests.get('https://docs.google.com/forms/d/1ugPH89EBC1RSVJrrHKs3qnYnyR3y5rXAVwK43wamthE/viewform', allow_redirects=True)
print('Redirected URL:', r.url)
