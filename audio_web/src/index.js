import React from "react";
import ReactDOM from "react-dom";
import {Breadcrumb, Layout, Menu} from "antd";
import {AudioOutlined, BarsOutlined, FireOutlined, BranchesOutlined, CodeOutlined} from "@ant-design/icons";
import {BrowserRouter as Router, Link, Route, Routes} from "react-router-dom";
import AudioList from "./AudioList/AudioList";
import PerturbationDisplay from "./AudioPerturbationDisplay/PerturbationDisplay";
import Validation from "./AudioValidation/Validation";
import "antd/dist/antd.css";
import "./css/index.css";
import PerturbationAttach from "./AudioPerturbationAttach/PerturbationAttach";
import "default-passive-events"

const {Header, Content, Footer, Sider} = Layout;
const {SubMenu} = Menu;

class Index extends React.Component {
    state = {
        collapsed: false,
        selectedPath: ["list"],
        choice: "音频列表",
        subChoice: "",
        openKeys: [],
    };

    componentDidMount() {
        this.changeSelectedKeys()
    }

    onCollapse = (collapsed) => {
        this.setState({collapsed});
    };

    handleClick = (e) => {
        this.changeSelectedKeys()
        if (e.key === "title") {
            return;
        }
        const map = new Map([["list", "音频列表"], ["perturbationAttach", "添加扰动"],
            ["perturbationDisplay", "扰动概况"], ["validation", "质量分析"]]);
        if (e.key === "perturbationAttach" || e.key === "perturbationDisplay") {
            this.setState({
                choice: "音频扰动",
                subChoice: map.get(e.key)
            })
        } else {
            this.setState({
                choice: map.get(e.key),
                subChoice: null
            })
        }
    };

    changeSelectedKeys = () => {
        let curPath = []
        let path = new URL(window.location.href).pathname
        if (path === "/") {
            curPath.push("list")
        } else {
            if (path === "/perturbationAttach" || path === "/perturbationDisplay") {
                curPath.push("noise")
            }
            curPath.push(path.substring(1))
        }
        this.setState({
            selectedPath: curPath,
            openKeys: curPath.length === 2 ? ["noise"] : []
        })
    }

    handleOpenChange = () => {
        this.setState({
            openKeys: ["noise"]
        })
    }

    render() {
        const {collapsed} = this.state;
        return (
            <Router>
                <Layout style={{minHeight: "100vh"}}>
                    <Sider collapsible collapsed={collapsed} onCollapse={this.onCollapse}>
                        <Menu theme="dark" mode="inline" onClick={this.handleClick}
                              selectedKeys={this.state.selectedPath}
                              openKeys={this.state.openKeys}
                              onOpenChange={this.handleOpenChange}>
                            <Menu.Item className="title" key="title">
                                音频数据集系统
                            </Menu.Item>
                            <Menu.Item key="list" icon={<BarsOutlined/>}>
                                <Link to={"/list"}>音频列表</Link>
                            </Menu.Item>
                            <SubMenu key="noise" icon={<AudioOutlined/>} title={"音频扰动"}>
                                <Menu.Item key="perturbationAttach" icon={<BranchesOutlined/>}>
                                    <Link to={"/perturbationAttach"}>添加扰动</Link>
                                </Menu.Item>
                                <Menu.Item key="perturbationDisplay" icon={<CodeOutlined/>}>
                                    <Link to={"/perturbationDisplay"}>扰动概况</Link>
                                </Menu.Item>
                            </SubMenu>
                            <Menu.Item key="validation" icon={<FireOutlined/>}>
                                <Link to={"/validation"}>质量分析</Link>
                            </Menu.Item>
                        </Menu>
                    </Sider>
                    <Layout className="site-layout">
                        <Header className="site-layout-background" style={{padding: 0}}/>
                        <Content style={{margin: "0 16px"}}>
                            <Breadcrumb style={{margin: "16px 0"}}>
                                <Breadcrumb.Item>音频数据集系统</Breadcrumb.Item>
                                <Breadcrumb.Item>{this.state.choice}</Breadcrumb.Item>
                                <Breadcrumb.Item>{this.state.subChoice}</Breadcrumb.Item>
                            </Breadcrumb>
                            <div className="site-layout-background" style={{minHeight: 400}}>
                                <Routes>
                                    <Route exact path="/" element={<AudioList/>}/>
                                    <Route exact path="/list" element={<AudioList/>}/>
                                    <Route exact path="/perturbationAttach" element={<PerturbationAttach/>}/>
                                    <Route exact path="/perturbationDisplay" element={<PerturbationDisplay/>}/>
                                    <Route exact path="/validation" element={<Validation/>}/>
                                </Routes>
                            </div>
                        </Content>
                        <Footer style={{textAlign: "center"}}>Audio System ©2022 Created by Nakano Miku</Footer>
                    </Layout>
                </Layout>
            </Router>
        );
    }
}

ReactDOM.render(<Index/>, document.getElementById("root"));
