import React, {Component} from "react"
import "echarts/lib/chart/bar"
import "echarts/lib/component/tooltip"
import "echarts/lib/component/title"
import "echarts/lib/component/legend"
import "echarts/lib/component/markPoint"
import ReactEcharts from "echarts-for-react"
import {sendGet} from "../Util/axios";
import {message} from "antd";


class NoisePatternChart extends Component {
    constructor(props) {
        super(props);
        this.state = {
            columns: ["Animal", "Gaussian noise", "Human sounds", "Music", "Natural sounds"
                , "Sound level", "Sound of things", "Source-ambiguous sounds"],
            data: []
        }
    }

    componentDidMount() {
        if (this.props.dataset !== "") {
            sendGet("/patternSummary", {
                params: {
                    dataset: this.props.dataset
                }
            }).then(res => {
                if (res.data.code === 400) {
                    message.error(res.data.data).then()
                } else {
                    const rawData = JSON.parse(res.data.data)
                    const info = []
                    for (let i = 0; i < this.state.columns.length; i++) {
                        let legend = this.state.columns[i];
                        if (typeof rawData[legend] == "undefined") {
                            info.push(0)
                        } else {
                            info.push(rawData[legend])
                        }
                    }
                    this.setState({
                        data: info
                    }, () => {
                        this.setState({
                            series: [
                                {
                                    name: "扰动数目",
                                    type: "bar",
                                    barWidth: "25%",
                                    data: this.state.data
                                }
                            ]
                        })
                    })
                }
            }).catch(error => {
                message.error(error).then()
            })
        }
    }

    getOption = () => {
        return {
            title: {
                text: "扰动数量",
                left: "45%"
            },
            tooltip: {
                trigger: "axis"
            },
            xAxis: {
                data: this.state.columns,
                "axisLabel": {
                    interval: 0,
                    formatter: function (value) {
                        if (value.length > 15) {
                            let space = value.lastIndexOf(" ");
                            return value.substring(0, space) + "\n" + value.substring(space)
                        } else {
                            return value
                        }
                    }
                }
            },
            yAxis: {
                type: "value"
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