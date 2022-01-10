import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import NoisePatternChart from "./NoisePatternChart";
import {Option} from "antd/es/mentions";
import {Button, Modal, Select} from "antd";
import {BarChartOutlined} from "@ant-design/icons";
import NoisePatternDetail from "./NoisePatternDetail";

class Perturbation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataset: "cv-corpus-arabic",
            visible: false
        }
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
                        <span>选择数据集:</span>
                        <Select defaultValue="cv-corpus-arabic" className={"select"} bordered={false}
                                size={"large"} onChange={this.handleChange}>
                            <Option value="cv-corpus-arabic">cv-corpus-arabic</Option>
                            <Option value="cv-corpus-chinese">cv-corpus-chinese</Option>
                            <Option value="cv-corpus-french">cv-corpus-french</Option>
                            <Option value="cv-corpus-german">cv-corpus-german</Option>
                            <Option value="cv-corpus-japanese">cv-corpus-japanese</Option>
                            <Option value="cv-corpus-russian">cv-corpus-russian</Option>
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
                <NoisePatternChart key={this.state.dataset}/>
                <Modal style={{marginTop: 30}} title={this.state.dataset} visible={this.state.visible}
                       footer={null} onCancel={this.handleCancel} width={650}>
                    <NoisePatternDetail dataset={this.state.dataset}/>
                </Modal>
            </div>
        );
    }
}

export default Perturbation
