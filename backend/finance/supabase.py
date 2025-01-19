from supabase import create_client
from django.conf import settings

supabase = create_client(
    supabase_url=settings.SUPABASE_URL, supabase_key=settings.SUPABASE_KEY
)
