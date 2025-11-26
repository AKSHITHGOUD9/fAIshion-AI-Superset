# superset-stack/superset_config.py

# 1. Tell Superset to trust the Ngrok headers (Fixes the redirect/SSL issues)
ENABLE_PROXY_FIX = True

# 2. Disable strict HTTPS enforcement
TALISMAN_ENABLED = False

# 3. Disable CSRF protection (Essential for Ngrok tunnels to work)
WTF_CSRF_ENABLED = False

# 4. Allow the database to be added (just in case)
PREVENT_UNSAFE_DB_CONNECTIONS = False