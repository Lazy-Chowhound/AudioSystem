import React from "react";
import ReactEcharts from 'echarts-for-react'
import {Card} from 'antd'

class NoisePatternDetail extends React.Component {
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
                    type: 'pie',
                    data: [
                        {value: 1000, name: '星期一'},
                        {value: 1500, name: '星期二'},
                        {value: 2000, name: '星期三'},
                        {value: 2500, name: '星期四'},
                        {value: 3000, name: '星期五'},
                        {value: 2300, name: '星期六'},
                        {value: 1600, name: '星期日'}
                    ],
                    top:"20"
                }
            ]
        })
    }

    getOption = () => {
        return {
            title: {
                text: '扰动数量与种类',
                x: 'center',
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                top: 10,
                right: 5,
                data: ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
            },
            series: this.state.series
        };
    }

    render() {
        return (
            <ReactEcharts option={this.getOption()}/>
        )
    }
}

export default NoisePatternDetail