import React, {Component} from 'react'
import 'echarts/lib/chart/bar'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/title'
import 'echarts/lib/component/legend'
import 'echarts/lib/component/markPoint'
import ReactEcharts from 'echarts-for-react'
import sendGet from "../Util/axios";
import {message} from "antd";


class NoisePatternChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: ['Animal', 'Gaussian noise', 'Human Sounds', 'Music', 'Natural Sounds',
                'Source-ambiguous\nsounds', 'Sound level', 'Sound of things'],
            data: []
        }
    }

    componentDidMount() {
        sendGet("/noisePatternSummary", {
            params: {
                dataset: this.props.dataset
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then(r => console.log(r))
            } else {
                const rawData = JSON.parse(res.data.data)
                const info = []
                for (let i = 0; i < this.state.columns.length; i++) {
                    if (typeof rawData[this.state.columns[i]] == "undefined") {
                        info.push(0)
                    } else {
                        info.push(rawData[this.state.columns[i]])
                    }
                }
                this.setState({
                    data: info
                }, () => {
                    this.setState({
                        series: [
                            {
                                name: '扰动数目',
                                type: 'bar',
                                barWidth: '25%',
                                data: this.state.data
                            }
                        ]
                    })
                })
            }
        }).catch(error => {
            message.error(error).then(r => console.log(r))
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
                data: this.state.columns,
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