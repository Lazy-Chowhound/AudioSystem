import React from "react";
import {Button, message, Modal, Progress, Result, Select, Table} from "antd";
import PatternDisplay from "./PatternDisplay";
import {CloudUploadOutlined} from "@ant-design/icons";
import sendGet from "../Util/axios";
import getAudioSet from "../Util/AudioUtil";

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
            dataset: "cv-corpus-chinese",
            options: [],
            pageSize: 5,
            total: 0,
            loading: true
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
            title: "更改扰动",
            render: (item) => <PatternDisplay parent={this} row={item.key}/>,
            align: "center"
        }];

    componentDidMount() {
        this.getAudioSetList()
        this.getPatternDetail()
        this.setState({
            operationDone: false,
            operationCancel: false,
        })
    }

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
                const data = JSON.parse(r.data.data)
                this.setState({
                    dataSource: data,
                    total: data.length,
                    loading: false
                })
            }
        ).catch(err => {
            message.error(err).then()
            this.setState({
                loading: false
            })
        })
    }

    handleCancel = () => {
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
        params["audioName"] = this.state.dataSource[selectedKey].name
        params["dataset"] = this.state.dataset
        params["formerPattern"] = this.state.dataSource[selectedKey].pattern
        if (params["formerPattern"] !== "Gaussian noise") {
            params["formerPatternType"] = this.state.dataSource[selectedKey].patternType
        }
        if (pattern[0] !== "Gaussian noise") {
            params["specificPattern"] = pattern[1]
        }
        console.log([urls[pattern[0]], params])
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

    render() {
        const {selectedRowKeys} = this.state;
        const locales = {selectionAll: "全选", selectNone: "清空所有"}
        const rowSelection = {
            selectedRowKeys,
            onChange: this.onSelectChange,
            selections: [Table.SELECTION_ALL, Table.SELECTION_NONE],
        };

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

        let select =
            <div>
                <span>数据集:</span>
                <Select defaultValue={this.state.dataset} bordered={false}
                        onChange={this.datasetChange}>
                    {this.state.options.map(val => <Select.Option key={val} value={val}/>)}
                </Select>
            </div>

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
                    <Table rowSelection={rowSelection} columns={this.columns} dataSource={this.state.dataSource}
                           locale={locales} summary={() => (summaryRow)} loading={this.state.loading}
                           title={() => {
                               return (select)
                           }}
                           pagination={{
                               pageSize: this.state.pageSize,
                               total: this.state.total,
                               showSizeChanger: false,
                               showQuickJumper: true,
                           }}
                    />
                    <Modal style={{marginTop: 80}} title={this.state.title} key={this.state.visible}
                           visible={this.state.visible} footer={null}
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