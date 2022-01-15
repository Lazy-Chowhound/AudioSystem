import React from 'react';
import 'antd/dist/antd.css';
import NoisePatternChart from "./NoisePatternChart";
import {Button, message, Modal, Select} from "antd";
import {BarChartOutlined} from "@ant-design/icons";
import NoisePatternDetail from "./NoisePatternDetail";
import "../css/PerturbationDisplay.css"
import sendGet from "../Util/axios";

class PerturbationDisplay extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataset: "cv-corpus-arabic",
            visible: false,
            options: []
        }
    }

    componentDidMount() {
        sendGet("/audioSetList", {
            params: {
                path: "D:/AudioSystem/Audio/"
            }
        }).then(res => {
            const audioList = JSON.parse(res.data.data)
            const ops = []
            for (let i = 0; i < audioList.length; i++) {
                ops.push(audioList[i])
            }
            this.setState({
                options: ops
            })
        }).catch(error => {
            message.error(error).then(r => console.log(r))
        })
    }

    handleChange = (e) => {
        this.setState({
            dataset: e
        })
    }

    handleCancel = () => {
        this.setState({
            visible: false
        })
    }

    render() {
        return (
            <div className="content" style={{padding: 10}}>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <div>
                        <span>数据集:</span>
                        <Select defaultValue="cv-corpus-chinese" bordered={false}
                                size={"large"} onChange={this.handleChange}>
                            {this.state.options.map(val => <option value={val}>{val}</option>)}
                        </Select>
                    </div>
                    <Button type="primary" icon={<BarChartOutlined/>} onClick={() => {
                        this.setState({
                            visible: true
                        })
                    }}>
                        查看详情
                    </Button>
                </div>
                <NoisePatternChart key={this.state.dataset} dataset={this.state.dataset}/>
                <Modal style={{marginTop: 30}} title={this.state.dataset} visible={this.state.visible}
                       footer={null} onCancel={this.handleCancel} width={750}>
                    <NoisePatternDetail dataset={this.state.dataset}/>
                </Modal>
            </div>
        );
    }
}

export default PerturbationDisplay
