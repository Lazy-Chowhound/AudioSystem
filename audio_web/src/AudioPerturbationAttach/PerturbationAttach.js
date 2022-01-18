import React from "react";
import {Button, Modal, Progress, Result, Table} from "antd";
import PatternDisplay from "./PatternDisplay";
import {CloudUploadOutlined} from "@ant-design/icons";
import "../css/PerturbationAttach.css"
import sendGet from "../Util/axios";

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
            disabled: true
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
            render: (item) => <PatternDisplay parent={this} row={item.key}/>,
            align: "center"
        }
    ];

    componentDidMount() {
        this.setState({
            operationDone: false,
            operationCancel: false,
        })
        const d = []
        for (let i = 0; i < 46; i++) {
            d.push({
                key: i,
                name: "mp3 " + i,
                pattern: "Sounds of things",
                patternType: "Miscellaneous sources",
            });
        }
        this.setState({
            dataSource: d
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
                title: "警告",
                content: "您尚未选择任何音频",
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
                        title: "警告",
                        content: "选中行的 添加/更改扰动 为必选项",
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
                            let percent = Math.min((this.state.percent +
                                (this.state.selectedRowKeys.length === 0 ? 0 : 100 / this.state.selectedRowKeys.length)).toFixed(1), 99.9);
                            this.setState({
                                percent: percent
                            })
                        }
                    }).catch(() => {
                        flag = false
                    })
                    if (!flag) {
                        break;
                    }
                }
                if (i !== this.state.selectedRowKeys.length) {
                    this.setState({
                        operationCancel: true
                    })
                } else {
                    setTimeout(() => {
                        this.setState({
                            percent: 100,
                            title: "处理完成",
                            disabled: false
                        })
                    }, 1000)
                }
            }
        }
    }

    handleCancel = () => {
        this.setState({
            visible: false
        })
    }

    showResult = () => {
        this.setState({
            operationDone: true,
            title: "处理完成"
        })
    }

    render() {
        const {selectedRowKeys} = this.state;
        const locales = {selectionAll: "全选", selectNone: "清空所有"}
        const rowSelection = {
            selectedRowKeys,
            onChange: this.onSelectChange,
            selections: [
                Table.SELECTION_ALL,
                Table.SELECTION_NONE
            ],
        };

        let content;
        if (this.state.operationDone) {
            content = <Result status="success" title="Add Noise Pattern Successfully!"
                              subTitle={`You have add or change ${this.state.selectedRowKeys.length} noise patterns`}
                              extra={[
                                  <Button type="primary" key="add"><a href={"/perturbationAttach"}>Add
                                      Again</a></Button>,
                                  <Button key="detail"><a href={"/perturbationDisplay"}>See Detail</a></Button>,
                              ]}
            />
        } else if (this.state.operationCancel) {
            content = <Result status="warning"
                              title="There are some problems with your operation."
                              extra={
                                  <Button type="primary" key="add"><a href={"/perturbationAttach"}>Add
                                      Again</a></Button>
                              }/>
        } else {
            content =
                <div>
                    <Table rowSelection={rowSelection} columns={this.columns}
                           dataSource={this.state.dataSource} locale={locales}
                           summary={() => (
                               <Table.Summary fixed>
                                   <Table.Summary.Row>
                                       <Table.Summary.Cell index={0}>Summary</Table.Summary.Cell>
                                       <Table.Summary.Cell index={1}>
                                           <div style={{textAlign: "center"}}>{selectedRowKeys.length >= 10 ?
                                               `${selectedRowKeys.length} items selected / total ${this.state.dataSource.length} items` :
                                               `${selectedRowKeys.length} items selected / total ${this.state.dataSource.length} items`}
                                           </div>
                                       </Table.Summary.Cell>
                                       <Table.Summary.Cell index={2}>
                                           <div style={{textAlign: "center"}}>
                                               <Button type="primary" shape="round" icon={<CloudUploadOutlined/>}
                                                       onClick={() => {
                                                           this.handleClick().then(() => {
                                                           })
                                                       }}>
                                                   确认提交
                                               </Button>
                                           </div>
                                       </Table.Summary.Cell>
                                   </Table.Summary.Row>
                               </Table.Summary>
                           )}
                    />
                    <Modal title={this.state.title} key={this.state.visible} visible={this.state.visible} footer={null}
                           width={400}
                           onCancel={this.handleCancel}>
                        <div style={{
                            display: "flex",
                            flexDirection: "column",
                        }}>
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
        return (
            <div>
                {content}
            </div>
        );
    }
}

export default PerturbationAttach