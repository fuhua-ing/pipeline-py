servers = []
server_num=1
if server_num > 0:
    for n in range(1, server_num + 1, 1):
        i = str(n)
        server_info = str("root:45.5465.5646:23").split(":")
        ip = str(server_info[1])
        port = str(server_info[2])
        user = str(server_info[0])
        passwd = "asdf"
        env_info_dict = {'ip': ip, 'port': port, 'user': user, 'passwd': passwd}
        servers.append(env_info_dict)

print servers
print len(servers)


server_num = int(os.getenv('SERVER_NUM'))
servers = []
if server_num > 0:
    for n in range(1, server_num + 1, 1):
        i = str(n)
        server_info = str(os.getenv('SERVER_' + i)).split(":")
        ip = str(server_info[1])
        port = str(server_info[2])
        user = str(server_info[0])
        passwd = os.getenv('SERVER_PASSWD_' + i)
        env_info_dict = {'ip': ip, 'port': port, 'user': user, 'passwd': passwd}
        servers.append(env_info_dict)

print servers
pool = threadpool.ThreadPool(multiprocessing.cpu_count())
requests = threadpool.makeRequests(dowork, servers)
for req in requests:
    pool.putRequest(req)
pool.wait()