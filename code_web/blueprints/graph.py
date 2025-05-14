# 完成整个网站的可视化部分
# 路由/visualization
# 关联文件graph.html/graph.css/graph.js
# 连接服务器的 MySQL 数据库，host=master,port=3306,root=root,password=1234,database=beike_dws;

# beike_dws中的图表如下：
# dws_area: 折线图：总价和面积的关系
# dws_district: 柱状图：总价和区域的关系
# dws_orient: 柱状图：总价和房屋朝向的关系
# dws_floor: 柱状图：总价和楼层的关系
# dws_type: 折线图：总价和房屋户型的关系
# dws_owner: 柱状图：总价和产权所属的关系
# dws_lift: 柱状图：总价和配备电梯的关系

# 使用pyechart完成可视化图表
# 使用bootstrap，保持网站设计风格统一

from flask import Blueprint, render_template
import pymysql as mysql, json
from pyecharts import options as opts
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType

graph = Blueprint('graph', __name__, url_prefix='/visualization')

def get_db_connection():
    """创建数据库连接"""
    try:
        conn = mysql.connect(
            host='192.168.6.131',
            port=3306,
            user='root',
            passwd='1234',
            db='beike_dws'
        )
        return conn
    except Exception as e:
        print(f"数据库连接失败: {str(e)}")
        return None

def execute_query(sql):
    """执行SQL查询"""
    try:
        conn = get_db_connection()
        if not conn:
            return []
        
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except Exception as e:
        print(f"查询执行失败: {str(e)}")
        return []

@graph.route('/')
def show_graphs():
    """显示所有图表"""
    try:
        charts = {
            'area_chart': create_area_chart(),
            'district_chart': create_district_chart(),
            'orient_chart': create_orient_chart(),
            'floor_chart': create_floor_chart(),
            'type_chart': create_type_chart(),
            'owner_chart': create_owner_chart(),
            'lift_chart': create_lift_chart()
        }
        
        # 打印图表数据用于调试
        for name, data in charts.items():
            print(f"{name} 数据长度: {len(str(data))}")
            
        return render_template('graph.html', **charts)
    except Exception as e:
        print(f"图表生成失败: {str(e)}")
        return render_template('graph.html', error="图表加载失败")

def create_area_chart():
    """创建面积分布图表"""
    try:
        data = execute_query("SELECT * FROM dws_area")
        if not data:
            print("面积数据为空")
            return "{}"
        
        # 打印数据用于调试
        print("面积数据:", data)
        
        c = (
            Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis([str(d[0]) for d in data])
            .add_yaxis("平均价格", [d[1] for d in data])
            .set_global_opts(
                title_opts=opts.TitleOpts(title="房屋面积分布"),
                xaxis_opts=opts.AxisOpts(
                    name="面积范围(㎡)",
                    axislabel_opts={"rotate": 45}
                ),
                yaxis_opts=opts.AxisOpts(name="平均价格"),
                tooltip_opts=opts.TooltipOpts(trigger="axis")
            )
        )
        return c.dump_options()
    except Exception as e:
        print(f"创建面积图表失败: {str(e)}")
        return "{}"

def create_district_chart():
    """创建区域分布图表"""
    data = execute_query("SELECT * FROM dws_district")
    if not data:
        return "{}"
    
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([d[0] for d in data])
        .add_yaxis("平均价格", [d[1] for d in data])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各区域房源分布"),
            xaxis_opts=opts.AxisOpts(
                name="区域", 
                axislabel_opts={"rotate": 45}
            ),
            yaxis_opts=opts.AxisOpts(name="平均价格"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.dump_options()

def create_orient_chart():
    """创建朝向分布图表"""
    data = execute_query("SELECT * FROM dws_orient")
    if not data:
        return "{}"
    
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([d[0] for d in data])
        .add_yaxis("平均价格", [d[1] for d in data])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="房屋朝向分布"),
            xaxis_opts=opts.AxisOpts(name="朝向"),
            yaxis_opts=opts.AxisOpts(name="平均价格"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.dump_options()

def create_floor_chart():
    """创建楼层分布图表"""
    data = execute_query("SELECT * FROM dws_floor")
    if not data:
        return "{}"
    
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([str(d[0]) for d in data])
        .add_yaxis("平均价格", [d[1] for d in data])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="楼层分布"),
            xaxis_opts=opts.AxisOpts(
                name="楼层",
                axislabel_opts={'rotate': 45}
            ),
            yaxis_opts=opts.AxisOpts(name="平均价格"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.dump_options()

def create_type_chart():
    """创建户型分布图表"""
    data = execute_query("SELECT * FROM dws_type")
    if not data:
        return "{}"
    
    c = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([str(d[0]) for d in data])
        .add_yaxis("平均价格", [d[1] for d in data])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="户型分布"),
            xaxis_opts=opts.AxisOpts(
                name="户型", 
                axislabel_opts={"rotate": 45}
            ),
            yaxis_opts=opts.AxisOpts(name="平均价格"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.dump_options()

def create_owner_chart():
    """创建产权所属分布图表"""
    data = execute_query("SELECT * FROM dws_owner")
    if not data:
        return "{}"
    
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([str(d[0]) for d in data])
        .add_yaxis("平均价格", [d[1] for d in data])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="产权所属分布"),
            xaxis_opts=opts.AxisOpts(name="产权所属"),
            yaxis_opts=opts.AxisOpts(name="平均价格"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.dump_options()

def create_lift_chart():
    """创建电梯配备分布图表"""
    data = execute_query("SELECT * FROM dws_lift")
    if not data:
        return "{}"
    
    c = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis([str(d[0]) for d in data])
        .add_yaxis("平均价格", [d[1] for d in data])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="电梯配备分布"),
            xaxis_opts=opts.AxisOpts(name="电梯配备"),
            yaxis_opts=opts.AxisOpts(name="平均价格"),
            tooltip_opts=opts.TooltipOpts(trigger="axis")
        )
    )
    return c.dump_options()
