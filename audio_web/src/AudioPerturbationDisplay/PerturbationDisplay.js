import React from "react";
import "antd/dist/antd.css";
import NoisePatternChart from "./NoisePatternChart";
import {Button, message, Modal, Select} from "antd";
import {PieChartOutlined} from "@ant-design/icons";
import NoisePatternDetail from "./NoisePatternDetail";
import "../css/PerturbationDisplay.css"
import {getAudioSet} from "../Util/AudioUtil"

class PerturbationDisplay extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataset: null,
            visible: false,
            options: []
        }
    }

    componentDidMount() {
        getAudioSet().then(res => {
            this.setState({
                options: res
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    datasetChange = (e) => {
        this.setState({
            dataset: e
        })
    }

    handleCancel = () => {
        this.setState({
            visible: false
        })
    }

    showDetail = () => {
        this.setState({
            visible: true
        })
    }

    render() {
        return (
            <div className="content" style={{padding: 10}}>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <div>
                        <span>数据集:</span>
                        <Select placeholder={"选择数据集"} value={this.state.dataset} bordered={false}
                                onChange={this.datasetChange}>
                            {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                    <Button type="primary" icon={<PieChartOutlined/>} onClick={this.showDetail}>
                        查看详情
                    </Button>
                </div>
                <NoisePatternChart key={this.state.dataset} dataset={this.state.dataset}/>
                <Modal style={{marginTop: 30}} title={this.state.dataset}
                       visible={this.state.visible} footer={null} onCancel={this.handleCancel} width={750}>
                    <NoisePatternDetail key={this.state.dataset} dataset={this.state.dataset}/>
                </Modal>
            </div>
        );
    }
}

export default PerturbationDisplay
