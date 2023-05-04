import os
from supabase import create_client
from datetime import datetime, timedelta
from gotrue.exceptions import APIError

url = os.getenv("SUPABASE_URL") # from your `.env` file
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)

# Creating an account
email: str = ''
password: str = ''
# user = supabase.auth.sign_up(email = email, password = password)

# Authentication
session = None
try:
    session = supabase.auth.sign_in(email = email, password = password)
    supabase.postgrest.auth(session.access_token) # authenticate the client (which has RLS)
except APIError:
    print("Authentication failed")

resp = supabase.storage().from_('images').get_public_url('cebdc7a2-d8af-45b3-b37f-80f328ff54d6/69893963-c755-4a46-802b-b729c5482cd5')
print(resp)

# Upload image/file
#resp = supabase.storage().from_('images').upload('auth.py', 'auth.py', {'content-type': 'image/jpeg'})
res = supabase.storage().from_('avatars').list()
data = supabase.table('profiles').select('*').execute()
print("")
print(res)
print("")
print(session.user.id)
print('')
res = supabase.storage().from_('images').download('cebdc7a2-d8af-45b3-b37f-80f328ff54d6/69893963-c755-4a46-802b-b729c5482cd5')

supabase.auth.sign_out()