import React from "react";
import {Button, message, Modal, Table, Tooltip} from "antd";
import ImageDisplay from "./ImageDisplay";
import sendGet from "../Util/axios";
import baseUrl from "../Util/url";
import AudioPlay from "./AudioPlay";

class AudioDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            isModalVisible: false,
            ImageType: null,
            AbsoluteUrl: null,
            ImageUrl: null,
            currentPage: 1,
            total: null,
            pageSize: 5,
            loading: true
        };
    }

    columns = [
        {
            title: "音频",
            dataIndex: "name",
            key: "name",
            align: "center",
            width: 320,
            render: item => <AudioPlay name={item}
                                       src={baseUrl + "/Audio/" + this.props.choice + "/clips/" + item}/>
        },
        {
            title: "时长",
            dataIndex: "size",
            align: "center"
        },
        {
            title: "声道",
            dataIndex: "channel",
            align: "center"
        },
        {
            title: "采样率",
            dataIndex: "sampleRate",
            align: "center"
        },
        {
            title: "位深",
            dataIndex: "bitDepth",
            align: "center"
        },
        {
            title: "内容",
            dataIndex: "content",
            align: "center",
            ellipsis: {
                showTitle: false,
            },
            render: address => (
                <Tooltip placement="topLeft" title={address}>
                    {address}
                </Tooltip>
            ),
        },
        {
            title: "波形图",
            dataIndex: "distribution",
            render: item =>
                <Button type={"link"} size={"small"} onClick={() => {
                    this.showWaveForm(item)
                }}>查看波形图</Button>,
            align: "center"
        },
        {
            title: "频谱图",
            dataIndex: "list",
            render: item =>
                <Button type={"link"} size={"small"} onClick={() => {
                    this.showMelSpectrum(item)
                }}>查看频谱图</Button>,
            align: "center"
        },
    ];

    componentDidMount() {
        this.getPage()
    }

    showWaveForm = (item) => {
        sendGet("/getWaveForm", {
            params: {
                audioSet: this.props.choice,
                audioName: item.name
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                const path = res.data.data
                this.setState({
                    ImageType: "波形图",
                    isModalVisible: true,
                    AbsoluteUrl: path,
                    ImageUrl: path.replace("D:/AudioSystem", baseUrl)
                })
            }
        }).catch(error => {
                message.error(error).then()
            }
        )
    }

    showMelSpectrum = (item) => {
        sendGet("/getMelSpectrum", {
            params: {
                audioSet: this.props.choice,
                audioName: item.name
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                const path = res.data.data
                this.setState({
                    ImageType: "Mel频谱图",
                    isModalVisible: true,
                    AbsoluteUrl: path,
                    ImageUrl: path.replace("D:/AudioSystem", baseUrl)
                })
            }
        }).catch(error => {
                message.error(error).then()
            }
        )
    }

    handleCancel = () => {
        this.setState({
            isModalVisible: false
        })
        sendGet("/removeImage", {
            params: {
                path: this.state.AbsoluteUrl
            }
        }).catch(error => {
            message.error(error).then()
        })
    }

    changePage = (page) => {
        this.setState({
            currentPage: page.current
        }, () => {
            this.getPage()
        })
    }

    getPage = () => {
        this.setState({
            dataSource: [],
            loading: true
        })
        sendGet("/audioDescription", {
            params: {
                audioSet: this.props.choice,
                page: this.state.currentPage,
                pageSize: this.state.pageSize
            }
        }).then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
                this.setState({
                    loading: false
                })
            } else {
                const data = JSON.parse(res.data.data)
                const totalLen = data.shift().total
                console.log(totalLen)
                console.log(data)
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
        })
    }

    render() {
        return (
            <div>
                <Table loading={this.state.loading} columns={this.columns} dataSource={this.state.dataSource}
                       pagination={{
                           pageSize: this.state.pageSize, total: this.state.total,
                           showQuickJumper: true, showSizeChanger: false
                       }} onChange={this.changePage}/>
                <Modal style={{marginTop: 30}} title={this.state.ImageType} visible={this.state.isModalVisible}
                       footer={null}
                       onCancel={this.handleCancel} width={600}>
                    <ImageDisplay src={this.state.ImageUrl}/>
                </Modal>
            </div>
        )
    }
}

export default AudioDetail