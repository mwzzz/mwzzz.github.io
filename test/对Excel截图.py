import pandas as pd
import imgkit
import os

# 读取 Excel 文件中的指定 Sheet
def read_excel_sheets(file_path):
    # 使用 pandas 读取 Excel 文件
    xl = pd.ExcelFile(file_path)
    sheet_names = xl.sheet_names  # 获取所有 sheet 的名称
    sheets = {}

    # 读取每个 sheet
    for sheet in sheet_names:
        sheets[sheet] = xl.parse(sheet)
    return sheets

# 截取指定区域的数据
def extract_region(dataframe, start_cell, end_cell):
    # 转换起始单元格和结束单元格为行列号
    start_row, start_col = start_cell
    end_row, end_col = end_cell

    # 截取数据
    return dataframe.iloc[start_row-1:end_row, start_col-1:end_col]  # 注意：这里减1是因为Excel索引从1开始，而Pandas从0开始

# 将 DataFrame 转换为 HTML 并保存为图片
def save_dataframe_as_image(df, output_file, config=None):
    # 将 DataFrame 转换为 HTML 表格
    html = df.to_html(index=False)

    # 临时保存 HTML 文件
    temp_html = 'temp_table.html'
    with open(temp_html, 'w', encoding='utf-8') as f:
        f.write(html)

    # 将 HTML 转换为图片
    if config is None:
        imgkit.from_file(temp_html, output_file)
    else:
        imgkit.from_file(temp_html, output_file, config=config)

    # 删除临时 HTML 文件
    os.remove(temp_html)

# 主函数：读取 Excel 并对指定区域截图
def main(file_path, regions, output_dir, wkhtmltoimage_path=None):
    # 读取所有 sheet
    sheets = read_excel_sheets(file_path)

    # 配置 imgkit
    if wkhtmltoimage_path:
        config = imgkit.config(wkhtmltoimage=wkhtmltoimage_path)
    else:
        config = None

    # 遍历每个 sheet
    for sheet_name, sheet_data in sheets.items():
        for region_name, (start_cell, end_cell) in regions.items():
            # 截取指定区域
            region_data = extract_region(sheet_data, start_cell, end_cell)

            # 保存截图
            output_file = os.path.join(output_dir, f"{sheet_name}_{region_name}.png")
            save_dataframe_as_image(region_data, output_file, config)
            print(f"Saved screenshot: {output_file}")

# 示例使用
if __name__ == '__main__':
    # Excel 文件路径
    excel_file = "1.xlsx"

    # 指定需要截图的区域 (起始单元格，结束单元格)
    # 例如：(1, 1) 表示 A1 单元格，(5, 5) 表示 E5 单元格
    regions_to_capture = {
        "region1": ((1, 1), (10, 5)),  # A1 到 E10
        "region2": ((6, 1), (15, 5))   # A6 到 E15
    }

    # 输出目录
    output_directory = "screenshots"
    os.makedirs(output_directory, exist_ok=True)

    # 可选：设置 wkhtmltoimage 的路径
    wkhtmltoimage_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe"  # 根据实际情况修改路径

    # 执行主程序
    main(excel_file, regions_to_capture, output_directory, wkhtmltoimage_path)