import { createClient } from '@supabase/supabase-js';
import Moralis from 'moralis/.';

const supabaseUrl = "https://qwbufbmxkjfaikoloudl.supabase.co";
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Njk5NDE3NTksImV4cCI6MTk4NTUxNzc1OX0.RNz5bvsVwLvfYpZtUjy0vBPcho53_VS2AIVzT8Fm-lk";
const supabaseServiceRole = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3YnVmYm14a2pmYWlrb2xvdWRsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY2OTk0MTc1OSwiZXhwIjoxOTg1NTE3NzU5fQ.YEicNFgQ3DolbXQVBRMrbqoJS3qLDEf5TKJ8dphZRRc"
export const supabase = createClient(supabaseUrl, supabaseServiceRole);

Moralis.start({
    apiKey: 'kJfYYpmMmfKhvaWMdD3f3xMMb24B4MHBDDVrfjslkKgTilvMgdwr1bwKUr8vWdHH'
});