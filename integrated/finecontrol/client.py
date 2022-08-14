import bluepy.btle as btle
p = btle.Peripheral("c9:0a:c6:85:3f:18")
services=p.getServices()
s = p.getServiceByUUID(list(services)[2].uuid)
c = s.getCharacteristics()[0]
c.write(bytes("2", "utf-8"))
p.disconnect()