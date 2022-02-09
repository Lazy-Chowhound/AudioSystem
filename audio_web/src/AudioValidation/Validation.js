import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import {message, Select, Table} from "antd";
import {getAudioSet} from "../Util/AudioUtil";


class Validation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            loading: true,
            dataset: "cv-corpus-chinese",
            options: [],
            modal: "模型1"
        }
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            align: "center"
        },
        {
            title: "原始音频",
            dataIndex: "sourceAudio",
            align: "center"
        },
        {
            title: "内容",
            dataIndex: "preContent",
            align: "center"
        },
        {
            title: "扰动音频",
            dataIndex: "noiseAudio",
            align: "center"
        },
        {
            title: "识别内容",
            dataIndex: "postContent",
            align: "center"
        },
    ];

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

    modalChange = (e) => {
        this.setState({
            modal: e
        })
    }

    render() {
        return (
            <div style={{whiteSpace: "pre", padding: 10}}>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <div>
                        <span>数据集:</span>
                        <Select defaultValue="cv-corpus-chinese" bordered={false}
                                size={"large"} onChange={this.datasetChange}>
                            {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                    <div>
                        <span>模型:</span>
                        <Select defaultValue="模型1" bordered={false}
                                onChange={this.modalChange}>
                            <Select.Option key={"模型1"} value={"模型1"}/>
                            <Select.Option key={"模型2"} value={"模型2"}/>
                            <Select.Option key={"模型3"} value={"模型3"}/>
                        </Select>
                    </div>
                </div>
                <Table loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showSizeChanger: false
                       }}/>
            </div>
        );
    }
}

export default Validation
