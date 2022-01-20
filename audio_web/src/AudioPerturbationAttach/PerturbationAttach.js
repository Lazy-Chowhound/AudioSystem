import React from "react";
import {Button, message, Modal, Progress, Result, Select, Table} from "antd";
import PatternDisplay from "./PatternDisplay";
import {CloudUploadOutlined} from "@ant-design/icons";
import "../css/PerturbationAttach.css"
import sendGet from "../Util/axios";
import getAudioSet from "../Util/AudioUtil";

class PerturbationAttach extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedRowKeys: [],
            dataSource: [],
            patternChoices: [],
            percent: 0,
            visible: false,
            operationDone: false,
            operationCancel: false,
            title: "处理中......",
            disabled: true,
            dataset: "cv-corpus-arabic",
            options: []
        };
    }

    columns = [
        {
            title: "音频名称",
            dataIndex: "name",
            key: "name",
            align: "center",
            width: 320
        },
        {
            title: "扰动类型",
            dataIndex: "pattern",
            align: "center",
        },
        {
            title: "具体扰动",
            dataIndex: "patternType",
            align: "center",
        },
        {
            title: "添加/更改扰动",
            render: (item) => <PatternDisplay parent={this} row={item.key}/>, align: "center"
        }];

    componentDidMount() {
        this.getAudioSet()
        this.getPatternDetail()
        this.setState({
            operationDone: false,
            operationCancel: false,
        })
    }

    getChildren = (children, option) => {
        const choices = this.state.patternChoices
        choices.push(option)
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
        const choices = this.state.patternChoices
        const selectedKeys = this.state.selectedRowKeys
        if (selectedKeys.length === 0) {
            Modal.warning({
                title: "警告", content: "您尚未选择任何音频",
            });
        } else {
            let count = 0;
            for (let i = 0; i < selectedKeys.length; i++) {
                for (let j = 0; j < choices.length; j++) {
                    if (choices[j][0] === selectedKeys[i]) {
                        count++;
                        break;
                    }
                }
                if (count !== i + 1) {
                    Modal.error({
                        title: "警告", content: "选中行的 添加/更改扰动 为必选项",
                    });
                    break;
                }
            }
            if (count === selectedKeys.length) {
                this.setState({
                    visible: true,
                    percent: 0
                })
                let i = 0;
                for (; i < this.state.selectedRowKeys.length; i++) {
                    let flag = true;
                    await sendGet("/test", {}).then((res) => {
                        if (res.data.code === 400) {
                            flag = false
                        } else {
                            this.setState((state) => ({
                                percent: Math.min((state.percent + 100 / state.selectedRowKeys.length).toFixed(1), 99.9)
                            }));
                        }
                    }).catch(() => {
                        flag = false
                    })
                    if (!flag) {
                        break;
                    }
                }
                if (i !== this.state.selectedRowKeys.length) {
                    setTimeout(() => {
                        this.setState({
                            operationCancel: true
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

    getAudioSet = () => {
        getAudioSet().then(res => {
            this.setState({
                options: res
            })
        }).catch(error => {
            message.error(error).then()
        })
    }

    getPatternDetail = () => {
        sendGet("/audioSetPattern", {
            params: {
                dataset: this.state.dataset
            }
        }).then(r => {
                this.setState({
                    dataSource: JSON.parse(r.data.data)
                })
            }
        ).catch(err => {
            message.error(err).then()
        })
    }

    handleCancel = () => {
        this.setState({
            visible: false
        })
    }

    datasetChange = (e) => {
        this.setState({
            dataset: e
        }, () => {
            this.getPatternDetail()
        })
    }

    showResult = () => {
        this.setState({
            operationDone: true,
        })
    }

    render() {
        const {selectedRowKeys} = this.state;
        const locales = {selectionAll: "全选", selectNone: "清空所有"}
        const rowSelection = {
            selectedRowKeys, onChange: this.onSelectChange, selections: [Table.SELECTION_ALL, Table.SELECTION_NONE],
        };

        let summaryRow =
            <Table.Summary fixed>
                <Table.Summary.Row>
                    <Table.Summary.Cell index={0}>总 计</Table.Summary.Cell>
                    <Table.Summary.Cell index={1}>
                        <div
                            style={{textAlign: "center"}}>{selectedRowKeys.length >= 10 ? `选择了 ${selectedRowKeys.length} 项 / 总共 ${this.state.dataSource.length} 项` : `选择了 ${selectedRowKeys.length} 项 / 总共 ${this.state.dataSource.length} 项`}
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

        let select =
            <div>
                <span>数据集:</span>
                <Select defaultValue="cv-corpus-arabic" bordered={false}
                        onChange={this.datasetChange}>
                    {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                </Select>
            </div>

        let content;
        if (this.state.operationDone) {
            content = <Result status="success" title="成功添加/修改扰动!"
                              subTitle={`成功添加或修改 ${this.state.selectedRowKeys.length} 个噪声扰动`}
                              extra={[<Button type="primary" key="add"><a
                                  href={"/perturbationAttach"}>继续添加</a></Button>,
                                  <Button key="detail"><a href={"/perturbationDisplay"}>查看详情</a></Button>,]}/>
        } else if (this.state.operationCancel) {
            content = <Result status="warning"
                              title="操作出现了未知错误"
                              extra={<Button type="primary" key="reAdd"><a
                                  href={"/perturbationAttach"}>重新添加</a></Button>}/>
        } else {
            content = <div style={{whiteSpace: "pre"}}>
                <Table rowSelection={rowSelection} columns={this.columns}
                       dataSource={this.state.dataSource} locale={locales}
                       title={() => {
                           return (select)
                       }}
                       summary={() => (summaryRow)}
                />
                <Modal title={this.state.title} key={this.state.visible} visible={this.state.visible} footer={null}
                       width={400} onCancel={this.handleCancel}>
                    <div style={{display: "flex", flexDirection: "column"}}>
                        <div style={{textAlign: "center"}}>
                            <Progress type="circle" percent={this.state.percent}/>
                        </div>
                        <div style={{marginTop: 20, textAlign: "center"}}>
                            <Button style={{width: 100}} type={"primary"} disabled={this.state.disabled}
                                    onClick={() => {
                                        this.showResult()
                                    }}>确认</Button>
                        </div>
                    </div>
                </Modal>
            </div>
        }
        return (<div>
            {content}
        </div>);
    }
}

export default PerturbationAttach