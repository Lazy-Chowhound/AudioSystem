import React, {Component} from 'react'
import 'echarts/lib/chart/bar'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/title'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/markPoint'
import ReactEcharts from 'echarts-for-react'


class NoisePatternChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            series: []
        }
    }

    componentDidMount() {
        this.setState({
            series: [
                {
                    name: '扰动数目',
                    type: 'bar',
                    barWidth: '20%',
                    data: [800, 1300, 2000, 2300, 1800, 1100, 500, 700]
                }
            ]
        })
    }

    getOption = () => {
        return {
            title: {
                text: '扰动数量',
                left: "45%"
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                data: ['A']
            },
            xAxis: {
                data: ['Gaussian noise', 'Sound level', 'Animal', 'Source-ambiguous\nsounds', 'Natural Sounds',
                    'Sound of things', 'Human Sounds', 'Music'],
                "axisLabel": {
                    interval: 0,
                }
            },
            yAxis: {
                type: 'value'
            },
            series: this.state.series
        };
    }

    render() {
        return (
            <ReactEcharts style={{marginTop: 20}} option={this.getOption()}/>
        )
    }
}

export default NoisePatternChart