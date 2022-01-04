import React from "react";
import {Button, message, Modal, Table} from "antd";
import axios from "axios";
import ImageArea from "./ImageArea";

class AudioDetail extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            dataSource: [],
            isModalVisible: false,
            ImageType: null,
            AbsoluteUrl: null,
            ImageUrl: null
        };
    }

    columns = [
        {
            title: '音频名称',
            dataIndex: 'name',
            key: 'name',
            align: "center"
        },
        {
            title: '时长',
            dataIndex: 'size',
            key: 'size',
            align: "center"
        },
        // {
        //     title: '性别',
        //     dataIndex: 'gender',
        //     key: 'gender',
        //     align: "center"
        // },
        // {
        //     title: '年龄',
        //     dataIndex: 'age',
        //     key: 'age',
        //     align: "center"
        // },
        {
            title: '声道',
            dataIndex: 'channel',
            key: 'channel',
            align: "center"
        },
        {
            title: '采样率',
            key: 'sampleRate',
            dataIndex: 'sampleRate',
            align: "center"
        },
        {
            title: '位深',
            key: 'bitDepth',
            dataIndex: 'bitDepth',
            align: "center"
        },
        {
            title: '内容',
            key: 'content',
            dataIndex: 'content',
            align: "center"
        },
        {
            title: "波形图",
            key: 'distribution',
            render: item =>
                <Button type={"link"} size={"small"} onClick={() => {
                    this.showWaveForm(item)
                }}>查看波形图</Button>,
            align: "center"
        },
        {
            title: '频谱图',
            key: 'list',
            render: item =>
                <Button type={"link"} size={"small"} onClick={() => {
                    this.showMelSpectrum(item)
                }}>查看频谱图</Button>,
            align: "center"
        },
    ];

    componentDidMount() {
        const url = "http://localhost:8080/audioDescription"
        axios.get(url, {
            params: {
                audioSet: this.props.choice,
                page: 1,
                pageSize: 1
            }
        }).then(
            (response) => {
                this.setState({
                    dataSource: JSON.parse(response.data.data)
                })
            }
        ).catch((error) => {
                message.error(error)
            }
        )
    }

    showWaveForm = (item) => {
        const url = "http://localhost:8080/getWaveForm"
        axios.get(url, {
            params: {
                audioSet: this.props.choice,
                audioName: item.name
            }
        }).then(
            (response) => {
                const path = response.data.data
                this.setState({
                    ImageType: "波形图",
                    isModalVisible: true,
                    AbsoluteUrl: path,
                    ImageUrl: path.replace("D:/AudioSystem/audio_java/src/main/resources/static/", "http://localhost:8080/")
                })

            }
        ).catch((error) => {
                message.error(error)
            }
        )
    }

    showMelSpectrum = (item) => {
        const url = "http://localhost:8080/getMelSpectrum"
        axios.get(url, {
            params: {
                audioSet: this.props.choice,
                audioName: item.name
            }
        }).then(
            (response) => {
                const path = response.data.data
                this.setState({
                    ImageType: "Mel频谱图",
                    isModalVisible: true,
                    AbsoluteUrl: path,
                    ImageUrl: path.replace("D:/AudioSystem/audio_java/src/main/resources/static/", "http://localhost:8080/")
                })

            }
        ).catch((error) => {
                message.error(error)
            }
        )
    }

    handleCancel = () => {
        this.setState({
            isModalVisible: false
        })
        const url = "http://localhost:8080/removeImage"
        axios.get(url, {
            params: {
                path: this.state.AbsoluteUrl
            }
        }).then(() => {
            }
        ).catch((error) => {
                message.error(error)
            }
        )
    }

    render() {
        return (
            <div>
                <Table columns={this.columns} dataSource={this.state.dataSource}/>
                <Modal title={this.state.ImageType} visible={this.state.isModalVisible} footer={null}
                       onCancel={this.handleCancel} width={500}>
                    <ImageArea src={this.state.ImageUrl}/>
                </Modal>
            </div>
        )
    }
}

export default AudioDetail