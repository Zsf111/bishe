// 传递后端数据到前端
window.addEventListener('DOMContentLoaded', function() {
    try {
        const chartOptions = {
            areaChart: JSON.parse('{{ area_chart | safe }}'),
            districtChart: JSON.parse('{{ district_chart | safe }}'),
            orientChart: JSON.parse('{{ orient_chart | safe }}'),
            floorChart: JSON.parse('{{ floor_chart | safe }}'),
            typeChart: JSON.parse('{{ type_chart | safe }}'),
            ownerChart: JSON.parse('{{ owner_chart | safe }}'),
            liftChart: JSON.parse('{{ lift_chart | safe }}')
        };

        // 初始化所有图表
        // const charts = {
        //     areaChart: echarts.init(document.getElementById('area-chart')),
        //     districtChart: echarts.init(document.getElementById('district-chart')),
        //     orientChart: echarts.init(document.getElementById('orient-chart')),
        //     floorChart: echarts.init(document.getElementById('floor-chart')),
        //     typeChart: echarts.init(document.getElementById('type-chart')),
        //     ownerChart: echarts.init(document.getElementById('owner-chart')),
        //     liftChart: echarts.init(document.getElementById('lift-chart'))
        // };
        const charts = {
            areaChart: charts.init(document.getElementById('area-chart')),
            districtChart: charts.init(document.getElementById('district-chart')),
            orientChart: charts.init(document.getElementById('orient-chart')),
            floorChart: charts.init(document.getElementById('floor-chart')),
            typeChart: charts.init(document.getElementById('type-chart')),
            ownerChart: charts.init(document.getElementById('owner-chart')),
            liftChart: charts.init(document.getElementById('lift-chart'))
        };

        // 设置图表选项
        Object.keys(charts).forEach(key => {
            charts[key].setOption(chartOptions[key]);
        });

        // 响应式处理
        window.addEventListener('resize', function() {
            Object.values(charts).forEach(chart => chart.resize());
        });
    } catch (error) {
        console.error('图表初始化失败:', error);
    }
});



// 初始化所有图表
document.addEventListener('DOMContentLoaded', function() {
    // 获取后端传递的数据
    const chartData = document.getElementById('chart-data');
    if (!chartData) {
        console.error('找不到图表数据元素');
        return;
    }

    try {
        const chartOptions = {
            areaChart: JSON.parse(chartData.getAttribute('data-area')),
            districtChart: JSON.parse(chartData.getAttribute('data-district')),
            orientChart: JSON.parse(chartData.getAttribute('data-orient')),
            floorChart: JSON.parse(chartData.getAttribute('data-floor')),
            typeChart: JSON.parse(chartData.getAttribute('data-type')),
            ownerChart: JSON.parse(chartData.getAttribute('data-owner')),
            liftChart: JSON.parse(chartData.getAttribute('data-lift'))
        };

        // 初始化所有图表
        const charts = {
            areaChart: echarts.init(document.getElementById('area-chart')),
            districtChart: echarts.init(document.getElementById('district-chart')),
            orientChart: echarts.init(document.getElementById('orient-chart')),
            floorChart: echarts.init(document.getElementById('floor-chart')),
            typeChart: echarts.init(document.getElementById('type-chart')),
            ownerChart: echarts.init(document.getElementById('owner-chart')),
            liftChart: echarts.init(document.getElementById('lift-chart'))
        };

        // 设置图表选项
        Object.keys(charts).forEach(key => {
            if (chartOptions[key]) {
                charts[key].setOption(chartOptions[key]);
            } else {
                console.error(`未找到 ${key} 的数据`);
            }
        });

        // 响应式处理
        window.addEventListener('resize', function() {
            Object.values(charts).forEach(chart => chart.resize());
        });
    } catch (error) {
        console.error('图表初始化失败:', error);
    }
});
