import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import {message, Select, Table} from "antd";
import {getAudioSet, getAudioUrl} from "../Util/AudioUtil";
import sendGet from "../Util/axios";
import AudioPlay from "../AudioList/AudioPlay";


class Validation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            loading: true,
            dataset: "cv-corpus-chinese",
            options: [],
            modal: "模型1",
            currentPage: 1,
            pageSize: 5,
            total: null
        }
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            align: "center",
            render: (text, record) => <AudioPlay name={record.name}
                                                 src={getAudioUrl(this.state.dataset, record.name)}/>
        },
        {
            title: "原始音频",
            dataIndex: "sourceAudio",
            align: "center",
        },
        {
            title: "内容",
            dataIndex: "preContent",
            align: "center",
            ellipsis: {
                showTitle: false,
            },
        },
        {
            title: "扰动音频",
            dataIndex: "noiseAudio",
            align: "center"
        },
        {
            title: "识别内容",
            dataIndex: "postContent",
            align: "center",
            ellipsis: {
                showTitle: false,
            },
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
        this.getAudioSetContrastContentByPage()
    }

    getAudioSetContrastContentByPage = () => {
        sendGet("/audioSetContrastContentByPage", {
                params: {
                    dataset: this.state.dataset,
                    page: this.state.currentPage,
                    pageSize: this.state.pageSize
                }
            }
        ).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
                this.setState({
                    loading: false
                })
            } else {
                const data = JSON.parse(res.data.data)
                const totalLen = data.shift().total
                this.setState({
                    dataSource: data,
                    total: totalLen,
                    loading: false
                })
            }
        }).catch(error => {
                message.error(error).then()
                this.setState({
                    loading: false
                })
            }
        )
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
