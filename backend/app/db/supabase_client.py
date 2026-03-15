
"""
Supabase database client for Luminara
"""

from supabase import create_client
from core.config import settings

# Create Supabase client
supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)
