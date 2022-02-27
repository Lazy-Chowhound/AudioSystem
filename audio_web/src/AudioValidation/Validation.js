import React from 'react';
import 'antd/dist/antd.css';
import '../css/index.css';
import {Button, message, Select, Table, Upload} from "antd";
import {getAudioSet, getAudioUrl} from "../Util/AudioUtil";
import {sendGet} from "../Util/axios";
import {UploadOutlined} from "@ant-design/icons";


class Validation extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            loading: true,
            dataset: null,
            options: [],
            currentPage: 1,
            pageSize: 5,
            total: null,
            fileList: [],
            uploading: false,
            modelList: [],
            currentModel: null,
        }
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            align: "center",
        },
        {
            title: "内容",
            dataIndex: "preContent",
            align: "center",
            ellipsis: true
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
                options: res,
                dataset: res[0]
            })
        }).catch(error => {
            message.error(error).then()
        })
        this.getModels()
        // this.getAudioSetContrastContentByPage()
    }

    getModels = () => {
        sendGet("/models").then(res => {
            const data = JSON.parse(res.data.data)
            this.setState({
                modelList: data,
                currentModel: data[0]
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    getAudioSetContrastContentByPage = () => {
        this.setState({
            loading: true
        })
        sendGet("/audioSetContrastContentByPage", {
                params: {
                    audioSet: this.state.dataset,
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
        }, () => {
            this.getAudioSetContrastContentByPage()
        })
    }

    modalChange = (e) => {
        this.setState({
            currentModel: e
        })
    }

    beforeUpload = (file, fileList) => {
        console.log(fileList)
        this.setState({
            uploading: true
        })
        const data = new FormData();
        fileList.forEach((file) => {
            data.append('files[]', file);
        });
        // data.append("file", file)
        // sendFile("/uploadModel", data,
        //     {headers: {'Content-Type': 'multipart/form-data'}}).then(res => {
        //         if (res.data.code === 400) {
        //
        //         } else {
        //             message.error("上传失败").then()
        //         }
        //     }
        // ).catch(err => {
        //     message.error(err).then()
        // })
        // setTimeout(() => {
        //     this.setState({
        //         uploading: false
        //     })
        // }, 500)
        return false;
    }

    render() {
        return (
            <div style={{whiteSpace: "pre", padding: 10}}>
                <div style={{display: "flex", justifyContent: "space-between"}}>
                    <div>
                        <span>数据集:</span>
                        <Select value={this.state.dataset} bordered={false} size={"large"}
                                onChange={this.datasetChange}>
                            {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                    <Upload beforeUpload={this.beforeUpload} directory showUploadList={false}>
                        <Button icon={<UploadOutlined/>} loading={this.state.uploading} type="primary">上传模型</Button>
                    </Upload>
                    <div>
                        <span>模型:</span>
                        <Select value={this.state.currentModel} bordered={false} onChange={this.modalChange}>
                            {this.state.modelList.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                    </div>
                </div>
                <Table loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showSizeChanger: false
                       }}
                       expandable={{
                           expandedRowRender: record => {
                               return (
                                   <div>
                                       <span style={{marginRight: 20}}>{"原音频:"}</span>
                                       <audio
                                           src={getAudioUrl(this.state.dataset, record.name)}
                                           style={{height: 30, width: 300, verticalAlign: "middle"}}
                                           controls={true}
                                       />
                                       <span style={{marginLeft: 20, marginRight: 20}}>{"扰动音频:"}</span>
                                       <audio
                                           src={getAudioUrl(this.state.dataset, record.name)}
                                           style={{height: 30, width: 300, verticalAlign: "middle"}}
                                           controls={true}
                                       />
                                   </div>
                               )
                           },
                           rowExpandable: () => true
                       }}/>
            </div>
        );
    }
}

export default Validation
