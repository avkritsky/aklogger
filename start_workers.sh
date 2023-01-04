pip install --upgrade pip >/dev/null 2>&1
pip install --no-cache-dir --root-user-action=ignore -r /var/www/html/requirements.txt
cp /var/www/html/src/entrypoints/workers.py /var/www/html/workers.py
python /var/www/html/workers.py
tail -f /dev/null