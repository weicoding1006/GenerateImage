import json
import shutil
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from shapely.affinity import translate

# 獲取 JSON 文件路徑
json_file_path = sys.argv[1]

# 讀取 JSON 文件內容
with open(json_file_path, 'r', encoding='utf-8') as file:
    all_alert_data = json.load(file)

# 設定輸入的 GeoJSON 文件路徑
input_geojson = "C:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\county.geojson"
output_directory = "C:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\output_images"
overlay_image_path = "C:\\Users\\2309013\\Desktop\\後端製圖\\pythonGenerateImage-main\\下載.png"
if(os.path.exists(output_directory)):
    shutil.rmtree(output_directory)
# 讀取 GeoJSON 文件
gdf = gpd.read_file(input_geojson)

# 確保輸出目錄存在
os.makedirs(output_directory, exist_ok=True)

# 找到金門縣和連江縣的幾何形狀並移動到合適的位置
def adjust_special_counties(gdf):
    # 找到金門縣的幾何形狀
    kinmen = gdf[gdf['COUNTYNAME'] == '金門縣']

    # 計算金門縣的位置偏移量，將其移到圖片的左上角
    x_offset = gdf.total_bounds[0] - kinmen.geometry.bounds.minx.values[0] + 4.8
    y_offset = gdf.total_bounds[3] - kinmen.geometry.bounds.maxy.values[0] - 1.35
    kinmen_shifted = kinmen.geometry.apply(lambda geom: translate(geom, xoff=x_offset, yoff=y_offset))
    gdf.loc[gdf['COUNTYNAME'] == '金門縣', 'geometry'] = kinmen_shifted

    # 找到連江縣的幾何形狀
    lienchiang = gdf[gdf['COUNTYNAME'] == '連江縣']

    # 計算連江縣的位置偏移量，將其移到合適位置
    x_offset_lienchiang = -0.5
    y_offset_lienchiang = gdf.total_bounds[3] - lienchiang.geometry.bounds.maxy.values[0] - 1.1
    lienchiang_shifted = lienchiang.geometry.apply(lambda geom: translate(geom, xoff=x_offset_lienchiang, yoff=y_offset_lienchiang))
    gdf.loc[gdf['COUNTYNAME'] == '連江縣', 'geometry'] = lienchiang_shifted

adjust_special_counties(gdf)

# 定義警戒等級與顏色對應表
styles = {
    "W00": {'fillColor': 'red', 'color': 'red'},
    "W06": {'fillColor': 'orange', 'color': 'orange'},
    "W12": {'fillColor': 'green', 'color': 'green'},
    "W24": {'fillColor': 'blue', 'color': 'blue'},
    "W36": {'fillColor': 'gray', 'color': 'gray'},
    "WAA": {'fillColor': 'white', 'color': 'black'}
}

# 定義線條數據
lines_data = [
    {"start": [120.4, 24.8], "end": [120.95, 24.8], "countyName": "新竹市"},
    {"start": [120.1, 24.25], "end": [120.65, 24.25], "countyName": "台中市"},
    {"start": [120.5, 23.5], "end": [120.1, 23.3], "countyName": "嘉義市"},
    {"start": [120.1, 23.3], "end": [119.95, 23.1], "countyName": "嘉義市"},
    {"start": [119.95, 23.1], "end": [119.9, 23.1], "countyName": "嘉義市"},
    {"start": [120.2513, 22.95], "end": [119.95, 22.95], "countyName": "台南市"},
    {"start": [120.3, 22.8], "end": [120.02, 22.8], "countyName": "高雄市"},
    {"start": [120.38, 22.55], "end": [120.12, 22.55], "countyName": "高雄市"},
    {"start": [120.52, 22.73], "end": [120.45, 22.43], "countyName": "屏東縣"},
    {"start": [120.45, 22.43], "end": [120.22, 22.43], "countyName": "屏東縣"},
    {"start": [120.75, 22.02], "end": [120.42, 22.02], "countyName": "屏東縣"},
    {"start": [121.2, 22.87], "end": [121.56, 22.87], "countyName": "台東縣"},
    {"start": [121.46, 22.66], "end": [121.86, 22.66], "countyName": "台東縣"},
    {"start": [121.58, 24], "end": [121.96, 24], "countyName": "花蓮縣"},
    {"start": [121.75, 24.8], "end": [122.1, 24.8], "countyName": "宜蘭縣"}
]


# 定義圓點數據
circle_data = [
    {"x": 120.4, "y": 24.8, "color": "#BF0100", "countyName": "新竹市"},
    {"x": 120.1, "y": 24.25, "color": "#BF0100", "countyName": "臺中市"},
    {"x": 119.85, "y": 23.1, "color": "green", "countyName": "嘉義市"},
    {"x": 119.95, "y": 22.95, "color": "green", "countyName": "臺南市"},
    {"x": 120.02, "y": 22.8, "color": "green", "countyName": "高雄市"},
    {"x": 120.12, "y": 22.55, "color": "green", "countyName": "高雄市"},
    {"x": 120.22, "y": 22.43, "color": "blue", "countyName": "屏東縣"},
    {"x": 120.42, "y": 22.02, "color": "blue", "countyName": "屏東縣"},
    {"x": 121.56, "y": 22.87, "color": "blue", "countyName": "臺東縣"},
    {"x": 121.86, "y": 22.66, "color": "gray", "countyName": "臺東縣"},
    {"x": 121.96, "y": 24, "color": "gray", "countyName": "花蓮縣"},
    {"x": 122.1, "y": 24.8, "color": "gray", "countyName": "宜蘭縣"}
]


# 定義文字數據
text_data = [
    {"x": 120.1, "y": 24.78, "text": "P0 W00","countyName": "新竹市"},
    {"x": 119.8, "y": 24.23, "text": "MQ M00", "countyName": "臺中市"},
    {"x": 119.85 - 0.3, "y": 23.1 - 0.02, "text": "KU W12", "countyName": "嘉義市"},
    {"x": 119.95- 0.3, "y": 22.95 - 0.02, "text": "WS W12", "countyName": "臺南市"},
    {"x": 120.02- 0.3, "y": 22.8 - 0.02, "text": "AY W12", "countyName": "高雄市"},
    {"x": 120.12- 0.3, "y": 22.55 - 0.02, "text": "KH W12", "countyName": "高雄市"},
    {"x": 120.22- 0.3, "y": 22.43 - 0.02, "text": "DC W24", "countyName": "屏東縣"},
    {"x": 120.42- 0.3, "y": 22.02 - 0.02, "text": "DC W24", "countyName": "屏東縣"},
    {"x": 121.56 + 0.3, "y": 22.87 - 0.02, "text": "ZN W24", "countyName": "臺東縣"},
    {"x": 121.86 + 0.3, "y": 22.66 - 0.02, "text": "LT W36", "countyName": "臺東縣"},
    {"x": 121.96 + 0.3, "y": 24 - 0.02, "text": "YU W36", "countyName": "花蓮縣"},
    {"x": 122.1 + 0.3, "y": 24.8 - 0.02, "text": "MS W36", "countyName": "宜蘭縣"}
    # 添加更多文字數據...
]


# 迭代處理每個 key，並生成對應的圖片
for key, alertJsonData in all_alert_data.items():
    # 創建一個字典，用於存儲縣市到警戒數據的映射
    county_alert_map = {alert['County']: alert['AlertNumberString'] for alert in alertJsonData if not alert.get('District')}

    # 根據 COUNTYNAME 產生顏色
    def assign_color(county_name):
        alert_level = county_alert_map.get(county_name, "")
        style = styles.get(alert_level, None)
        if style:
            return style['fillColor'], "#000000"
        else:
            return "#ffffff", "#000000"

    gdf['fill_color'], gdf['line_color'] = zip(*gdf['COUNTYNAME'].apply(assign_color))

    # 設置正方形的圖片尺寸
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))

    # 設置台灣的經緯度範圍來放大地圖並調整位置
    minx, maxx = 119.2, 121
    miny, maxy = 21.85, 25.3
    range_x = maxx - minx
    range_y = maxy - miny
    max_range = max(range_x, range_y)

    # 調整 xlim 和 ylim 保持正方形比例
    ax.set_xlim(minx, minx + max_range)
    ax.set_ylim(miny, miny + max_range)

    # 繪製地圖
    gdf.plot(ax=ax, color=gdf['fill_color'], edgecolor=gdf['line_color'])

    # 繪製線條
    for line in lines_data:
        x_values = [line["start"][0], line["end"][0]]
        y_values = [line["start"][1], line["end"][1]]
        ax.plot(x_values, y_values, color="black", linewidth=2)

    # 繪製圓點
    for circle in circle_data:
        circle_color = styles.get(county_alert_map.get(circle["countyName"], ""), {"color": "black"})["color"]
        ax.plot(circle["x"], circle["y"], 'o', color=circle_color, markersize=10)

    # 添加文字標註
    for text in text_data:
        ax.text(text["x"], text["y"], text["text"], fontsize=14, ha='center')

    # 去除軸線
    ax.axis('off')

    # 疊加左下角的PNG圖片
    overlay_image = mpimg.imread(overlay_image_path)
    fig.figimage(overlay_image, xo=10, yo=fig.bbox.ymin + 10, zorder=3, alpha=1)

    # 保存地圖為圖片
    output_image = os.path.join(output_directory, f"colored_map_{key}.png")
    plt.savefig(output_image)
    plt.close()

print(f"所有圖片已生成並保存至資料夾。")
