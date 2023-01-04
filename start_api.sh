pip install --upgrade pip >/dev/null 2>&1
pip install --no-cache-dir --root-user-action=ignore -r /var/www/html/requirements.txt
python -m aiohttp.web -H 0.0.0.0 -P 7007 src.entrypoints.api_app:init