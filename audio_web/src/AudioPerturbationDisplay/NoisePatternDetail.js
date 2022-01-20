import React from "react";
import ReactEcharts from "echarts-for-react"
import sendGet from "../Util/axios";
import {message, Select} from "antd";
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
                text: "扰动数量与种类",
                x: "center",
            },
            tooltip: {
                trigger: "item",
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: "vertical",
                top: 10,
                right: 5,
            },
            series: this.state.series
        };
    }

    getDetail = () => {
        sendGet("/noisePatternDetail", {
            params: {
                dataset: this.props.dataset,
                patternType: this.state.patternType
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                const rawData = JSON.parse(res.data.data)
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
                                    name: "扰动数目",
                                    type: "pie",
                                    data: this.state.info,
                                    top: "20"
                                }
                            ]
                        })
                    }
                )
            }
        }).catch(error => {
            message.error(error).then()
        })
    }

    render() {
        return (
            <div>
                <div style={{marginTop: -20}}>
                    <Select defaultValue="Sound level" bordered={false} onChange={this.handleChange}>
                        <Select.Option value="Sound level">Sound level</Select.Option>
                        <Select.Option value="Gaussian noise">Gaussian noise</Select.Option>
                        <Select.Option value="Animal">Animal</Select.Option>
                        <Select.Option value="Source-ambiguous sounds">Source-ambiguous sounds</Select.Option>
                        <Select.Option value="Natural Sounds">Natural Sounds</Select.Option>
                        <Select.Option value="Sound of things">Sound of things</Select.Option>
                        <Select.Option value="Human Sounds">Human Sounds</Select.Option>
                        <Select.Option value="Music">Music</Select.Option>
                    </Select>
                </div>
                <ReactEcharts option={this.getOption()}/>
            </div>
        )
    }
}

export default NoisePatternDetail