# test_config.py

from fa_passkeys.config import settings

print("Database URI:", settings.db_uri)
print("Database Name:", settings.db_name)
print("Relying Party Name:", settings.rp_name)
print("Relying Party ID:", settings.rp_id)
print("Origin:", settings.origin)
print("Logging Level:", settings.logging_level)
print("Admin Username:", settings.admin_username)
