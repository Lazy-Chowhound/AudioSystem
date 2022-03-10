import React from "react";
import {
    Button,
    Drawer,
    List,
    message,
    Modal,
    notification,
    Popconfirm,
    Progress,
    Result,
    Select,
    Table,
    Tooltip
} from "antd";
import PatternDisplay from "./PatternDisplay";
import {
    CloudUploadOutlined,
    QuestionCircleOutlined,
} from "@ant-design/icons";
import {sendGet} from "../Util/axios";
import {formatTime, formatTimeStamp, getAudioSet, getNoiseAudioUrl} from "../Util/AudioUtil";
import AudioPlay from "../AudioList/AudioPlay";
import PatternDrawer from "./PatternDrawer";

class PerturbationAttach extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedRowKeys: [],
            dataSource: [],
            patternChoices: {},
            percent: 0,
            visible: false,
            operationDone: false,
            operationCancel: false,
            title: "处理中......",
            errorMessage: null,
            disabled: true,
            dataset: "",
            options: [],
            pageSize: 5,
            total: 0,
            loading: false,
            drawerVisible: false,
            historyVisible: false,
            operationHistory: []
        };
    }

    patternToName = {
        "Gaussian noise": "gaussian_white_noise", "Sound level": "sound_level",
        "Animal": "animal", "Source-ambiguous sounds": "source_ambiguous_sounds",
        "Natural sounds": "natural_sounds", "Sound of things": "sound_of_things",
        "Human sounds": "human_sounds", "Music": "music"
    }

    columns = [
        {
            title: "现音频",
            dataIndex: "name",
            align: "center",
            width: 320,
            render: (text, record) => <AudioPlay name={record.name}
                                                 src={getNoiseAudioUrl(this.state.dataset, this.getAudioName(record))}/>
        },
        {
            title: "扰动类型",
            dataIndex: "pattern",
            align: "center",
            filters: [{
                text: "Animal",
                value: "Animal",
            }, {
                text: "Gaussian noise",
                value: "Gaussian noise",
            }, {
                text: "Human sounds",
                value: "Human sounds",
            }, {
                text: "Music",
                value: "Music",
            }, {
                text: "Natural sounds",
                value: "Natural sounds",
            }, {
                text: "Sound level",
                value: "Sound level",
            }, {
                text: "Sounds of things",
                value: "Sounds of things",
            }, {
                text: "Source-ambiguous sounds",
                value: "Source-ambiguous sounds",
            }],
            onFilter: (value, record) => record.pattern.includes(value)
        },
        {
            title: "具体扰动",
            dataIndex: "patternType",
            align: "center",
        },
        {
            title: "更改扰动",
            render: (item) => <PatternDisplay parent={this} row={item.key}/>,
            align: "center"
        }];

    componentDidMount() {
        this.getAudioSetList()
        this.setState({
            operationDone: false,
            operationCancel: false,
        })
    }

    getAudioName = (record) => {
        let name = record.name, pattern = record.pattern, patternType = record.patternType
        name = name.substring(0, name.indexOf(".")) + "_"
            + this.patternToName[pattern] + name.substring(name.indexOf("."))
        if (pattern !== "Gaussian noise") {
            patternType = patternType.replace(" ", "_").toLowerCase()
            name = name.substring(0, name.indexOf(".")) + "_" + patternType + name.substring(name.indexOf("."))
        }
        return name
    }

    // 获取子组件的值
    getChildren = (children, option) => {
        const choices = this.state.patternChoices
        if (option.length !== 0) {
            choices[option[0]] = option[1]
        } else {
            delete choices.option[0]
        }
        this.setState({
            patternChoices: choices
        })
    }

    onSelectChange = (selectedRowKeys) => {
        this.setState({
            selectedRowKeys: selectedRowKeys
        });
    };

    handleClick = async () => {
        this.setState({
            percent: 0
        })
        const selectedKeys = this.state.selectedRowKeys
        if (selectedKeys.length === 0) {
            Modal.warning({
                title: "警告", content: "您尚未选择任何音频",
            });
        } else {
            if (this.checkValid()) {
                this.setState({
                    visible: true,
                    percent: 0
                })
                let i = 0;
                for (; i < selectedKeys.length; i++) {
                    let errorMsg = null
                    const info = this.getSelectedRowParam(selectedKeys[i])
                    let flag = true, url = info[0], parameters = info[1]
                    await sendGet(url, {
                        params: parameters
                    }).then((res) => {
                        if (res.data.code === 400) {
                            errorMsg = res.data.data
                            flag = false
                        } else {
                            this.setState((state) => ({
                                percent: Math.min(
                                    (state.percent + 100 / state.selectedRowKeys.length).toFixed(1), 99.9
                                )
                            }));
                        }
                    }).catch((error) => {
                        flag = false
                        errorMsg = error
                    })
                    if (!flag) {
                        this.setState({
                            errorMessage: errorMsg
                        })
                        break;
                    }
                }
                if (i !== this.state.selectedRowKeys.length) {
                    setTimeout(() => {
                        this.setState({
                            operationCancel: true,
                        })
                    }, 1000)
                } else {
                    setTimeout(() => {
                        this.setState({
                            percent: 100, title: "处理完成", disabled: false
                        })
                    }, 1000)
                }
            }
        }
    }

    getAudioSetList = () => {
        getAudioSet().then(res => {
            this.setState({
                options: res,
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    getPatternDetail = () => {
        sendGet("/audioClipsPattern", {
            params: {
                dataset: this.state.dataset
            }
        }).then(res => {
                if (res.data.code === 400) {
                    message.error(res.data.data).then()
                    this.setState({
                        loading: false
                    })
                } else {
                    const data = JSON.parse(res.data.data)
                    this.setState({
                        dataSource: data,
                        total: data.length,
                        loading: false
                    })
                }
            }
        ).catch(err => {
            message.error(err).then()
            this.setState({
                loading: false
            })
        })
    }

    closeModal = () => {
        this.setState({
            visible: false
        })
    }

    datasetChange = (e) => {
        this.setState({
            dataset: e,
            loading: true
        }, () => {
            this.getPatternDetail()
        })
    }

    getSelectedRowParam = (selectedKey) => {
        let urls = {
            "Gaussian noise": "/addGaussianNoise",
            "Sound level": "/addSoundLevel",
            "Natural sounds": "/addNaturalSounds",
            "Animal": "/addAnimal",
            "Sound of things": "/addSoundOfThings",
            "Human sounds": "/addHumanSounds",
            "Music": "/addMusic",
            "Source-ambiguous sounds": "/addSourceAmbiguousSounds"
        }
        let key = this.state.dataSource[selectedKey].key
        let pattern = this.state.patternChoices[key]
        let params = {};
        params["dataset"] = this.state.dataset
        params["audioName"] = this.state.dataSource[selectedKey].name
        params["currentPattern"] = this.state.dataSource[selectedKey].pattern
        if (params["currentPattern"] !== "Gaussian noise") {
            params["currentPatternType"] = this.state.dataSource[selectedKey].patternType
        }
        if (pattern[0] !== "Gaussian noise") {
            params["specificPattern"] = pattern[1]
        }
        return [urls[pattern[0]], params]
    }

    checkValid = () => {
        let selectedKeys = this.state.selectedRowKeys
        let valid = true
        for (let i = 0; i < selectedKeys.length; i++) {
            const choice = this.state.patternChoices[selectedKeys[i]]
            if (typeof choice === "undefined") {
                valid = false;
                Modal.error({
                    title: "警告", content: "选中行的更改扰动为必选项",
                });
                break;
            } else {
                let pattern = choice[0]
                let patternType = (choice.length === 2 ? choice[1] : null)
                if (pattern === this.state.dataSource[selectedKeys[i]].pattern) {
                    if ((patternType != null && patternType === this.state.dataSource[selectedKeys[i]].patternType)
                        || patternType === null) {
                        Modal.error({
                            title: "警告", content: "更改扰动不允许和当前一样",
                        });
                        valid = false;
                        break;
                    }
                }
            }
        }
        return valid
    }

    showResult = () => {
        this.setState({
            operationDone: true,
        })
    }

    // 绑定子组件
    bindPatternDrawer = (ref) => {
        this.patternDrawer = ref
    }

    openDrawer = () => {
        this.patternDrawer.openDrawer()
    }

    showHistory = () => {
        this.setState({
            historyVisible: true
        }, () => {
            this.getOperationHistory()
        })
    }

    getOperationHistory = () => {
        sendGet("/operationHistory").then(res => {
            if (res.data.code === 400) {
                message.error(res.data.data).then()
            } else {
                const data = JSON.parse(res.data.data)
                const histories = []
                for (let i = 0; i < data.length; i++) {
                    const history = {}
                    history['key'] = data[i]['id']
                    history['dataset'] = data[i]['dataset']
                    history['audioName'] = data[i]['audioName']
                    history['formerType'] = data[i]['formerType']
                    history['latterType'] = data[i]['latterType']
                    history['time'] = formatTime(data[i]['time'])
                    histories.push(history)
                }
                this.setState({
                    operationHistory: histories
                })
            }
        }).catch(() => {
            message.error("获取历史记录失败").then()
        })
    }

    confirm = () => {
        this.clearHistory()
    }

    clearHistory = () => {
        if (this.state.operationHistory.length !== 0) {
            sendGet("/clearOperationHistory").then(() => {
                notification.success({
                    message: '清空历史成功',
                    duration: 1.0
                })
                this.setState({
                    operationHistory: []
                })
            }).catch(err => {
                message.error(err).then()
            })
        } else {
            notification.warning({
                message: '无可清空历史',
                duration: 1.0
            })
        }
    }

    closeHistory = () => {
        this.setState({
            historyVisible: false,
        });
    };

    deleteHistory = (item) => {
        const dataset = item.dataset;
        const audioName = item.audioName;
        const formerType = item.formerType;
        const latterType = item.latterType;
        const time = formatTimeStamp(item.time).toString()
        sendGet("/deleteOperationHistory", {
            params: {
                dataset: dataset,
                audioName: audioName,
                formerType: formerType,
                latterType: latterType,
                time: time
            }
        }).then(() => {
            notification.success({
                message: '删除成功',
                duration: 1.0
            })
            this.getOperationHistory()
        }).catch(error => {
            message.error(error).then()
        })
    }

    render() {
        const {selectedRowKeys} = this.state;
        const locales = {selectionAll: "全选", selectNone: "清空所有", filterConfirm: '确定', filterReset: '重置'}
        const rowSelection = {
            selectedRowKeys,
            onChange: this.onSelectChange,
            selections: [Table.SELECTION_ALL, Table.SELECTION_NONE],
        };

        let drawerTitle =
            <div>
                <span>操作历史</span>
                <Popconfirm placement="leftBottom" title="确定清空？"
                            onConfirm={this.confirm} okText="确定" cancelText="取消">
                    <Button style={{marginLeft: 60}} type={"dashed"}>清空所有历史</Button>
                </Popconfirm>
            </div>

        let summaryRow =
            <Table.Summary fixed>
                <Table.Summary.Row>
                    <Table.Summary.Cell index={0}>总 计</Table.Summary.Cell>
                    <Table.Summary.Cell index={1}>
                        <div style={{textAlign: "center"}}>
                            {`选择了 ${selectedRowKeys.length} 项 / 总共 ${this.state.dataSource.length} 项`}
                        </div>
                    </Table.Summary.Cell>
                    <Table.Summary.Cell index={2}>
                        <div style={{textAlign: "center"}}>
                            <Button type="primary" shape="round" icon={<CloudUploadOutlined/>}
                                    onClick={() => {
                                        this.handleClick().then()
                                    }}>
                                确认提交
                            </Button>
                        </div>
                    </Table.Summary.Cell>
                </Table.Summary.Row>
            </Table.Summary>

        let content;
        if (this.state.operationDone) {
            content =
                <Result status="success" title="成功修改扰动!"
                        subTitle={`成功修改 ${this.state.selectedRowKeys.length} 个噪声扰动`}
                        extra={[<Button type="primary" key="add"><a
                            href={"/perturbationAttach"}>继续操作</a></Button>,
                            <Button key="detail"><a href={"/perturbationDisplay"}>查看详情</a></Button>,]}/>
        } else if (this.state.operationCancel) {
            content =
                <Result status="warning"
                        title="操作出现了未知错误"
                        subTitle={this.state.errorMessage}
                        extra={<Button type="primary" key="reAdd"><a
                            href={"/perturbationAttach"}>重新操作</a></Button>}/>
        } else {
            content =
                <div style={{whiteSpace: "pre"}}>
                    <div style={{padding: 10}}>
                        <span>数据集:</span>
                        <Select value={this.state.dataset} bordered={false} onChange={this.datasetChange}
                                size={"large"}>
                            {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                        </Select>
                        <Tooltip placement="right" title="点击查看所有扰动类别">
                            <QuestionCircleOutlined onClick={this.openDrawer}/>
                            <PatternDrawer bindChildren={this.bindPatternDrawer}/>
                        </Tooltip>
                        <Button style={{marginLeft: "100px"}} onClick={this.showHistory}
                                type={"primary"}>查看操作历史</Button>
                    </div>
                    <Table rowSelection={rowSelection} columns={this.columns} dataSource={this.state.dataSource}
                           locale={locales} summary={() => (summaryRow)} loading={this.state.loading}
                           pagination={{
                               pageSize: this.state.pageSize,
                               total: this.state.total,
                               showSizeChanger: false,
                               showQuickJumper: true,
                           }}/>
                    <Modal style={{marginTop: 80}} title={this.state.title} key={this.state.visible}
                           visible={this.state.visible} footer={null}
                           width={400} onCancel={this.closeModal}>
                        <div style={{display: "flex", flexDirection: "column"}}>
                            <div style={{textAlign: "center"}}>
                                <Progress type="circle" percent={this.state.percent}/>
                            </div>
                            <div style={{marginTop: 20, textAlign: "center"}}>
                                <Button style={{width: 100}} type={"primary"} disabled={this.state.disabled}
                                        onClick={this.showResult}>确认</Button>
                            </div>
                        </div>
                    </Modal>
                    <Drawer title={drawerTitle} placement="right" onClose={this.closeHistory}
                            visible={this.state.historyVisible} style={{whiteSpace: "pre-wrap"}}>
                        <List itemLayout="vertical" dataSource={this.state.operationHistory}
                              renderItem={item => (
                                  <List.Item actions={[<Button type={"link"} onClick={() => {
                                      this.deleteHistory(item)
                                  }}>删除此条</Button>]}>
                                      <List.Item.Meta
                                          title={item.formerType + " --> " + item.latterType}
                                          description={item.time}/>
                                      {"数据集：" + item.dataset + "\n音频名：" + item.audioName}
                                  </List.Item>
                              )}/>
                    </Drawer>
                </div>
        }
        return (<div>{content}</div>);
    }
}

export default PerturbationAttach