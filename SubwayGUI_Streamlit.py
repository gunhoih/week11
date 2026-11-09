import streamlit as st
from subwayPath import loadSubway, drawMap

st.title('지하철 최단 경로 검색')
st.write('출발역과 도착역을 선택한 후 검색 버튼을 눌러주세요.')

nodes, subwayLoc, d = loadSubway()
stationList = sorted(nodes)

col1, col2 = st.columns(2)
with col1:
    station_start = st.selectbox('출발역', stationList, index=stationList.index('남태령(4)'))
with col2:
    station_destination = st.selectbox('도착역', stationList, index=stationList.index('종각(1)'))

if st.button('최단 경로 검색'):
    pathList, dist = d.getPath(station_start, station_destination)

    if len(pathList) == 0:
        st.warning('경로를 찾을 수 없습니다.')
    else:
        st.subheader('검색 결과')
        st.write(' → '.join(pathList))
        if len(dist) > 0:
            st.write(f'총 소요시간: {dist[-1]}분')
        else:
            st.write('총 소요시간: 0분')

        # 기존 PyQt에서 지도를 새 창으로 열던 부분을 Streamlit 화면에 표시한다.
        map_osm = drawMap(pathList, subwayLoc)
        st.iframe(map_osm.get_root().render(), height=550)
