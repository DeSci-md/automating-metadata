import os
from supabase import create_client
from datetime import datetime, timedelta

url = os.getenv("SUPABASE_URL") # from your `.env` file
key = os.getenv("SUPABASE_KEY")
supabase = create_client(url, key)
res = supabase.storage().from_('images').list()

created_at = datetime.utcnow() # - timedelta(hours=2)
# data = supabase.table('todos').insert({'name':'Todo 3', "created_at": str(created_at)}).execute()
data = supabase.table('todos').update({'name': 'Todo 2.0'}).eq('id', 2).execute()
data = supabase.table('todos').delete().eq('id', 3).execute()
data = supabase.table('todos').select('*').execute()
print(data)