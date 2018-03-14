import os

from python.release.jdd_release_common import code_path, pared_pom_xml

print 'start to find pom.xml'
p = os.popen('cd ' + code_path + ' && find ' + code_path + ' -name "pom.xml"')
str_line = list()
for line in p.readlines():
    line = line.strip()
    if not len(line):
        continue
    str_line.append(line)
print str_line
for file_name in str_line:
    pared_pom_xml(file_name)

print 'end of change snapshot'
