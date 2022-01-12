import React from "react";
import ReactEcharts from 'echarts-for-react'
import sendGet from "../Util/axios";
import {message, Select} from "antd";
import {Option} from "antd/es/mentions";
import "../css/NoisePatternDetail.css"

class NoisePatternDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            legend: [],
            info: [],
            patternType: "Sound level"
        }
    }

    componentDidMount() {
        this.getDetail()
    }

    handleChange = (e) => {
        this.setState({
            patternType: e
        }, () => {
            this.getDetail()
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
                data: this.state.legend
            },
            series: this.state.series
        };
    }

    getDetail = () => {
        sendGet("/noisePatternDescription", {
            params: {
                dataset: this.props.dataset,
                patternType: this.state.patternType
            }
        }).then(res => {
            const rawData = JSON.parse(res.data.data)
            console.log(rawData)
            const legend = []
            const info = []
            for (const key in rawData) {
                legend.push(key)
                info.push({value: rawData[key], name: key})
            }
            this.setState({
                    legend: legend,
                    info: info
                }, () => {
                    this.setState({
                        series: [
                            {
                                name: '扰动数目',
                                type: 'pie',
                                data: this.state.info,
                                top: "20"
                            }
                        ]
                    })
                }
            )
        }).catch(error => {
            message.error(error).then(r => console.log(r))
        })
    }

    render() {
        return (
            <div>
                <div style={{marginTop: -20}}>
                    <Select defaultValue="Sound level" className={"select"}
                            bordered={false} onChange={this.handleChange}>
                        <Option value="Sound level">Sound level</Option>
                        <Option value="Gaussian noise">Gaussian noise</Option>
                        <Option value="Animal">Animal</Option>
                        <Option value="Source-ambiguous sounds">Source-ambiguous sounds</Option>
                        <Option value="Natural Sounds">Natural Sounds</Option>
                        <Option value="Sound of things">Sound of things</Option>
                        <Option value="Human Sounds">Human Sounds</Option>
                        <Option value="Music">Music</Option>
                    </Select>
                </div>
                <ReactEcharts option={this.getOption()}/>
            </div>
        )
    }
}

export default NoisePatternDetail