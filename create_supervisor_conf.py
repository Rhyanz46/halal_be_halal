import os

folder_supervisor = "/etc/supervisor/conf.d"
config = '[program:be_halal_be_halal]' \
         '\ndirectory={}' \
         '\ncommand={}/env/bin/gunicorn -w 4 wsgi:app -b localhost:3000' \
         '\nautostart=true' \
         '\nautorestart=true\n'.format(os.getcwd(), os.getcwd())

if os.path.isdir(folder_supervisor):
    try:
        supervisor_result = folder_supervisor + "/be_halal_be_halal.conf"
        f = open(supervisor_result, "w")
        f.write(config)
        f.close()
        print("success to write " + supervisor_result)
    except:
        print("error to write " + supervisor_result)
else:
    print("supervisor for this service is not running")
    print("make sure you supervisor is installed...!!!")
