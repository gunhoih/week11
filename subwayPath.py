class Dijkstra:
    def __init__(self,nodes):
        self.nodes = set(nodes)
        self.g = {}
        self.dist = {}
        for node in nodes:
            self.g[node] = {}
            self.dist[node] = [float("inf"), "none"]

    def setEdge(self,a,b,w,bidirection=True):
        self.g[a][b] = w
        if bidirection == True: self.g[b][a] = w

    def _dicFilter(self, cost, nodes):
        import sys
        mini = sys.maxsize
        curNode = None
        for key, value in cost.items():
            if key in nodes:
                if value[0] < mini:
                    mini = value[0]
                    curNode = key
        return curNode

    def getPath(self,start,end):
        # 다시 검색할 때도 사용할 수 있도록 노드와 거리값을 초기화한다.
        nodes = self.nodes.copy()
        for node in nodes:
            self.dist[node] = [float("inf"), "none"]

        visits = set()
        curNode = start
        self.dist[curNode][0] = 0
        while True:
            visits.add(curNode)
            nodes.remove(curNode)
            neighbors = self.g[curNode]

            for node in neighbors:
                if min(self.dist[node][0], self.dist[curNode][0] + self.g[curNode][node]) < self.dist[node][0]:
                    self.dist[node][0] = min(self.dist[node][0], self.dist[curNode][0] + self.g[curNode][node])
                    self.dist[node][1] = curNode

            if curNode == end:
                break
            if len(nodes) > 0:
                curNode = self._dicFilter(self.dist, nodes)
                if curNode is None:
                    break
            else:
                break

        if self.dist[end][0] == float("inf"):
            return [], []

        path = [end]
        dist = []

        while end != start:
            path.append(self.dist[end][1])
            dist.append(self.dist[end][0])
            end = self.dist[end][1]

        return path[::-1], dist[::-1]


import csv
import folium  # pip install folium
from pathlib import Path


def loadSubway():
    # 기존 절대경로 대신 현재 파이썬 파일이 있는 폴더에서 csv를 읽는다.
    dataPath = Path(__file__).resolve().parent

    subwayLoc = {} # 지하철역 이름과 [위도, 경도] 딕셔너리 구성
    f = open(dataPath / 'subwayLocation.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)
    for line in rdr:
        if line[0] not in subwayLoc:
            subwayLoc[line[0]] = [float(line[1]), float(line[2])]
    f.close()

    f = open(dataPath / 'subway.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)
    # 지하철역간의 거리 데이터로 부터 역 집합을 만든다.
    nodes = set()
    for line in rdr:
        temp1 = line[0]
        temp2 = line[1]
        nodes.add(temp1)
        nodes.add(temp2)
    f.close()

    d = Dijkstra(nodes)

    f = open(dataPath / 'subway.csv', 'r', encoding='utf-8-sig')
    rdr = csv.reader(f)
    for line in rdr:
        d.setEdge(line[0], line[1], int(line[2])) # 역1, 역2 노드 소요시간 지정
    f.close()

    return nodes, subwayLoc, d


def drawMap(pathList, subwayLoc):
    pathNames = []
    pathLine = []
    xbar = 0
    ybar = 0
    for item in pathList:
        pathNames.append(item[:-3])
        xbar += subwayLoc[item[:-3]][0]
        ybar += subwayLoc[item[:-3]][1]
        pathLine.append(item[-2])

    xbar = xbar / len(pathList)
    ybar = ybar / len(pathList)

    # folium 패키지를 이용하여 평균 위치의 지도를 가져온다.
    map_osm = folium.Map(location=[xbar, ybar], zoom_start=12)
    paths = []
    # 지도상에 경로상의 지하철역을 CircleMarker로 표시하고 역 사이를 PolyLine으로 연결한다.
    for idx, name in enumerate(pathNames):
        loc = subwayLoc[name]
        if pathLine[idx] == '1': color = 'blue'
        elif pathLine[idx] == '2': color = 'green'
        elif pathLine[idx] == '3': color = 'orange'
        elif pathLine[idx] == '4': color = 'cyan'
        folium.CircleMarker(loc, radius=5, popup=name, color=color, fill=True, fill_color=color).add_to(map_osm)
        paths.append(loc)

    folium.PolyLine(paths, color="red", weight=3, opacity=1).add_to(map_osm)
    return map_osm
