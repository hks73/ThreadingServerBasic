Firstly



45 is a global key used basic authentication

---> Run Server using command line
      python3 mine_what.py

now in another terminals run :
 curl -H "Authorization:Basic 45" -X GET 'localhost:8012?delay=1&increment=1'


 second terminal:

 curl -H "Authorization:Basic 45" -X GET 'localhost:8012?delay=10&increment=1'


if You want to change the port name then you can go to a file change the server name.
