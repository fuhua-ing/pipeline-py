# volume = '/a:/s'
# for v in volume.split(','):
#     print v

paramter_ports = '456:4654,464:469'

port_line = ''
for port in paramter_ports.split(','):
    print port
    port_line = port_line + '"' + port.split(':')[1] + '/tcp"' + ':' + '[{"HostPort":' + '"' + port.split(
        ':')[0] + '"' + '}],'
print port_line
