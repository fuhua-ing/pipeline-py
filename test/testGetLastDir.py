import urllib2


def getCounterCode(url, pipelineId):
    resp = urllib2.urlopen(url + '?pipelineId=' + pipelineId)
    print resp.code
    data = resp.read()
    print 'The counter num is :'
    print data
    return data


cont = getCounterCode(url='http://192.168.136.158:8080/deploy/getCounterCode', pipelineId='dac')
print type(cont)
print cont.strip()