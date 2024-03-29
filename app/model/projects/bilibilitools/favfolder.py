from urllib import request
import json,time


rplchrdict_unix = {"/": "-",
             "\\": "-",
             ":": "-",
             "*": "-",
             "?": "-",
             "<": "-",
             ">": "-",
             "|": "-",
             "：" : "-",
             "\"" : "-",
             "→" : "-",
             " " : "' '",
             "&" : "-",
             "'" : "\"'\"",
             "(" : "-",
             ")" : "-"
            }

rplchrdict_windows = {"/": "-",
             "\\": "-",
             ":": "-",
             "*": "-",
             "?": "-",
             "<": "-",
             ">": "-",
             "|": "-",
             "：" : "-",
             "\"" : "-",
             "→" : "-",
             "&" : "-",
            }

unicdchr = {"\\u0026": "&",
              "\\u003c" : "<",
              "\\u003e" : ">"}


def rplchr(s,opsys) :
    if opsys == "Windows":
        chrdict = rplchrdict_windows
    else:
        chrdict = rplchrdict_unix

    newstr = ""
    for i in range(len(s)):
        if s[i] in chrdict:
            newstr += chrdict[s[i]]
        else:
            newstr += s[i]
    if s[0] == "-":
        s = "rmv"+s
    return newstr

def unicdefmt(s):
    for key, value in unicdchr.items():
        s = s.replace(key, value)
    return s


class favfolder(object):
    def __init__(self,media_id,ps = 20):
        self.__media_id = media_id
        self.__ps = ps
        self.__apiurl = "https://api.bilibili.com/medialist/gateway/base/spaceDetail?media_id=%s&ps=%s&pn=%s" % (self.__media_id, self.__ps, "%s")
        if self.isValid():
            self.__data = self.reqData()
        else:
            self.__data = []

    @classmethod
    def initFromLink(cls,favlink):
        parameters = favlink[favlink.find("?", 0) + 1::].split("&")
        media_id = ""
        for para in parameters:
            if "fid" in para:
                media_id = para[4::]
        if not media_id.isdigit():
            media_id = ""
        return cls(media_id)

    def isValid(self):
        if len(self.__media_id) == 0:
            return False
        else:
            return True

    def isNone(self):
        if len(self.__data) == 0:
            return True
        else:
            return False

    def getNumVideo(self):
        return len(self.__data)


    def getData(self,ps=20):
        parsedlist = [[] for i in range((self.getNumVideo() - 1) // ps + 1)]
        for i in range(self.getNumVideo()):
            parsedlist[i // ps].append(self.__data[i])
        return parsedlist


    def reqData(self):
        def tryget(wholeurl):
            try:
                wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
                jsondata = json.loads(wholeHTML)
            except:
                time.sleep(3)
                while True:
                    try:
                        wholeHTML = request.urlopen(wholeurl).read().decode("utf-8")
                        jsondata = json.loads(wholeHTML)
                        break
                    except:
                        time.sleep(3)
            return jsondata

        data = []
        pn = 1
        while True:
            wholeurl = self.__apiurl % pn

            jsondata = tryget(wholeurl)
            code = jsondata["code"]
            if code != 0:
                return []
            if not "data" in jsondata.keys():
                return []
            else:
                while not "data" in jsondata.keys():
                    jsondata = tryget(wholeurl)

            if jsondata["data"]["info"]["media_count"] == 0:
                break
            medias = jsondata["data"]["medias"]

            for item in medias:
                data.append({"aid": str(item["id"]),
                             "title": unicdefmt(str(item["title"])),
                             "pic": str(item["cover"]),
                             "state": str(item["attr"]),
                             "mid": str(item["upper"]["mid"]),
                             "upname": str(item["upper"]["name"])})

            pn +=1
        return data
