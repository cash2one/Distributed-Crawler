from Dao.redisClient import RedisClient
from GetProxy.GetFreeProxy import FreeProxy


class ProxyManager(object):
    def __init__(self):
        self.db = RedisClient('proxy', 'localhost', 6379)
        self.raw_proxy_queue = 'raw_proxy'
        self.useful_proxy_queue = 'useful_proxy'

    def refresh(self):

        self.db.deleteAll('proxy')
        self.db.deleteAll('raw_proxy')
        self.db.deleteAll('useful_proxy')
        proxy_set = set()

        for proxy in FreeProxy().getFirstFreeProxy():
            if proxy.strip():
                proxy_set.add(proxy.strip())


        for proxy in FreeProxy().getSecondFreeProxy():
            if proxy.strip():
                proxy_set.add(proxy.strip())



        self.db.changeName(self.raw_proxy_queue)
        for proxy in proxy_set:
            self.db.put(proxy)


    def get(self):
        self.db.changeName(self.useful_proxy_queue)
        return self.db.get()

    def delete(self, proxy):
        self.db.changeName(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        self.db.changeName(self.raw_proxy_queue)
        return self.db.getList()

    def getNum(self):
        self.db.changeName(self.raw_proxy_queue)
        total_raw_proxy = self.db.getNumber()
        self.db.changeName(self.useful_proxy_queue)
        total_useful_proxy = self.db.getNumber()

        return {
            'raw_proxy_num': total_raw_proxy,
            'useful_proxy_num': total_useful_proxy,
        }


if __name__ == "__main__":
    pp = ProxyManager()
    pp.refresh()
    print(pp.getNum())